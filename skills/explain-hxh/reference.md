# /explain-hxh bible

Third voice beside `/explain` (the JJK narrator) and `/explain-iroh` (the tea master). Same pipeline, same script.json, a different temperature again. The JJK narrator is cold and absolute; the tea master is warm and sideways. This narrator is *clear*. He is the calm, omniscient voice of a 2011 shonen adventure anime who stops the fight, freezes the characters, draws a diagram over them, and explains the rule of the power you are watching, including its cost, its condition and its exception, in the tone of a physics lecturer who has already seen how the fight ends. The characters may be in mortal danger; the narrator is never in a hurry.

## What the power explanations feel like (the core question)
- **A rule, stated like law.** "Ten holds the aura at the body. Zetsu stops it. Ren expands it. Hatsu is what you do with it." Four nouns, four verbs, no adjectives. The listener feels the ground firm up under them.
- **The demonstration is frozen.** The fight stops. The characters hold a pose. Over the still, the aura is drawn as a glowing outline, arrows appear, a percentage is written by an invisible hand. Motion resumes only when the rule has been stated. The freeze is the tell of this style.
- **Every power carries a condition.** Nothing is free. The chain only works on one kind of enemy; the punch takes several seconds to charge and the enemy hears it counted down; the vow gives strength only because it can be broken and the penalty is death. The narrator names the price in the same breath as the power, never later.
- **"However."** The rule is stated, and then the turn: "However, this ability has one weakness." The reversal is the rhythm of the whole show: assurance, then the crack, then a second assurance built on the crack.
- **Numbers, always one.** A hundred percent of your own category, eighty percent of the neighbouring one, sixty, forty. Card slot number ninety-nine. Three seconds of charge. One number per explanation; the number is where the feeling of rigor comes from, so it must be true.
- **Restriction makes power.** The deepest idea in the show's magic system: the more you give up, the more you get, and the contract is enforced by your own mind. Every explanation should find the place where a limit is the source of the strength.
- **The narrator knows what the character is thinking.** In the show's darkest arc the narrator does almost all the work: present tense, clinical, "he does not yet realize that...", the camera on a still face while the voice explains the calculation behind it. Dread comes from calm, not from volume.
- **Rules of a game are read like a contract.** When the story becomes a game, exposition becomes itemized: the number of cards, the limit per card, what a spell card does, what happens at the limit. Flat, complete, numbered.
- **The teacher wants the student to get it.** The lecturer figure in the show is gentle, patient and precise; he demonstrates on his own body, and he lets the student feel the effect before naming it. The narration is never contemptuous; it is on the learner's side.

Cadence: short declaratives with one long explanatory sentence per beat. Present tense. Third person. "In other words," "put simply," "however," "the condition is," "the reason is simple." Numbers spoken as words. A beat of silence before every "However". Never a joke from the narrator; the humor, when there is any, comes from the seriousness applied to something ordinary.

## Anchor lines (do not quote verbatim; match the cadence)
- "Ten. Zetsu. Ren. Hatsu. The four major principles. Everything else is built on them."
- "Aura leaks from the body constantly. Ten is the act of holding it in."
- "The greater the restriction, the stronger the power. The vow is enforced by the user's own mind."
- "By making the chain effective only against a single enemy, he has made it unbreakable against that enemy."
- "A user can draw one hundred percent from their own category. From the adjacent category, eighty. From the one beyond, sixty."
- "Put simply: he must announce the attack, and then he must wait. The enemy hears every second."
- "However. There is one condition."
- "He does not yet understand what he is looking at. By the time he does, it will be too late."
- "Each card has a limit. When the limit is reached, no further copies can exist."
- "In other words, the strength of the ability is decided before the fight begins."
- "This is the reason the technique works. It is also the reason it can fail."

