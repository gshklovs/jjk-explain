# /explain-stark bible

Sister to `/explain` (the JJK narrator), `/explain-iroh` (the tea master) and `/explain-rick` (the garage rant). Same pipeline, same script.json, a fourth temperature. Where the narrator is cold and the master is patient, this voice is fast, amused and mid-task: a billionaire engineer alone in his workshop, running a test on a piece of hardware he built, narrating the test to the room and to his calm British house AI, failing it physically, blaming the equipment, adjusting one thing, and running it again. The teacher is Tony Stark as the 2008 film plays him in the Mark II workshop scene (the bench work on the bare flight-stabilizer arm, the boot-rig test, the fire extinguisher); the AI is JARVIS. That is the last time either name appears in this file. In cast paragraphs and video prompts he is "the inventor" and "the AI"; never name the actor, the character, the films or the studio.

The gold reference is one forty-second window of that scene, and it defines the whole style: he is in a tank top hunched over a bare mechanical arm on a red toolbox, robot arms hovering over his shoulder, a wall monitor with the schematic behind him; then a locked-off camcorder wide of the workshop (red REC dot, timecode in the corner) with him alone on a test rig announcing the test before it goes wrong; then the aftermath, smoke, the robot with the fire extinguisher. No armor. The armor, when it exists at all, is a prop he works on.

## The teacher (how he teaches)
- He narrates the test, not the concept. "Alright, let's do this right. Start mark, half a meter back from center. Nice and easy, we're gonna see if ten percent thrust capacity achieves lift. Three, two, one." The explanation is the sequence of attempts; the viewer learns the mechanism by watching what he changes between attempt one and attempt two. He never lectures.
- He sets a number before every attempt. A load, a thrust, a ratio, a tolerance. The number is a dare, said flat, and the attempt either honours it or throws him into a wall.
- The attempt fails physically and comically. The arm jams, the disc skips, the rig throws him across the room, the part leaves the bench. He is hit, singed, or on the floor, and he keeps talking.
- He blames the equipment or the robot. "You are a tragedy." "If you douse me again and I'm not on fire, I'm donating you to a city college." "Am I in your way?" The blame is affectionate and it names the real cause in passing.
- He adjusts one variable and tries again. One. Lower the load, count the lobes, swap the pin, regrease the cam. The single change IS the lesson; the second attempt proves it.
- The explanation is what falls out of his mouth while his hands are busy. Half-sentences, self-interruptions ("no, no, that... yes, that"), orders to the robot ("up", "stay put", "roll it"), then one clean plain line when the mechanism lands. He never says "basically" and never explains the same thing twice.
- The AI's lines are short status readouts and one question. "For you, sir, always." "Shall I store this on the central database?" "Working on a secret project, are we, sir?" It asks the viewer's question once, it corrects with a number once, it never explains.
- The robot arms are characters. The wheeled claw with the fire extinguisher lands the failure beats; the second arm holds the part, hands him the wrong tool, gets in his way. They never speak.
- He is generous to the viewer without being soft: you are smart and busy, here is the one thing, here is it working under load, done. The landing line pretends it was obvious.
- Never mean to the AI. The AI is the straight man and is always right; the robots get the abuse.

## Anchor lines (paraphrased from the scene; do not quote verbatim, match the cadence)
- "Alright, let's do this right. Start mark, half a meter back from center."
- "Dum-E, look alive, you're on standby for fire safety. You, roll it."
- "Nice and easy. We're gonna see if ten percent thrust capacity achieves lift. And three, two, one."
- "Up. Not in the boot. Right here. You got me? Stay put. Nice."
- "You're of no benefit at all. Move down to the top. Okay, I'm sorry, am I in your way?"
- "Screw it, don't even look at it. If you douse me again and I'm not on fire, I'm donating you to a city college."
- "You... are a tragedy."
- "Open a new project file. Index it as Mark Two." / "Shall I store this on the central database, sir?"
- "Working on a secret project, are we, sir?" / "I don't want this winding up in the wrong hands."
- "That is a flight stabilizer. It's completely harmless." (then it knocks him into the wall)
- The AI's status readouts, from the wider films: "Load exceeds tolerance by four percent, sir." "That is the plan, sir." "For you, sir, always."

