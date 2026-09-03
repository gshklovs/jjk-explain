# /explain-rick bible

Third voice beside `/explain` (the JJK narrator) and `/explain-iroh` (the tea master). Same pipeline, same script.json, a third temperature. The JJK narrator is cold and absolute; the tea master is warm and patient; this one is fast, contemptuous and *right*. The teacher is a drunk genius grandfather in a garage laboratory, and the student is his nervous grandson, who asks the question the viewer is too embarrassed to ask. The lesson works because the insults carry content, the throwaway line is the real explanation, and the boy's clumsy restatement at the end proves it landed.

## The teacher (how he teaches)
- He teaches while doing something else. His hands are always on a prop: a disc, a flask, a gadget, the guts of a machine. The mechanism gets named mid-gesture, as if it were too obvious to stop for.
- He is dismissive of the question and generous with the answer. "That's a dumb question, Morty" is followed by the exact answer. The insult is the attention grab; the content follows in the same breath.
- Throwaway lines are the explanation. The key idea is never framed as important. It is muttered while he is looking for a screwdriver, and the boy has to catch it.
- One concrete number, said with contempt for anyone who wouldn't know it. "Eleven lobes, twelve pins. Eleven to one. It's arithmetic, Morty."
- Physical demos, not diagrams. He never draws; he holds the thing, spins it, breaks it, throws it at the boy. The prop physically IS the mechanism.
- The boy's question is the viewer's question. He asks the naive version ("why not just use gears?"), gets mocked, and gets an answer that is better than the mockery.
- The boy's restatement confirms understanding. Near the end, the boy repeats the mechanism in his own words, half-wrong, and the teacher grunts "yeah, basically" or fixes one word. That is the only time the teacher does not insult him.
- Stutters and burps land between clauses, never on the key word. A burp is punctuation, not a joke. Keep at most one per scene, rendered as "*burp*" in narration.
- Usable takeaway at the end. He states where the thing is used, in the world, in one line, then dismisses the whole subject ("anyway, it's in every robot arm, hand me that").
- He is never wrong about the mechanism. The comedy is in the register, not in bad science. Do not simplify to the point of lying; he would hate that.

## Anchor lines (do not quote verbatim; match the cadence)
- "Listen, Morty, this is important, so pay attention, because I'm only going to say it once, and then I'm going to say it again, slower, because you're you."
- "It's not magic, Morty. It's a ratio. Count the lobes. Now count the pins. Subtract. Congratulations, you're an engineer."
- "You know what the difference between this and a gearbox is? Nothing hits anything. It rolls. Rolling is quiet. Quiet is precise."
- "Don't touch that. I mean, touch it, it's fine, but don't touch that one."
- "Wubba lubba... no, forget that. Focus."
- "Every robot arm you've ever seen a video of has one of these in the elbow, Morty. Every single one."
- The boy: "So it's, like, uh... the disc wobbles, and the wobble is... the gear?" / "Oh jeez, Rick." / "Okay, okay, I think I get it."
- The teacher's sign-off: "Great. Now hand me the *burp* the other thing."

Cadence: run-on sentences that snap into two-word verdicts. Direct address ("Morty, look"). Second person to the boy, first person for himself. Contractions everywhere. The number comes out flat, no drama. He never speaks more than three sentences without a gesture, a burp, or the boy interrupting.

## Beats (the garage segment)
1. TITLE CARD: dark green-black card, acid-green block capitals, English subtitle beneath. "CYCLOIDAL ACTUATORS / the gearbox that rolls". Silent except the garage hum.
2. THE BOY'S QUESTION: the naive question, which is the viewer's question. One line. The teacher, back to camera, is already holding the prop.
3. THE PROP: the teacher holds the thing that IS the mechanism, in frame, and names its parts while turning it. No mechanism yet, just "this is the disc, these are the pins".
4. THE MECHANISM, IN ONE BREATH: the rule stated fast, with contempt, with the one concrete number. The prop is manipulated to show it (the cam spins, the disc walks around the ring).
5. WHY ANYONE CARES: the throwaway line: where it lives in the world, what it beats, what it costs. Stated while looking for something else.
6. THE BOY'S RESTATEMENT: the boy says it back in his own words, slightly wrong. The teacher corrects one word or grunts assent.
7. SIGN-OFF: dismissive, a burp, a demand for a tool, the flask. Hold on the garage.

Keep the two hard rules from `/explain`: exactly one concrete number per video, and the concept shown as a physical thing the characters touch (a disc, a cam, a ring of pins, a wire, a flask of liquid), never a diagram or a whiteboard equation.

## Registers (--register)
- rick-lecture (default): fast, dismissive, correct. The insults are casual, not angry. The prop is always in hand.
- rick-annoyed: the boy asked twice. Shorter sentences, more stutters, "oh my god, Morty". Good for concepts everybody gets wrong; the annoyance is at the world, not the boy.
- rick-drunk-genius: flask in hand, slurring, the explanation still perfect. Tangents that turn out to be the point. Use when the concept has a surprising twist (the "backwards" property, the dual).
- morty-gets-it: the counterpart register for beats 2 and 6 only. Nervous, stammering, "uh", "oh jeez", but the restatement at beat 6 is actually right. Never use the boy's voice for explanation.