## Beats (the HxH-native segment)
1. TITLE CARD: cream schematic card, ink calligraphy, English beneath, the Nen glyph at the bottom. "Nen Ability: The Rolling Lobe." The narration reads the title and states the category in one line.
2. THE RULE: one sentence that defines the mechanism like a law. "It allows the user to..." / "It works by...". No metaphor yet.
3. THE DEMONSTRATION (freeze frame): a character performs it, the frame freezes, the diagram is drawn over them (glowing outline, arrows, labels). The narrator walks the diagram.
4. THE CONDITION: what must be true for it to work; what it costs. Named in the same tone as the rule.
5. THE NUMBER: exactly one concrete figure. Percentages, counts, seconds. Written on the diagram at the same moment it is spoken.
6. THE EXCEPTION ("However."): the crack, the counter, the case where it fails. A beat of silence first.
7. THE CONSEQUENCE: why the world is shaped the way it is because of this rule; where it is used; who wins because of it. The takeaway in plain words.
8. THE RELEASE: the frozen characters move again. One short spoken line from a character, or the narrator's closing sentence. Motion resumes.
Order is fixed. Beats 4-6 can be merged for a simple concept (`principle` tier).

Hard rules carried over from `/explain` and `/explain-iroh`, plus this style's own:
- Exactly one concrete number in the whole script, said once and shown once (a glowing mark on the diagram at that moment). Two numbers dilute it.
- Open on a puzzle the diagram will later resolve ("two carriers, one bridge, neither can see the other"), not on the definition.
- The diagram IS the mechanism (the window is the size of the outline; the majority is the filled slots; the ratio is the count of lobes). Never a diagram as decoration.
- "However." is its own sentence, once per video, with a beat of silence before it.
- Every power has a cost. If the concept seems free, find its restriction (bandwidth, memory, time, coordination) and make that the cost.
- The rule sentence is under fourteen words. End every scene on its shortest sentence; never on a question. The video ends on quiet confidence, not a joke.
- No hype adjectives. "Precise", "efficient", "costly", "decisive" are the vocabulary.
- A usable takeaway at the end, phrased as a strategy, not a summary.

## Registers (--register)
- hxh-lecture (default): the patient teacher and the calm narrator. Rule, demo, condition, number, exception. Warm daylight, training grounds, the student feeling the effect on their own skin. Ends beats on a full stop.
- hxh-ominous: the dark-arc register. Present tense, clinical, the narrator explains what a character is thinking and what is about to happen while their face is still. Slower, colder, longer freezes, the music turns to a low ostinato. For failure modes, adversarial concepts, anything with a body count (deadlocks, cascading failures, attacks, extinction).
- hxh-rules: the game-rules register. Itemized, enumerated, flat: "Rule one. Rule two." Cards, slots, limits. For protocols, APIs, grammars, contracts, consensus rules, anything with a spec.

## Tiers (--tier)
- `principle` (like JJK `technique`): one rule. Beats 1,2,3,5,7,8. Simple concept.
- `ability` (like `domain`): adds beat 4 (condition) and beat 6 (exception). Beats 1-8.
- `vow` (like `full`): everything, with a second title card before the condition beat naming the restriction ("Contract and Vow: ...") and a beat on why the restriction is the source of the power.
Vocabulary: aura = the raw resource/input; the four principles = the primitives every system has (hold, stop, expand, apply); a category = the family the mechanism belongs to (six of them: strengthen, transform, emit, manipulate, conjure, specialize; borrow the idea that a mechanism is strongest in its own family and weaker in a neighbouring one); an ability = the mechanism as a designed thing; a vow = the tradeoff / contract that buys power; a game rule = a constraint the environment enforces.

