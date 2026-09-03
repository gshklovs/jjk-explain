# /explain-rick research

Sister to `/explain-iroh`. Same pipeline, opposite teacher. Iroh teaches sideways with tea and patience; this one teaches at full speed, drunk, insulting, while soldering something, and the insults carry the content. The bible may name the show; the prompts sent to the video model must NOT (describe only).

Status: written from knowledge first (2026-09-02), search notes appended at the end under "Search notes".

## 1. How Rick actually teaches (the rhythm)

The show's explanation scenes are almost always: Morty asks a dumb question that is exactly the viewer's question; Rick answers it in one contemptuous breath while doing something else with his hands; the answer is correct and complete; Morty restates it badly; Rick either corrects the restatement with more contempt or lets it stand and moves on. The lecture is never the point of the scene for Rick (he wants the thing done), which is why it reads as truth rather than exposition.

Mechanics of the register:
- Rapid, dismissive, front-loaded. The mechanism is said first, fast, then the insult, then a throwaway that is actually the second half of the mechanism. He never builds up to the point; he drops it and complains that you needed it.
- Burps and stutters are punctuation, not noise. A burp lands mid-clause, usually right before the key noun ("it's a *burp* hash function, Morty"). Stutters ("M-M-Morty", "the thing is, the thing is") are the sound of him thinking faster than he speaks. In TTS/script terms: one burp per shot at most, marked in the narration only if the voice can do it; otherwise leave it to the prompt ("he belches mid-sentence").
- Insults that carry real content. "You're thinking about it like a 14-year-old, Morty. Nobody ever waits for the whole thing, that's why we send it in pieces." The insult is a clause that names the mistake in Morty's mental model, so it is a teaching move.
- Throwaway lines that ARE the explanation. He says the actual mechanism in a subordinate clause while fixing the ship ("...because a receiver that's drowning just stops answering, hand me the thing, the THING, Morty").
- Morty's dumb question is the viewer's question. "But Rick, how does it know which one to pick?" is never mocked by the show, only by Rick. The script must ask the exact question a smart beginner would ask.
- Morty's restatement confirms understanding. "So... it's like, the more it drops, the slower you go?" is the beat where the viewer checks their own model. Rick's reply is "Yeah. Sure. Basically." or "No, Morty, the OPPOSITE, listen..." (a second pass at the mechanism).
- "Morty, listen." / "Listen, Morty." / "Okay, okay, okay" is the attention grab; it opens the mechanism beat.
- "It's simple / obviously / it's not that complicated" applied to hard science. He treats a Kalman filter the way you'd treat a can opener. That contempt for difficulty is the confidence the viewer borrows.
- He names the mechanism while doing something else with his hands (tightening a bolt, pouring from the flask, holding a screwdriver in his teeth, tossing a gadget to Morty). The prop in his hands should BE the mechanism, not illustrate it.
- Sudden earnestness for one line, then it's gone. Once per lesson he says the real reason it matters, flat and quiet, then covers it with a burp or an insult.
- Cynical cosmic frame. "Nobody designed it, Morty, it's just what survives" is a Rick-native way to say "this is an emergent/evolved solution". Use for anything greedy/heuristic/evolved.

### Anchor lines (cadence only; paraphrase, never quote verbatim in output)
1. "Wubba lubba dub dub" -- his catchphrase; a nonsense sign-off. Use the RHYTHM of a nonsense sign-off, not the phrase (IP).
2. "Listen, Morty, I hate to break it to you, but what people call 'love' is just a chemical reaction that compels animals to breed." -- the register: a hard thing reduced to its mechanism in one sentence, with contempt for the softer framing.
3. "Nobody exists on purpose, nobody belongs anywhere, everybody's gonna die. Come watch TV." -- the sudden-earnest line followed immediately by the deflection. This is the beat-6 shape.
4. "Sometimes science is more art than science, Morty. Lot of people don't get that." -- the "it's simple/obvious" register applied to something that is not simple.
5. "I'm not looking for judgment, just a yes or no. Can you assimilate a giraffe?" -- how he asks questions: precise, absurd, expects a specific answer.
6. "To live is to risk it all; otherwise you're just an inert chunk of randomly assembled molecules drifting wherever the universe blows you." -- the cosmic frame, used to make a technical point (do something / act) land.
7. "Weddings are basically funerals with cake." -- compression: a definition as a joke. Every mechanism line should aim for this shape (X is basically Y with Z).
8. "Don't think about it." -- his answer to a question he does not want to explain; in a lesson, use it once, for the part that is genuinely out of scope, then explain anyway.
9. "You gotta get schwifty" / the nonsense-word register: he coins words for things. A lesson can coin a name for the mechanism (Morty repeats the coined word in the restatement).
10. "Your boos mean nothing, I've seen what makes you cheer." -- contempt for the audience's intuition, i.e. "your intuition about this is wrong, and here is why".
11. "I turned myself into a pickle, Morty!" -- the demo-prop energy: he has physically become the thing. The prop beat should have this pride ("I built the thing, Morty, look at it").
12. Morty: "Aw geez, Rick" / "Oh man" / "That's... that's really messed up, Rick" -- Morty's fillers. Nervous, apologetic, always ends with "Rick".

