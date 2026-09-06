---
name: explain-matan
description: Explain a concept as a ~45-60s deadpan interview with no guest, from a teenage podcast host at a black folding table (Matan Even / "The Matan Show" style): an absurd premise asked as a sincere question, the answer treated as data, the idea pushed one step past where it breaks, half the shots documentary b-roll, one number, an abrupt administrative exit. Same pipeline as /explain (script.json, MiniMax H3-Max clips on fal, ffmpeg), different bible, locked-off studio style lock, seeded on real-footage stills, a clip-cut voice sample (lean mode, no TTS on character shots), a private fish.audio clone for the snaps, word-group captions with one yellow word, 1.5 s word-slam title, no music.
argument-hint: <concept or question> [--tier verdict|playbook|full] [--register matan-deadpan|matan-gotcha|matan-game] [--dry-run]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py *), Bash(open *), Bash(osascript *)
---

# /explain-matan

Turn `$ARGUMENTS` into a short: he asks the viewer a question with a ridiculous premise, names a concrete running example inside it, shows what everyone does instead, states the one idea as if reading it off his card, pushes it to its limit inside the example, rewrites the concept's slogan as one of his questions, and ends the show because the next guest is here. The renderer is shared with `/explain`: `${CLAUDE_SKILL_DIR}/../explain/scripts/render.py`. The only switch is `"style": "matan"` in script.json.

## 1. Load the bible
Read `${CLAUDE_SKILL_DIR}/reference.md` (how he teaches, anchor lines, the beats, registers, tiers, style lock, cast paragraph, captions and snap rules, the six-shot arc). Do not skip it; it is the whole voice. Do not load the JJK, Iroh, Rick, Stark, HxH or Clav bibles; the voices must not blend (Clav is the guest in the seed interview, not the host; his verdict vocabulary and ratings belong to `/explain-clav`).

## 2. Understand the concept
If the concept refers to the current conversation or codebase, gather what you need first. Reduce it to: the absurd premise as a question, the running example (a concrete everyday trade or place, never anything from the podcast, content or interview business), the wrong way (what everyone does instead and why), the one idea, the limit it reaches inside the example, the concept's slogan rewritten as his question, the one number, and the exit line. Pick a tier unless `--tier` is given. Roll the "temperature": vary tier, register, the running example and the exit; never reuse the previous run's example. The cast paragraph is fixed; the room may change.

Object references: if the concept is or contains a specific complicated object (a branded sneaker, a drive, an engine), fetch 2-3 reference images of it first via a research subagent and pass them as `"objects"` or as a snap's `"image"` (see the bible's "Object references" section).

## 3. Write `script.json`
Workspace root: `python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py --where` (the repo, or `$EXPLAIN_HOME`). Path: `<workspace>/out/<slug>-matan/script.json`. Shape and rules are in reference.md. Mandatory: `"style": "matan"` at the top level. Target 45-60 s: 100-125 words, six shots after an optional 1.5 s word-slam title (`"kanji"` holds the English title in caps, `"english"` the subtitle; omit the title scene for no card). Character shots at most 22 words, snaps 10-16. Every shot gets a `video_prompt` that stands alone (the renderer prepends the style lock and the reference-image prefix) and a `sound` line ending in "no music". Exactly one concrete number in the whole script. Never name him, the show, the guest, the platforms or any brand in a video prompt.

Prompts: on character shots paste the cast paragraph verbatim (the renderer checks the first 40 characters, "a teenage-looking young man with a big m") and add one small action; he looks into the lens as if it were the guest. On snap shots never mention him; describe the picture the line names, with "no face near the camera, no readable text anywhere". Add `"keywords"` per scene for the words the captions should paint yellow, and `"labels"` on snaps for anything enumerated.

Default shape: the bible's six-shot arc (hook, the wrong way, the premise, the mechanism, the trick, the verdict): three `"shot": "character"` shots (the hook, the premise, the verdict; face on screen, lip-synced on the reference path from the stills and the voice sample) interleaved with three `"shot": "snap"` shots (no face: documentary b-roll, a side-by-side, a thing on the table; turbo, dubbed by the Fish clone, cut to the line). Never two character shots in a row. Then ASK THE USER (AskUserQuestion, one question, multi-select over the shots) which shots should change kind, showing the proposed kind and the estimated cost per shot (snap ~$0.15-0.25, character ~$0.35-0.50 at 480P regular price); apply their answer before rendering. When the user is not in the loop, keep the default split.