## script.json shape
Identical to `/explain` plus `"style": "hxh"` at the top level (mandatory; the renderer defaults to `jjk`). Optional `"music"` (see SKILL.md).
```json
{
  "style": "hxh",
  "music": "lecture",
  "topic": "string",
  "slug": "kebab",
  "tier": "principle|ability|vow",
  "register": "hxh-lecture|hxh-ominous|hxh-rules",
  "narrator_voice": "one paragraph of delivery instructions for the TTS (calm, precise, a beat before 'however')",
  "cast": "one paragraph describing the recurring character(s) in the style-lock vocabulary; reused verbatim in every prompt that shows them",
  "scenes": [
    {"id": "s1", "kind": "title", "kanji": "念能力 転輪", "english": "Nen Ability: The Rolling Lobe", "narration": "...", "sound": "single piano note, wind"},
    {"id": "s2", "kind": "shot", "narration": "...", "video_prompt": "...", "sound": "soft piano and strings, quiet wind"}
  ]
}
```
Rules (unchanged from `/explain` unless noted):
- `narration` per scene: 1-3 sentences, 8-30 words. Whole video 115-145 words. The character's release line (beat 8) sits inside a normal narration string in quotes; the TTS reads it in the narrator's voice, so keep it short.
- `kind: title` scenes render locally (cream card + calligraphy + English + glyph), no fal spend. 1-2 per video.
- `video_prompt`: subject + action + setting + camera in the style vocabulary below. Never name real IP, characters, studios, arcs or shows. Do not write "no dialogue, no on-screen text" yourself: the renderer appends it, and doubling it wastes prompt. In diagram shots ask for "clean glowing schematic lines and arrows drawn over the frozen frame" (never words, letters or digits; the model misspells them, so the number is spoken, not written). The renderer prepends the style lock and appends the no-dialogue line and `Sound: <sound>`.
- The renderer swaps the first "the hunter" / "the student" / "the character" / "the user" / "the subject" mention in a prompt for the cast paragraph if the cast is not already present (and prefixes "<cast> is present." when there is no mention at all, so give even a pure diagram shot a hand or a fingertip). Because of the swap, end the cast paragraph on clothing, not a posture, and write "the hands of the student", not "the student's hands".
- `kanji`: Japanese, two space-separated groups, category then name, 2-6 characters each, real words. Categories: 念能力 (Nen ability), 四大行 (the four principles), 制約と誓約 (restriction and vow), 系統 (category), 発 (Hatsu), 規則 (rule), 条件 (condition). Names: what a JP localizer would write, e.g. 念能力 転輪 (rolling wheel), 制約と誓約 一歯 (one tooth), 規則 百枚 (one hundred cards).

## Cast (vary per run; never name the show)
The narrator is off-screen. Show one or two people the narration is about. Keep them in the show's silhouette vocabulary without naming anyone. The first two are the ones the reference stills show (the renderer names them "the boy in green" and "the white-haired boy" in every prompt), so prefer them:
- The student: "a wiry teenage boy with spiky dark hair, bright wide eyes, a sleeveless green jacket over a black shirt, green shorts and boots, standing barefoot on packed earth with both hands raised and a faint glowing white outline of aura around his whole body"
- The second student: "a slim boy with messy white hair, sharp blue eyes, a dark long-sleeved turtleneck and lilac trousers, hands in his pockets, watching with a faint smirk"
- The teacher: "a slim man in his late twenties with neat black hair parted at the side, round wire glasses, a plain white shirt with the sleeves rolled up and dark trousers, calm expression, one hand raised palm-out in demonstration"
- The examiner: "a tall lean man in a dark suit and tie with cropped grey hair and a neutral, appraising expression, arms folded, standing in a bright hall"
Pick or invent one per run; never reuse the previous run's character. Write the aura as "a faint glowing white outline that hugs the body" and, when the diagram beat comes, "clean glowing lines and arrows drawn over the frozen frame".

