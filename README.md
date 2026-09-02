# jjk-explain

Explain any concept as a ~60 second anime explainer, in the voice of the Jujutsu Kaisen narrator revealing a sorcerer's cursed technique and domain expansion. Original characters (or your own robot), real narrator cadence, kanji title cards, generated footage. One Claude Code command.

<table>
<tr>
<td width="50%"><img src="docs/media/inverse-kinematics.gif" alt="/explain inverse kinematics" width="100%"></td>
<td width="50%"><img src="docs/media/gradient-descent.gif" alt="/explain gradient descent" width="100%"></td>
</tr>
<tr>
<td align="center"><code>/explain ik</code> with a reference image of the user's robot<br><a href="https://github.com/gshklovs/jjk-explain/releases/download/v0.1/inverse-kinematics.mp4">▶ full video with narration (85 s)</a></td>
<td align="center"><code>/explain gradient descent</code><br><a href="https://github.com/gshklovs/jjk-explain/releases/download/v0.1/gradient-descent.mp4">▶ full video with narration (82 s)</a></td>
</tr>
</table>

> *Cursed Technique: Inverse Kinematics. The user does not choose the angles of its joints. It chooses only where the hand must arrive.*
> ...
> *Its binding vow is damping. Near a singularity, where the arm locks straight and the map collapses, the user surrenders exactness for stability, and the joints stay calm.*

Full examples with scripts and transcripts: [inverse kinematics](examples/inverse-kinematics/), [gradient descent](examples/gradient-descent/), [the fold flywheel](examples/fold-flywheel/).

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
