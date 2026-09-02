#!/usr/bin/env python3
"""Render a /explain script.json into an mp4.

Pipeline per scene: TTS narration (OpenAI) -> clip (fal MiniMax H3-Max, or local title card /
dry-run placeholder) -> normalize + fit clip to narration -> mix. Then concat, music bed with
ducking, burned-in captions.

Usage: render.py script.json [--out DIR] [--dry-run] [--music FILE] [--resolution 768P|480P]
                             [--no-captions] [--voice onyx|fish] [--narration FILE] [--jobs 6]
       render.py --where            # print the workspace root (where out/ and assets/ live)
Env (or <repo>/.env): FAL_API_KEY (or FAL_KEY), FISH_AI_API_KEY, OPENAI_API_KEY,
     EXPLAIN_HOME (workspace root, default: the repo containing this script),
     EXPLAIN_MUSIC (music bed; default: first file in $EXPLAIN_HOME/assets/),
     EXPLAIN_JP_FONT / EXPLAIN_EN_FONT (fontconfig names for the title cards)
"""
import argparse, glob, json, math, os, subprocess, sys, textwrap, time
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


def default_music():
    if os.environ.get("EXPLAIN_MUSIC"):
        return os.environ["EXPLAIN_MUSIC"]
    hits = sorted(glob.glob(os.path.join(HOME, "assets", "*.m4a")) + glob.glob(os.path.join(HOME, "assets", "*.mp3"))
                  + glob.glob(os.path.join(HOME, "assets", "*.wav")))
    return hits[0] if hits else None

STYLE_LOCK = ("2D Japanese TV anime, dark modern shonen, 2020s prestige studio look, hand-drawn cel "
              "shading, flat color fills, thin clean linework with heavy black ink shadow shapes, "
              "painterly matte-painting background, desaturated navy and charcoal palette, film grain, "
              "24fps anime motion, limited animation with smear frames. ")
FAL_ENDPOINT = "minimax/h3-max/text-to-video"
FAL_PRICE = {"480P": 0.05, "768P": 0.08}  # $/s regular
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
FISH_VOICE = "179b5cc736974d96913c7849d0bb68c5"   # "jjk narrator" on fish.audio (454k generations)
FISH_MODEL = "s1"
FISH_SPEED = 1.0   # always 1.0: pacing comes from per-scene chunking + gaps, never from prosody
FISH_SPLIT = True    # one generation per sentence, stitched with real silence (the pauses are ours)
PAUSE_SENTENCE = 0.9    # seconds of silence between sentences


def split_sentences(text):
    import re
    return [t for t in re.split(r"(?<=[.!?])\s+", text.strip()) if t]


def fish_tts(text, out, speed=1.0):
    """Whole-scene generation by default; optional per-sentence generations stitched with silence."""
    key = os.environ.get("FISH_AI_API_KEY")
    if not key:
        raise SystemExit("FISH_AI_API_KEY not set")
    h = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": FISH_MODEL}
    parts = []
    chunks = split_sentences(text) if FISH_SPLIT else [" ".join(text.split())]
    for i, sent in enumerate(chunks):
        seg = f"{out[:-4]}_{i}.wav"
        if not os.path.exists(seg):
            for attempt in range(6):
                r = requests.post("https://api.fish.audio/v1/tts", headers=h, timeout=180, json={
                    "text": sent, "reference_id": FISH_VOICE, "format": "wav", "latency": "normal",
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
                  f"apad=pad_dur={PAUSE_SENTENCE if i < len(parts) - 1 else 0.15}[p{i}]")
    fc.append("".join(f"[p{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[a]")
    sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[a]", out])


def tts(text, voice, instructions, out):
    stamp = out + ".txt"
    sig = f"{voice}|{FISH_SPEED if voice == 'fish' else ''}|{text}\n{instructions}"
    if os.path.exists(out) and os.path.exists(stamp) and open(stamp).read() == sig:
        return
    open(stamp, "w").write(sig)
    if voice == "fish":
        return fish_tts(text, out, FISH_SPEED)
    from openai import OpenAI
    client = OpenAI()
    with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts", voice=voice, input=text,
            instructions=instructions, response_format="wav") as r:
        r.stream_to_file(out)


# ---------- clips ----------
def fal_clip(prompt, seconds, resolution, out, image=None):
    """image: optional local path used as the first frame (switches to the image-to-video endpoint)."""
    if os.path.exists(out):
        return 0.0
    key = os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")
    if not key:
        raise SystemExit("FAL_KEY / FAL_API_KEY not set (use --dry-run to test without it)")
    h = {"Authorization": f"Key {key}", "Content-Type": "application/json"}
    body = {"prompt": prompt, "duration": int(seconds), "resolution": resolution,
            "prompt_expansion_mode": "balanced"}
    endpoint = FAL_ENDPOINT
    if image:
        import base64, mimetypes
        mime = mimetypes.guess_type(image)[0] or "image/jpeg"
        body["image_url"] = f"data:{mime};base64," + base64.b64encode(open(image, "rb").read()).decode()
        endpoint = FAL_ENDPOINT.replace("text-to-video", "image-to-video")
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
    return time.time() - t0


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
    lines = kanji.split() or [kanji]
    # size each line to fit 90% of the width; first line largest
    parts = []
    y = -60 - 55 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        size = min(150 if i == 0 else 96, int(W * 0.9 / max(1, len(ln))))
        parts.append(f"drawtext=font='{JP_FONT}':text='{esc(ln)}':fontcolor=white:fontsize={size}:"
                     f"x=(w-tw)/2:y=(h-th)/2+({y}):alpha='if(lt(t,{0.15 + 0.25 * i}),0,1)'")
        y += size + 20
    parts.append(f"drawtext=font='{EN_FONT}':text='{esc(english)}':fontcolor=0xBBBBBB:fontsize=34:"
                 f"x=(w-tw)/2:y=(h-th)/2+({y + 10}):alpha='if(lt(t,0.7),0,min(1,(t-0.7)/0.4))'")
    parts.append("noise=alls=6:allf=t")
    sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={seconds}",
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-vf", ",".join(parts), "-t", str(seconds),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", out])


