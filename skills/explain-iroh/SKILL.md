---
name: explain-iroh
description: Explain a concept as a ~60-80s warm tea-shop lesson from an old firebending master to a stuck student (Uncle Iroh style). Same pipeline as /explain (script.json, MiniMax H3-Max clips on fal, fish.audio voice, ffmpeg), different bible, style lock, voice and title cards.
argument-hint: <concept or question> [--tier form|set|mastery] [--register iroh-teaching|iroh-gentle|iroh-playful] [--dry-run]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py *), Bash(open *), Bash(osascript *)
---

# /explain-iroh

Turn `$ARGUMENTS` into an old-master tea lesson video. The renderer is shared with `/explain`: `${CLAUDE_SKILL_DIR}/../explain/scripts/render.py`. The only switch is `"style": "iroh"` in script.json.

## 1. Load the bible
Read `${CLAUDE_SKILL_DIR}/reference.md` (how the master teaches, beats, registers, tiers, style lock, cast paragraph, title-card and sound vocabulary). Do not skip it; it is the whole voice. Do not load the JJK bible; the two voices must not blend.

## 2. Understand the concept
If the concept refers to the current conversation or codebase, gather what you need first. Reduce it to: the student's frustration (what is stuck), the physical metaphor (something on the table), the mechanism in one breath, the borrowed wisdom (a second discipline it resembles), the caution (the cost or the pride trap), and the line the student says when they get it. Pick a tier unless `--tier` is given. Roll the "temperature": vary tier, register, the student, the setting and the metaphor; never reuse the previous run's student or metaphor. The master paragraph is fixed; the student changes.

Object references: if the concept is or contains a specific complicated object (a drive, a gripper, an engine, a specific character, vehicle or product), fetch 2-3 reference images of it first via a research subagent and pass them as `"objects"` (see the bible's "Object references" section). The model will not get a complicated shape right from words alone.

## 3. Write `script.json`
Workspace root: `python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py --where` (the repo, or `$EXPLAIN_HOME`). Path: `<workspace>/out/<slug>-iroh/script.json` (slug = kebab of the concept; the `-iroh` suffix keeps it apart from a JJK take on the same concept). Shape and rules are in reference.md. Mandatory: `"style": "iroh"` at the top level (without it the renderer uses the JJK look and voice). Target 60-80 s: 115-145 words, 6-8 scenes, 1-2 title cards. Title-card `kanji` is Chinese, two space-separated groups (category, then name). Every shot gets a `video_prompt` that stands alone (the renderer prepends the Iroh style lock) and a `sound` line from the bible's vocabulary. Exactly one concrete number in the whole script; the concept is a physical thing the characters touch.

## 4. Render
```
python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py <workspace>/out/<slug>-iroh/script.json --voice fish
```
Flags are the same as `/explain`: `--dry-run` (placeholder clips, no fal spend), `--music /path.mp3` (default for this style: first audio file in `<workspace>/assets/iroh/`, else `assets/`, else `$EXPLAIN_MUSIC`), `--resolution 480P` (cheaper probe), `--no-captions`, `--narration FILE`, `--voice fish` (the Iroh fish.audio voice, picked automatically from the style; override with `IROH_FISH_VOICE_ID`), `--voice onyx` (OpenAI fallback).
Model and resolution: defaults are `h3-max-turbo` at `480P` (the cheapest: $0.025/s regular, $0.00625/s until 2026-09-07). Override with `--model h3-max|h3-max-turbo`, `--resolution 480P|768P`, a top-level `"model"` / `"resolution"` in script.json, or `EXPLAIN_MODEL` / `EXPLAIN_RESOLUTION` in the environment or `.env`. Turbo has no reference endpoint, so any scene with `refs`, `ref_videos` or `lipsync` is routed to `h3-max` reference-to-video automatically ($0.08/s at either resolution; Reference-to-video costs the same at 480P and 768P, so the renderer always requests reference scenes at 768P (`EXPLAIN_REF_RESOLUTION` overrides). the log line per clip names the model used).
Keys: the renderer reads `<workspace>/.env` (see `.env.example`) and the environment. If they live only in the user's shell rc, load them without printing: `eval "$(grep -E "^\s*export (FAL_API_KEY|FISH_AI_API_KEY|OPENAI_API_KEY)=" ~/.zshrc)"`. If the fal key is missing, run with `--dry-run` and tell the user.

### Lean mode (the default): no per-scene TTS
The style carries `voice_sample: assets/ref/iroh/iroh-voice.wav` (a 12 s clip of the Iroh voice). With no `lipsync` key in the script, the renderer skips Fish entirely: each shot's narration is written into the prompt ("says, in the voice of Audio 1, exactly these words"), the sample goes in as `reference_audio_urls`, and the model speaks the line in sync with the mouth. Scene length is estimated from word count (1.9 words/s plus pauses), so keep each shot under ~22 words; title cards are silent over music. Speaker tags are ignored in lean mode (one voice per script). Set `"voice_sample": null` or `"lipsync": true` to go back to Fish narration. Cost is the reference-to-video rate ($0.08/s) whatever the model default.

### Lip sync via Fish narration (alternative)
Set `"lipsync": true` at the top level (or per scene). The renderer passes that scene's finished narration wav as `reference_audio_urls` on the reference-to-video call; the model then speaks the same words at the same timing and animates the mouth to them, and the mix keeps the model's own re-spoken track as the voice (`lipsync_audio: "model"`, the style default), because the model drifts after sentence pauses and our narration would fall out of sync with the mouth. The Fish narration is still generated: it is the reference the model imitates, and it drives the captions and scene timing. Verified 2026-09-02: voice and sync judged "perfect" by the user. Hard limit: the endpoint takes 2-15 s of reference audio, so with 1.4 s sentence pauses keep every shot's narration under ~22 words and 3 sentences; a longer scene silently loses lip sync (the log prints `[lipsync] sN: ... skipping`). Write the prompt with him "looking straight into the camera and speaking to the viewer, mouth moving as he talks".

### Two voices
Narration may switch speakers inline with tags: `[zuko] Uncle, does it think? [iroh] No. It guesses the next word.` Untagged text is the master. Each tag maps to a fish.audio voice in the style's `voices` table in `render.py` (`iroh` = the user's clone, `zuko` = the public "Prince Zuko" voice). Tags are stripped from captions. Use the student's voice only for his own short lines (beats 2 and 7), never for explanation. Keep the master plain and direct: he explains like a grandfather who wants to be understood, not admired; one image per idea, then the idea in ordinary words.