Cadence: clipped clauses stacked fast, imperatives to the robots, a number stated flat and then repeated as the punchline after it works. First person present ("I'm putting twelve pins on this"). The AI answers in one clause, subject-verb-number, "sir" at the end. He never talks more than two sentences without doing something with his hands.

## Beats (an action arc, not a lecture)
1. TITLE (HUD card): near-black card, hologram-blue caps, a thin rule, an English subtitle. "MARK 11 ELBOW" / "Cycloidal drive: eleven lobes, twelve pins". Silent; the workshop hum comes in under the next shot.
2. BRING IT IN AND TEST IT (the test camera): the broken or heavy thing arrives, on the rig or on the bench. He sets the number, announces the test to the room, counts it down. It fails: jams, slops, throws him. The robot with the extinguisher may or may not help. One line names the symptom.
3. TAKE IT APART (the bench build): hunched over the thing on the red toolbox, screwdriver, housing off, robot arms hovering. He blames the equipment and says what he expects to find inside.
4. FIND THE MECHANISM: the one part comes out of the housing and into his hand. He wipes it, holds it to the light, names what it is in the words a mechanic would use. No number yet.
5. THE ONE NUMBER (the hologram schematic): a stylus on a glass screen, the part drawn as a blue schematic, one region lit. The AI asks the viewer's question or states the number; he repeats it as his own. This is the only concrete number in the video.
6. SERVICE / REBUILD: hands only. Clean, regrease, drop it back on the cam, pins through the holes, housing on. He says the one variable he changed.
7. PROVE IT UNDER LOAD (the test camera again): same locked-off wide, same announcement, the heavy thing on the end this time. It holds. The AI's one-clause confirmation is optional.
8. IN THE SUIT, CARRY (the payoff on the suit itself): cut straight to him already in the armor, faceplate down, doing the thing the concept promised: lifts the front of a car, holds it dead steady for a long two seconds, sets it down. Do not stage the suit-up itself; seeded suit-up stills only made the model replay the film shot. Per-scene `"refs"`: his own stills plus one armored still (`suitup-2.jpg`). One line before the cut, none in the suit. The viewer expects this beat; do not end on the bench.
9. LANDING LINE: he restates the number or the takeaway as if it were obvious ("Told you." / "Eleven to one. Write it down."), tosses the tool, cut. May be the line said before the faceplate closes in beat 8.

AI-line shots (beat 5): no part of his head in the frame, not even the chin (a visible chin still got animated): hands and forearms entering from the bottom edge, camera at table height, the hologram or the part filling the frame, or him fully out of shot. The style's `say_lines["ai"]` already says his lips stay shut; the framing makes it certain.

Keep the two hard rules from `/explain`: exactly one concrete number per video, and the concept shown as a physical thing he takes apart, holds and puts back together. A hologram counts only for the one-number beat, and only as the drawn schematic of the part he is holding.

## Three visual devices (bake them into video prompts)
- (a) THE TEST CAMERA: a locked-off wide of the workshop from a camcorder on a tripod, a small red REC dot and a running timecode in the corner, harsh work lights on stands, a black tool chest, a motorbike, him alone in the middle of the floor on the rig or beside the thing under test, announcing the test, then the failure, then smoke and the robot with the extinguisher rolling in. Use for every attempt beat (2 and 7). Ask for "camcorder look, slight video softness" inside the shot; the film lock stays on the rest.
- (b) THE BENCH BUILD: tank top, hunched over the bare mechanical part on a red toolbox, screwdriver in hand, two robot arms hovering over his shoulder, a wall monitor with the blue schematic behind him, cars under covers far in the background, warm tungsten practicals. Use for the take-apart and service beats (3, 4, 6). Shoot the hands and the part: close on the screwdriver, the housing coming off, the disc in his palm.
- (c) THE HOLOGRAM SCHEMATIC: a stylus on a glass drafting screen, the part drawn in pale blue lines that lift off the glass as a hologram, one region lit brighter; he traces the part with the stylus while the AI talks. Use for the one-number beat (5) only.

## Prompts: hands and the part, not him
The reference stills already carry his face and build, so a `video_prompt` spends at most one clause on him and the rest on what his hands do with the part and how the camera sees it. Shoot what matters: hands, close-ups, the part in isolation, cutaways to the mechanism moving, the wide only when the failure needs the room. A prompt that describes his expression, his clothes or the armor for more than one clause is wrong. Test: strip him out of the prompt and the shot should still explain the concept.

