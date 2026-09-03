#!/usr/bin/env python3
"""Render a /explain script.json into an mp4.

Pipeline per scene: TTS narration (OpenAI) -> clip (fal MiniMax H3-Max, or local title card /
dry-run placeholder) -> normalize + fit clip to narration -> mix. Then concat, music bed with
ducking, burned-in captions.

Usage: render.py script.json [--out DIR] [--dry-run] [--music FILE] [--model h3-max-turbo|h3-max] [--resolution 480P|768P]
                             [--no-captions] [--voice onyx|fish] [--narration FILE] [--jobs 6]
       render.py --where            # print the workspace root (where out/ and assets/ live)
Env (or <repo>/.env): FAL_API_KEY (or FAL_KEY), FISH_AI_API_KEY, OPENAI_API_KEY,
     EXPLAIN_HOME (workspace root, default: the repo containing this script),
     EXPLAIN_MUSIC (music bed; default: first file in $EXPLAIN_HOME/assets/),
     EXPLAIN_JP_FONT / EXPLAIN_EN_FONT (fontconfig names for the title cards),
     IROH_FISH_VOICE_ID (override the fish.audio voice used when script.json has "style": "iroh")
     HXH_FISH_VOICE_ID (same, for "style": "hxh"; only used off lean mode, which is that style's default)
     RICK_FISH_VOICE_ID / MORTY_FISH_VOICE_ID (fish voices for "style": "rick"; only needed off lean mode)
     EXPLAIN_LEAN_DRY=1 (with --dry-run: still compose lean prompts; missing samples/refs only warn; no fal call)
     STARK_FISH_VOICE_ID / AI_FISH_VOICE_ID (the inventor and the AI voices for "style": "stark")
Styles: script.json may carry a top-level "style": "jjk" (default) | "iroh" | "hxh" | "stark" | "rick". The style picks the
     prompt style lock, the title-card look, the default fish voice and the default music
     ($EXPLAIN_HOME/assets/iroh/ first for iroh, then $EXPLAIN_HOME/assets/; "rick" defaults to no music).
     "rick" is two-voice lean mode: "[rick] ..." / "[morty] ..." pick the voice sample and the prompt's speaker.
"""
import argparse, glob, json, math, os, re, subprocess, sys, textwrap, time
from concurrent.futures import ThreadPoolExecutor

import requests

HOME = os.environ.get("EXPLAIN_HOME") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


def load_env():
    """Load <repo>/.env (KEY=value lines) without overriding real env vars."""
    f = os.path.join(HOME, ".env")
    if os.path.exists(f):
        for line in open(f):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip().replace("export ", ""), v.strip().strip('"').strip("'"))
load_env()


def _audio_files(d):
    return sorted(glob.glob(os.path.join(d, "*.m4a")) + glob.glob(os.path.join(d, "*.mp3")) + glob.glob(os.path.join(d, "*.wav")))


def default_music(style="jjk"):
    """$EXPLAIN_MUSIC, else the first audio file in assets/<style>/ (non-jjk styles), else assets/."""
    if os.environ.get("EXPLAIN_MUSIC"):
        return os.environ["EXPLAIN_MUSIC"]
    hits = []
    if style != "jjk":
        hits = _audio_files(os.path.join(HOME, "assets", style))
    hits = hits or _audio_files(os.path.join(HOME, "assets"))
    return hits[0] if hits else None

def resolve_music(name, style="jjk"):
    """script.json "music": an absolute path, a path relative to the workspace, or a bare name
    (with or without extension) matched against assets/<style>/ then assets/."""
    if not name:
        return None
    name = os.path.expanduser(name)
    cands = [name, os.path.join(HOME, name)]
    for d in ([os.path.join(HOME, "assets", style)] if style != "jjk" else []) + [os.path.join(HOME, "assets")]:
        cands.append(os.path.join(d, name))
        stem = os.path.splitext(os.path.basename(name))[0].lower()
        cands += [f for f in _audio_files(d) if stem in os.path.splitext(os.path.basename(f))[0].lower()]
    for c in cands:
        if os.path.isfile(c):
            return c
    raise SystemExit(f"music not found: {name!r} (looked in assets/{style}/ and assets/)")