# ---------- per-scene assembly ----------
def build_scene(clip, nar, out, is_title):
    """Normalize clip, extend to cover narration, mix narration over clip audio."""
    if os.path.exists(out):
        return dur(out)
    cd, nd = dur(clip), dur(nar)
    lead = 0.6
    target = max(cd, nd + lead + 1.0)
    amb_gain = "-100dB" if is_title else "-9dB"
    fc = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
          f"fps={FPS},format=yuv420p,tpad=stop_mode=clone:stop_duration={max(0, target-cd)+0.1}[v];"
          f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={amb_gain},apad[amb];"
          f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={int(lead*1000)}|{int(lead*1000)}[nar];"
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
        text = sc["narration"].strip()
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
    ap.add_argument("--music", default=default_music())
    ap.add_argument("--resolution", default="768P", choices=["480P", "768P"])
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
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.script)), "render")
    os.makedirs(out, exist_ok=True)
    scenes = S["scenes"]
    instr = S.get("narrator_voice", "Deep, calm, solemn anime narrator. Slow, deliberate, absolute. Pause at full stops.")
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
    else:
        print(f"[tts] {len(scenes)} scenes via " + ("fish.audio/" + FISH_MODEL + " jjk narrator, per-sentence" if a.voice == "fish" else f"gpt-4o-mini-tts/{a.voice}"), flush=True)
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
            import re
            vp, n = re.subn(r"\b[Tt]he (sorceress|sorcerer|user|character|protagonist)\b", cast, vp, count=1)
            if n == 0:
                vp = cast[0].upper() + cast[1:] + " is present. " + vp
        prompt = STYLE_LOCK + vp + " No dialogue, no on-screen text. Sound: " + sc.get("sound", "low ominous drone") + "."
        open(f"{out}/{sc['id']}_prompt.txt", "w").write(prompt)
        if a.dry_run:
            placeholder_clip(f"{sc['id']}  {secs}s", secs, clip)
            return 0.0
        if os.path.exists(clip):
            return 0.0
        image = sc.get("image", S.get("image"))
        if image:
            image = os.path.expanduser(image)
            if not os.path.isabs(image):
                image = os.path.join(HOME, image)
        t = fal_clip(prompt, secs, a.resolution, clip, image=image)
        print(f"[fal] {sc['id']} {secs}s in {t:.0f}s" + (" (image-to-video)" if image else ""), flush=True)
        return secs * FAL_PRICE[a.resolution]
    print(f"[clips] {FAL_ENDPOINT} @ {a.resolution}", flush=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        spend = sum(ex.map(make_clip, range(len(scenes))))

    # 3. per-scene mix
    scene_files, durs = [], []
    for i, sc in enumerate(scenes):
        f = f"{out}/{sc['id']}_scene.mp4"
        durs.append(build_scene(f"{out}/{sc['id']}_clip.mp4", f"{out}/{sc['id']}_nar.wav", f, sc["kind"] == "title"))
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
        if sc["kind"] == "title" and "領域" in sc.get("kanji", ""):
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
    print(f"\n[done] {final}\n[summary] {len(scenes)} scenes, {total:.1f}s, fal spend ~${spend:.2f} ({a.resolution})", flush=True)


if __name__ == "__main__":
    main()