## Registers (--register)
- stark-build (default): mid-task, fast, amused. Hands busy in every shot, the test camera for the attempts, the bench for the take-apart. The mechanism is what he changed between attempt one and attempt two.
- stark-lecture: the press-conference / hearing showman. He stands, he has an audience, the hologram becomes a big presentation screen. He explains by putting the wrong answer on the screen and humiliating it, then the right answer in one sentence and a mic-drop. He still fails something small on the screen to make the point. Use for concepts that are mostly a misconception to correct.
- stark-sleep-deprived: 72 hours in, the basement register. 4 a.m., the fourth rebuild, coffee, sentences trail off, the AI more parental (one parental line per segment, never more: "seventy-two hours is a long time between siestas, sir"). Slower, funnier, more honest; the mechanism gets stated almost by accident and then he wakes up and hears it. Use for concepts about limits, budgets, failure modes and tradeoffs.
- the-AI: the counterpart voice. Calm, dry, British, never explains. Its lines are one of three things: the viewer's question ("Why one fewer lobe than pins, sir?"), a correction ("That is twelve, sir, not eleven"), or a number ("Eleven to one"). One clause, at most twelve words, "sir" once per exchange, no jokes of its own; its humour is understatement and literalism. It is a voice only: blue HUD text, rings, a waveform; never a body, a face or a robot.

## Tiers (--tier), in workshop vocabulary
- `build` (like JJK `technique`): one part, one fix. Beats 1,2,3,4,5,8 (the retest folds into the landing line). For a simple concept.
- `system` (like `domain`): the part in its system; adds beat 6 (service) and beat 7 (under load), so the guarantee is shown, "what this always does when built right". Beats 1-8.
- `mastery` (like `full`): everything, with a second HUD card before beat 5 for the number (e.g. "SPEC" / "11:1, no backlash").
Vocabulary: the rig = the raw problem; the part = the core mechanism; the system = the mechanism in its environment with its guarantee; the test = the mechanism run forward; the failure = the tradeoff or the limit; the Mark number = which iteration this is.

## script.json shape
Identical to `/explain` plus `"style": "stark"` at the top level (the renderer defaults to `jjk`, so this field is mandatory here).
```json
{
  "style": "stark",
  "topic": "string",
  "slug": "kebab",
  "tier": "build|system|mastery",
  "register": "stark-build|stark-lecture|stark-sleep-deprived",
  "music": "optional bare name, substring match against assets/stark/; omit for no music",
  "refs": "optional; omit to use the style's five stills of him with seed 42, or [] for text-only",
  "narrator_voice": "one paragraph of delivery instructions for the TTS fallback (fast, wry, self-interrupting; the AI is calm, dry, British, one clause)",
  "cast": "the inventor paragraph below, verbatim",
  "scenes": [
    {"id": "s1", "kind": "title", "kanji": "MARK 11 ELBOW", "english": "Cycloidal drive: eleven lobes, twelve pins", "narration": "", "sound": "arc-reactor hum, a soft hologram chime, no music"},
    {"id": "s2", "kind": "shot", "narration": "[stark] Alright, let's do this right. Mark Eleven elbow, full load, nice and easy. Dum-E, fire safety. And... lift.", "video_prompt": "...", "sound": "camcorder room tone, servo whine, a heavy clunk, no music"},
    {"id": "s5", "kind": "shot", "narration": "[ai] Eleven lobes on the disc, twelve pins in the ring, sir. Why one short?", "video_prompt": "...", "sound": "soft hologram chimes, stylus on glass, workshop hum, no music"}
  ]
}
```
Rules (unchanged from `/explain` unless noted):
- `narration` per scene: 1-3 sentences, at most 22 words. Whole video 100-135 words. Speaker tags: `[stark]` and `[ai]`; untagged text is the inventor. In lean mode the leading tag picks the voice sample for the whole scene, so give the AI its own short scenes and never put both voices in one shot.
- `kind: title` scenes render locally (HUD card), no fal spend. 1 per video, 2 at `mastery`. Title-card narration is empty or one short line; the card is silent in lean mode.
- `kanji` holds the English HUD title in caps on one line (the style sets `split: false`, so spaces do not break lines); at most ~16 characters ("MARK 11 ELBOW"). To stack two lines write them with " / " between ("CYCLOIDAL / DRIVE"). `english` is the subtitle in sentence case. No CJK.
- `video_prompt`: what the hands do + the part + the camera, in the vocabulary below; at most one clause on him. Paste the inventor paragraph verbatim where he appears (the renderer checks the first 40 characters of `cast`, so every prompt with him in it must contain "a dark-haired man with a trimmed goatee" exactly, or the whole paragraph gets bolted on the front). Never name real IP, actors, characters, films or studios. Do not write "no on-screen text" or "no dialogue": the renderer appends "No on-screen text." itself (and strips "no dialogue" on shots where he speaks). In test-camera shots the REC dot and timecode are wanted, so describe them as "the camcorder's own red REC dot and timecode burned into the corner as part of the picture". The renderer prepends the style lock and appends `Sound: <sound>`.
- Every `[stark]` shot gets a "what the hands do" clause first: "hands pull the lobed disc out of the ring of pins", "a screwdriver backs four bolts out of the elbow housing", "a gloved thumb smears grease around the cam". Then the part, then the camera, then (optionally) him.
- Exactly one concrete number in the whole script; it belongs to beat 5 and he repeats it at the end.
- Helmet, armor: not his. If a suit appears it is a part on the bench, on a stand or on the rig, never on him. The suit-up stills (`suitup-*.jpg`) are for the final under-load beat only, via a per-scene `"refs"`.

