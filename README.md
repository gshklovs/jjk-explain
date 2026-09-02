# jjk-explain

Explain any concept as a ~60 second anime explainer, in the voice of the Jujutsu Kaisen narrator revealing a sorcerer's cursed technique and domain expansion. Original characters, real narrator cadence, kanji title cards, generated footage.

![gradient descent, domain expansion](examples/gradient-descent/thumb.jpg)

`/explain gradient descent` produces:

> Cursed Technique: Descent. The user is granted no sight of the terrain. Only the slope beneath their feet.
> ...
> Its binding vow: with each step, the stride grows shorter. Speed is surrendered so the descent may settle, instead of oscillating forever.

Full example: [examples/gradient-descent/transcript.md](examples/gradient-descent/transcript.md), script: [script.json](examples/gradient-descent/script.json).

## What the human does

Two API keys. Both are card-on-file, pay-as-you-go, no approval process:

1. **fal.ai** key from https://fal.ai/dashboard/keys. Runs MiniMax H3-Max, the video model. A 60 s video is about $1 at 480p, about $4 at 768p (regular pricing).
2. **fish.audio** key from https://fish.audio/app/developers, then top up API credit on the same page. This is the narrator voice. A whole video costs about one cent. API credit is separate from a fish.audio subscription.

Optional: any music file dropped into `assets/`. The canonical bed is the "Delirious" 1 hour loop from the JJK OST; fine for personal use, expect a Content ID claim if you upload.

## What the agent does

Everything else. Point Claude Code (or any agent) at this repo and say "set this up"; [AGENTS.md](AGENTS.md) has the steps. By hand:

```bash
git clone https://github.com/gshklovs/jjk-explain && cd jjk-explain
./install.sh                      # symlinks skills/explain into ~/.claude/skills
cp .env.example .env              # add the two keys
brew install ffmpeg               # if missing
pip install -r requirements.txt
```

Then in Claude Code:

```
/explain gradient descent
/explain the thing we just debugged
/explain raft consensus --register nanami --tier full
```

The skill writes `out/<slug>/script.json` (the narrator script plus one video prompt per scene), renders, and opens the mp4. Outputs land in `out/<slug>/render/`: the mp4 with an embedded thumbnail, `thumb.jpg`, `transcript.md`, `captions.srt`, and every intermediate clip and narration file so reruns are free.

## How it works

```
concept ─► Claude writes script.json (reference.md is the bible: beats, registers, taxonomy, style lock)
           │
           ├─ narration: fish.audio "jjk narrator" voice, one call per sentence, stitched with real silence
           ├─ title cards: ffmpeg, black + brush kanji + english (never asked of the video model)
           ├─ shots: fal minimax/h3-max/text-to-video, 5-15 s each, native ambience, parallel
           │
           └─ ffmpeg: fit each clip to its narration ─► concat ─► music bed with sidechain ducking
                      ─► burned captions ─► brightest domain-reveal frame as cover art
```

The metaphor structure is fixed by a small taxonomy: cursed energy is the input, the innate technique is the core mechanism, the domain is the environment plus its guarantee, the binding vow is the tradeoff, and the weakness is the crack. `--tier technique|domain|full` picks how many beats a concept gets. `--register narrator|sukuna|nanami|gojo` picks who is explaining.

## Renderer flags

```
python3 skills/explain/scripts/render.py out/<slug>/script.json [--voice fish|onyx] [--resolution 480P|768P]
        [--dry-run] [--music FILE] [--narration FILE] [--no-captions] [--jobs N]
```

`--dry-run` renders everything with placeholder clips and zero fal spend, the right way to check a script. `--narration` uses one recorded take instead of TTS, scenes timed by word count. Reruns reuse every cached file, so tweaking the music or a single scene costs only that scene.

## Layout

```
skills/explain/SKILL.md        the Claude Code skill
skills/explain/reference.md    the bible: narrator beats, registers, taxonomy, style lock, prompt rules
skills/explain/scripts/render.py
examples/                      two finished scripts with transcripts
eval/cases.json                real ELI5 asks used as test inputs
docs/research.md               model/voice/format research behind the design (Sept 2026)
assets/  out/                  gitignored: music bed, renders
```

## Notes

- macOS first. Title cards use Hiragino Mincho; on Linux set `EXPLAIN_JP_FONT` to a font with kanji glyphs (Noto Serif CJK JP) and `EXPLAIN_EN_FONT`.
- Characters are original by design. Prompts never name the show, the studio, or its cast; the style lock in `reference.md` reproduces the look. Named IP is also blocked by the video API.
- The fish.audio narrator voice is a community voice model. Personal use.
- fal promo pricing on H3-Max (about a quarter of the regular rate) was running through early September 2026.