Cadence summary: long run-on sentence with three commas and a burp, then a two-word sentence. "Morty" as a comma. Questions to Morty are rhetorical and hostile ("You know what a checksum is? No. Of course not."). Morty's lines are short, start with "Aw geez" or "But Rick", and end up-inflected.

## 2. Registers

- **rick-lecture (default).** Fast, bored, correct. He is fixing something at the workbench and explains without looking up. The mechanism comes out in one breath with an insult in the middle; the number is thrown away ("it's like, ten to the nine, Morty, whatever"). Use for any concept with a clean mechanism (data structures, protocols, control loops). One burp per shot max; one earnest line per lesson.
- **rick-annoyed.** Morty asked twice. Shorter sentences, louder, more "listen", he puts the tool down and turns to face Morty, jabs the prop at him. The mechanism is said TWICE, second time slower and dumber ("Okay. OKAY. Slower, for you."). Use when the concept has a common misconception that the restatement will get wrong; the second pass is where the correction lives. Also the register for the sign-off if Morty's restatement was wrong.
- **rick-drunk-genius.** Flask register. Slurred, tangential, three ideas at once, but the tangent is the borrowed-wisdom beat (he compares the mechanism to something from a different field, a different dimension, a thing he built once). Moments of clarity: mid-slur he says the mechanism perfectly, then loses it again. Use for concepts that are genuinely cross-disciplinary (Kalman filter = weighted average of two guesses = how you cross a street; gradient descent = walking downhill blindfolded). Fewer numbers, more metaphor; keep the one number in a moment of clarity.
- **morty-gets-it.** The counterpart voice for beats 2 and 7. Nervous, stammering, "aw geez", but the restatement is actually right, and the show's rule is that when Morty gets it he says it plainer than Rick did. That plain restatement is the viewer's takeaway line; write it as the sentence you'd want on a flashcard, in a 14-year-old's words. Rick's response is grudging ("...yeah. Don't let it go to your head.").

## 3. Visual vocabulary

The garage lab: a suburban two-car garage converted into a lab. A long cluttered workbench under a window; pegboard with tools; shelves of jars, beakers with glowing green/teal liquid, coils of cable; a half-built flying saucer (junk-metal, riveted, a dome) parked in the middle; a portal gun (a boxy handheld device with a green-glowing bulb) on the bench; scattered blueprints; a whiteboard with scrawled equations; holographic readouts floating over a console; a garage door, a fridge, a washing machine; the portal itself is a swirling green disc of light that lights everything it touches green. Junk everywhere: pizza boxes, empty bottles, alien parts.

Animation style facts for the style lock: 2D American adult TV animation; thick, uniform-weight black outlines on everything (no brush taper); flat saturated fills with almost no shading (at most one flat shadow tone); simple rounded shapes and slightly wobbly, imperfect linework (deliberately "off-model" charm); big round eyes with small pupils, wide mouths with visible teeth rows; drool and stubble drawn as a few lines; muted domestic background colours (beige walls, grey concrete) hit by sickly green/teal or cold fluorescent light; no anime shading, no gradients on characters, no film grain, no lens effects.

### Style-lock sentence (draft; prompts must agree with it; never names the show)
"2D American adult TV animation, thick uniform black outlines, flat saturated colours with minimal cel shading, simple rounded slightly wobbly character shapes, big round eyes with small pupils, plain cluttered suburban-garage backgrounds in beige and grey lit by sickly green and teal glow and cold fluorescent light, 24fps limited animation, no anime shading, no gradients on characters, no film grain."

### Cast paragraphs (describe only; never name the show, characters, studio or real people)
Scientist: "a tall thin elderly man scientist with spiky pale-blue hair swept up and back, a single thick unibrow, sunken eyes with heavy bags, a long face with a line of drool at the corner of his mouth, wearing a white lab coat over a teal shirt and brown trousers, holding a small silver flask, slouching, gesturing with a screwdriver, sneering and talking fast"
Boy: "a short nervous fourteen-year-old boy with short brown hair, big round eyes, a small mouth, wearing a plain yellow T-shirt and blue jeans with white sneakers, shoulders hunched, hands fidgeting, looking worried"