## Cast (use verbatim; never name the films)
Inventor: "a dark-haired man with a trimmed goatee in a dark tank top, oil on his hands and forearms, no armor, at a steel workbench in a private workshop"
The AI: "an unseen calm British-accented artificial intelligence, present only as pale blue holographic rings, text and schematic lines floating in the air"
Robots (optional, describe only): "a wheeled robotic arm with a three-finger claw holding a fire extinguisher"; "a second robotic arm on a rail holding the part up to the light".

## Style lock (the renderer prepends this; write prompts that agree with it)
"Live-action cinematic footage, anamorphic lens with gentle horizontal flare, shallow depth of field, cool blue holographic key light against warm tungsten workshop practicals, polished concrete and steel workshop, 24fps film look, fine film grain, photoreal. "
Accents per scene: hologram blue and white / warm tungsten amber from work lamps / the red toolbox and red tool chests / harsh white work lights on stands in the test-camera wide / a single red REC dot / welding white-orange sparks / grey smoke after a failure.
Settings: the bench (a steel bench, a red toolbox, the part on it, robot arms on rails, a wall monitor with a blue schematic, cars under covers behind glass); the test floor (a wide empty stretch of polished concrete, work lights on tripods, a black tool chest, a motorbike, a camcorder on a tripod); the glass drafting screen (a lit glass table, a stylus, the hologram lifting off it).
Lighting: warm tungsten practicals on the bench, cool blue from the monitor and the hologram, harsh white from the work-light stands on the test floor, reflections on concrete, dust in the beam, deep but readable shadows, no flat overhead light.
Camera grammar:
- title (HUD card): handled locally, no prompt.
- bring it in / test (the test camera): locked-off wide from a tripod camcorder, REC dot and timecode top corner, him small in the frame with the thing under test; hold through the failure; no cuts inside the shot.
- take it apart (the bench build): medium over the red toolbox, then close on the screwdriver and the housing coming off, robot arms hovering at the top of frame, the wall schematic soft behind.
- find the mechanism: close-up on his palm with the part in it, turned to the light; a cut-in to the part alone on the bench with the pins around it.
- the number (the hologram): close on the stylus on glass, the drawn schematic rising as a hologram, one region lit; his face out of focus behind it.
- service: hands only, macro: grease, the cam, the disc dropping on, the pins through the holes, the housing bolted down.
- under load (the test camera again): same locked-off wide, the heavy thing on the end, it holds, smoke from last time still in the room.
- landing line: medium close-up, he tosses the tool to the robot, one line, hold.
Physical prop presets (original): a bare mechanical arm on a red toolbox (the elbow reducer, the actuator); a printed disc with a lobed edge inside a ring of pins (ratios, reduction); a boot rig with thrusters (control, overshoot, damping); a padlock the robot arm cannot open (public keys); a tray of labelled bins he sorts bolts into (hashing, buckets); a disc under a strobe (sampling, aliasing); an engine block on a chain hoist (load, torque, proof).