## Tiers (--tier)
- `demo` (like `technique`): one prop, one rule. Beats 1,2,3,4,6,7. Simple concept, 5 scenes.
- `build` (like `domain`): adds beat 5 (why anyone cares, what it beats, the cost). Beats 1-7. 6 scenes.
- `blueprint` (like `full`): everything, with a second title card before beat 5 ("THE CATCH", the tradeoff).
Vocabulary: the prop = the core mechanism; the ratio/number = the guarantee; the catch = the tradeoff; the garage = the wider field; "every robot arm" = where it lives.

## script.json shape
Identical to `/explain` plus `"style": "rick"` at the top level (mandatory; without it the renderer uses the JJK look and voice).
```json
{
  "style": "rick",
  "topic": "string",
  "slug": "kebab",
  "tier": "demo|build|blueprint",
  "register": "rick-lecture|rick-annoyed|rick-drunk-genius",
  "narrator_voice": "one paragraph of delivery instructions (fast, slurred, casual insults; the boy nervous and higher)",
  "cast": "the two cast paragraphs below, verbatim",
  "seed": 4242,
  "scenes": [
    {"id": "s1", "kind": "title", "kanji": "CYCLOIDAL / ACTUATORS", "english": "the gearbox that rolls instead of meshing", "narration": "Cycloidal actuators.", "sound": "garage laboratory hum, fluorescent buzz"},
    {"id": "s2", "kind": "shot", "narration": "[morty] Rick, why not just use normal gears? Gears work.", "video_prompt": "...", "sound": "garage hum, a gadget beeping"},
    {"id": "s3", "kind": "shot", "narration": "[rick] Because gears hit each other, Morty. This rolls. Watch.", "video_prompt": "...", "sound": "garage hum, plastic disc clicking against pins"}
  ]
}
```
Rules:
- Every shot narration starts with a speaker tag, `[rick]` or `[morty]`, and stays with that speaker for the whole scene (lean mode picks the voice sample from the first tag; a scene that mixes tags uses the first and warns). One speaker per scene.
- `narration` per shot: 1-3 sentences, at most 22 words (the model's reference-audio window is 15 s; 22 words at 2.6 words/s plus pauses is about 11 s). Whole video 110-140 words, 5-6 scenes, 1 title card.
- The boy speaks in exactly two scenes: the question (beat 2) and the restatement (beat 6). Everything else is the teacher.
- `kind: title` scenes render locally: dark green-black card, acid-green capitals, English subtitle. `kanji` holds the big English text; " / " splits lines. No CJK. 1-2 per video.
- `video_prompt`: subject + action + setting + camera in the style vocabulary below. Never name real IP, characters, studios, shows or people. Do not write "no dialogue" (the character speaks in lean mode) or "no on-screen text"; the renderer appends the latter itself.
- The renderer swaps the first "the scientist" / "the old scientist" / "the boy" / "the kid" mention in a prompt for the cast paragraph if the cast is not already present. The check is the first 40 characters of `cast`, so every prompt must contain the phrase "a tall thin elderly scientist with spiky pale-blue hair" verbatim (even when he is only in the background), or the whole cast paragraph gets bolted on the front. Describe the speaking character in full and the other one briefly.
- Exactly one concrete number in the whole script. The concept must be a physical prop that the teacher holds.

## Cast (use verbatim; never name the show)
Teacher: "a tall thin elderly scientist with spiky pale-blue hair, a single heavy unibrow, dark bags under half-lidded eyes, a permanent smirk with a thread of drool at the corner of the mouth, wearing a white lab coat over a teal shirt with brown trousers and black shoes, holding a small metal flask, gesturing sharply with the other hand"
Student: "a short skinny teenage boy with short brown hair, a round anxious face with wide eyes and a slightly open mouth, wearing a plain yellow T-shirt, blue jeans and white sneakers, shoulders hunched, hands half-raised"

## Style lock (the renderer prepends this; write prompts that agree with it)
"2D American adult TV animation, thick uniform black outlines, flat saturated colours with no gradients, simple rounded shapes, slightly wobbly hand-drawn linework, sickly green and teal fluorescent lighting, cluttered sci-fi garage laboratory backgrounds, limited 24fps animation, exaggerated expressive faces, no anime shading, no film grain. "
Palette: sickly green and teal on grey concrete / acid-green glow from a portal or a screen / warm yellow from a bare bulb over the workbench / the boy's yellow shirt as the only warm colour in the frame.
Settings (all inside one suburban garage turned laboratory): a long metal workbench buried in wires, circuit boards, beakers and half-built gadgets; a rolling tool chest; a whiteboard covered in scrawl (never legible, never the explanation); a small dented flying saucer parked at the back with its hatch open; a green glowing circular portal on the wall; shelves of jars and blinking devices; a concrete floor with a drain; a garage door half open on a suburban street at dusk.
Lighting: flat fluorescent tubes overhead, a sick green cast on everything, one warm bulb over the workbench, the portal or a screen as a green key light, no rim light, no film grain.
Camera grammar:
- title: handled locally, no prompt.
- the boy's question: medium two-shot, the boy in the foreground turning to the teacher, the teacher back to camera bent over the bench.
- the prop: close-up on the teacher's hands holding the object, then a tilt up to his face as he names it; the object big in frame.
- mechanism: static medium shot, the teacher facing camera, the prop held at chest height and turned, one quick cut-in to the moving part.
- why anyone cares: wide garage, the teacher walking away from camera toward a shelf, still talking; the boy watches holding the prop.
- restatement: reverse of the question shot; the boy now facing camera holding the prop, the teacher half in frame, unimpressed.
- sign-off: medium close-up, the teacher takes a swig from the flask, wipes his mouth, hold on the garage.
Prop presets (original): a printed plastic disc with lobed edges inside a ring of pins (ratios, rolling contact); a coil of wire he unspools and drops loops of (queues, windows); a jar of marbles he pours through a funnel (throughput, congestion); a rubber sheet he stretches over a bowl and rolls a ball on (gradients, potentials); two flashlights with coloured gels crossed on the bench (interference, superposition); a pegboard with hooks and a bucket of keys (hash tables); a spring scale he bounces (control loops, damping).

## Title card (the renderer draws this locally)
Near-black card with a dark green cast, faint static noise, big acid-green block capitals in a bold sans (one or two lines, split on " / "), the English subtitle in pale green beneath. No glyph. Fade in hard like a monitor switching on.

## Sound line
H3-Max generates native audio. Ask only for ambience; no music, ever, in this style. Vocabulary: "garage laboratory hum", "fluorescent tube buzz", "small gadgets beeping", "a flask sloshing", "tools clinking on a metal bench", "plastic disc clicking against steel pins", "a portal whoosh and crackle", "a servo whine", "a garage door rattling", "a car passing on the street outside". Do not write "no dialogue"; the characters speak.

## Reference images (default)
The style carries default `refs` (the stills in `assets/ref/rick/`: three of the teacher, two of the boy) with `ref_owners` so the renderer tells the model which images are which character, and a default `seed`. Override per script with `"refs"` + `"ref_owners"`. Details in SKILL.md. Describe both characters in `cast` anyway so text-only shots stay consistent.

## Research
Source notes, verified anchor lines, five worked lesson ideas and the asset inventory (which still is which character, source clip and timestamp) are in `docs/rick-research.md`.

## Narration is not stage direction (applies to every style)
The spoken line carries the idea: the rule, the condition, the cost, the number, the consequence, or something one person says to another. The `video_prompt` carries the action. Never narrate what the camera shows ("he turns the cam", "the disc wobbles", "the frame freezes", "she holds it up to the light"): the viewer can see it, and spoken shot description sounds like a prompt being read aloud. Test before rendering: if a narration sentence could be pasted into `video_prompt` unchanged, cut it or turn it into a claim ("A cam offset from center forces the disc to orbit, not spin"). Describing a character's decision or intent in the present tense is allowed only where the bible's register calls for it, and only about intent, never about motion. Lines addressed to someone (the student, the viewer) are the surest way to stay on the right side of this.

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

## No meta examples: the running example is a concrete product, never the craft itself
When the concept is about communication, marketing, teaching, writing or persuasion, the running example must be a concrete, everyday product or situation (a canned cold brew, a bakery, a bike lock, a dentist), never an example drawn from the same craft (a founder buying "a content strategy" to illustrate marketing; a lesson about lessons). A same-craft example makes the viewer lose track of what is the lesson and what is the illustration ("before you are invisible and after you are invisible?"). Test: could a twelve-year-old say which sentence is the product's and which is the narrator's? If not, change the product.

## Full sentences, five ideas, one thread
- Full sentences only: 7 to 16 words each, at most 3 per shot, every one ending in a full stop. No fragments ("Shoulder, far. Wrist, barely."), no colon lists, no riddles. A fragment is folded into the sentence before it ("A turn at the shoulder carries the cup far; at the wrist, barely at all."). The TTS rushes a four-word sentence and it stops sounding like the narrator; the viewer hears a shot list.
- At most five ideas per video, one per shot. The last shot carries only the payoff of the running example and the takeaway; it introduces no new fact. If the property list is longer than five, cut properties, do not pack them.
- One thread: the running example is named in at least every other shot, so the payoff lands on something the viewer has been holding. A puzzle set up in shot 2 and next mentioned in the last shot arrives cold.
- The payoff states the consequence in words ("the spare joint is a choice: bend low, pass beneath the lamp, and the cup reaches the shelf"), never a pose or a gesture ("Elbow high meets the lamp. Elbow low, the shelf.").
Evidence: the fresh inverse-kinematics render had six four-word sentences in its last shot, a puzzle abandoned for five shots, and a payoff written as two poses; the user heard cut-offs, lines "not in the narrator's voice", and a story that "made slightly less sense".