Set presets (original phrasing): "a cluttered suburban two-car garage converted into a laboratory, long workbench covered in tools, wires, beakers of glowing green liquid, a junk-metal flying saucer parked in the middle, pegboard of tools, a whiteboard of equations, a garage door behind"; "close on the workbench, soldering iron, coils of cable, a boxy handheld device with a green-glowing bulb"; "a swirling green portal of light on the garage wall casting green light across the room".

Camera grammar (mirroring the Iroh bible):
- title: local card, no prompt.
- Morty's question: medium two-shot, the boy in foreground looking at the scientist's back at the bench.
- prop grab: close-up on the scientist's hands lifting the object off the bench, green bench light, shallow focus.
- mechanism: static medium close-up of the scientist speaking straight to camera, mouth moving, one hand holding the prop, the other gesturing with a screwdriver; small camera shake when he shouts.
- the number: insert shot of the prop with a scrawled number on the whiteboard behind (no on-screen text; say "a whiteboard of scribbles" rather than a number, because the model cannot render clean digits).
- where it's used: wide shot of the garage, the scientist walking away toward the saucer, thrown over his shoulder.
- Morty restates: reverse shot, the boy facing camera, hopeful.
- sign-off: the scientist takes a swig from the flask, belches, turns back to the bench, hold on his back; a green portal opens behind him.

## 4. Beats of a Rick lesson
1. TITLE CARD (local): a "title" card in the show's green/black register (see PM for the local drawing; suggestion: black card, acid-green sans-serif title, small portal-swirl glyph, VHS-free, no flicker). Narration: Rick reads the title with contempt ("Okay, 'How TCP works'. Great. Thrilling.").
2. MORTY'S STUCK/DUMB QUESTION: the viewer's question, in Morty's voice, 8-15 words. "Rick, why doesn't the internet just send everything as fast as it can?"
3. RICK GRABS A PROP THAT PHYSICALLY IS THE MECHANISM: he picks a thing off the bench and it works the way the concept works (a hose with a valve, a bag of jars, a spring-loaded gadget). No explanation yet; he insults Morty for not seeing it.
4. THE MECHANISM IN ONE BREATH WITH INSULTS: the rule, fast, complete, one burp, one insult that names Morty's wrong model.
5. ONE CONCRETE NUMBER: exactly one per video, thrown away ("it halves, Morty, HALVES, fifty percent, every time it drops one").
6. WHY IT MATTERS / WHERE IT'S USED (throwaway): over his shoulder, walking off. One sentence; this is the earnest line if the lesson has one.
7. MORTY'S RESTATEMENT: plain, nervous, right. The flashcard sentence.
8. RICK'S DISMISSIVE SIGN-OFF + BURP: "Yeah. Whatever. Get in the ship." Swig, belch, portal.

Hard rules carried over from `/explain`: exactly one concrete number per video; the concept shown as a physical thing the characters handle, never a diagram. Extra Rick rule: the prop must be in his hands when he says the mechanism.

## 5. Five lesson ideas

1. **TCP congestion control.** Puzzle (Morty): "Why can't the internet just send everything as fast as it can?" Prop: a garden hose with a hand valve into a bucket that overflows; Rick opens the valve a bit more each second until the bucket spills, then slams it to half. Mechanism: send a little, double it every round trip until something drops, then cut the window in half and creep up again; the whole internet is a million idiots doing this at once, which is why it doesn't collapse. Number: the window HALVES on a drop. Takeaway (Morty): "So it goes faster and faster until it breaks, then backs off halfway and tries again." Where used: every video stream, every download.
2. **Cycloidal actuators / drives.** Puzzle: "How does the robot arm hold that heavy without stripping its gears?" Prop: a wobbly disc with lobes rolling inside a ring of pins from a disassembled drive; Rick spins the input and the disc wobbles around slowly. Mechanism: the disc has one fewer lobe than the ring has pins, so each turn of the eccentric input advances the disc by exactly one lobe; every lobe shares the load at once, so nothing strips. Number: 1 fewer lobe = 1 lobe per turn, so 30 lobes = 30:1 reduction (pick "thirty to one"). Takeaway: "It walks around one bump per turn, and everything is touching so nothing breaks." Where used: robot joints, the ship's landing gear.
3. **Hash tables.** Puzzle: "How does it find my thing without looking at every thing?" Prop: a shelf of numbered jars; Rick mashes a label through a "grinder" gadget that spits a number, then drops the part into that jar. Collision: two parts in one jar, he just chains them. Mechanism: turn the name into a number, use the number as the shelf address; lookup is the same grind, one jar, done. Number: one jar out of a thousand, so a lookup is about one step no matter how many jars. Takeaway: "You don't search for it, you compute where you put it." Where used: every dictionary, every cache, every login.
4. **Gradient descent.** Puzzle: "How does the thing learn if nobody tells it the answer?" Prop: a marble on a lumpy sheet of foil over junk; Rick tilts, nudges, the marble rolls downhill in little steps; too big a nudge and it flies off. Mechanism: measure how wrong you are, feel which way is downhill for every knob, move every knob a tiny bit that way, repeat a million times. Number: one step of 0.01 (the learning rate) or "a million steps". Takeaway: "It doesn't know the answer, it just knows which way is less wrong." Where used: every neural net Morty has ever complained about.
5. **Kalman filter.** Puzzle: "The ship's GPS is jumpy and the speedometer drifts, which one do I trust?" Prop: two flasks, Rick pours from both into one beaker, more from the flask he trusts; the beaker is the estimate. Mechanism: predict where you are from what you did, measure where you are with the noisy sensor, blend the two weighted by how much you trust each, and update the trust; the blend is always better than either. Number: the gain (0.7 from the sensor, or "trust it 70 percent"). Takeaway: "You guess, you look, you average, but you average smart." Where used: every phone's blue dot, rockets, the ship's autopilot (drunk-genius register fits this one).