## Title card (the renderer draws this locally)
Near-black background (0x05080F), the HUD title in hologram-blue caps on one line (Latin font, no CJK), a thin blue rule beneath, then the English subtitle in a paler blue. No noise, no glyph. Lines fade in one after another like a HUD booting; the subtitle last.

## Sound line
H3-Max generates native audio. Ask only for ambience and machines: "workshop hum", "servo whir", "camcorder room tone", "a socket wrench ratcheting", "a screwdriver on steel", "a heavy clunk", "a chain hoist", "stylus on glass", "soft hologram chimes", "a compressor kicking on", "a robot arm on rails", "a fire extinguisher hiss", "a part skittering across concrete", "grey smoke settling". Always end with "no music" unless the script sets a `"music"` bed.

## Reference images (default on)
The style sets `"refs"` to five stills of him cut from the workshop scene (`assets/ref/stark/tony-face.jpg`, `tony-bust.jpg`, `tony-3q.jpg`, `tony-full.jpg`, `tony-hands.jpg`) and `"seed": 42`, so every shot uses the reference-to-video endpoint and he is the same man across cuts. The renderer prepends "Image 1 to Image 5 show the same man; keep his face, hair, goatee and build consistent with them." Extras on disk: `tony-rig.jpg` (on the boot rig, test-camera framing), `tony-hands-alt.jpg` (grey T-shirt, different day; do not mix into the defaults), `suitup-1..3.jpg` (robot arms assembling the armor on him, the finished suit, stepping off the platform; for the under-load beat via per-scene `"refs"`), `set-rec-1.jpg` / `set-rec-2.jpg` (the empty test floor from the camcorder, before and after, with smoke), `set-workshop-1.jpg` / `set-workshop-2.jpg` (the bench and the wide workshop, no people). The old armor stills (`suit-*.jpg`, `mk2-*.jpg`) are kept but not in the defaults. If the user drops their own stills, save them as `assets/ref/stark/user-*.jpg` (16:9, 1280x720) and list them FIRST in a script-level `"refs"`. A script-level or per-scene `"refs"` / `"seed"` overrides; `"refs": []` renders text-only. A default still missing from disk is skipped with a warning; a still the script names itself must exist. `"image": "assets/ref/stark/set-rec-1.jpg"` uses one still as a first frame. Details and the still recipe are in SKILL.md. Describe him in `cast` anyway so text-only shots stay consistent.

## Lean-mode rules
- At most 22 words and 3 sentences per shot; the reference-audio window is 2-15 s.
- The scene's leading `[tag]` picks the voice sample (`[ai]` = the AI sample, `[stark]` or untagged = the inventor). Both samples are cut from real clip dialogue (`stark-voice.wav`, `ai-voice.wav`); the fish.audio generations are kept beside them as `*-tts.wav`.
- A `[stark]` scene is phrased so he keeps working and talks to the AI or the room, not to the lens ("the inventor keeps his hands on the part and says, half to the AI and half to the room..."); do not write "looks into the camera" in these prompts. An `[ai]` scene is an unseen voice from the ceiling speakers; nobody on screen mouths it. A scene with both voices is rendered entirely in the leading speaker's voice, so keep the AI to its own short scenes.
- Title cards are silent. The AI has no mouth: its scene shows the hologram and his hands on the stylus.
- Exactly one concrete number per video; it lives in beat 5 and he repeats it at the end.
- The mechanism is a physical thing he takes apart and holds; the hologram is only its drawing.

