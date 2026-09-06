# Building a new `/explain-*` style: the playbook

Read this before adding a voice. It is the distilled record of what went wrong building the first six (JJK, Iroh, Rick, Stark, HxH, Clav) and what fixed it. The renderer is shared; a style is a data-table entry in `skills/explain/scripts/render.py` (`STYLES`) plus a bible (`skills/explain-<name>/reference.md`) and a `SKILL.md`. Do not fork the renderer; add fields.

## 1. Research the voice (before writing anything)
- Get real footage: the user's clips first (`~/Library/Messages` attachments or links they texted themselves), then 2-3 more via `yt-dlp` (`--write-auto-sub --skip-download` gives cadence cheaply). Transcribe with Whisper (word timestamps) so the bible quotes real rhythm, not an impression.
- Study the gold clip frame by frame (ffmpeg tile + view it): how it is cut, how captions look and how fast they change, where it snaps to a visual, what the person does with their hands.
- If the seed video is age-gated (yt-dlp lists no formats without a login and browser cookies are off limits), the same episode is usually a podcast: `yt-dlp` on the Apple Podcasts episode URL gives the full audio for Whisper and the voice sample, and podscripts.co has the text with minute marks (no speaker labels; separate the speakers by reading, then confirm each cut window by re-transcribing it). Stills then come from the person's own 1080p uploads and guest appearances; crop out any picture-in-picture inset, which carries other faces. Say in the bible where the stills came from.
- For a questioner persona (an interviewer), the explainer shape is an interview with no guest: the viewer is the guest, the character asks the lens, and the follow-up questions carry the explanation. Write the anchor lines as questions, not verdicts, or the voice collapses into the nearest sibling style.
- Collect the persona, not just the register: 12-15 of the person's funniest lines and bits, each tagged by what it is for (a rating, a dismissal, a self-own, a flex, a fake-serious aside), their vocabulary (Clav: mogged, over, brutal, jester, chud, ascending, descending), their tics (Rick's burp, Stark's number-before-every-attempt, Iroh's tea). Turn that into a per-script QUIRK BUDGET in `SKILL.md` step 3: a ceiling of one or two of the person's moves per video, placed where they land on their own, never all of them (five in sixty seconds read as forced). Without any, the writer produces the topic's own phrasing ("competition is for losers") instead of the character's ("competition is for jesters"). And keep the character on screen: two of six shots as the face when the likeness holds; zero face is a fallback, not a style.

## 2. Assets (`assets/ref/<name>/`, gitignored)
- Stills cut from footage: face, bust, three-quarter, full, hands; 1280x720, no captions/watermarks; view every one. The stills' COMPOSITION is copied along with the face: interview frames with the subject left of centre looking off-axis produced every face shot off-centre no matter what the prompt said. Crop the refs so the subject is centred and roughly frontal, then write the framing in the prompt too. Soft or vertical crops give a "random dude" likeness: if the stills are weak, plan for zero or one character shot.
- Voice sample 10-14 s, mono, no music, verified by transcription. Real clip audio beats a TTS clone. For dubbed shots, a fish.audio public clone or a private clone made from the sample. The clone must HEAR the character's signature words: train it on windows where they say their own vocabulary ("billboard got mogged", "that guy's a jester"), or it guesses the pronunciation ("mog it" came out wrong from an interview-only sample). And write the vocabulary the way they use it (his verdict is "got mogged", never the command "mog it").
- A clone from many short windows beats one long window: `POST /model` accepts several `voices` files with matching `texts`; eleven verified 2-14 s cuts of the person's own signature lines trained instantly and pronounce their vocabulary. Cut each window from the word timestamps, fade 30-50 ms at both ends, and transcribe every cut before training: a window that catches the other speaker's first word poisons the clone.
- Reference photos must fill 16:9: crop with `scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720`, never pad; a padded photo used as a first frame puts its black bars in the video. And a first-frame photo overrides the line's time of day and place, so either write the prompt to the photo or leave `"image"` out and let the prompt carry it.
- Object references for anything with a specific shape (Wikipedia diagrams, product photos), padded to 16:9. Colored diagrams need "monochrome wireframe, ignore the reference's colors" in the prompt.

## 3. Renderer entry (`STYLES["<name>"]`)
lock, fish_voice/voices (+ env override), voice_sample/voice_samples, lipsync_audio "model", words_per_sec, pause, music (None for conversation styles), cast_words, default_sound, default_instr, title dict (English-only styles set font/hud/seconds), thumb_kanji, label look, offscreen tags, say_lines per speaker, lean_tag, refs/ref_owners/ref_labels/refs_prefix/seed, outro, cast_on_work, captions mode. Every shared behaviour is a field; if a style needs new behaviour, add a field with the old behaviour as default and prove the other styles are byte-identical (`EXPLAIN_LEAN_DRY=1 --dry-run` on one example per style; diff `s*_prompt.txt` and `captions.srt`).