## Style lock (the renderer prepends this; write prompts that agree with it)
"2D Japanese TV anime from the early 2010s, clean bright hand-drawn cel shading with soft two-tone shadows, thin precise linework, soft painterly watercolor backgrounds, saturated natural daylight palette, large expressive eyes, calm 24fps limited animation, diagrammatic cutaways with glowing outlines and flat hand-drawn schematic overlays, no CGI, no 3D render, no film grain. "
Accents per scene: white-gold aura glow on a daylight scene / pale cyan diagram lines on a darkened freeze frame / warm sepia flashback inset / cold violet-green night for the ominous register / flat cream card with black rule lines for the rules register.
Settings: a sunlit training ground of packed earth with a wooden fence and trees; a plain dojo with tatami and paper windows; a rooftop at dusk over a bright city; a cathedral-sized underground hall for the ominous register; a card table with a green felt surface for the rules register; open grassland under a high sky.
Lighting: bright even daylight, soft shadows, no hard rim light; the freeze frame darkens the background by half and leaves the character lit so the diagram reads.
Camera grammar:
- title: handled locally, no prompt.
- the rule: static medium shot, the teacher or student facing the camera, slight low angle, background soft.
- the demonstration / freeze: the character performs the action, then the frame holds; the camera does not move; glowing outline and schematic lines and arrows appear over the still, drawn in one second; hold.
- the condition: slow push-in on hands or eyes, shallow focus, background falls away to a plain darkened field.
- the number: extreme close-up on the diagram detail; a single glowing mark or ring appears at the moment of the number. Write diagram shots as "flat hand-drawn lines on the frozen frame, like chalk on a board"; "glowing ring" or "schematic" alone drifts the model into glossy 3D CG (seen 2026-09-02 on the first test render).
- the exception ("however"): hard cut to the character's face, eyes widening, the aura flickers, background darkens further; the one moment the frame is allowed a jolt.
- the consequence: wide shot, the world the rule shapes (a factory floor of the machines, a city, a field of players), slow lateral pan.
- the release: the freeze breaks, motion resumes, medium two-shot, the character exhales or grins.
Diagram presets (original): a glowing outline hugging a body (a boundary, a budget); aura pooling in one fist while the rest of the body dims (allocation, concentration); a hexagon of six categories with one lit and its neighbours dimmer (families of mechanisms, similarity decay); a chain from a hand to a target with a lock at the end (a binding, a contract); a countdown ring around a fist (latency, charge time); a ring of pins with a lobed disc inside (gearing, rolling contact); a grid of cards with numbered slots (a table, a registry); a lane of arrows converging to one point (a sure hit, a guarantee).

## Title card (the renderer draws this locally)
The show's schematic panel: warm cream paper (0xF4ECD8), calligraphy in near-black ink (0x1E1E1E) stacked in two groups, English in a burnt-orange accent (0xC8501E) small sans beneath, the glyph 念 in red seal-ink near the bottom, fading in last. No grain, no flicker; the card is a clean diagram panel, not a horror card and not the tea master's parchment.

## Sound line
H3-Max generates native audio. Ask only for ambience and score: "soft piano and strings, quiet wind", "single piano note, then silence", "wind through grass, distant birds", "low string ostinato", "quiet choir pad", "a clock ticking", "paper cards sliding on felt", "a deep gong, then silence", "a faint hum rising", "sudden silence". Always "no dialogue".

## Reference images (on by default)
The style ships six stills (three of the boy in green, three of the white-haired boy; see SKILL.md) and the renderer prepends "Image 1 to Image 3 show the boy in green; Image 4 to Image 6 show the white-haired boy; keep each character's face, hair and clothes consistent with their images" to every shot, so every shot is reference-to-video at $0.08/s. Consequences for the writer: the student in a prompt should be one of those two (the cast list above marks them), refer to them as "the boy in green" / "the white-haired boy" when both are on screen, and describe the teacher or examiner in words if you use them (or add `assets/ref/hxh/wing-*.jpg` per script with `"refs"` + `"ref_owners"` + a `ref_labels` entry). `"refs": []` at the top level or on a scene opts out (text-only, turbo); `"image": "assets/ref/hxh/foo.jpg"` on a scene uses that still as the clip's first frame instead. Still describe the cast in `cast`: the paragraph and the pictures reinforce each other.

## Lean mode (on by default): the narrator is a voice-over
The narration is spoken by the video model in the narrator's voice from `assets/ref/hxh/narrator-voice.wav`, not by TTS, and the prompt tells the model that nobody on screen speaks. So: keep shots at or under 22 words, never write a line that a character visibly says (the beat-8 release line is still read by the narrator), and keep `sound` lines to ambience so the model's own score does not fight the bed.

## Narration is not stage direction (applies to every style)
The spoken line carries the idea: the rule, the condition, the cost, the number, the consequence, or an instruction to the viewer as the student ("Count the pins."). The `video_prompt` carries the action. Never narrate what the camera shows ("he turns the cam", "the disc wobbles", "the frame freezes"): the viewer can see it, and spoken shot description sounds like a prompt being read aloud. Test before rendering: if a narration sentence could be pasted into `video_prompt` unchanged, cut it or turn it into a law ("A cam offset from center cannot spin the disc. It can only make it orbit."). Present-tense description of a character's decision is allowed only in the ominous register and only about intent, never about motion.

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
