# For agents setting this up

You are installing the `/explain` Claude Code skill for a human. They only need to supply two API keys; you do everything else.

1. `git clone <this repo> && cd jjk-explain && ./install.sh`
2. Ask the human for `FAL_API_KEY` (fal.ai) and `FISH_AI_API_KEY` (fish.audio, and they must add API credit at https://fish.audio/app/developers, which is separate from a platform subscription). Write them to `.env`. Never print the keys back.
3. Optional: ask for a music file to drop into `assets/`.
4. Verify without spending: `python3 skills/explain/scripts/render.py examples/gradient-descent/script.json --out /tmp/explain-test --dry-run --voice onyx` needs `OPENAI_API_KEY`; without any key, `--dry-run --narration <any audio file>` exercises everything except TTS.
5. First real run (about $1 of fal at 480p, about one cent of Fish): `python3 skills/explain/scripts/render.py examples/gradient-descent/script.json --voice fish --resolution 480P`.
6. From then on the human types `/explain <concept>` in Claude Code. Read `skills/explain/SKILL.md` and `reference.md`; the bible in reference.md is the whole voice, do not improvise around it.

Conventions the renderer relies on: one Fish generation per sentence at speed 1.0, stitched with real silence; the cast paragraph from `script.json` is auto-substituted for "the sorcerer/sorceress" in every shot prompt; title cards are rendered locally with ffmpeg, never by the video model; the thumbnail is the brightest caption-free frame of the domain reveal.
