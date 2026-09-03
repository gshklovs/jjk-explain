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
Styles: script.json may carry a top-level "style": "jjk" (default) | "iroh". The style picks the
     prompt style lock, the title-card look, the default fish voice and the default music
     ($EXPLAIN_HOME/assets/iroh/ first for iroh, then $EXPLAIN_HOME/assets/).
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
    sig = f"{voice}|{(STYLE['fish_voice'] + '@' + str(fspeed) + '/' + str(STYLE.get('pause', PAUSE_SENTENCE)) + str(sorted(STYLE.get('voices', {}).items()))) if voice == 'fish' else ''}|{text}\n{instructions}"
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
        endpoint = base + "/reference-to-video"
    elif image:
        body["image_url"] = _data_url(image)
        endpoint = base + "/image-to-video"
    else:
        body["aspect_ratio"] = "16:9"
    r = requests.post(f"https://queue.fal.run/{endpoint}", json=body, headers=h, timeout=60)
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
    lines = kanji.split() or [kanji]
    # size each line to fit 90% of the width; first line largest
    parts = []
    y = -60 - 55 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        size = min(150 if i == 0 else 96, int(W * 0.9 / max(1, len(ln))))
        parts.append(f"drawtext=font='{JP_FONT}':text='{esc(ln)}':fontcolor={T['ink']}:fontsize={size}:"
                     f"x=(w-tw)/2:y=(h-th)/2+({y}):alpha='if(lt(t,{0.15 + 0.25 * i}),0,1)'")
        y += size + 20
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


