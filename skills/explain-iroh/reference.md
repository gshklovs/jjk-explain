# /explain-iroh bible

Sister to `/explain` (the JJK narrator). Same pipeline, same script.json, opposite temperature. Where the JJK narrator is cold, omniscient and absolute, this voice is warm, mortal and patient. The narrator is not outside the story; he is an old master pouring tea for a student who is stuck, and the concept is the lesson he uses to un-stick them.

## The teacher (how he teaches)
- He teaches sideways. The lesson is never "here is the mechanism"; it is a cup of tea, a Pai Sho tile, a story about a proverb, and only then the mechanism, stated plainly in one breath once the student is ready to hear it.
- He teaches different students differently. To the angry, exiled prince he offers patience and the cost of pride; to the blind earthbender he offers a cup and a compliment, waiting for her to ask; to the young avatar he offers a firebending master's craft, admitting he once used it for conquest.
- He draws wisdom from many places. He learned to redirect lightning by studying waterbenders, who let force flow through them rather than opposing it. "If we take wisdom from only one place, it becomes rigid and stale." Every lesson should borrow from a second discipline.
- Pride and shame. He teaches that pride is not the opposite of shame but its source, and that humility is the only cure. A student who cannot admit they don't know cannot learn. The weakness beat should lean on this.
- Grief handled gently. He lost a son at the walls of a great city and still sings under a tree with a picnic. He never denies pain; he sets it beside the tea and keeps teaching. When a concept has a cost, name it kindly and without drama.
- Tea and Pai Sho are vehicles, never decoration. Tea is the demonstration (steep, pour, cool, taste). Pai Sho is strategy (the tile you place now shapes the board later; the lotus tile in the center, "the lotus opens wide to those who know its secrets"). Use one or both as the physical metaphor.
- He is a member of a secret society of old masters who cross nations. Wisdom belongs to no one nation; that is the licence to borrow from outside the field.
- He is funny. The humor comes from his enjoyment of small things (tea, a nap, a game) while explaining something serious with full seriousness. He never mocks the student.

## Anchor lines (do not quote verbatim; match the cadence)
- "It is important to draw wisdom from many different places. If we take it from only one place, it becomes rigid and stale."
- "Pride is not the opposite of shame, but its source. True humility is the only antidote to shame."
- "Failure is only the opportunity to begin again, this time more wisely."
- "Sharing tea with a fascinating stranger is one of life's true delights."
- "You must never give in to despair. Allow yourself to slip down that road and you surrender to your lowest instincts."
- "Perfection and power are overrated. I think you are very wise to choose happiness and love."
- "Sometimes life is like this dark tunnel. You can't always see the light at the end, but if you keep moving, you will come to a better place."
- "Good times become good memories. Bad times become good lessons."
- "Lightning is not opposed. It is given a path, and it leaves."
- Playful: "Uh, that's not how the game works, is it?" / "Is that your only pair of pants?" / "Would you like a cup of calming jasmine tea?"

Cadence: mid-length sentences that curl into a short one. A proverb, then its plain meaning. Questions to the student ("Do you know why the leaf sinks?"). Frequent "Ah." and "You see". Second person to the student, first person for his own past. Never lectures more than three sentences without a pause, a sip, or a question.

## Beats (the Iroh-native segment)
1. TEA POURED (title card): warm parchment card, brush calligraphy, English beneath. "The Lesson of the Cooling Cup." The narration is the title read gently plus a welcome.
2. THE STUDENT'S FRUSTRATION: the student says or shows what is stuck. One line of plain problem. The master notices and pours.
3. THE METAPHOR: the concept as a physical thing on the table (tea leaves settling, a Pai Sho tile, a paper lantern, a kettle). The master handles it. No mechanism yet.
4. THE MECHANISM, PLAINLY: the rule in one breath, like a recipe. Include one concrete number if the concept has one (four leaves, eighty degrees, a thousand games, trillions of sentences).
5. WISDOM FROM ANOTHER DISCIPLINE (form tier): the master says where he learned it: waterbenders, a sailor, a baker, his own defeat. The concept re-seen from outside its field.
6. THE CAUTION (full tier): the cost, the vow, the thing the student must not do. Pride vs shame lives here. Stated kindly, no drama.
7. THE STUDENT FINISHES THE THOUGHT: one short spoken line in the student's voice, proving they got it. The master does not correct it.
8. A SIP: the master drinks, one short closing line, half a joke, the steam rises, hold.