# ---------- styles ----------
# script.json "style" selects one of these. Existing scripts have no field and get "jjk" unchanged.
STYLES = {
    "jjk": {
        "lock": ("2D Japanese TV anime, dark modern shonen, 2020s prestige studio look, hand-drawn cel "
                 "shading, flat color fills, thin clean linework with heavy black ink shadow shapes, "
                 "painterly matte-painting background, desaturated navy and charcoal palette, film grain, "
                 "24fps anime motion, limited animation with smear frames. "),
        "fish_voice": "179b5cc736974d96913c7849d0bb68c5",   # "jjk narrator" on fish.audio (454k generations)
        "voice_label": "jjk narrator",
        "fish_speed": 1.0,      # never slower: 0.9 made the narrator sound 20% too slow
        "pause": 0.9,           # seconds of silence between sentences
        "cast_words": r"sorceress|sorcerer|user|character|protagonist",
        "default_sound": "low ominous drone",
        "default_instr": "Deep, calm, solemn anime narrator. Slow, deliberate, absolute. Pause at full stops.",
        "title": {"bg": "black", "ink": "white", "en": "0xBBBBBB", "glyph": None, "noise": True},
        "thumb_kanji": "領域",   # prefer the first shot after a title containing this
        "outro": 5.0,            # hold the last frame this long after the final line; the theme plays on
        "outro_fade": 2.0,       # and the whole mix fades out over the last N seconds of that hold
    },
    "iroh": {
        "lock": ("2D American TV animation from the mid-2000s with strong East Asian influence, clean "
                 "confident ink linework with thick-to-thin brush weight, warm flat cel shading with soft "
                 "two-tone shadows, painted watercolor and gouache backgrounds with visible paper texture, "
                 "elemental color palettes, gentle 24fps character animation, expressive faces, no film grain. "),
        "fish_voice": os.environ.get("IROH_FISH_VOICE_ID") or "2356d9b259824b9f8b0aafb362f7c7f8",
        "voice_label": "iroh",
        "voices": {"iroh": "2356d9b259824b9f8b0aafb362f7c7f8",      # the user's clone
                   "zuko": "77ef9b463d2a49488e799ddd08fea3f8"},     # "Prince Zuko" public fish.audio voice
        # narration may switch speakers inline: "[zuko] Uncle, does it think? [iroh] No. It guesses."
        "fish_speed": 1.0,      # 0.85 was too slow; pacing comes from the pauses
        "lipsync_audio": "model",   # the model re-speaks the narration in the clone's voice, in sync by construction
        "voice_sample": "assets/ref/iroh/iroh-voice.wav",   # lean mode: no per-scene TTS, the model speaks from this sample
        "pause": 1.4,
        "cast_words": r"old master|master|teacher|old man|student",
        "default_sound": "quiet tea shop, erhu far away",
        "default_instr": "Warm, patient, elderly teacher. Unhurried, a smile in the voice, gentle pauses. Short lines land softly.",
        "title": {"bg": "0xEBDCBA", "ink": "0x2A1E14", "en": "0x6B4A2B", "glyph": "茶", "noise": False},
        "thumb_kanji": "戒",
    },
    "rick": {
        "lock": ("2D American adult TV animation, thick uniform black outlines, flat saturated colours with no "
                 "gradients, simple rounded shapes, slightly wobbly hand-drawn linework, sickly green and teal "
                 "fluorescent lighting, cluttered sci-fi garage laboratory backgrounds, limited 24fps animation, "
                 "exaggerated expressive faces, no anime shading, no film grain. "),
        "fish_voice": os.environ.get("RICK_FISH_VOICE_ID") or "d2e75a3e3fd6419893057c02a375a113",   # "Rick Sanchez" public fish.audio voice (110k generations)
        "voice_label": "rick",
        "voices": {"rick": os.environ.get("RICK_FISH_VOICE_ID") or "d2e75a3e3fd6419893057c02a375a113",
                   "morty": os.environ.get("MORTY_FISH_VOICE_ID") or "377e4ac186da47faa3b644d033775954"},   # "Morty Smith" public voice (36k generations)
        "fish_speed": 1.0,
        "lipsync_audio": "model",
        "voice_sample": "assets/ref/rick/rick-voice.wav",   # lean mode default (untagged narration)
        "voice_samples": {"rick": "assets/ref/rick/rick-voice.wav",      # lean mode: sample per leading [tag]
                          "morty": "assets/ref/rick/morty-voice.wav"},
        "pause": 0.7,
        "words_per_sec": 2.6,   # lean duration estimate (he talks fast)
        "music": None,          # no music bed unless the script or --music asks for one
        "cast_words": r"scientist|old scientist|the old man|boy|teenager|the kid|grandson|grandfather",
        "default_sound": "garage laboratory hum, fluorescent buzz, small gadgets beeping, no music",
        "default_instr": "Fast, dismissive, brilliant old scientist, slurring slightly, stutters and mid-sentence burps, insults delivered casually; the boy is nervous, higher, stammering.",
        "title": {"bg": "0x061A0E", "ink": "0x39FF14", "en": "0xA8F0B0", "glyph": None, "noise": True,
                  "font": "Helvetica Neue", "split": False},   # fontconfig family for the big English lines (drawtext ignores :style= patterns); lines split on " / "
        "thumb_kanji": "",      # no preferred title; thumbnail falls back to the brightest frame
        # default reference stills (script "refs" wins); missing defaults are skipped with a warning
        "refs": ["assets/ref/rick/rick-bust-iso.jpg", "assets/ref/rick/rick-3q-iso.jpg", "assets/ref/rick/rick-full-iso.jpg",
                 "assets/ref/rick/morty-bust-iso.jpg", "assets/ref/rick/morty-full-iso.jpg"],
        "ref_owners": ["rick", "rick", "rick", "morty", "morty"],   # parallel to refs
        "ref_labels": {"rick": "the old scientist", "morty": "the boy"},   # how the prompt names each speaker
        "seed": 4242,           # default seed (script "seed" wins)
    },
    "hxh": {
        "lock": ("2D Japanese TV anime from the early 2010s, clean bright hand-drawn cel shading with soft "
                 "two-tone shadows, thin precise linework, soft painterly watercolor backgrounds, saturated "
                 "natural daylight palette, large expressive eyes, calm 24fps limited animation, diagrammatic "
                 "cutaways with glowing outlines and flat hand-drawn schematic overlays, no CGI, no 3D render, no film grain. "),
        "fish_voice": os.environ.get("HXH_FISH_VOICE_ID") or "07f821df8a8e4eb7af871d19de5c4619",   # "Hunter x Hunter Narrator" on fish.audio (29k generations, en)
        "voice_label": "hxh narrator",
        "fish_speed": 1.0,
        "lipsync_audio": "model",
        # lean mode (default): no TTS; the model speaks each scene's narration in this voice, OFF-SCREEN.
        # The sample is a 14 s fish.audio generation of the narrator voice above (no music under it).
        # "voice_sample": null or "lipsync": true in script.json restores the Fish narration path.
        "voice_sample": "assets/ref/hxh/narrator-voice.wav",
        "words_per_sec": 2.0,   # lean duration estimate; the Fish narrator clone measures ~2.4 wps with its own pauses
        "pause": 1.0,
        # lean mode: untagged narration is treated as the speaker "narrator" (lean_tag), whose say_lines entry asks
        # for a voice-over: the narrator has no body, so nobody on screen mouths the words (same mechanism as stark's AI)
        "lean_tag": "narrator",
        "say_lines": {"narrator": ("The characters on screen do not speak and keep their mouths closed. An unseen narrator "
                                   "says, in the voice of Audio 1, exactly these words and nothing else: \"{line}\"")},
        # style-level reference stills (script "refs" wins; "refs": [] opts out): the two students, three angles each
        "refs": ["assets/ref/hxh/gon-bust.jpg", "assets/ref/hxh/gon-3q.jpg", "assets/ref/hxh/gon-full.jpg",
                 "assets/ref/hxh/killua-bust.jpg", "assets/ref/hxh/killua-3q.jpg", "assets/ref/hxh/killua-full.jpg"],
        "ref_owners": ["gon", "gon", "gon", "killua", "killua", "killua"],   # parallel to refs
        "ref_labels": {"gon": "the boy in green", "killua": "the white-haired boy", "narrator": "the narrator"},
        "seed": 1128,           # default seed (script "seed" wins)
        "cast_words": r"hunter|student|character|user|subject|protagonist",
        "default_sound": "soft piano and strings, quiet wind",
        "default_instr": "Calm, precise, omniscient anime narrator. Measured and clinical, every rule stated plainly, a beat before each condition or exception. Pause at full stops.",
        "title": {"bg": "0xF4ECD8", "ink": "0x1E1E1E", "en": "0xC8501E", "glyph": "念", "noise": False},   # cream schematic panel, red 念 seal
        "thumb_kanji": "念",
    },
    "stark": {
        "lock": ("Live-action cinematic footage, anamorphic lens with gentle horizontal flare, shallow depth of "
                 "field, cool blue holographic key light against warm tungsten workshop practicals, polished "
                 "concrete and steel workshop, 24fps film look, fine film grain, photoreal. "),
        # public fish.audio voices, the most-used English ones (2026-09-02): "Iron Man/Tony Stark" 8.9k uses,
        # "Jarvis (MCU)" 106k uses. STARK_FISH_VOICE_ID / AI_FISH_VOICE_ID override. Only used off lean mode.
        "fish_voice": os.environ.get("STARK_FISH_VOICE_ID") or "d7a76ce437d34163a48b7e683f85cac7",
        "voice_label": "stark",
        "voices": {"stark": os.environ.get("STARK_FISH_VOICE_ID") or "d7a76ce437d34163a48b7e683f85cac7",   # the inventor
                   "ai": os.environ.get("AI_FISH_VOICE_ID") or "612b878b113047d9a770c069c8b4fdfe"},        # the calm British AI
        # narration may switch speakers inline: "[ai] Sir, the ratio is eleven to one. [stark] Eleven. Fine."
        "fish_speed": 1.0,
        "lipsync_audio": "model",
        "voice_sample": "assets/ref/stark/stark-voice.wav",   # lean mode default (untagged narration)
        "voice_samples": {"stark": "assets/ref/stark/stark-voice.wav",   # lean mode: sample per leading [tag]
                          "ai": "assets/ref/stark/ai-voice.wav"},
        "pause": 0.8,
        "words_per_sec": 2.5,   # lean duration estimate (he talks fast; the AI is slower but short)
        "music": None,          # no music bed unless the script or --music asks for one
        "cast_words": r"inventor|engineer|mechanic|man at the bench",
        "default_sound": "workshop hum, servo whir, soft hologram chimes, no music",
        "default_instr": "Fast, wry, confident inventor narrating a test to the room while his hands work. Jokes carry the explanation. The AI is calm, dry, British, one clause.",
        # English-only HUD card: near-black bg, hologram-blue ink, EN font for the stacked lines, a thin rule
        # "split": False keeps "MARK 11 CYCLOID" on one line; " / " in kanji breaks lines
        "title": {"bg": "0x05080F", "ink": "0x6EC6FF", "en": "0x9FD8FF", "glyph": None, "noise": False, "font": "en", "hud": True, "split": False},
        "thumb_kanji": "",      # no preferred title; thumbnail falls back to the brightest frame
        # lean mode: untagged narration is the inventor (lean_tag). How the prompt asks for each speaker's line:
        # he keeps working and talks to the AI / the room (not to the lens); the AI has no body, so its lines are an
        # unseen voice and nobody on screen mouths them.
        "lean_tag": "stark",
        # speakers with no body: their scenes are rendered SILENT (no reference audio, so no mouth can be animated)
        # and the line is spoken by the tag's fish.audio voice, mixed over the clip like ordinary narration
        "offscreen": ["ai"],
        "say_lines": {"stark": ("The inventor keeps his hands on the part and keeps working while he talks, half to the AI and "
                                "half to the room, and says, in the voice of Audio 1, exactly these words and nothing else: \"{line}\""),
                      "ai": ("The man never speaks in this shot: his lips stay pressed shut the whole time, he only listens, "
                             "nods once and keeps working. The AI is an unseen voice from the ceiling speakers, not a person; "
                             "no mouth on screen moves. The voice of Audio 1 says exactly these words and nothing else: \"{line}\"")},
        # style-level defaults for the likeness path; a script's "refs": [] opts out, "seed" overrides
        # five stills of him cut from the workshop scene (no armor); user-*.jpg seeds go FIRST via a script "refs"
        "refs": ["assets/ref/stark/tony-face.jpg", "assets/ref/stark/tony-bust.jpg", "assets/ref/stark/tony-3q.jpg",
                 "assets/ref/stark/tony-full.jpg", "assets/ref/stark/tony-hands.jpg"],
        "seed": 42,
        "refs_prefix": ("Image 1 to Image {n} show the same man; keep his face, hair, goatee and build consistent "
                        "with them. "),
        "ref_labels": {"stark": "the inventor", "ai": "the AI"},   # how lean prompts name each speaker
    },
}
STYLE = STYLES["jjk"]   # set from script.json in main()
# Models: "h3-max-turbo" (default; text/image-to-video only) and "h3-max" (adds reference-to-video:
# character refs, reference video, lip-sync audio). Scenes that need references are routed to h3-max
# automatically whatever the default. Prices are $/s of output, regular (turbo is 75% off until 2026-09-07).
MODELS = {
    "h3-max-turbo": {"base": "minimax/h3-max-turbo", "reference": False,
                     "price": {"480P": 0.025, "768P": 0.04}},
    "h3-max":       {"base": "minimax/h3-max", "reference": True,
                     "price": {"480P": 0.08, "768P": 0.08}},   # reference-to-video is 0.08 at both
}
DEFAULT_MODEL = os.environ.get("EXPLAIN_MODEL", "h3-max-turbo")
DEFAULT_RESOLUTION = os.environ.get("EXPLAIN_RESOLUTION", "480P")
W, H, FPS = 1280, 720, 24
JP_FONT = os.environ.get("EXPLAIN_JP_FONT", "Hiragino Mincho ProN")   # macOS default; Linux: "Noto Serif CJK JP"
EN_FONT = os.environ.get("EXPLAIN_EN_FONT", "Helvetica Neue")          # Linux: "DejaVu Sans"


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit(f"command failed: {' '.join(cmd[:3])} ...")
    return r.stdout


