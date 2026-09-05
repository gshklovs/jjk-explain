---
name: explain
description: Explain a concept as a ~60s Jujutsu-Kaisen-style narrator video (cursed technique / domain expansion). Writes a scene script, renders clips with MiniMax H3-Max on fal, narrates with TTS, assembles with ffmpeg.
argument-hint: <concept or question> [--tier technique|domain|full] [--register narrator|sukuna|nanami] [--dry-run]
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*), Bash(open *), Bash(osascript *)
---

# /explain

Turn `$ARGUMENTS` into a JJK narrator explainer video.

## 1. Load the bible
Read `${CLAUDE_SKILL_DIR}/reference.md` (format beats, register, taxonomy, style lock, prompt rules). Do not skip it; it is the whole voice.

## 2. Understand the concept
If the concept refers to the current conversation or codebase, gather what you need first. Reduce it to: the core mechanism (technique), the guarantee/environment (domain), the tradeoff (binding vow), the weakness. Pick a tier from the taxonomy unless `--tier` is given. Roll the "temperature": vary tier, register and the metaphor; never reuse the previous run's cast description.

Object references: if the concept is or contains a specific complicated object (a drive, a gripper, an engine, a specific character, vehicle or product), fetch 2-3 reference images of it first via a research subagent and pass them as `"objects"` (see the bible's "Object references" section). The model will not get a complicated shape right from words alone.

## 3. Write `script.json`
Workspace root: `python3 ${CLAUDE_SKILL_DIR}/scripts/render.py --where` (the repo, or `$EXPLAIN_HOME`). Path: `<workspace>/out/<slug>/script.json` (slug = kebab of the concept). Shape and rules are in reference.md. Target 60-75 s total: 115-145 words (the narrator voice runs ~1.9 words/s plus scene padding). 6-8 scenes. Title-card kanji: put the category (領域展開) and the name as two space-separated groups; the renderer stacks them. Every scene gets a `video_prompt` that stands alone (the renderer prepends the style lock), and a `sound` line. The render ends with a 5 s hold on the last frame while the theme plays and fades (style `outro`; see the bible), so end on a shot that can sit still.

Off-screen speakers: a tagged speaker with no body on screen (an AI, a radio, a narrator nobody should mouth) goes in `"offscreen": ["tag"]` (style default or script level); its scenes render silent and the line comes from that tag's fish.audio voice, so no mouth can be animated. See the bible's "Off-screen speakers" section.

## 4. Render
```
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py <workspace>/out/<slug>/script.json --voice fish
```
Flags: `--dry-run` (placeholder clips, no fal spend), `--music /path.mp3` (default: first audio file in `<workspace>/assets/`, or `$EXPLAIN_MUSIC`), `--resolution 480P` (cheaper probe), `--no-captions`, `--narration FILE` (use one pre-recorded narration take instead of TTS; scenes are timed by word count), `--voice fish` (fish.audio JJK narrator voice, one generation per sentence stitched with real pauses; the default choice when `FISH_AI_API_KEY` is set), `--voice onyx` (OpenAI fallback).
Model and resolution: defaults are `h3-max-turbo` at `480P` (the cheapest: $0.025/s regular, $0.00625/s until 2026-09-07). Override with `--model h3-max|h3-max-turbo`, `--resolution 480P|768P`, a top-level `"model"` / `"resolution"` in script.json, or `EXPLAIN_MODEL` / `EXPLAIN_RESOLUTION` in the environment or `.env`. Turbo has no reference endpoint, so any scene with `refs`, `ref_videos` or `lipsync` is routed to `h3-max` reference-to-video automatically ($0.05/s at 480P, $0.08/s at 768P, so keep 480P unless a shot needs the detail; `EXPLAIN_REF_RESOLUTION` forces a resolution for reference scenes alone. the log line per clip names the model used).
Keys: the renderer reads `<workspace>/.env` (see `.env.example`) and the environment. If they live only in the user's shell rc, load them without printing: `eval "$(grep -E "^\s*export (FAL_API_KEY|FISH_AI_API_KEY|OPENAI_API_KEY)=" ~/.zshrc)"`. Needs `FAL_API_KEY` (or `FAL_KEY`) for clips, `FISH_AI_API_KEY` for `--voice fish` (the JJK narrator voice), or `OPENAI_API_KEY` for the fallback voice. If the fal key is missing, run with `--dry-run` and tell the user.

## 5. Deliver
Print the narrator script (scene by scene) and the final path, then open the mp4. QuickTime shows a blank document if the same path was re-rendered while open, so quit it first: `osascript -e 'tell application "QuickTime Player" to quit'; open -a "QuickTime Player" <path>`. Report cost from the renderer's summary line.