Quirk budget, verified before rendering (the bible's "Quirk budget"): it is a ceiling. (1) the hook is an absurd premise asked straight, always; (2) then at most one or two of: the logic pushed one step too far, the flat restatement ("Yeah, I mean, that's a lot of pipes."), a callback, "But congratulations.", one unexplained non-sequitur question, the administrative exit ("That's it. I have to film with the plumber in five minutes."); (3) the concept's slogan rewritten as one of his questions; a famous phrasing left intact has failed item 3. Never a rating, a decimal or "bro": those are the other short-form voice. If a line would work without the quirk, leave the quirk out.

## 4. Render
```
python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py <workspace>/out/<slug>-matan/script.json
```
Flags are the same as `/explain`: `--dry-run` (placeholder clips, no fal spend; add `EXPLAIN_LEAN_DRY=1` to the environment to see the assembled lean prompts in `render/*_prompt.txt` and the caption file `render/captions.ass`), `--resolution 480P|768P`, `--no-captions`, `--music FILE` (off by default), `--voice fish` (Fish narration for everything, using the style's clone).
Model: snaps route to `h3-max-turbo` ($0.025/s) and are dubbed with Fish; character shots use reference stills and the voice sample, so they route to `h3-max` reference-to-video ($0.05/s at 480P). Three of each is about $2.5 at 480P. Dry-run first and read the prompts; run the sound-off test (strip the narration: the pictures should still tell the story in order); grep the prompts for digits and for sign|price|menu|label|screen|text|number|written|chalk|form.
Proving refs out: the default stills are 1080p-native close-ups from his guest appearances plus his own studio; they held on the first render (`out/schlep-blindness-matan/`, three character shots), pending the user's verdict. Look at a contact sheet: if any character shot is not clearly him, convert it to a snap and re-render that shot on turbo (the bible's "Never lip-sync a stranger").
Keys: the renderer reads `<workspace>/.env` and the environment. If they live only in the user's shell rc, load them without printing: `eval "$(grep -E "^\s*export (FAL_API_KEY|FISH_AI_API_KEY|OPENAI_API_KEY)=" ~/.zshrc)"`. `FAL_API_KEY` for the clips, `FISH_AI_API_KEY` for the snap dubs, `OPENAI_API_KEY` for Whisper (caption and label timing; without it captions fall back to an even spread). If a key is missing, run with `--dry-run` and tell the user.

### Lean mode (the default): one clip-cut voice sample, no TTS on character shots
The style carries `voice_sample: "assets/ref/matan/matan-voice.wav"` (13.3 s of him alone, cut from the interview's podcast audio). With no `lipsync` key in the script, the renderer skips TTS on character shots: the narration is written into the prompt ("the young man sits low at the black folding table with the yellow index card in one hand, glances down at the card, then looks straight into the camera, deadpan, no smile, hands still, and says, in the voice of Audio 1, exactly these words"), the sample goes in as `reference_audio_urls`, and the model speaks the line in sync with the mouth. Scene length is estimated from word count (`words_per_sec` 3.3 plus 0.6 s per sentence pause), so keep each character shot at or under 22 words. Snap shots are work shots: rendered silent on turbo and dubbed with the style's Fish voice, then cut to the length of the dub (plus 0.3 s, never under 2.5 s). Set `"voice_sample": null` or `"lipsync": true` to go back to Fish narration everywhere.

### Captions in his style
The style sets `"captions": {"mode": "words", "group": 3}`: the renderer writes `render/captions.ass` with the line in groups of two to three words, bold white caps (Arial Black, 60 px on 720p) with a thick black outline, centred just below the middle of the frame, one word per group in yellow, timed from Whisper on each shot's own audio. `"keywords"` on a scene picks the yellow words; otherwise numbers, then the longest non-stopword. A script-level `"captions"` object overrides the style's (`group`, `size`, `y`, `font`, `color`, `highlight` as BGR hex, `outline`, `upper`). `--no-captions` turns them off.

### The Fish voice (snap dubs)
`voices: {"matan": ...}` is a private fish.audio clone trained on eleven windows of him alone, including his signature lines (`4d4d9d307b4f4df1bc125c923fc16fd2`, on the user's account). `MATAN_FISH_VOICE_ID` overrides it. Needs `FISH_AI_API_KEY`.

### No music
`music: None`: no bed unless `--music FILE` or a script `"music"` key. The `sound` lines carry the room and the b-roll.

### Reference stills and video (the likeness path)
Paths relative to the workspace root, all under `assets/ref/matan/` (gitignored; the recipe is in `docs/matan-research.md`):
- Default refs: `iv-front.jpg`, `iv-hands.jpg`, `iv-bust.jpg`, `iv-table.jpg`, `iv-3q.jpg` (cut from the seed interview's solo stretch, him alone and centred at the table, 1080p) with `"seed": 2007`. The renderer prepends "Image 1 to Image 5 show the same young man; keep his face, the mop of dark curly hair, round cheeks and build consistent with them; his clothes and the room follow the description." Override with a top-level or per-scene `"refs"` / `"seed"`; `"refs": []` renders text-only. A default still missing from disk is skipped with a `[refs]` warning.
- Extras: `iv-face.jpg` (tight, soft); the channel set `matan-face.jpg`, `matan-front.jpg`, `matan-3q.jpg`, `matan-set.jpg`, `matan-hands.jpg`, `matan-profile.jpg`, `matan-down.jpg`, `matan-brick.jpg` (1080p-native crops from his guest appearances and own uploads; the first default, proven on one render); `matan-ref.mp4` (7 s 480p of him talking with both hands) for `"ref_videos"`, untested.
- User seeds: crop the user's image 16:9 at 1280x720, save it as `user-<n>.jpg` and list it FIRST in a top-level `"refs"`.
- `"image": "<path>"` on a snap uses a fetched photo as the first frame (turbo image-to-video); `"objects"` refs move the shot to the reference model.
Making more stills: the interview is a wide two-table shot where he is small, except the solo ad-read stretch (about 21:40-22:45 in the 1080p upload) where he is alone and centred; crop 16:9 windows centred on him, crop out the sponsor banner along the bottom and any picture-in-picture inset, and view every frame before keeping.

## 5. Deliver
Print the script scene by scene, the final path, then open the mp4. QuickTime shows a blank document if the same path was re-rendered while open, so quit it first: `osascript -e 'tell application "QuickTime Player" to quit'; open -a "QuickTime Player" <path>`. Report cost from the renderer's summary line.