## 6. Look-alike videos with seed images / reference stills
(see Search notes; to be filled from searches)

## 7. Sound vocabulary for prompts (no music)
"low garage hum", "fluorescent tube buzz", "gadgets beeping softly", "a flask sloshing", "tools clinking on a metal bench", "a soldering iron hiss", "a distant washing machine", "a portal whoosh and crackle", "electrical arc snap", "a belch", "the saucer's engine ticking as it cools", "garage door rattling in the wind", "a fridge compressor". Always "no music, no dialogue" unless lean mode is speaking the line (then "no music").

## Search notes (appended 2026-09-02)

### 6. Look-alike videos with reference stills (what worked)
Sources scanned (4 searches): Kling "Elements" / character-consistency guides, Veo "Ingredients", Runway References/Gen-4, Midjourney `--cref`, "Rick and Mortify" (Medium), Atlabs/ReelMind/Pixwit fan-video how-tos, Flick/Neolemon consistency guides.
- Everyone converges on the same workflow: lock the identity in ONE clean master still first, then reuse that still (plus 2-3 more angles of the same design) in every shot; the prompt then describes only action, camera and setting, never the face again. This is exactly the Iroh `refs` + `seed` path.
- Cut-outs beat full frames. The "Rick and Mortify" storyboard project got the best fidelity by cropping character poses out of show frames and removing the background before using them as references; busy backgrounds leak into the output. If likeness drifts, make transparent/plain-background crops of the stills below.
- Multiple angles, same clothes. Front + three-quarter + full-body of the same outfit; do not mix outfits across refs (a bearded/tan-jacket variant of the scientist exists in the show and would poison the set, so it was excluded).
- Style words matter as much as refs for this look: "thick uniform black outlines, flat colours, no shading" keeps the model from drifting into anime or 3D. Say "no gradients on characters" explicitly.
- Sequential context: some pipelines feed the previous clip's last frame as the next clip's first frame (`image:`) for continuity; use on 2-3 shots max as the Iroh bible already warns.
- Motion reference (`ref_videos`) is the least documented; the show's characters gesture with whole arms and lean at the waist, so a 6 s bench clip is included (untested on the endpoint).
- Untested by me: none of the above was run on fal/H3-Max; these are practitioner reports, not measurements.

### Asset notes
Stills are 1280x720 from official Adult Swim YouTube uploads (720p), with the bottom-right channel bug cropped away (crop 1152x648 at origin, then rescale). The garage stills come from the S1 "Rick Potion #9" cold open and pilot; the street and alien-planet stills are included only for full-body views. See the asset inventory in the PM report.

### Anchor lines checked against real transcripts (auto-subs, for cadence)
- "Morty, the answer is don't think about it. It's not like we can do this every week anyways. We get three or four more of these, tops." (dismissal + a thrown-away number)
- "You're thinking of bullets, Morty. Death crystals show you how you're going to die." (the insult that names the wrong model, then the definition)
- "Your future stems from your present, which, if you're living right, keeps changing." (mechanism in one breath)
- "Faster, good idea, Morty. It'll get us through these asteroids sooner." (sarcastic agreement as correction)
- Morty: "Aw geez, you're really this pissed about my mom making sure I'm okay?" / "Why are they called death crystals? Do they kill you?" (the viewer's question, literally)
- Morty (plain restatement register): "So we bailed on that reality and we came to this one, because in this one the world wasn't destroyed."
