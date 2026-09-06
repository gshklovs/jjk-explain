---
name: explain-clav
description: Explain a concept as a ~45-60s deadpan short from a fast-talking looksmaxxing streamer to his phone camera (Clavicular / "Clav" style): a hook question, one blunt analogy carried all the way, hard cuts to a visual the instant a thing is named, one number, a one-word verdict. Same pipeline as /explain (script.json, MiniMax H3-Max clips on fal, ffmpeg), different bible, phone-shot style lock, seeded on real-footage stills, a clip-cut voice sample (lean mode, no TTS on character shots), big word-group captions with one yellow word, 1.5 s word-slam title, no music.
argument-hint: <concept or question> [--tier verdict|playbook|full] [--register clav-deadpan|clav-rant|clav-rating] [--dry-run]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py *), Bash(open *), Bash(osascript *)
---

# /explain-clav

Turn `$ARGUMENTS` into a short: he asks the viewer's question, names a concrete running example, shows the wrong way, states the one idea inside an analogy, shows the right way and the one number, and ends on a verdict word. The renderer is shared with `/explain`: `${CLAUDE_SKILL_DIR}/../explain/scripts/render.py`. The only switch is `"style": "clav"` in script.json.

## 1. Load the bible
Read `${CLAUDE_SKILL_DIR}/reference.md` (how he teaches, anchor lines, the beats, registers, tiers, style lock, cast paragraph, captions and snap rules, the six-shot arc). Do not skip it; it is the whole voice. Do not load the JJK, Iroh, Rick, Stark or HxH bibles; the voices must not blend.

## 2. Understand the concept
If the concept refers to the current conversation or codebase, gather what you need first. Reduce it to: the viewer's pain as a question, the running example (a concrete everyday product, never anything from the content or marketing business), the analogy that carries the whole short, the wrong way (what the copy does and why it fails), the one idea that makes the right way work, the one number, and the verdict word. Pick a tier unless `--tier` is given. Roll the "temperature": vary tier, register, the running example and the verdict word; never reuse the previous run's example. The cast paragraph is fixed; the room may change.

Object references: if the concept is or contains a specific complicated object (a branded sneaker, a drive, an engine), fetch 2-3 reference images of it first via a research subagent and pass them as `"objects"` or as a snap's `"image"` (see the bible's "Object references" section).

## 3. Write `script.json`
Workspace root: `python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py --where` (the repo, or `$EXPLAIN_HOME`). Path: `<workspace>/out/<slug>-clav/script.json`. Shape and rules are in reference.md. Mandatory: `"style": "clav"` at the top level. Target 45-60 s: 100-125 words, six shots after an optional 1.5 s word-slam title (`"kanji"` holds the English title in caps, `"english"` the subtitle; omit the title scene for no card). Character shots at most 22 words, snaps 10-16. Every shot gets a `video_prompt` that stands alone (the renderer prepends the style lock and the reference-image prefix) and a `sound` line ending in "no music". Exactly one concrete number in the whole script. Never name him, the platforms or any brand in a video prompt.

Prompts: on character shots paste the cast paragraph verbatim (the renderer checks the first 40 characters, "a young man with dark wavy hair, a sharp") and add one small gesture; he looks into the lens in this style. On snap shots never mention him; describe the picture the line names, with "no face near the camera, no readable text anywhere". Add `"keywords"` per scene for the words the captions should paint yellow, and `"labels"` on snaps for anything enumerated.

Default shape: the bible's six-shot arc (hook, the wrong way, the mechanism, the right way, the number, the verdict), alternating `"shot": "character"` (face on screen, lip-synced on the reference path) and `"shot": "snap"` (no face: b-roll, a side-by-side, a card; turbo, dubbed by the Fish clone, cut to the line). Then ASK THE USER (AskUserQuestion, one question, multi-select over the shots) which shots should be lip-synced character shots and which dubbed snaps, showing the proposed kind and the estimated cost per shot (character ~$0.50, snap ~$0.15-0.25 at 480P regular price); apply their answer before rendering.