def write_srt(scenes, starts, nar_durs, path):
    """One cue per sentence, spread proportionally to character count within the narration."""
    import re
    n, lines = 1, []
    for sc, st, nd in zip(scenes, starts, nar_durs):
        text = strip_speakers(sc["narration"])
        sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]
        total = sum(len(s) for s in sents) or 1
        t = st + 0.35
        for s in sents:
            d = nd * len(s) / total
            a, b = t, t + d
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
        a.music = resolve_music(S.get("music"), style) or default_music(style)
    a.resolution = a.resolution or S.get("resolution") or DEFAULT_RESOLUTION
    a.model = a.model or S.get("model") or DEFAULT_MODEL
    if a.model not in MODELS:
        raise SystemExit(f"unknown model {a.model!r}; known: {', '.join(MODELS)}")
    # lean mode: a voice sample (script "voice_sample", else the style default) and no explicit lipsync
    # -> skip TTS, the model speaks each scene's narration in that voice. "voice_sample": null turns it off.
    _vs = S["voice_sample"] if "voice_sample" in S else STYLE.get("voice_sample")
    LEAN = None
    if _vs and not S.get("lipsync") and not a.dry_run and a.narration is None:
        LEAN = _vs if os.path.isabs(_vs) else os.path.join(HOME, _vs)
        if not os.path.exists(LEAN):
            raise SystemExit(f"voice_sample not found: {LEAN}")
        S["voice_sample"] = LEAN
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
        # lean mode: no TTS; silent stand-ins sized from word count, the video model speaks the lines
        print(f"[lean] no TTS; {os.path.basename(LEAN)} sets the voice, prompts carry the lines", flush=True)
        pause = STYLE.get("pause", PAUSE_SENTENCE)
        nar_durs = []
        for sc in scenes:
            text = strip_speakers(sc["narration"])
            nd = 3.0 if sc["kind"] == "title" else min(14.0, len(text.split()) / 1.9 + pause * max(0, len(split_sentences(text)) - 1) + 0.6)
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
        speaks = bool(sc.get("lipsync", S.get("lipsync", False)) or sc.get("voice_sample", S.get("voice_sample")))
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
        ref_videos = [ws(v) for v in (sc.get("ref_videos", S.get("ref_videos")) or [])]
        missing = [r for r in refs + ref_videos if not os.path.exists(r)]
        if missing:
            raise SystemExit(f"{sc['id']}: reference image(s) not found: {', '.join(missing)}")
        if refs:
            # cite the sheet so the model binds the description to the pictures
            prompt = f"Image 1 to Image {len(refs)} show the same character; keep the face, hair, beard and clothes consistent with them. " + prompt
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
        sample = sc.get("voice_sample", S.get("voice_sample"))
        if sample and not ref_audio and not a.dry_run:
            # lean mode: one voice sample sets the voice; the video_prompt carries the words the character says
            ref_audio = ws(sample)
            if not os.path.exists(ref_audio):
                raise SystemExit(f"{sc['id']}: voice_sample not found: {ref_audio}")
            line = strip_speakers(sc["narration"])
            prompt = ("Audio 1 is the character's voice. " + prompt +
                      f" The character looks at the camera and says, in the voice of Audio 1, exactly these words and nothing else: \"{line}\"")
        open(f"{out}/{sc['id']}_prompt.txt", "w").write(prompt)
        if a.dry_run:
            placeholder_clip(f"{sc['id']}  {secs}s", secs, clip)
            return 0.0
        if os.path.exists(clip):
            return 0.0
        t, used = fal_clip(prompt, secs, a.resolution, clip, image=image, refs=refs, seed=sc.get("seed", S.get("seed")), ref_videos=ref_videos, ref_audio=ref_audio, model=a.model)
        mode = f" (reference-to-video, {len(refs)} refs, {len(ref_videos)} ref videos{', lipsync' if ref_audio else ''})" if (refs or ref_videos or ref_audio) else (" (image-to-video)" if image else "")
        print(f"[fal] {sc['id']} {secs}s in {t:.0f}s via {used}{mode}", flush=True)
        return secs * MODELS[used]["price"][a.resolution]
    print(f"[clips] {a.model} @ {a.resolution} (scenes with refs/lipsync -> h3-max reference-to-video)", flush=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        spend = sum(ex.map(make_clip, range(len(scenes))))

    # 3. per-scene mix
    scene_files, durs = [], []
    for i, sc in enumerate(scenes):
        f = f"{out}/{sc['id']}_scene.mp4"
        durs.append(build_scene(f"{out}/{sc['id']}_clip.mp4", f"{out}/{sc['id']}_nar.wav", f, sc["kind"] == "title",
                                lipsync=bool(sc.get("lipsync", S.get("lipsync", False))) and sc["kind"] != "title" and not a.dry_run,
                                model_audio=((sc.get("lipsync_audio", S.get("lipsync_audio", STYLE.get("lipsync_audio", "narration"))) == "model"
                                              and bool(sc.get("lipsync", S.get("lipsync", False))))
                                             or bool(sc.get("voice_sample", S.get("voice_sample")))) and sc["kind"] != "title" and not a.dry_run))
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
    if full_nar:
        inputs += ["-i", full_nar]
        fc.append("[1:a]adelay=350|350,volume=8dB,apad[nar];[0:a][nar]amix=inputs=2:duration=first:normalize=0[base]")
        mi = 2
    else:
        fc.append("[0:a]anull[base]"); mi = 1
    if a.music and os.path.exists(a.music):
        inputs += ["-stream_loop", "-1", "-i", a.music]
        fc.append(f"[base]asplit=2[voice][key];"
                  f"[{mi}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=-15dB[mus];"
                  "[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=700[duck];"
                  "[voice][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]")
        amap = "[a]"
    else:
        if a.music:
            print(f"[music] not found: {a.music}", flush=True)
        fc.append("[base]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"); amap = "[a]"
    if a.no_captions:
        vmap = "0:v"
    else:
        srt = f"{out}/captions.srt"
        write_srt(scenes, starts, nar_durs, srt)
        style = "FontName=Helvetica Neue,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=1.5,Shadow=0,Alignment=2,MarginV=40"
        fc.append(f"[0:v]subtitles='{srt}':force_style='{style}'[v]"); vmap = "[v]"
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", vmap, "-map", amap,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", final])

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
        if sc["kind"] == "title" and STYLE["thumb_kanji"] in sc.get("kanji", ""):
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