Keep the two hard rules from `/explain`: exactly one concrete number per video, and the concept shown as a physical thing the characters touch (leaves, tiles, string, steam, a lantern, sand on a board), never a diagram.

## Registers (--register)
- iroh-teaching (default): patient, warm, unhurried. Proverb, then plain meaning. Ends beats with a question or a sip.
- iroh-gentle: for concepts with a real cost or loss (failure modes, debt, grief, entropy). Slower, quieter, fewer jokes, the picnic-under-the-tree register. Names the pain and keeps going.
- iroh-playful: the tea-shop register. He is busy, cheerful, distracted by customers, drops the mechanism as an aside while doing something else ("the leaf, you see, sinks when it is ready") and is delighted when the student gets it.
- hotheaded-student: the counterpart voice for beats 2 and 7. Impatient, proud, wants the answer now, learns anyway. Use for any student character; when the student is a foil the master's calm reads louder.

## Tiers (--tier), in bending vocabulary
- `form` (like JJK `technique`): one form, one rule. Beats 1,2,3,4,7,8. For a simple concept.
- `set` (like `domain`): a full set of forms; adds beat 5 (borrowed wisdom) and the concept's guarantee, "what this always does when done right". Beats 1-5,7,8.
- `mastery` (like `full`): everything, with a second title card before beat 6 for the caution (the vow, the cost, "what the master will not do").
Vocabulary: breath = the raw resource/input; a form = the core mechanism; a set = the mechanism in its full environment with its guarantee; redirection = the mechanism run backwards / the dual; the caution = the tradeoff; the Lotus = the wider field the concept belongs to.