def dur(path):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=nw=1:nk=1", path]).strip())


def esc(t):
    return t.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace("%", "\\%")


# ---------- narration ----------
FISH_MODEL = "s1"
FISH_SPEED = 1.0   # always 1.0: pacing comes from per-scene chunking + gaps, never from prosody
FISH_SPLIT = True    # one generation per sentence, stitched with real silence (the pauses are ours)
PAUSE_SENTENCE = 0.9    # seconds of silence between sentences


def split_sentences(text):
    import re
    return [t for t in re.split(r"(?<=[.!?])\s+", text.strip()) if t]


SPEAKER_TAG = r"\[([a-z][a-z0-9_-]*)\]"

def split_speakers(text):
    """'[zuko] Hi. [iroh] Sit.' -> [('zuko','Hi.'),('iroh','Sit.')]; untagged text -> speaker None."""
    import re
    parts = re.split(SPEAKER_TAG, text)
    out, spk = [], None
    for i, chunk in enumerate(parts):
        if i % 2 == 1:
            spk = chunk.lower(); continue
        chunk = " ".join(chunk.split())
        if chunk:
            out.append((spk, chunk))
    return out

def strip_speakers(text):
    import re
    return " ".join(re.sub(SPEAKER_TAG, " ", text).split())


def fish_tts(text, out, speed=1.0):
    """Whole-scene generation by default; optional per-sentence generations stitched with silence."""
    key = os.environ.get("FISH_AI_API_KEY")
    if not key:
        raise SystemExit("FISH_AI_API_KEY not set")
    h = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": FISH_MODEL}
    parts = []
    voices = STYLE.get("voices", {})
    chunks = []
    for spk, chunk in split_speakers(text):
        vid = voices.get(spk, STYLE["fish_voice"]) if spk else STYLE["fish_voice"]
        if not vid:
            raise SystemExit(f"fish voice for speaker {spk or STYLE.get('voice_label', 'default')} not set: export RICK_FISH_VOICE_ID / MORTY_FISH_VOICE_ID")
        for sent in (split_sentences(chunk) if FISH_SPLIT else [chunk]):
            chunks.append((vid, sent))
    for i, (vid, sent) in enumerate(chunks):
        seg = f"{out[:-4]}_{i}.wav"
        if not os.path.exists(seg):
            for attempt in range(6):
                r = requests.post("https://api.fish.audio/v1/tts", headers=h, timeout=180, json={
                    "text": sent, "reference_id": vid, "format": "wav", "latency": "normal",
                    "temperature": 0.6, "top_p": 0.7, "prosody": {"speed": speed, "volume": 0}})
                if r.status_code == 429:
                    time.sleep(2 + 2 * attempt); continue
                break
            if not r.ok:
                raise SystemExit(f"fish tts {r.status_code}: {r.text[:200]}")
            open(seg, "wb").write(r.content)
        parts.append(seg)
    # stitch: seg0, pause, seg1, pause, ...
    inputs, fc, n = [], [], 0
    for i, seg in enumerate(parts):
        inputs += ["-i", seg]
        fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                  f"apad=pad_dur={STYLE.get('pause', PAUSE_SENTENCE) if i < len(parts) - 1 else 0.15}[p{i}]")
    fc.append("".join(f"[p{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[a]")
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[a]", out])


def tts(text, voice, instructions, out):
    stamp = out + ".txt"
    fspeed = STYLE.get("fish_speed", FISH_SPEED)
    sig = f"{voice}|{(str(STYLE['fish_voice']) + '@' + str(fspeed) + '/' + str(STYLE.get('pause', PAUSE_SENTENCE)) + str(sorted(STYLE.get('voices', {}).items()))) if voice == 'fish' else ''}|{text}\n{instructions}"
    if os.path.exists(out) and os.path.exists(stamp) and open(stamp).read() == sig:
        return
    open(stamp, "w").write(sig)
    if voice == "fish":
        return fish_tts(text, out, fspeed)
    from openai import OpenAI
    client = OpenAI()
    with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts", voice=voice, input=strip_speakers(text),
            instructions=instructions, response_format="wav") as r:
        r.stream_to_file(out)