## 4. Bible sections every style carries (copy from `explain-stark/reference.md`)
How they teach (anchor lines from transcripts) · beats · registers · tiers · script.json shape · cast paragraph (describe, never name IP in prompts) · style lock · title card · sound line · reference images · lean-mode rules · lesson ideas · and the shared rules: Narration is not stage direction · Object references · Off-screen speakers · Say the number once (repeat the MAIN POINT, never an incidental figure) · No meta examples · Full sentences, five ideas, one thread · Two kinds of shots (character vs work, interleaved, ask the user which) · The six-shot arc · Labels and reference visuals on work shots (the line asks, the visual answers; hands act per part; name every motion; ≤30 words per dubbed shot) · Never lip-sync a stranger · Visualizing the words (verb not noun, no text in the picture, nobody talking in dubbed b-roll, continuity lightly, optional prop paragraph).

## 5. Test protocol
1. Dry-run; read every prompt; sound-off test: strip the narration and the pictures should still tell the story in order.
2. One-scene probe of any new mechanism (a voice-over from a sample, a hologram from a reference, a caption mode) before a full render.
3. Full test: the six-shot arc, 3-4 work/snap shots dubbed on turbo, 2-3 character shots on the reference path only if the likeness proves out; the user decides the split when present.
4. Check the render on a contact sheet before showing it: likeness, no stranger talking, no garbled text, labels on cue, the visual answering the line.
5. Costs: reference-to-video $0.05/s at 480P; turbo $0.025/s (promos apply to turbo only, as of Sep 2026). A six-shot seeded lesson is $2-3; killed runs still bill submitted clips.
6. Byte-identical check: run the six baseline dry-runs BEFORE editing the renderer, into scratch `--out` dirs (never into `out/`), then again after; diff `s*_prompt.txt` and the caption files. The JJK example does real OpenAI TTS even in dry-run, so its `captions.srt` drifts by 20-200 ms between runs; a third run that drifts again proves it is TTS, not the edit. The lean styles are deterministic.

## 6. Failure modes seen, in the order they were found
| Symptom | Cause | Fix (now in the bibles or renderer) |
|---|---|---|
| Narrator reads what the camera shows | stage-direction lines | Narration is not stage direction |
| Ratio repeated three times, "no one cares" | one-number rule applied as a refrain | Say the number once; other lines carry distinct properties |
| Story "all over the place" | seven metaphors, no running object | Full sentences, five ideas, one thread; running example |
| "Before you are invisible, after you are invisible" | a meta example (marketing explained with a marketing purchase) | No meta examples: a concrete product |
| Lines cut off; fast, un-narrator-like delivery | 2-4 word fragments; TTS trims tails | segment tail pad in the renderer; full sentences only |
| Edited line plays the old audio | TTS segments cached by index; scenes never rebuilt | cache by content; rebuild stale scenes |
| Chin/mouth moves during the AI's line | reference audio attached to a shot with any face | offscreen speakers: silent clip + Fish dub; no head in frame |
| Suit-up replayed the film shot | seeded suit-up stills | cut straight to him in the suit; one armored still |
| Hologram of a hiking boot; "Exploded view" spoken as a caption | vague prop names; the line captions the picture | name props literally; the line asks, the visual answers |
| Hands bob; nothing spins; diagram colors bleed in | one gesture; motion not named; colored reference | hands act per part in label order; name every motion; monochrome rule |
| A stranger's face in a turbo work shot | "hands rest at the edge" invites a body | "nobody in the room" written outright |
| Random people talking; numbers on signs | b-roll illustrates nouns; text asked for | Visualizing the words; no text; nobody talking |
| Garbled prices / counters / handwriting | any prompt or line that needs a number or word drawn | No numbers, no text, in the footage: show quantities physically, words go in labels; the renderer warns on digits and sign/price/menu/written in a prompt |
| Lip-synced "random dude" instead of the character | soft vertical stills | Never lip-sync a stranger; dubbed b-roll instead |
| Agents idle 35 min with no files | tmux teammates parked on the folder-trust dialog (shell `cd` before spawn) | never `cd`; in-process teammates; pane watchdog |
| Render exits 0 with a clip missing | fal lock/rate limit mid-run | retry missing clips once, then fail loudly |
| Everything at 768P "same price" | wrong assumption | reference is $0.05 at 480P; follow --resolution |
| Seed video cannot be downloaded (age gate) | YouTube login wall; cookies denied | podcast feed for the audio, transcript site for the text, the person's own uploads for stills |
| Captions diff in the byte-identical check on the JJK example | real TTS in dry-run, durations drift | compare prompts and the lean styles' captions; re-run once to confirm drift |
| Lip-synced clip dissolves into a reference still for its last two seconds | a face still from a different room than the cast paragraph; the model treats it as a second location | "One unbroken take in this one room, no cut, no dissolve, no second location" in the style's say_lines; reseed and re-render the one shot (move the clip and its _words.json aside, never delete under out/) |
| Black bars in a photo-seeded snap | reference photo padded to 16:9 | crop to fill (`force_original_aspect_ratio=increase`) |
| Face shots off-centre despite "centred" in the prompt | reference stills were off-centre interview frames; composition is copied | re-crop refs centred; never name a light in the prompt (it gets drawn and pushes the subject aside); `reframe` a shot deterministically rather than re-rolling |

## 7. Shipping
Symlink in `install.sh` and `~/.claude/skills/`, one bullet under "Other voices" and one under the collapsed changelog in README, never more; assets stay gitignored; commit the skill, not the renders; release videos as GitHub release assets.
