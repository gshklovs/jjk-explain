# Building a new `/explain-*` style: the playbook

Read this before adding a voice. It is the living record of what went wrong building the first eight (JJK, Iroh, Rick, Stark, HxH, Clav, Matan) and what fixed it; every new style appends what it learned. The renderer is shared; a style is a data-table entry in `skills/explain/scripts/render.py` (`STYLES`) plus a bible (`skills/explain-<name>/reference.md`) and a `SKILL.md`. Do not fork the renderer; add fields.

## 0. First decide which kind of voice it is
Every style is one of three kinds, and the kinds have different lessons. Pick the kind first; then the general steps below, then the kind-specific section.

| Kind | Examples | Who speaks | Where the face is | Cost per lesson |
|---|---|---|---|---|
| NARRATOR | JJK (`/explain`), HxH | an off-screen voice over generated footage; characters on screen never speak | optional; the cast can be original, or seeded stills with mouths closed | $0.30-2 on turbo |
| CHARACTER / DIALOGUE | Iroh, Rick, Stark | one or two on-screen characters talking to each other or to the viewer, plus a bodiless voice (an AI, a student off-screen) | the seeded likeness, lip-synced on character shots; hands-only work shots between | $2-3 |
| MONOLOGUE / SHORT-FORM | Clav, Matan | one real person talking to the lens, cut with snaps | the real person, seeded from real footage; three face shots, three snaps | $1.7-2.5 |

### Narrator styles: what we learned
- The narrator is Fish TTS over turbo clips; no likeness path needed, so it is the cheapest kind. Music bed with sidechain ducking, kanji title cards drawn locally, an outro hold (5 s, fades) so the theme plays out.
- Captions are estimate-based per sentence; fine, because the TTS is ours. Pad every TTS segment's tail (the renderer does) or short sentences clip.
- The writing carries everything: puzzle-first, the mechanism shown as a physical thing, one number said once, full sentences (fragments read as a shot list and the TTS rushes them), never narrate the camera, the last line a repeatable takeaway.
- A seeded cast is possible without lip sync (HxH: refs for the two students, an off-screen narrator sample, mouths closed via `say_lines`), but the reference path costs 2-3x turbo; use it only where the likeness is the point.
- Mechanism visuals: study a real diagram before writing the prompt (the cycloidal disc came out as a spur gear until we did), pass it as `objects` when exact shape matters, say "monochrome wireframe, ignore the reference's colors" for colored diagrams. Generative video will not enforce contact geometry; for a mechanism where the motion is the lesson, a computed diagram clip is the honest route.
- Regression: the same script through the renderer must give byte-identical prompts; re-run the v0.1 example after big changes.

### Character / dialogue styles: what we learned
- Likeness = stills cut from real footage (4-5, first 4 free) + a fixed seed; voice = a 10-14 s clip-cut sample in lean mode (the model speaks and lip-syncs itself); the Fish clone is only for dubbed work shots. Never let a look-alike mouth the lines: if the likeness fails, the shot becomes dubbed b-roll.
- Two speakers: tags per scene; a bodiless voice (the AI, the narrator) is `offscreen` (silent clip + Fish dub, no head in frame, not even a chin) or the model animates whatever face it finds.
- The six-shot arc: character intro with the quirk, zoomed visualization of the object with labels, the mechanism on the object, reaction/stakes, the result, the concluding phrase. Half the shots are work shots (hands, the part, the hologram, the sand) on turbo, dubbed; ask the user which shots are lip-synced.
- Work shots: the line asks, the visual answers, in that order; hands do one thing per named part in label order; name every motion; no face (write "nobody in the room" outright on turbo); ≤30 words per dubbed line; labels drawn by the renderer, never text in the picture; vary the device (the AI reads it, he builds it, he breaks it, on the suit, run it).
- Persona lives in the physical business (Stark's number before every attempt, the robot with the extinguisher, Iroh's tea), not in adjectives. The payoff is on the thing itself (the suit lifting the car), cut straight to it, do not stage a transformation from seeded stills (the model replays the film shot).
- Repetition: say the number once; repeat the main point only to conclude.

### Monologue / short-form styles: what we learned
- The person is the continuity: three face shots (hook, premise, verdict) seeded from the sharpest centred frontal stills, snaps between. Composition is copied from the stills (off-centre interview frames, a mic over the mouth, a second room in one still all showed up in the render): crop refs centred, keep one room, and `reframe` a shot deterministically rather than re-roll it. Never name a light in a prompt.
- Snaps: 3-5 s b-roll cut to the dub length, dubbed by a clone trained on windows with the person's own vocabulary (an interview-only sample mispronounced "mog"), visualizing the verb of the line (tired nurses walking out, not "a hospital"), nobody talking, no text, more than half the runtime if it keeps it interesting.
- Captions in their look: word groups timed per word from Whisper, one keyword highlighted, a word-slam title instead of a card, the face as the thumbnail with the phrase across it (he gets the clicks).
- Persona: collect 12-15 tagged funny moments; write a quirk CEILING of one or two moves placed where they land, never a checklist (five in sixty seconds read as forced); use their vocabulary the way they use it ("got mogged", not "mog it"); one out-of-pocket verdict at most. The premise carries the only number; no decimal ratings on top.
- Seeding on an interview: age-gated video needs exported cookies; the podcast feed gives the audio and transcript regardless; the solo stretch (an ad read) is where the clean stills are, but check what else is in those frames (a mic over the mouth came along for the ride, and the user preferred the channel stills with the mouth visible); a questioner persona becomes an interview with no guest.

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
| A microphone (or any prop) covers the mouth in every face shot | the reference stills have it there; composition is copied, props included, and "not covering his mouth" in the cast paragraph does nothing, even with clean-mouth face stills listed first | pick stills where the mouth is clear, or accept the hidden lips as the look; test on one shot before a full render |
| Black bars in a photo-seeded snap | reference photo padded to 16:9 | crop to fill (`force_original_aspect_ratio=increase`) |
| Face shots off-centre despite "centred" in the prompt | reference stills were off-centre interview frames; composition is copied | re-crop refs centred; never name a light in the prompt (it gets drawn and pushes the subject aside); `reframe` a shot deterministically rather than re-rolling |

## 7. Shipping
Symlink in `install.sh` and `~/.claude/skills/`, one bullet under "Other voices" and one under the collapsed changelog in README, never more; assets stay gitignored; commit the skill, not the renders; release videos as GitHub release assets.
