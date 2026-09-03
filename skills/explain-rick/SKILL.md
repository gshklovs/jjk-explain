---
name: explain-rick
description: Explain a concept as a ~50-70s garage-lab rant from a drunk genius scientist to his nervous grandson (Rick and Morty style). Same pipeline as /explain (script.json, MiniMax H3-Max clips on fal, ffmpeg), different bible, style lock, two voice samples (lean mode, no TTS), no music, acid-green title cards.
argument-hint: <concept or question> [--tier demo|build|blueprint] [--register rick-lecture|rick-annoyed|rick-drunk-genius] [--dry-run]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py *), Bash(open *), Bash(osascript *)
---

# /explain-rick

Turn `$ARGUMENTS` into a garage-lab lesson video. The renderer is shared with `/explain`: `${CLAUDE_SKILL_DIR}/../explain/scripts/render.py`. The only switch is `"style": "rick"` in script.json.

## 1. Load the bible
Read `${CLAUDE_SKILL_DIR}/reference.md` (how he teaches, beats, registers, tiers, style lock, both cast paragraphs, title-card and sound vocabulary). Do not skip it; it is the whole voice. Do not load the JJK or Iroh bibles; the voices must not blend.

## 2. Understand the concept
If the concept refers to the current conversation or codebase, gather what you need first. Reduce it to: the boy's naive question (the viewer's question), the prop that physically IS the mechanism (something he can hold and turn), the mechanism in one breath, the one concrete number, the throwaway line about where it lives in the world, and the boy's half-wrong restatement. Pick a tier unless `--tier` is given. Roll the "temperature": vary tier, register, the prop and the boy's question; never reuse the previous run's prop. Both cast paragraphs are fixed.

Object references: if the concept is or contains a specific complicated object (a drive, a gripper, an engine, a specific character, vehicle or product), fetch 2-3 reference images of it first via a research subagent and pass them as `"objects"` (see the bible's "Object references" section). The model will not get a complicated shape right from words alone.

## 3. Write `script.json`
Workspace root: `python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py --where` (the repo, or `$EXPLAIN_HOME`). Path: `<workspace>/out/<slug>-rick/script.json`. Shape and rules are in reference.md. Mandatory: `"style": "rick"` at the top level. Target 50-70 s: 110-140 words, 5-6 scenes, 1 title card. Every shot narration starts with `[rick]` or `[morty]` and is at most 22 words (one speaker per scene). Title-card `kanji` holds English capitals, lines split on " / ". Every shot gets a `video_prompt` that stands alone (the renderer prepends the style lock and the reference-image prefix) and a `sound` line from the bible's vocabulary (never music). Exactly one concrete number in the whole script; the concept is a prop the teacher holds.

## 4. Render
```
python3 ${CLAUDE_SKILL_DIR}/../explain/scripts/render.py <workspace>/out/<slug>-rick/script.json
```
Flags are the same as `/explain`: `--dry-run` (placeholder clips, no fal spend; add `EXPLAIN_LEAN_DRY=1` to the environment to see the assembled lean prompts), `--resolution 480P|768P`, `--no-captions`, `--music FILE` (off by default for this style), `--voice fish` (only with `RICK_FISH_VOICE_ID` and `MORTY_FISH_VOICE_ID` set; see below).
Model: every scene in this style uses reference stills and a voice sample, so it is routed to `h3-max` reference-to-video ($0.08/s at either resolution; 480P saves nothing). A 6-scene lesson is about $4-6. Reference-to-video costs the same at 480P and 768P, so the renderer always requests reference scenes at 768P (`EXPLAIN_REF_RESOLUTION` overrides).
Keys: the renderer reads `<workspace>/.env` (see `.env.example`) and the environment. If they live only in the user's shell rc, load them without printing: `eval "$(grep -E "^\s*export (FAL_API_KEY|FISH_AI_API_KEY|OPENAI_API_KEY)=" ~/.zshrc)"`. Only `FAL_API_KEY` is needed for the default (lean) path. If it is missing, run with `--dry-run` and tell the user.

### Lean mode (the default): two voice samples, no TTS
The style carries `voice_samples: {"rick": "assets/ref/rick/rick-voice.wav", "morty": "assets/ref/rick/morty-voice.wav"}` (10-14 s of clean solo dialogue each). With no `lipsync` key in the script, the renderer skips TTS entirely: each shot's narration is written into the prompt ("the old scientist looks at the camera and says, in the voice of Audio 1, exactly these words"), the sample chosen by the scene's leading `[tag]` goes in as `reference_audio_urls`, and the model speaks the line in sync with the mouth. A scene is one speaker; if a scene mixes tags the first wins and the log warns. Scene length is estimated from word count (`words_per_sec` 2.6 for this style, plus 0.7 s per sentence pause), so keep each shot at or under 22 words. Title cards are silent except the garage hum. Set `"voice_sample": null` or `"lipsync": true` to go back to Fish narration.

### No music
This style sets `music: None`: no bed is mixed unless `--music FILE` is passed or the script carries a `"music"` key. The video is a conversation in a garage full of humming gadgets; the `sound` lines carry the ambience.

### Fish narration (alternative, needs voice IDs)
`--voice fish`, `"lipsync": true` or `"voice_sample": null` uses fish.audio voices from the style's `voices` table: the most-used public voices on fish.audio as of 2026-09-02, `rick` = `d2e75a3e3fd6419893057c02a375a113` ("Rick Sanchez", ~110k generations) and `morty` = `377e4ac186da47faa3b644d033775954` ("Morty Smith", ~36k). Override with `RICK_FISH_VOICE_ID` / `MORTY_FISH_VOICE_ID`. Needs `FISH_AI_API_KEY`. Lean mode (the default) does not use Fish at all; it speaks from the clip wavs.

### Reference stills (the likeness path)
The style's default `refs` (`assets/ref/rick/rick-bust-iso.jpg`, `rick-3q-iso.jpg`, `rick-full-iso.jpg`, `morty-bust-iso.jpg`, `morty-full-iso.jpg`: single-character 16:9 crops cut from the raw stills `rick-front.jpg`, `rick-three-quarter.jpg`, `morty-front.jpg`, `morty-full.jpg`, which each show both characters) with `ref_owners` (`rick, rick, rick, morty, morty`) route every shot to reference-to-video; the renderer prepends "Image 1 to Image 3 show the old scientist; Image 4 to Image 5 show the boy; keep each character's face, hair and clothes consistent". Missing default stills are skipped with a warning. Default `seed` 4242 keeps the look stable; override with a top-level `"seed"`. Per-script `"refs"` + `"ref_owners"` (parallel lists) replace the defaults; `"ref_videos": ["assets/ref/rick/rick-ref-6s.mp4"]` adds motion reference (untested; try on one scene first). Stills and set frames on disk are listed in `docs/rick-research.md`; the `set-*.jpg` frames are for your own reference when writing prompts, not for `refs`.

## 5. Deliver
Print the script scene by scene (teacher and boy lines), the final path, then open the mp4. QuickTime shows a blank document if the same path was re-rendered while open, so quit it first: `osascript -e 'tell application "QuickTime Player" to quit'; open -a "QuickTime Player" <path>`. Report cost from the renderer's summary line.