# ---------- clips ----------
def _data_url(path):
    import base64, mimetypes
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def fal_clip(prompt, seconds, resolution, out, image=None, refs=None, seed=None, ref_videos=None, ref_audio=None, model="h3-max-turbo"):
    """image: optional local path used as the first frame (image-to-video endpoint).
    refs: optional list of local character-sheet images (up to 9) -> reference-to-video endpoint
    (minimax/h3-max/reference-to-video); the prompt may cite them as "Image 1", "Image 2", ...
    refs win over image when both are given."""
    if os.path.exists(out):
        return 0.0
    key = os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")
    if not key:
        raise SystemExit("FAL_KEY / FAL_API_KEY not set (use --dry-run to test without it)")
    h = {"Authorization": f"Key {key}", "Content-Type": "application/json"}
    body = {"prompt": prompt, "duration": int(seconds), "resolution": resolution,
            "prompt_expansion_mode": "balanced"}
    if seed is not None:
        body["seed"] = int(seed)
    needs_ref = bool(refs or ref_videos or ref_audio)
    if needs_ref and not MODELS[model]["reference"]:
        model = "h3-max"   # only h3-max has reference-to-video
    base = MODELS[model]["base"]
    endpoint = base + "/text-to-video"
    if needs_ref:
        if refs:
            body["reference_image_urls"] = [_data_url(r) for r in refs[:9]]
        if ref_videos:
            body["reference_video_urls"] = [_data_url(v) for v in ref_videos[:3]]
        if ref_audio:
            body["reference_audio_urls"] = [_data_url(ref_audio)]
        body["aspect_ratio"] = "16:9"
        # reference-to-video costs the same at 480P and 768P, so always take the higher one
        body["resolution"] = os.environ.get("EXPLAIN_REF_RESOLUTION", "768P")
        endpoint = base + "/reference-to-video"
    elif image:
        body["image_url"] = _data_url(image)
        endpoint = base + "/image-to-video"
    else:
        body["aspect_ratio"] = "16:9"
    for attempt in range(5):   # submit; 403/429/5xx (concurrency cap, throttling) are retried with backoff
        r = requests.post(f"https://queue.fal.run/{endpoint}", json=body, headers=h, timeout=60)
        if r.status_code in (403, 429) or r.status_code >= 500:
            print(f"[fal] {os.path.basename(out)}: submit {r.status_code}, retry {attempt + 1}/5 in {10 * (attempt + 1)}s", flush=True)
            time.sleep(10 * (attempt + 1)); continue
        break
    r.raise_for_status()
    q = r.json()
    t0 = time.time()
    while True:
        s = requests.get(q["status_url"], headers=h, timeout=60).json()
        if s.get("status") == "COMPLETED":
            break
        if s.get("status") in ("FAILED", "CANCELLED"):
            raise SystemExit(f"fal task failed: {s}")
        if time.time() - t0 > 900:
            raise SystemExit("fal task timed out")
        time.sleep(2)
    res = requests.get(q["response_url"], headers=h, timeout=60).json()
    if not isinstance(res, dict) or "video" not in res:
        raise SystemExit(f"fal returned no video for {os.path.basename(out)}: {json.dumps(res)[:600]}")
    url = res["video"]["url"]
    with open(out, "wb") as f:
        f.write(requests.get(url, timeout=300).content)
    return time.time() - t0, model


def placeholder_clip(label, seconds, out):
    if os.path.exists(out):
        return
    sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=0x101828:s={W}x{H}:r={FPS}:d={seconds}",
        "-f", "lavfi", "-i", f"anoisesrc=r=48000:a=0.02:d={seconds}",
        "-vf", f"drawtext=font='{EN_FONT}':text='{esc(label)}':fontcolor=0x334466:fontsize=48:x=(w-tw)/2:y=(h-th)/2",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ac", "2", "-shortest", out])


def title_clip(kanji, english, seconds, out):
    if os.path.exists(out):
        return
    T = STYLE["title"]
    split = T.get("split", True)
    if split:
        lines = kanji.split() or [kanji]
    else:   # English big text: lines split on " / " (so "CYCLOIDAL / ACTUATORS" is two lines), not on whitespace
        lines = [ln.strip() for ln in kanji.split(" / ") if ln.strip()] or [kanji]
    # "font": "en" -> EN_FONT; any other value is a fontconfig name for the big lines; default JP_FONT
    font = EN_FONT if T.get("font") == "en" else (T.get("font") or JP_FONT)
    cap0 = 110 if T.get("hud") else 150                    # smaller cap so a ~14-char English title fits
    # size each line to fit 90% of the width; first line largest
    parts = []
    y = -60 - 55 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        if split:
            size = min(cap0 if i == 0 else 96, int(W * 0.9 / max(1, len(ln))))
        else:   # Latin glyphs are ~0.6 em wide, so the per-character budget can be larger
            size = min(cap0 if i == 0 else 96, int(W * 0.9 / max(1, len(ln)) * 1.7))
        parts.append(f"drawtext=font='{font}':text='{esc(ln)}':fontcolor={T['ink']}:fontsize={size}:"
                     f"x=(w-tw)/2:y=(h-th)/2+({y}):alpha='if(lt(t,{0.15 + 0.25 * i}),0,1)'")
        y += size + 20
    if T.get("hud"):   # thin HUD rule between the title block and the English subtitle
        parts.append(f"drawbox=x=(iw-560)/2:y=ih/2+({y - 8}):w=560:h=2:color={T['ink']}@0.85:t=fill:"
                     f"enable='gte(t,0.5)'")
        y += 14
    parts.append(f"drawtext=font='{EN_FONT}':text='{esc(english)}':fontcolor={T['en']}:fontsize=34:"
                 f"x=(w-tw)/2:y=(h-th)/2+({y + 10}):alpha='if(lt(t,0.7),0,min(1,(t-0.7)/0.4))'")
    if T["glyph"]:   # small seal-like glyph near the bottom (a teacup/lotus stand-in), fades in last
        parts.append(f"drawtext=font='{JP_FONT}':text='{esc(T['glyph'])}':fontcolor=0x9E3B2E:fontsize=40:"
                     f"x=(w-tw)/2:y=h-90:alpha='if(lt(t,1.1),0,min(1,(t-1.1)/0.5))'")
    if T["noise"]:
        parts.append("noise=alls=6:allf=t")
    sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c={T['bg']}:s={W}x{H}:r={FPS}:d={seconds}",
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", ",".join(parts), "-t", str(seconds),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", out])


