# /explain-stark research: how Tony Stark teaches and builds on screen

Source material: Iron Man (2008), Iron Man 2 (2010), Iron Man 3 (2013), The Avengers (2012), Avengers: Age of Ultron (2015). This doc may name Stark, JARVIS and the films freely; VIDEO PROMPTS must never name the actor, character, films or studio (see section 7). Sister bible to `skills/explain-iroh/reference.md`; same pipeline, opposite temperature: Iroh is patient and sideways, Stark is impatient and head-on, but both teach with a physical object and exactly one number.

## 1. How he teaches
- He teaches by building, not by explaining. The explanation is what falls out of his mouth while his hands are busy. He never faces the camera to lecture; he faces the bench, the hologram, or the suit, and talks to JARVIS, Dum-E, or himself. The viewer is eavesdropping.
- Thinking out loud is the format. Half-sentences, self-interruptions, corrections mid-word ("no, no, that's... yes, that"). He says the wrong thing first, hears it, and fixes it out loud. The fix IS the lesson.
- The jokes carry the content. Every quip states a fact: "handles like a dream", "we're going to try a ten percent thrust capacity", "the icing problem", "it's a terrible idea, that's why it's going to work". Strip the joke and the number or the mechanism is still there. Never a joke that is only a joke.
- He orders JARVIS to make things visible: "run it", "pull up the schematics", "show me the stress points", "bring up the Expo model", "give me a readout", "what's the tolerance", "notify me when it's done". Every abstraction gets rendered as a hologram he can grab.
- He fails on purpose, on camera. Mark I is a cave prototype that barely flies; Mark II ices over at altitude ("JARVIS, we've got an icing problem"); the first boot test throws him into the wall, the first flight stabilizer test (Dum-E with the fire extinguisher) is a gag that reveals the real physics; Mark 42's separate-piece flight assembly hits him in the face and the crotch. Failure is beat three, never the ending.
- He diagnoses with the hologram. After a failure he doesn't guess; he opens the exploded view, rotates it, throws away the parts that aren't the problem ("this... don't need this... goodbye"), and finds the one component that matters. The Iron Man 2 new-element scene is the canonical version: the Stark Expo model exploded into rings, he strips the pavilions, the atom is left.
- He states the number as a dare. "Ten percent thrust." "Two point six seconds." "Four percent over tolerance" (JARVIS says this kind). One number per scene; he repeats it later as the punchline.
- He humiliates the wrong answer, never the student. In the senate hearing / press conference register he explains by making the mistaken idea look ridiculous ("you want my property? you can't have it."), then gives the right idea in one sentence. The viewer is on his side against the wrong answer.
- He cannot stop working. Sleep deprivation, coffee, a smoothie from Dum-E with motor oil in it; the domestic clutter of the workshop is the warmth. The armor is the only tidy thing in the room.
- The landing line: he ends by pretending it was obvious. "Yeah. I can fly." "Told you." "Tomorrow, then." "That's the plan" (JARVIS's phrase, stolen). A short line, dry, over the finished build, then cut.
- The "you can't / yes I can" reflex. Told something is impossible (a new element, a suit in a cave, a 12% thrust) he answers with the build already running.

## 2. Anchor lines (do not quote verbatim; match the cadence)
- "Sometimes you gotta run before you can walk."
- "Okay, let's do this right. Start mark, half a meter back from center. Dum-E, look alive, you're on standby for fire safety."
- "We're going to start off nice and easy. We're gonna see if ten percent thrust capacity achieves lift. And three, two, one."
- "JARVIS, are you up?" / "For you, sir, always."
- "Handles like a dream." (then the icing problem)
- "JARVIS, sometimes you gotta run before you can walk." / "There are still terabytes of calculations needed before an actual flight is..."
- "Add a little hot rod red." / "Yes, that should help you keep a low profile."
- "What's the tolerance?" / "Load exceeds tolerance by four percent, sir."
- "You can't." / "Yes I can." (new element)
- "Show me the stress points." / "Give me a readout."
- "Do me a favor and ignore that last thing I said." / "That is the plan, sir."
- "Told you." (Mark 42 catches the countdown)
- "Yeah. I can fly."

Cadence: clipped clauses, lists of three, an aside inside the sentence, a number stated flat and then repeated as a punchline. He talks to the object ("come on, come on") and to JARVIS by name. Rarely more than two sentences without a physical action beat (grabs, throws, welds, turns). Never says "in other words" or "basically"; he shows the other words on the hologram.

## 3. Beats of a Stark-native lesson segment
1. TITLE CARD, WORKSHOP: cold open on the bench, tungsten practicals, one blue hologram idling. Title as JARVIS HUD text (mono, blue): "Test 1: <concept name>". VO: one line, dismissive of the ceremony ("Okay. Let's get this over with.").
2. THE PUZZLE ON THE BENCH: a physical thing that is broken or wobbling or won't hold. He states the problem as a challenge in one sentence, in second person to JARVIS ("Why does the disc wobble?"). No mechanism yet.
3. "JARVIS, RUN IT": he orders the simulation / pull up the schematic. Hologram exploded view rises off the bench. Blue rings, the object in the middle.
4. FIRST BUILD FAILS: Dum-E hands him the wrong part / the prototype throws sparks / the sim turns red at one joint. He is hit, singed, or thrown. He does not stop talking. ("Okay. That was... that was informative.")
5. DIAGNOSE WITH THE HOLOGRAM: he grabs the exploded view, rotates it, flicks the irrelevant components away one by one ("don't need that... don't need that...") until one piece is left. That piece IS the mechanism. JARVIS names it with a number (form tier).
6. THE NUMBER: he says the single concrete number and dares the room with it ("ten percent, JARVIS"). Rebuild starts: robot arms, sparks, pneumatic hiss.
7. REBUILD WORKS: the thing spins / flies / holds. Held shot. JARVIS's dry confirmation, one line.
8. LANDING QUIP: he pretends it was obvious ("Told you." / "Yeah. It flies."). Cut on the reactor glow.

Keep the two hard rules from `/explain` and `/explain-iroh`: exactly one concrete number per video, and the concept shown as a physical thing the characters touch. Stark's version of "physical": a hologram he can grab counts as physical because he grabs it, rotates it, throws it away; the prop on the bench is the same thing solid.

## 4. Registers (--register)
- `stark-build` (default): building while talking. Half-sentences, orders to JARVIS, action beats every line. Warm workshop, one blue hologram. The failure beat is a gag with real physics. Jokes carry facts. Ends on the landing quip.
- `stark-lecture`: the press-conference / senate-hearing showman. He stands, he has an audience, a screen behind him. Explains by putting the wrong answer on the screen and humiliating it ("this is what everyone thinks happens... it doesn't"), then the right answer in one sentence and a mic-drop. Fewer action beats, more rhythm; the hologram becomes a big presentation screen. Use for concepts that are mostly a misconception to correct.
- `stark-sleep-deprived`: 72 hours in, the basement register (Iron Man 3 workshop after the mansion, Age of Ultron lab at night). Muttering, quieter, coffee, Dum-E with a dunce cap, sentences trail off. JARVIS is more parental ("I would recommend sleeping at some point, sir"; "you have been awake for seventy-two hours"). The mechanism gets stated almost by accident, gently, then he realizes it and wakes up. Use for concepts with a cost, a failure mode, or an obsessive edge.
- `jarvis` (counterpart voice, all registers): see section 5. Not a register the user picks; it is the second voice in every register.

## 5. JARVIS's rules
- Dry, British, calm, unhurried; never raises his voice, never jokes first. His humor is understatement ("Yes, that should help you keep a low profile") and literalism ("That is the plan, sir").
- He speaks only for three reasons: (a) to ask the viewer's question ("Sir, why would the disc wobble at all?"), (b) to correct with a number ("Load exceeds tolerance by four percent"), (c) to state a result ("The build is complete. It holds."). Never to explain the concept himself; that is Stark's job.
- He corrects Stark, and is usually right, in a sentence of at most twelve words. Stark ignores him and is proven wrong, then right. When JARVIS says "I'd recommend...", the next beat is the failure.
- He addresses Stark as "sir" once per exchange, not every line.
- He is rendered as a voice only: blue HUD text, rings, waveform. Never a body, never a face, never a robot. Dum-E and U (the robot arms) are the physical comedy; JARVIS is the ceiling.
- In `stark-sleep-deprived` he adds one parental line per segment, never more.

## 6. Five lesson ideas (puzzle, prop-as-mechanism, one number, takeaway)
1. Hash tables. Puzzle: JARVIS has 10,000 parts in the workshop and Stark wants any one of them in his hand in one move. Prop: a wall of numbered bins; the exploded hologram shows the part number folding into a bin number (the hash), and the failure is two parts in one bin (collision) so Dum-E hands him the wrong bolt. Number: "load factor point seven". Takeaway: constant-time lookup means "compute the address, don't search"; collisions are the price, and you keep the bins under seventy percent full.
2. PID control. Puzzle: the flight stabilizer overshoots and Stark hits the ceiling. Prop: the hover test itself; the hologram shows error, its accumulation and its rate as three glowing rings that he tunes by hand. Number: "ten percent thrust" (the P gain). Takeaway: P gets you close, I removes the leftover droop, D stops the overshoot; tune in that order.
3. Public-key encryption. Puzzle: send Pepper the reactor schematics so nobody in the building can read them, without ever meeting to swap a key. Prop: two physical padlocks fabricated by U; one snaps shut with no key (public), only Stark's key opens it (private). Number: "2048 bits". Takeaway: anyone can lock, only the owner can unlock; you publish the lock, never the key.
4. Resonance / the icing problem reframed. Puzzle: the Mark II shakes itself apart at one specific rotor speed and is fine above and below. Prop: the armor on the stand, hologram of the stress points lighting red at one frequency. Number: "forty-two hertz". Takeaway: every structure has a natural frequency; drive it there and small pushes add up; drive through it fast or stiffen the part.
5. Gradient descent. Puzzle: JARVIS must find the reactor's most efficient ring spacing and there are a million settings. Prop: a holographic bowl-shaped landscape over the bench; a glowing marble that Stark flicks, rolling downhill, stuck in a small dip (local minimum). Number: "learning rate point zero one". Takeaway: step downhill in proportion to slope; too big a step and you fly out of the bowl, too small and you're there all night; JARVIS: "you have been there all night, sir".

Each idea: exactly one number, the hologram/prop physically is the mechanism, JARVIS asks the viewer's question at beat 2 and states the number at beat 5, Stark's landing quip repeats the number.

## 7. Cast paragraphs (for video prompts; never name actor, character, film or studio)
- ARMORED INVENTOR: "A man in a sleek red-and-gold powered armor suit, full helmet with the faceplate down, narrow glowing white-blue eye slits, a glowing circular reactor set in the chest, segmented metal plates with visible seams and small servo joints, standing or working at a cluttered engineering workbench in a private underground workshop; when out of the helmet he is never shown, only the armor." (Style note: the stills in assets/ref/stark/ are a silver prototype suit; the prompt should say red-and-gold explicitly.)
- THE AI: "A calm, dry, British-accented voice with no body; on screen it exists only as translucent blue holographic interface elements: floating monospaced HUD text, concentric rotating rings, thin waveform lines and exploded-view schematics hovering over the bench, which the armored inventor grabs, rotates and flicks away with his hands. Never a face, never a robot, never a humanoid."
- Optional props: "a wheeled robotic arm with a three-finger claw, taped-on dunce cap, holding a fire extinguisher"; "a second robotic arm welding, sparks"; "the armor standing empty on a lit stand"; "a sports car under a cover in the background".

## 8. Style lock + sound vocabulary
Style lock sentence: "Live-action, cinematic, anamorphic lens with subtle horizontal flares, shallow depth of field, cool blue holographic key light against warm tungsten workshop practicals, concrete and steel underground workshop, 24fps, film grain, film look, no text overlays except in-world blue HUD."
Sound vocabulary (no music by default): low workshop hum (HVAC and transformers), servo whir on every armor movement, soft hologram chimes and glass-like ticks when a hologram is grabbed or thrown, steady arc-reactor hum (a filtered tone that rises when the reactor powers up), welding sparks and crackle from the robot arm, pneumatic hiss on plate clamps and boot locks, a clank of metal on the concrete floor, JARVIS's voice slightly roomy as if from ceiling speakers, Stark's voice close and dry. Failure beats: a thump, a clatter, then silence and the fire extinguisher hiss.

## 9. Assets: reference stills (assets/ref/stark/)
All 1280x720, jpg q2, letterbox bars cropped out (crop 1280:532:0:94 for the 2008 clip, 1280:544:0:88 for the 2010 clip), then 16:9 center crop.
Clips (yt-dlp, 720p, /tmp/stark-clips/):
- PvYhZT99g1s "Iron Man - First Flight Scene - Mark 2 'Handles Like A Dream'" (Iron Man, 2008, Mark II silver prototype).
- BddCrgqCnVM "Mark 42 Suit Test Iron Man 3" (Iron Man 3). Downloaded and scanned; the red-and-gold Mark 42 frames all have the faceplate up (face visible), so none kept. Also tried 98FO19TuI9A (Iron Man 3 suit-up, same scene): the hall-of-armors wide at 2:36 has letterbox bars plus a visible face, rejected.
- Ddk9ci6geSs "Tony Stark Discovers a New Element Scene - Iron-Man 2" (Iron Man 2). Last ~20 s carries a channel logo; avoided.
Kept:
- suit-bust.jpg: PvYhZT99g1s @ 2:15 (135 s). Night, helmet-on bust, glowing eye slits, dark metal.
- suit-three-quarter.jpg: PvYhZT99g1s @ 0:52. Three-quarter of the silver armor in the workshop, chest reactor glowing, eyes lit.
- suit-full.jpg: PvYhZT99g1s @ 0:53. Full body standing in the workshop, cars and benches behind.
- suit-workshop.jpg: PvYhZT99g1s @ 0:48. Armor in the garage/workshop with cars, eyes lit, three-quarter from below.
- set-workshop-1.jpg: Ddk9ci6geSs @ 0:46. The bench with the holographic city model rising off it; person in frame at the back.
- set-workshop-2.jpg: PvYhZT99g1s @ 0:14. Wide empty workshop with blue HUD overlay elements, no people.
Caveat: all suit stills are the silver Mark II, not red-and-gold. The cast paragraph states red-and-gold explicitly; the stills reference silhouette, helmet, eye slits and reactor.

## 10. Voices (fish.audio)
Search via `GET https://api.fish.audio/model?title=...&sort_by=task_count`.
- STARK: `d7a76ce437d34163a48b7e683f85cac7` "Iron Man/Tony Stark (Robert Downey Jr.)", en, task_count 8956, likes 41. Runner-ups (en): `b080dc966de544b99b3000c6fde1788e` "Iron Man" 8413 tasks; `b11cbcf305ad47e5b6035cf80da69491` "Tony stark" 3073; `5b4410e25b0f4248be0e7e2985999174` "Iron Man" 2884; `69c9678530a04cdf9022abb08e9941af` "Iron Man(Noise reduction)" 2402. Higher-count entries `f7129aa42b49406fa95475ecb822cc69` (15172) and `cc5584d3bd7645b68615df1aa401f364` (10042) are Spanish.
- JARVIS: `612b878b113047d9a770c069c8b4fdfe` "Jarvis (MCU) J.A.R.V.I.S", en, task_count 105832, likes 342 (by far the most used). Runner-ups (en): `7c1a7dc37829497593ab4db29eed387c` "J.A.R.V.I.S" 9799; `14129c3e320149449d6bada6862f7338` "Jarvis" 8782; `05b36da8574341d0803391491850db20` "Jarvis" 6181; `b841fc010afe43efa1b9fb702832988d` "JARVIS 1" 5800.
Samples (model s1, temperature 0.6, top_p 0.7, speed 1.0, converted to mono 48 kHz):
- assets/ref/stark/stark-voice.wav: 11.61 s, 1.1 MB. Text: "Okay. Here's the thing nobody tells you. The trick isn't power, it's ratio. Eleven lobes, twelve pins. Watch the disc. See that wobble? That wobble is the whole idea. Run it again."
- assets/ref/stark/ai-voice.wav: 11.80 s, 1.1 MB. Text: "Running the simulation now, sir. The first pass fails at the third lobe; load exceeds tolerance by four percent. May I suggest a slightly larger pin? I would also recommend sleeping at some point."

### 9b. PM revision (2026-09-02): red-and-gold stills replace the silver defaults
The four `suit-*.jpg` defaults are now the red-and-gold armor, helmet on, glowing eyes, pulled from 98FO19TuI9A (Iron Man 3 Mark 42 suit-up; letterbox crop 1280:528:0:96, then 938x528 centre crop to 16:9):
- suit-full.jpg: @ 159.0 s, full body crouched on the assembly platform, hall of armors behind, smoke.
- suit-workshop.jpg: @ 162.0 s, same platform, robot arm and workshop behind.
- suit-bust.jpg: 480x270 crop of the 159.0 s frame (head and chest, reactor lit), upscaled 2.67x.
- suit-three-quarter.jpg: 560x315 crop of the 162.0 s frame, upscaled.
The silver Mark II frames are kept as `mk2-bust.jpg`, `mk2-three-quarter.jpg`, `mk2-full.jpg`, `mk2-workshop.jpg` (not in the default refs; use `"refs": [...]` in script.json to pick them).
- set-workshop-1.jpg replaced (team-lead review: the old frame showed the unmasked actor). Now: the empty garage workshop with cars, a motorbike and blue HUD overlay, no person, from PvYhZT99g1s @ 22 s (letterbox crop 1280:532:0:94, 16:9 centre crop, trimmed to drop an oil-brand sign at the left edge).

### 9c. Rework (2026-09-02, late): real-footage seeds, clip-cut voices, the test-camera style
The user rejected the armor-seeded, fish.audio-voiced first render ("doesn't sound like him, doesn't look like him, the mouth moves with the mask on") and pointed at the gold window: Iron Man (2008), the Mark II workshop scene, bench work on the bare flight-stabilizer arm in a tank top, then the self-recorded boot-rig test. Same strategy as `/explain-rick`: seed on stills cut from the real clip, voice samples cut from the real dialogue, and a script where the concept is what he does with the part.
Sources (yt-dlp, 720p, letterbox `crop=1280:532:0:94` on both):
- WNu6fRo_7fg "Making the Mark II Armor - First Test" (186 s). Layout in this upload: 0:00-0:37 desk with the AI ("open a new project file, index as Mark II"), 0:37-1:14 bench work on the arm (tank top, red toolbox, robot arms, wall schematic), 1:15-1:54 the camcorder boot test (REC dot, timecode, work lights on stands; the announcement at 1:17-1:25 and 1:40-1:50, the crash and smoke 1:49-1:54), 1:55-2:20 desk / hologram gauntlet / hand repulsor at the bench in a grey T-shirt, 2:20-2:25 the wall, then an Iron Man 3 hall-of-armors tail. No auto-subs on this upload; timings from the OpenAI whisper API (`whisper-1`, verbose_json, per-30 s chunks; the single-pass transcript hallucinated in loops).
- 98FO19TuI9A (Iron Man 3 suit-up), window 1:50-2:55 downloaded; 2:00-2:45 used.
Stills (1280x720, q2), all viewed before keeping:
- tony-face.jpg: WNu6fRo_7fg @ 72.0 s, 480x270 window at (490,0) upscaled; face looking up from the arm.
- tony-bust.jpg: @ 71.5 s, 945x532 at x=260; frontal at the bench, robot arms over both shoulders, wall schematic behind.
- tony-3q.jpg: @ 55.0 s, x=335; three-quarter over the red toolbox, cars behind.
- tony-full.jpg: @ 85.0 s, 800x450 at (300,60); standing on the test floor with the arm stabilizers on, camcorder framing, REC bug and timecode cropped out.
- tony-hands.jpg: @ 63.5 s, x=335; hands inside the arm mechanism, screwdriver.
- tony-rig.jpg: @ 79.0 s, 800x450 at (0,10); on the boot rig in the REC wide (timecode cropped, "TCG" tag remains bottom-left).
- tony-hands-alt.jpg: @ 139.0 s, x=0; hands on the repulsor gauntlet at the bench, grey T-shirt (different outfit; not a default).
- suitup-1.jpg: 98FO19TuI9A @ 2:20 (clip t=30), x=130; robot arms assembling the armor on him.
- suitup-2.jpg: @ 2:25 (t=35), x=50; the finished suit standing, helmet on.
- suitup-3.jpg: @ 2:38 (t=48), x=250; stepping off the platform in the hall of armors, smoke.
- set-rec-1.jpg: WNu6fRo_7fg @ 76.0 s, x=170; the test floor from the camcorder, him at the left edge, REC dot.
- set-rec-2.jpg: @ 114.0 s, x=170; the same wide after the crash, smoke, REC dot.
- Kept, dropped from defaults: suit-*.jpg, mk2-*.jpg, set-workshop-*.jpg.
Motion reference: user-ref.mp4, 65.5-73.5 s, 854x354, 8 s, no audio (untested on the endpoint).
Voices (mono, 48 kHz, `loudnorm=I=-18:TP=-2`, verified by re-transcribing the wav):
- stark-voice.wav, 12.1 s, RMS -22.6 dB: 77.6-85.0 s ("Okay, let's do this right. Start mark, half a meter back from center.") + 0.3 s gap + 100.0-104.4 s ("We're gonna start off nice and easy. We're gonna see if ten percent thrust capacity achieves lift."). Camcorder-diegetic audio, no score.
- ai-voice.wav, 9.2 s, RMS -22.1 dB: 4.9-6.7 s ("For you, sir, always.") + 11.9-15.4 s ("Shall I store this on the ... central database?") + 24.3-27.6 s ("Working on a secret project, are we, sir?"), 0.3 s gaps. Faint room tone under the desk scene, no score.
- The fish.audio generations from section 10 are kept as stark-voice-tts.wav / ai-voice-tts.wav.
Style changes that came out of the window (in `skills/explain-stark/reference.md`): the explanation is a sequence of attempts (set a number, announce the test to the room, fail physically, blame the robot, change one variable, retry); beats are an action arc (bring it in, take it apart, find the part, the one number on the hologram, service, prove under load, landing line); three visual devices (the camcorder test wide with REC dot and timecode, the bench build over the red toolbox, the stylus hologram schematic); prompts spend at most one clause on him and the rest on hands and the part; cast is now "a dark-haired man with a trimmed goatee in a dark tank top, oil on his hands and forearms, no armor"; the armor is a prop.