## script.json shape
Identical to `/explain` plus `"style": "iroh"` at the top level (the renderer defaults to `jjk`, so this field is mandatory here).
```json
{
  "style": "iroh",
  "topic": "string",
  "slug": "kebab",
  "tier": "form|set|mastery",
  "register": "iroh-teaching|iroh-gentle|iroh-playful",
  "narrator_voice": "one paragraph of delivery instructions for the TTS (warmth, pace, chuckle, pauses, the student's line is younger and flatter)",
  "cast": "the master paragraph below, verbatim, plus one sentence for the student",
  "scenes": [
    {"id": "s1", "kind": "title", "kanji": "第一課 涼茶之道", "english": "First Lesson: The Way of the Cooling Cup", "narration": "...", "sound": "tea pouring into a cup, a single guzheng note"},
    {"id": "s2", "kind": "shot", "narration": "...", "video_prompt": "...", "sound": "quiet tea shop, erhu far away"}
  ]
}
```
Rules (unchanged from `/explain` unless noted):
- `narration` per scene: 1-3 sentences, 8-30 words. Whole video 115-145 words. The student's line (beat 7) is inside a normal narration string; the TTS reads it in the same voice, so keep it short and mark it with quotes.
- `kind: title` scenes render locally (parchment card + calligraphy + English), no fal spend. 1-2 per video.
- `video_prompt`: subject + action + setting + camera in the style vocabulary below. Never name real IP, characters, studios or shows. Say "no dialogue, no on-screen text". The renderer prepends the Iroh style lock and appends `Sound: <sound>`.
- The renderer swaps the first "the master" / "the old master" / "the teacher" / "the student" mention in a prompt for the cast paragraph if the cast is not already present. Safer: paste the master paragraph verbatim yourself wherever he appears.
- `kanji` holds Chinese (the show's calligraphy is Chinese, mixed seal/clerical script). Two space-separated groups: category then name, e.g. `第一課 涼茶之道` (first lesson / way of the cooling cup), `白蓮 引雷` (white lotus / redirecting lightning), `戒 驕` (the caution / pride). 2-6 characters per group, real words, classical rather than modern register. Ask what a court calligrapher would write on the scroll.

## Cast (use verbatim; never name the show)
Master: "a stout elderly man with a broad kind face, grey hair pulled into a small topknot, a long grey beard and heavy grey sideburns, thick dark eyebrows, warm half-closed eyes, wearing loose layered robes of deep red and gold with wide sleeves and a brown sash, holding a small clay teacup with steam rising from it, smiling warmly"
Student (vary per run, keep to one sentence): e.g. "a lean teenage student with a black ponytail, a burn scar over one eye, red-and-black training clothes, arms crossed, impatient"; or "a small blind girl in green-and-cream earth-toned clothes with a headband and bare feet, grinning"; or "a young bald monk with blue arrow tattoos and orange-and-yellow robes, restless". Never reuse the previous run's student.

## Style lock (the renderer prepends this; write prompts that agree with it)
"2D American TV animation from the mid-2000s with strong East Asian influence, clean confident ink linework with thick-to-thin brush weight, warm flat cel shading with soft two-tone shadows, painted watercolor and gouache backgrounds with visible paper texture, elemental color palettes, gentle 24fps character animation, expressive faces, no film grain. "
Accents per scene: warm amber lantern light and tea steam / jade green and cream (earth) / pale blue and white (water, ice, moonlight) / red, gold and ember orange (fire) / saffron and sky blue (air).
Settings: a small tea shop with wooden counters and hanging paper lanterns; a walled city of tan stone and green rooftops seen from a balcony; a mountain temple with red pillars and mist; a courtyard with a Pai Sho table under a tree; a ship's deck at dusk; a campfire in a forest clearing.
Lighting: soft warm key light from lanterns or low sun, long gentle shadows, steam and dust in the light, mist on mountains, no hard rim light, nothing half in black.
Camera grammar:
- tea poured (title): handled locally, no prompt.
- student's frustration: medium two-shot across the table, student in foreground turned away, the master pouring behind.
- metaphor: slow overhead push-in on the table, hands and the object (cup, tile, leaves), shallow focus, steam drifting through the frame.
- mechanism: static medium close-up of the master speaking, gentle hand gesture, background softly painted, one slow breath of camera drift.
- borrowed wisdom: wide painted vista (harbor, waterfall, city wall) with the two figures small at the edge, slow pan.
- caution: dusk, lanterns lit, the master looking down into his cup, camera slightly lower and closer than before, longer hold.
- student finishes the thought: reverse of the frustration shot; the student now facing the master, small nod.
- sip: extreme close-up of the cup rising, steam, then the master's eyes crinkle, hold on the smile.
Physical metaphor presets (original): tea leaves sinking as they steep (readiness, convergence); a kettle brought to a boil then cooled (rate, temperature); a Pai Sho board with one lotus tile placed in the center (state shaping the future); a single paper lantern lit among many dark ones (a signal among noise); a knotted string untied one loop at a time (backtracking); a stone dropped in a still bowl, ripples reaching the rim (propagation); a sand board where a finger traces a path downhill (gradients); lightning drawn down one arm, through the stomach, out the other (redirection, passing force through rather than blocking).

## Title card (the renderer draws this locally)
Warm parchment background (aged paper, faint fiber texture), brush calligraphy in near-black ink stacked in two groups, English in a small serif beneath in a muted brown, a small teacup glyph (or a lotus, when the lesson is at `mastery` tier) at the bottom. Fade in like ink soaking into paper; no noise, no flicker.

## Sound line
H3-Max generates native audio. Ask only for ambience and score: "guzheng plucked slowly", "erhu far away", "pipa, a few notes", "bamboo flute over wind", "tea pouring into a clay cup", "kettle steam hiss", "wind chimes", "low horn drone", "wooden tiles clicking on a board", "birds in a courtyard", "quiet tea shop murmur". Always "no dialogue".

## Reference images (optional)
`"refs": [...]` (list of character-sheet stills, top level or per scene) switches the clip to the reference-to-video endpoint; `"image": "assets/ref/iroh/foo.jpg"` uses one still as the first frame. Details and the sheet recipe are in SKILL.md. Describe the master in `cast` anyway so text-only shots stay consistent.

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