### Music (three beds in `assets/iroh/`, pick per lesson)
Set `"music"` at the top level of script.json (bare name, substring match against `assets/iroh/`): `"tsungi"` = Iroh's Tsungi Horn, gentle and playful, the default mood for a tea-shop lesson; `"leaves"` = Leaves from the Vine, quiet grief, for loss or cost concepts (iroh-gentle register); `"agni"` = The Last Agni Kai, slow and solemn strings, for a caution or mastery beat that must land heavily. `--music FILE` on the command line overrides; with neither, the first file alphabetically in `assets/iroh/` is used.

### Reference stills and video (the likeness path)
Two mechanisms, both paths relative to the workspace root:
- `"refs": ["assets/ref/iroh/front.jpg", "assets/ref/iroh/three-quarter.jpg", "assets/ref/iroh/profile.jpg", "assets/ref/iroh/full.jpg"]` at script top level (or per scene) routes every shot to `minimax/h3-max/reference-to-video` (up to 9 images; the renderer prepends "Image 1 to Image N show the same character; keep the face, hair, beard and clothes consistent"). Use the same 3-4 character-sheet images in every clip and set a top-level `"seed"` so the master stays the same person across shots. The prompt then describes only action, camera and setting. Cost: $0.08/s of output; the first ~4 reference images are free.
- `"ref_videos": ["assets/ref/iroh/iroh-ref-6s.mp4"]` (top level or per scene, up to 3, keep each under ~10 s and 480p, no burned-in captions) adds `reference_video_urls` on the same endpoint so the model copies how the master moves and gestures; the renderer prepends "Video 1 shows how the same character moves". Untested as of 2026-09-02; try on one scene first.
- `"image": "assets/ref/iroh/bust.jpg"` on a scene uses that still as the clip's first frame (image-to-video). Use on 2-3 shots at most, or every clip opens on the same pose. `refs` wins when both are given.
Stills on disk now (2026-09-02): `full.jpg` (green robes, full body, 16:9), `bust.jpg` (smiling bust, 16:9), `paisho.jpg`, plus `iroh-*.png` character crops and `set-*.png` tea-shop settings. Default refs: `["assets/ref/iroh/full.jpg", "assets/ref/iroh/iroh-smile-bust.png", "assets/ref/iroh/iroh-paisho.png", "assets/ref/iroh/iroh-tan-full.png"]`; the stills wear green tea-shop robes, so describe him in green, not red, when using them.
Making more sheet views: generate 3-4 views of the master (front bust, three-quarter, profile, full body at a tea counter) with Midjourney (`--cref` between views), Nano Banana or GPT image, from the cast paragraph verbatim + the style lock + "plain warm parchment background, 16:9, 1280x720". Exact tuned prompt: TODO. Save under `assets/ref/iroh/`. If the folder is empty, render text-only; do not stop for it. Voice stays fish.audio; do not use the endpoint's `reference_audio_urls`.

## 5. Deliver
Print the script scene by scene (master and student lines), the final path, then open the mp4. QuickTime shows a blank document if the same path was re-rendered while open, so quit it first: `osascript -e 'tell application "QuickTime Player" to quit'; open -a "QuickTime Player" <path>`. Report cost from the renderer's summary line.