## 4. Render
```
python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py <workspace>/out/<slug>-clav/script.json
```
Flags are the same as `/explain`: `--dry-run` (placeholder clips, no fal spend; add `EXPLAIN_LEAN_DRY=1` to the environment to see the assembled lean prompts in `render/*_prompt.txt` and the caption file `render/captions.ass`), `--resolution 480P|768P`, `--no-captions`, `--music FILE` (off by default), `--voice fish` (Fish narration for everything, using the style's clone).
Model: character shots use reference stills and the voice sample, so they route to `h3-max` reference-to-video ($0.05/s at 480P); snaps route to `h3-max-turbo` ($0.025/s) and are dubbed with Fish. A six-shot short is about $2.50 at 480P. Dry-run first and read the prompts.
Keys: the renderer reads `<workspace>/.env` and the environment. If they live only in the user's shell rc, load them without printing: `eval "$(grep -E "^\s*export (FAL_API_KEY|FISH_AI_API_KEY|OPENAI_API_KEY)=" ~/.zshrc)"`. `FAL_API_KEY` for the clips, `FISH_AI_API_KEY` for the snap dubs, `OPENAI_API_KEY` for Whisper (caption and label timing; without it captions fall back to an even spread). If a key is missing, run with `--dry-run` and tell the user.

### Lean mode (the default): one clip-cut voice sample, no TTS on character shots
The style carries `voice_sample: "assets/ref/clav/clav-voice.wav"` (14 s of him alone, cut from the interview clip). With no `lipsync` key in the script, the renderer skips TTS on character shots: the narration is written into the prompt ("the young man looks straight into the phone camera, deadpan, small hand gestures, and says, in the voice of Audio 1, exactly these words"), the sample goes in as `reference_audio_urls`, and the model speaks the line in sync with the mouth. Scene length is estimated from word count (`words_per_sec` 2.8 plus 0.5 s per sentence pause), so keep each character shot at or under 22 words. Snap shots are work shots: rendered silent on turbo and dubbed with the style's Fish voice, then cut to the length of the dub (plus 0.3 s, never under 2.5 s). Set `"voice_sample": null` or `"lipsync": true` to go back to Fish narration everywhere.

### Captions in his style
The style sets `"captions": {"mode": "words"}`: the renderer writes `render/captions.ass` with the line in groups of two to four words, bold white caps (Arial Black, 64 px on 720p) with a thick black outline, centred just below the middle of the frame, one word per group in yellow, timed from Whisper on each shot's own audio. `"keywords"` on a scene picks the yellow words; otherwise numbers, then the longest non-stopword. A script-level `"captions"` object overrides the style's (`group`, `size`, `y`, `font`, `color`, `highlight` as BGR hex, `outline`, `upper`). `--no-captions` turns them off. The other styles keep their per-sentence bottom subtitles.

### The Fish voice (snap dubs)
`voices: {"clav": ...}` is a private fish.audio clone made from `clav-voice.wav` (`8a50551a527348a78507cb83fa300773`, on the user's account). `CLAV_FISH_VOICE_ID` overrides it; public "clav" / "Clavicular" voices exist on fish.audio (ids in `docs/clav-research.md`). Needs `FISH_AI_API_KEY`.

### No music
`music: None`: no bed unless `--music FILE` or a script `"music"` key. The `sound` lines carry the room and the b-roll.

### Reference stills and video (the likeness path)
Paths relative to the workspace root, all under `assets/ref/clav/` (gitignored; the recipe is in `docs/clav-research.md`):
- Default refs: `clav-face.jpg` (interview close-up), `clav-bust.jpg`, `clav-hands.jpg`, `clav-3q.jpg`, `clav-wide.jpg` (1280x720 crops of him in the ad's office) with `"seed": 1217`. The renderer prepends "Image 1 to Image 5 show the same young man; keep his face, dark wavy hair, jawline and build consistent with them; his clothes and the room follow the description." Override with a top-level or per-scene `"refs"` / `"seed"`; `"refs": []` renders text-only. A default still missing from disk is skipped with a `[refs]` warning.
- User seeds: crop the user's image 16:9 at 1280x720, save it as `user-<n>.jpg` and list it FIRST in a top-level `"refs"`.
- Extras: `clav-face-2.jpg` (second close-up), `clav-ref.mp4` (7 s 480p of him talking with both hands) for `"ref_videos"` (untested on the endpoint; try on one scene first).
- `"image": "<path>"` on a snap uses a fetched photo as the first frame (turbo image-to-video); `"objects"` refs move the shot to the reference model.
Making more stills: 16:9 windows of the source clips scaled to 1280x720, burned-in captions cropped out; the vertical interview frame's face is taller than any 16:9 window, so close-ups there are eyes-to-chin. View every frame before keeping.

## 5. Deliver
Print the script scene by scene, the final path, then open the mp4. QuickTime shows a blank document if the same path was re-rendered while open, so quit it first: `osascript -e 'tell application "QuickTime Player" to quit'; open -a "QuickTime Player" <path>`. Report cost from the renderer's summary line.