# ---------- per-scene assembly ----------
def build_scene(clip, nar, out, is_title, lipsync=False, model_audio=False):
    """Normalize clip, extend to cover narration, mix narration over clip audio.
    lipsync clips carry the model's own speech track (spoken in sync with the mouth by construction).
    model_audio=True keeps that track as the voice and drops our narration; otherwise the clip audio
    is muted and our narration starts at 0 (drifts after pauses)."""
    if os.path.exists(out):
        return dur(out)
    cd, nd = dur(clip), dur(nar)
    lead = 0.0 if (lipsync or model_audio) else 0.6
    target = max(cd, nd + lead + 1.0)
    amb_gain = "-100dB" if (is_title or (lipsync and not model_audio)) else ("0dB" if model_audio else "-9dB")
    nar_gain = "-100dB" if model_audio else "0dB"
    fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
          f"fps={FPS},format=yuv420p,tpad=stop_mode=clone:stop_duration={max(0, target-cd)+0.1}[v];"
          f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={amb_gain},apad[amb];"
          f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={nar_gain},adelay={int(lead*1000)}|{int(lead*1000)}[nar];"
          f"[amb][nar]amix=inputs=2:duration=longest:normalize=0[a]")
    sh(["ffmpeg", "-y", "-i", clip, "-i", nar, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
        "-t", f"{target:.3f}", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k", out])
    return dur(out)


def lean_sentence_timings(clip, sents, cache):
    """Lean mode: the video model spoke the line at its own pace, so time captions from the clip's own
    audio. Whisper word timestamps (OpenAI API) are mapped onto the script's sentences by word count.
    Returns [(start, end), ...] relative to the clip, or None if no key / transcription failed."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    if os.path.exists(cache):
        words = json.load(open(cache))
    else:
        wav = cache.replace(".json", ".wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", clip, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
        r = subprocess.run(["curl", "-s", "https://api.openai.com/v1/audio/transcriptions",
                            "-H", f"Authorization: Bearer {key}", "-F", f"file=@{wav}", "-F", "model=whisper-1",
                            "-F", "response_format=verbose_json", "-F", "timestamp_granularities[]=word",
                            "-F", "language=en"], capture_output=True, text=True)
        try:
            words = [(w["word"], float(w["start"]), float(w["end"])) for w in json.loads(r.stdout)["words"]]
        except Exception:
            print(f"[captions] whisper failed for {os.path.basename(clip)}: {r.stdout[:200]}", flush=True)
            return None
        json.dump(words, open(cache, "w"))
    if not words:
        return None
    counts = [len(re.findall(r"[A-Za-z0-9']+", s)) for s in sents]
    scale = len(words) / max(1, sum(counts))   # whisper may split/merge a few tokens; spread the difference
    out, k = [], 0
    for i, c in enumerate(counts):
        n = len(words) - k if i == len(counts) - 1 else max(1, round(c * scale))
        seg = words[k:k + n] or words[-1:]
        nxt = words[k + n][1] if k + n < len(words) else seg[-1][2] + 0.25
        out.append((seg[0][1], min(seg[-1][2] + 0.25, nxt)))   # hold a beat, never overlap the next cue
        k += n
    return out


def write_srt(scenes, starts, nar_durs, path, timings=None):
    """One cue per sentence, spread proportionally to character count within the narration,
    unless timings[scene_id] gives measured (start, end) pairs per sentence (lean mode)."""
    import re
    n, lines = 1, []
    for sc, st, nd in zip(scenes, starts, nar_durs):
        text = strip_speakers(sc["narration"])
        sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]
        total = sum(len(s) for s in sents) or 1
        t = st + 0.35
        measured = (timings or {}).get(sc["id"])
        for j, s in enumerate(sents):
            d = nd * len(s) / total
            a, b = t, t + d
            if measured and j < len(measured):
                a, b = st + measured[j][0], st + measured[j][1]
            def ts(x):
                h, r = divmod(x, 3600); m, s2 = divmod(r, 60)
                return f"{int(h):02}:{int(m):02}:{int(s2):02},{int((s2 % 1) * 1000):03}"
            lines.append(f"{n}\n{ts(a)} --> {ts(b)}\n{textwrap.fill(s, 48)}\n")
            n += 1; t = b
    open(path, "w").write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script", nargs="?")
    ap.add_argument("--where", action="store_true", help="print the workspace root and exit")
    ap.add_argument("--out")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--music", help="music bed (default: first audio file in assets/<style>/ then assets/, or $EXPLAIN_MUSIC)")
    ap.add_argument("--resolution", default=None, choices=["480P", "768P"],
                    help=f"default: script.json 'resolution', else $EXPLAIN_RESOLUTION, else {DEFAULT_RESOLUTION}")
    ap.add_argument("--model", default=None, choices=list(MODELS),
                    help=f"default: script.json 'model', else $EXPLAIN_MODEL, else {DEFAULT_MODEL}; scenes with refs/lipsync always use h3-max")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--voice", default="onyx", help="OpenAI voice name, or 'fish' for the fish.audio JJK narrator clone")
    ap.add_argument("--narration", help="single pre-recorded narration file for the whole script (skips TTS)")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    if a.where:
        print(HOME); return
    if not a.script:
        ap.error("script.json required")

    S = json.load(open(a.script))
    global STYLE
    style = S.get("style", "jjk")
    if style not in STYLES:
        raise SystemExit(f"unknown style {style!r}; known: {', '.join(STYLES)}")
    STYLE = STYLES[style]
    if a.music is None:
        if S.get("music"):
            a.music = resolve_music(S.get("music"), style)
        elif STYLE.get("music", "auto") is not None:   # a style may default to no bed ("music": None)
            a.music = default_music(style)
    a.resolution = a.resolution or S.get("resolution") or DEFAULT_RESOLUTION
    a.model = a.model or S.get("model") or DEFAULT_MODEL
    if a.model not in MODELS:
        raise SystemExit(f"unknown model {a.model!r}; known: {', '.join(MODELS)}")
    # lean mode: a voice sample (script "voice_sample", else the style default) and no explicit lipsync
    # -> skip TTS, the model speaks each scene's narration in that voice. "voice_sample": null turns it off.
    _vs = S["voice_sample"] if "voice_sample" in S else STYLE.get("voice_sample")
    LEAN = None
    LEAN_DRY = bool(a.dry_run and os.environ.get("EXPLAIN_LEAN_DRY"))   # dry-run that still composes lean prompts
    if _vs and not S.get("lipsync") and (not a.dry_run or LEAN_DRY) and a.narration is None:
        LEAN = _vs if os.path.isabs(_vs) else os.path.join(HOME, _vs)
        if not os.path.exists(LEAN):
            if LEAN_DRY:
                print(f"[lean-dry] voice_sample not found (ignored): {LEAN}", flush=True)
            else:
                raise SystemExit(f"voice_sample not found: {LEAN}")
        S["voice_sample"] = LEAN
        # per-speaker samples (style "voice_samples", script "voice_samples" wins): checked here, picked per scene
        _vss = S.get("voice_samples", STYLE.get("voice_samples")) or {}
        for _tag, _p in _vss.items():
            _p = _p if os.path.isabs(_p) else os.path.join(HOME, _p)
            if not os.path.exists(_p):
                if LEAN_DRY:
                    print(f"[lean-dry] voice_samples[{_tag}] not found (ignored): {_p}", flush=True)
                else:
                    raise SystemExit(f"voice_samples[{_tag}] not found: {_p}")
    OFFSCREEN = set(S.get("offscreen", STYLE.get("offscreen", [])) or [])
    def lean_tag_of(sc):
        tags = [t for t, _ in split_speakers(sc.get("narration", "")) if t]
        return tags[0] if tags else STYLE.get("lean_tag")
    def is_offscreen(sc):
        return bool(LEAN) and lean_tag_of(sc) in OFFSCREEN
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.script)), "render")
    os.makedirs(out, exist_ok=True)
    scenes = S["scenes"]
    instr = S.get("narrator_voice", STYLE["default_instr"])
    print(f"[style] {style}" + (f", music {os.path.basename(a.music)}" if a.music else ", no music"), flush=True)
    if a.dry_run:
        print("[dry-run] placeholder clips, no fal spend", flush=True)

    # 1. narration
    full_nar = None
    if a.narration:
        full_nar = f"{out}/narration_full.wav"
        sh(["ffmpeg", "-y", "-i", a.narration, "-ar", "48000", "-ac", "2", full_nar])
        D = dur(full_nar)
        words = [len(sc["narration"].split()) for sc in scenes]
        nar_durs = [D * w / sum(words) for w in words]
        print(f"[narration] {os.path.basename(a.narration)} {D:.1f}s, split by word count", flush=True)
        for sc, nd in zip(scenes, nar_durs):  # silent stand-ins so scenes are sized correctly
            w = f"{out}/{sc['id']}_nar.wav"
            sh(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{nd:.3f}", w])
            open(w + ".txt", "w").write("SILENT")
        for sc in scenes:
            for f in (f"{out}/{sc['id']}_scene.mp4",):
                if os.path.exists(f): os.remove(f)
    elif LEAN:
        # lean mode: no TTS; silent stand-ins sized from word count, the video model speaks the lines.
        # Exception: off-screen speakers (style/script "offscreen": [tag, ...]) get real Fish TTS, and their
        # clips are rendered silent, so nothing on screen can mouth a bodiless voice.
        print(f"[lean] no TTS; {os.path.basename(LEAN)} sets the voice, prompts carry the lines", flush=True)
        pause = STYLE.get("pause", PAUSE_SENTENCE)
        nar_durs = []
        for sc in scenes:
            text = strip_speakers(sc["narration"])
            if is_offscreen(sc) and sc["kind"] != "title" and not a.dry_run:
                w = f"{out}/{sc['id']}_nar.wav"
                tts(sc["narration"], "fish", instr, w)
                nar_durs.append(dur(w))
                print(f"[lean] {sc['id']}: off-screen speaker, Fish TTS over a silent clip", flush=True)
                continue
            nd = 3.0 if sc["kind"] == "title" else min(14.0, len(text.split()) / STYLE.get("words_per_sec", 1.9) + pause * max(0, len(split_sentences(text)) - 1) + 0.6)
            w = f"{out}/{sc['id']}_nar.wav"
            if not (os.path.exists(w) and os.path.exists(w + ".txt") and open(w + ".txt").read() == f"LEAN {nd:.3f}"):
                sh(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{nd:.3f}", w])
                open(w + ".txt", "w").write(f"LEAN {nd:.3f}")
            nar_durs.append(nd)
    else:
        print(f"[tts] {len(scenes)} scenes via " + ("fish.audio/" + FISH_MODEL + " " + STYLE["voice_label"] + ", per-sentence" if a.voice == "fish" else f"gpt-4o-mini-tts/{a.voice}"), flush=True)
        with ThreadPoolExecutor(1 if a.voice == "fish" else a.jobs) as ex:  # fish: low concurrency limit
            list(ex.map(lambda sc: tts(sc["narration"], a.voice, instr, f"{out}/{sc['id']}_nar.wav"), scenes))
        nar_durs = [dur(f"{out}/{sc['id']}_nar.wav") for sc in scenes]

    # 2. clips in parallel
    spend = 0.0
    def make_clip(i):
        sc = scenes[i]; nd = nar_durs[i]
        clip = f"{out}/{sc['id']}_clip.mp4"
        if sc["kind"] == "title":
            title_clip(sc["kanji"], sc.get("english", ""), max(3.0, nd + 1.0), clip)
            return 0.0
        secs = min(15, max(5, math.ceil(nd + 0.8)))
        vp = sc["video_prompt"].strip()
        cast = S.get("cast", "").strip()
        if cast and cast[:40].lower() not in vp.lower():
            # enforce character consistency: expand the first generic mention into the full cast description
            vp, n = re.subn(r"\b[Tt]he (" + STYLE["cast_words"] + r")\b", cast, vp, count=1)
            if n == 0:
                vp = cast[0].upper() + cast[1:] + " is present. " + vp
        speaks = bool(sc.get("lipsync", S.get("lipsync", False)) or sc.get("voice_sample", S.get("voice_sample"))) and not is_offscreen(sc)
        snd = sc.get("sound", STYLE["default_sound"])
        if speaks:
            snd = re.sub(r",?\s*no dialogue", "", snd, flags=re.I).strip(" ,")
        prompt = STYLE["lock"] + vp + (" No on-screen text. Sound: " if speaks else " No dialogue, no on-screen text. Sound: ") + snd + "."
        def ws(p):
            p = os.path.expanduser(p)
            return p if os.path.isabs(p) else os.path.join(HOME, p)
        image = sc.get("image", S.get("image"))
        image = ws(image) if image else None
        refs = [ws(r) for r in (sc.get("refs", S.get("refs")) or [])]
        owners = list(sc.get("ref_owners", S.get("ref_owners")) or []) if refs else []   # parallel to refs, optional
        if not refs and "refs" not in sc and "refs" not in S and STYLE.get("refs"):
            # style default stills: skip the ones missing on disk (with a warning) instead of failing
            d_own = list(STYLE.get("ref_owners") or [])
            for k, r in enumerate(ws(r) for r in STYLE["refs"]):
                if os.path.exists(r):
                    refs.append(r); owners.append(d_own[k] if k < len(d_own) else None)
                else:
                    print(f"[refs] {sc['id']}: default ref missing, skipped: {r}", flush=True)
        ref_videos = [ws(v) for v in (sc.get("ref_videos", S.get("ref_videos")) or [])]
        # object references: {"objects": {"assets/ref/objects/cycloidal/disc.jpg": "the cycloidal disc and its ring of pins"}}
        # (script or scene level) for things whose exact shape has to be right (a drive, a gripper, an engine, a sneaker)
        obj_items = [(ws(q), lbl) for q, lbl in (sc.get("objects", S.get("objects")) or {}).items()]
        missing = [r for r in refs + ref_videos + [q for q, _ in obj_items] if not os.path.exists(r)]
        if missing:
            if LEAN_DRY:
                print(f"[lean-dry] {sc['id']}: reference image(s) not found (ignored): {', '.join(missing)}", flush=True)
            else:
                raise SystemExit(f"{sc['id']}: reference image(s) not found: {', '.join(missing)} "
                                 f"(set \"refs\": [] in script.json to render text-only)")
        if refs:
            # cite the sheet so the model binds the description to the pictures
            if len(owners) == len(refs) and all(owners):
                # several characters: group consecutive same-owner runs ("Image 1 to Image 3 show the old scientist; ...")
                labels = STYLE.get("ref_labels", {})
                runs, k = [], 0
                while k < len(owners):
                    j = k
                    while j + 1 < len(owners) and owners[j + 1] == owners[k]:
                        j += 1
                    name = labels.get(owners[k], owners[k])
                    runs.append((f"Image {k + 1} to Image {j + 1} show " if j > k else f"Image {k + 1} shows ") + name)
                    k = j + 1
                prompt = "; ".join(runs) + "; keep each character's face, hair and clothes consistent with their images. " + prompt
            else:
                prompt = (STYLE.get("refs_prefix") or "Image 1 to Image {n} show the same character; keep the face, hair, beard and clothes consistent with them. ").format(n=len(refs)) + prompt
        if obj_items:
            obj_items = obj_items[:max(0, 9 - len(refs))]   # the endpoint takes 9 images in all
            base = len(refs)
            refs = refs + [q for q, _ in obj_items]
            prompt = ("; ".join(f"Image {base + i + 1} shows {lbl}" for i, (_, lbl) in enumerate(obj_items))
                      + "; reproduce that object's exact shape, parts and proportions wherever it appears. " + prompt)
        if ref_videos:
            prompt = f"Video 1 shows how the same character moves, gestures and holds his face; match that manner. " + prompt
        lipsync = bool(sc.get("lipsync", S.get("lipsync", False))) and not a.dry_run and a.narration is None
        ref_audio = None
        if lipsync:
            nar_wav = f"{out}/{sc['id']}_nar.wav"
            if os.path.exists(nar_wav) and 2.0 <= dur(nar_wav) <= 15.0:
                ref_audio = nar_wav
                prompt = ("Audio 1 is the old man's voice. He speaks exactly these words to the camera, "
                          "mouth and jaw moving in sync with the audio, natural pauses where the audio pauses. " + prompt)
            else:
                print(f"[lipsync] {sc['id']}: narration missing or outside 2-15 s, skipping reference audio", flush=True)
        sample = None if is_offscreen(sc) else sc.get("voice_sample", S.get("voice_sample"))
        if sample and not ref_audio and (not a.dry_run or LEAN_DRY):
            # lean mode: a voice sample sets the voice; the video_prompt carries the words the character says.
            # The leading [tag] of the narration picks a per-speaker sample (style/script "voice_samples").
            tags = [t for t, _ in split_speakers(sc["narration"]) if t]
            tag = tags[0] if tags else STYLE.get("lean_tag")   # a style may treat untagged lines as a named speaker (hxh: the off-screen narrator)
            if tag and len(set(tags)) > 1:
                print(f"[lean] {sc['id']}: mixed speakers, using {tag}", flush=True)
            if "voice_sample" not in sc and tag:
                sample = (S.get("voice_samples", STYLE.get("voice_samples")) or {}).get(tag, sample)
            ref_audio = ws(sample)
            if not os.path.exists(ref_audio):
                if LEAN_DRY:
                    print(f"[lean-dry] {sc['id']}: voice_sample not found (ignored): {ref_audio}", flush=True)
                else:
                    raise SystemExit(f"{sc['id']}: voice_sample not found: {ref_audio}")
            who = STYLE.get("ref_labels", {}).get(tag, "the character") if tag else "the character"
            line = strip_speakers(sc["narration"])
            say = (STYLE.get("say_lines") or {}).get(tag) if tag else None   # per-speaker phrasing (e.g. a bodiless AI, an off-screen narrator)
            prompt = (f"Audio 1 is {who}'s voice. " + prompt + " " +
                      (say.format(line=line) if say else
                       f"{who[0].upper() + who[1:]} looks at the camera and says, in the voice of Audio 1, exactly these words and nothing else: \"{line}\""))
            if LEAN_DRY:
                ref_audio = None   # dry run: no fal call, the prompt file is the product
        open(f"{out}/{sc['id']}_prompt.txt", "w").write(prompt)
        if a.dry_run:
            placeholder_clip(f"{sc['id']}  {secs}s", secs, clip)
            return 0.0
        if os.path.exists(clip):
            return 0.0
        t, used = fal_clip(prompt, secs, a.resolution, clip, image=image, refs=refs, seed=sc.get("seed", S.get("seed", STYLE.get("seed"))), ref_videos=ref_videos, ref_audio=ref_audio, model=a.model)
        mode = f" (reference-to-video, {len(refs)} refs, {len(ref_videos)} ref videos{', lipsync' if ref_audio else ''})" if (refs or ref_videos or ref_audio) else (" (image-to-video)" if image else "")
        print(f"[fal] {sc['id']} {secs}s in {t:.0f}s via {used}{mode}", flush=True)
        return secs * MODELS[used]["price"][a.resolution]
    print(f"[clips] {a.model} @ {a.resolution} (scenes with refs/lipsync -> h3-max reference-to-video @ {os.environ.get('EXPLAIN_REF_RESOLUTION', '768P')}, same price)", flush=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        spend = sum(ex.map(make_clip, range(len(scenes))))
    # a failed submit (fal lock, rate limit) used to leave one clip missing and exit 0; retry those once, then fail loudly
    if not a.dry_run:
        missing = [i for i, sc in enumerate(scenes) if not os.path.exists(f"{out}/{sc['id']}_clip.mp4")]
        if missing:
            print(f"[clips] {len(missing)} clip(s) missing after the first pass ({', '.join(scenes[i]['id'] for i in missing)}); retrying once", flush=True)
            time.sleep(15)
            for i in missing:
                spend += make_clip(i)
            still = [scenes[i]["id"] for i in missing if not os.path.exists(f"{out}/{scenes[i]['id']}_clip.mp4")]
            if still:
                raise SystemExit(f"clips still missing after retry: {', '.join(still)}. Check the fal balance/lock and re-run; finished clips are cached.")

    # 3. per-scene mix
    scene_files, durs = [], []
    for i, sc in enumerate(scenes):
        f = f"{out}/{sc['id']}_scene.mp4"
        durs.append(build_scene(f"{out}/{sc['id']}_clip.mp4", f"{out}/{sc['id']}_nar.wav", f, sc["kind"] == "title",
                                lipsync=bool(sc.get("lipsync", S.get("lipsync", False))) and sc["kind"] != "title" and not a.dry_run,
                                model_audio=((sc.get("lipsync_audio", S.get("lipsync_audio", STYLE.get("lipsync_audio", "narration"))) == "model"
                                              and bool(sc.get("lipsync", S.get("lipsync", False))))
                                             or bool(sc.get("voice_sample", S.get("voice_sample")))) and sc["kind"] != "title" and not a.dry_run
                                             and not is_offscreen(sc)))
        scene_files.append(f)
    starts = [sum(durs[:i]) for i in range(len(durs))]

    # 4. concat
    lst = f"{out}/concat.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in scene_files))
    joined = f"{out}/joined.mp4"
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])

    # 5. music + captions
    final = f"{out}/{S.get('slug', 'explain')}.mp4"
    inputs = ["-i", joined]
    fc = []
    # outro: hold the last frame for `outro` seconds after the final line with the music bed still playing,
    # fading the whole mix over the last `outro_fade` seconds (JJK default 5 s / 2 s; other styles 0)
    outro = float(S.get("outro", STYLE.get("outro", 0.0)) or 0.0)
    outro_fade = min(outro, float(S.get("outro_fade", STYLE.get("outro_fade", 2.0)) or 0.0))
    total_len = dur(joined) + outro
    vsrc = "[0:v]"
    if outro > 0:
        fc.append(f"[0:v]tpad=stop_mode=clone:stop_duration={outro:.3f}[vx]"); vsrc = "[vx]"
        print(f"[outro] +{outro:.1f}s hold, {outro_fade:.1f}s fade", flush=True)
    fade = f",afade=t=out:st={total_len - outro_fade:.3f}:d={outro_fade:.3f}" if outro_fade > 0 else ""
    if full_nar:
        inputs += ["-i", full_nar]
        fc.append("[1:a]adelay=350|350,volume=8dB,apad[nar];[0:a]apad[a0];[a0][nar]amix=inputs=2:duration=first:normalize=0[base]")
        mi = 2
    else:
        fc.append("[0:a]apad[base]"); mi = 1
    if a.music and os.path.exists(a.music):
        inputs += ["-stream_loop", "-1", "-i", a.music]
        fc.append(f"[base]asplit=2[voice][key];"
                  f"[{mi}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=-15dB[mus];"
                  "[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=700[duck];"
                  f"[voice][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000{fade}[a]")
        amap = "[a]"
    else:
        if a.music:
            print(f"[music] not found: {a.music}", flush=True)
        fc.append(f"[base]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000{fade}[a]"); amap = "[a]"
    if a.no_captions:
        if outro > 0:
            vmap = "[vx]"
        else:
            vmap = "0:v"
    else:
        srt = f"{out}/captions.srt"
        timings = {}
        if LEAN and not a.dry_run:
            for sc in scenes:
                if sc["kind"] == "title" or not sc.get("narration", "").strip() or is_offscreen(sc):
                    continue
                sents = [x for x in re.split(r"(?<=[.!?])\s+", strip_speakers(sc["narration"])) if x]
                tm = lean_sentence_timings(f"{out}/{sc['id']}_clip.mp4", sents, f"{out}/{sc['id']}_words.json")
                if tm:
                    timings[sc["id"]] = tm
            print(f"[captions] lean mode: {len(timings)} scene(s) timed from the clip audio (whisper)", flush=True)
        write_srt(scenes, starts, nar_durs, srt, timings)
        style = "FontName=Helvetica Neue,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=1.5,Shadow=0,Alignment=2,MarginV=40"
        fc.append(f"{vsrc}subtitles='{srt}':force_style='{style}'[v]"); vmap = "[v]"
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", vmap, "-map", amap,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
        "-t", f"{total_len:.3f}", final])

    # 6. thumbnail: brightest, caption-free frame; prefer the domain reveal (first shot after a 領域展開 title)
    def yavg(path, t):
        r = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1",
                            "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"],
                           capture_output=True, text=True)
        import re
        m = re.findall(r"YAVG=([\d.]+)", r.stderr)
        return float(m[-1]) if m else 0.0
    shots = [i for i, sc in enumerate(scenes) if sc["kind"] != "title"]
    preferred = None
    for i, sc in enumerate(scenes):
        if sc["kind"] == "title" and STYLE.get("thumb_kanji") and STYLE["thumb_kanji"] in sc.get("kanji", ""):
            preferred = next((j for j in shots if j > i), None); break
    cands = []
    for j in shots:
        clip = f"{out}/{scenes[j]['id']}_clip.mp4"
        cd = dur(clip)
        for frac in (0.3, 0.5, 0.7):
            cands.append((j, clip, cd * frac, yavg(clip, cd * frac)))
    if cands:
        MIN_Y = 45.0  # never a black/near-black frame
        good = [c for c in cands if c[3] >= MIN_Y]
        pref = [c for c in good if c[0] == preferred]
        j, clip, t, _ = max(pref or good or cands, key=lambda c: c[3])
        thumb = f"{out}/thumb.jpg"
        sh(["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", clip, "-frames:v", "1", "-q:v", "2",
            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2", thumb])
        # make it frame one too (a 2-frame hold, invisible in playback, so every player's poster is this frame)
        hold = 2 / FPS
        tmp = final + ".tmp.mp4"
        sh(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{hold:.4f}", "-i", thumb,
            "-f", "lavfi", "-t", f"{hold:.4f}", "-i", "anullsrc=r=48000:cl=stereo", "-i", final,
            "-filter_complex", "[0:v]format=yuv420p,setsar=1[sv];[sv][1:a][2:v][2:a]concat=n=2:v=1:a=1[v][a]",
            "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", tmp])
        sh(["ffmpeg", "-y", "-i", tmp, "-i", thumb, "-map", "0", "-map", "1", "-c", "copy",
            "-c:v:1", "mjpeg", "-disposition:v:1", "attached_pic", "-movflags", "+faststart", final])
        os.remove(tmp)
        print(f"[thumb] {scenes[j]['id']} @ {t:.1f}s -> {thumb} (also frame 1 + cover art)", flush=True)
    total = dur(final)
    with open(f"{out}/transcript.md", "w") as f:
        f.write(f"# {S.get('topic', '')}\n\n")
        for sc, st in zip(scenes, starts):
            head = f"[{st:5.1f}s] {sc['id']}" + (f" TITLE {sc.get('kanji', '')} / {sc.get('english', '')}" if sc["kind"] == "title" else "")
            f.write(f"{head}\n{sc['narration']}\n\n")
    print(f"\n[done] {final}\n[summary] {len(scenes)} scenes, {total:.1f}s, fal spend ~${spend:.2f} ({a.model} {a.resolution}, regular price)", flush=True)


if __name__ == "__main__":
    main()