## Lesson ideas (the thing under test, the part inside, one number, the takeaway)
- Cycloidal drive: a suit arm slops at the elbow under load; inside is a lobed disc wobbling in a ring of pins on an eccentric cam; 11 lobes on 12 pins is 11:1; takeaway: every wobble the disc falls back one lobe, that is the whole gearbox, and every lobe carries load at once so nothing strips.
- PID control: the boot rig overshoots and kisses the ceiling; the part is the thruster valve and the height trace on the glass screen; the number is critical damping, one; takeaway: proportional chases, derivative brakes, integral pays off the leftover.
- Hash tables: he wants any bolt from ten thousand bins in one grab; the part is the stamp that prints a bin number from the bolt head; the first pass sends everything to one bin; the number is 0.7 (load factor, when to grow); takeaway: compute where it lives, do not search for it.
- Public keys: the robot arm must lock the schematics in a box that only he can open, without handing it a key; the part is a padlock that snaps shut without a key; the number is 2048 bits; takeaway: anyone can lock, only the owner unlocks; publish the lock, never the key.
- The Nyquist limit: a disc under a strobe looks like it spins backward on the test camera; the part is the strobe dial; the number is two samples per cycle; takeaway: sample at least twice as fast as the fastest thing you care about, or you film a lie.

## Narration is not stage direction (applies to every style)
The spoken line carries the idea: the rule, the condition, the cost, the number, the consequence, or something one person says to another. The `video_prompt` carries the action. Never narrate what the camera shows ("he turns the cam", "the disc wobbles", "the frame freezes", "she holds it up to the light"): the viewer can see it, and spoken shot description sounds like a prompt being read aloud. Test before rendering: if a narration sentence could be pasted into `video_prompt` unchanged, cut it or turn it into a claim ("A cam offset from center forces the disc to orbit, not spin"). Describing a character's decision or intent in the present tense is allowed only where the bible's register calls for it, and only about intent, never about motion. Lines addressed to someone (the AI, the robot, the room) are the surest way to stay on the right side of this; in this style the narration is what he says to the AI or the room while working, never a description of the shot.

## Object references (complicated shapes must be right)
If the concept is, or hinges on, a specific physical object with a complicated shape that has to be drawn correctly to make conceptual sense (a cycloidal drive, a robot gripper, an engine, a specific character or vehicle, a branded sneaker), the video model will not get it from words: the first cycloidal-drive render came out as a plain spur gear. Before writing `script.json`, dispatch a research subagent (Sonnet is enough) to fetch 2-3 clean reference images of the object (WebSearch/WebFetch, a product page, a paper figure, or yt-dlp frames), crop them to 16:9 1280x720 with no captions or watermarks, and save them under `<workspace>/assets/ref/objects/<object-slug>/`. Then put them on the scenes where the object is shown:
```json
"objects": {"assets/ref/objects/cycloidal/disc-and-pins.jpg": "the cycloidal disc with its scalloped lobed edge inside a ring of pins",
            "assets/ref/objects/cycloidal/exploded.jpg": "the drive's parts laid out: eccentric cam, lobed disc, pin ring, output pins"}
```
Script level applies to every shot; scene level to that shot. The renderer appends them after the character stills (nine images in all) and tells the model "Image N shows <label>; reproduce that object's exact shape, parts and proportions". A scene with only object references still routes to the reference-to-video endpoint. If the user supplies an image, use theirs first.

## Off-screen speakers (a voice with no body)
When a speaker has no body on screen (an AI in the ceiling, a radio, a narrator who must not be mouthed by anyone in frame), do not let the video model voice the line: given reference audio it will animate whatever face, or chin, it can find. List the tag in `"offscreen": ["ai"]` (style default or script level). The renderer then renders that scene as a silent clip with no reference audio, generates the line with the tag's fish.audio voice (`voices[tag]`), and mixes it over the clip like ordinary narration; captions follow the TTS. The screenwriter's part: tag the line (`[ai] ...`), keep it short, and still frame the shot so no face is prominent. Speakers who are on screen stay in lean mode.

## Say the number once; every other line is a different property
The one concrete number is the cause, not the takeaway. State it once, at the beat where it explains the mechanism, and never again. Repeating the MAIN POINT is fine, and good, when the last line drives it home; what must not be repeated is an incidental figure that means nothing on its own. Every other spoken line must carry a distinct property or consequence the viewer actually cares about (for a cycloidal drive: no backlash because half the pins share the load, torque density because the ratio fits in one disc, backdrivability because the arm can be pushed back by hand and feel what it holds). Before rendering, list each shot's line beside the property it states; if two shots state the same thing, or a line repeats a phrase from an earlier shot, rewrite it. The first Stark cut said "eleven to one" in three of six shots, and the user's verdict was that the ratio "doesn't mean much to the user".
