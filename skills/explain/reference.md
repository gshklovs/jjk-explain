# /explain bible

## The format (JJK narrator explaining a technique)
The anime narrator (revealed to be Tengen) explains things no character could know, in a calm, absolute, slightly reverent register. Sentences are short declaratives. No hedging, no jokes from the narrator itself; the humor comes from applying the register to a mundane concept with total seriousness.

Beats of a segment, in order:
1. TITLE CARD: hard cut to black. Kanji, English beneath. "Cursed Technique: X."
2. DEFINITION: one sentence. "It allows the user to ..."
3. MECHANISM: the rule, stated like physics. Include one concrete number if the concept has one.
4. GUARANTEE (domain tier): "Within the barrier, ... is a sure hit."
5. COST / CONDITION: what it consumes, what must be true to activate.
6. BINDING VOW (full tier): the tradeoff. "The greater the restriction, the greater the reward."
7. WEAKNESS / COUNTER: the crack. Domain clash rule: "the more refined domain conquers."
8. SNAP BACK: a character finishes the narrator's thought in one short spoken line.

Anchor lines (do not quote verbatim, match the cadence):
- "Manifesting one's innate domain without closing its barrier is akin to painting a masterpiece on air without a canvas."
- "Domain Expansion is the pinnacle of jujutsu. Any technique activated within it is a guaranteed hit."
- "When two domains clash, the more refined domain will conquer."
- "I can see everything. And because of that, I can do nothing."
- "Infinity exists everywhere."
- "The greater the restriction, the greater the reward."
- Nanami: "From here on, it's overtime." Output rises from eighty percent to one hundred twenty.

## Registers (--register)
- narrator (default): omniscient, solemn, reverent. Third person. Ends beats on a full stop.
- sukuna: contemptuous connoisseur explaining the opponent's technique to mock it, then admiring one detail. First person, addresses "you".
- nanami: dry, procedural, quantitative. States thresholds and conditions like an HR policy. Deadpan.
- gojo: playful lecturer, condescending, explains while bored, "you get it? no? that's fine."

## Taxonomy (--tier)
- Cursed energy = the raw resource/input.
- Innate technique = the core mechanism. One rule.
- Extension technique = a sub-feature / variant.
- Reversal = the mechanism run backwards / the dual.
- Maximum technique = the mechanism at its limit.
- Domain expansion = system level: environment + guarantee + cost + clash rule + counters.
- Binding vow = the tradeoff / contract / constraint that buys power.
Tiers: `technique` = beats 1,2,3,7,8 (simple concept). `domain` = adds 4,5. `full` = all beats, with a second title card for the domain.

## script.json shape
```json
{
  "topic": "string",
  "slug": "kebab",
  "tier": "technique|domain|full",
  "register": "narrator|sukuna|nanami|gojo",
  "narrator_voice": "one paragraph of delivery instructions for the TTS (pace, gravity, pauses)",
  "cast": "one paragraph describing the recurring character(s) in the style-lock vocabulary; reused verbatim in every prompt that shows them",
  "scenes": [
    {"id": "s1", "kind": "title", "kanji": "領域展開", "english": "Domain Expansion: Wheel of Correction", "narration": "...", "sound": "sub-bass hit, silence"},
    {"id": "s2", "kind": "shot", "narration": "...", "video_prompt": "...", "sound": "low ominous drone, distant wind"}
  ]
}
```
Rules:
- `narration` per scene: 1-3 sentences, 8-30 words (30 words is ~13 s of narration; clips max out at 15 s). Whole video 115-145 words.
- `kind: title` scenes render locally (black card + kanji + english), no fal spend. Use 1-2 per video.
- `video_prompt`: subject + action + setting + camera, in the style vocabulary below. Never name real IP, characters, studios or shows. Say "no dialogue, no on-screen text". The renderer prepends the style lock and appends `Sound: <sound>`.
- Use the cast paragraph verbatim whenever the character appears. When the concept is abstract, show the concept as a physical thing in the world (threads, brackets, a wheel, a barrier) that the character interacts with.
- Kanji: 2-6 characters, real words. Ask yourself what a JP localizer would call it. Examples: 術式 (technique), 領域展開 (domain expansion), 縛り (binding vow), 反転術式 (reverse technique), 極ノ番 (maximum technique).

## Style lock (the renderer prepends this; write prompts that agree with it)
"2D Japanese TV anime, dark modern shonen, 2020s prestige studio look, hand-drawn cel shading, flat color fills, thin clean linework with heavy black ink shadow shapes, painterly matte-painting background, desaturated navy and charcoal palette, film grain, 24fps anime motion, limited animation with smear frames."
Accents per scene: electric cyan-blue energy glow / deep crimson and black with blood-red rim light / sickly violet-black smoke / bone-white on black.
Lighting: hard one-sided rim light, face half in black shadow, cold fluorescent or streetlight, wet-asphalt reflections, empty rain-slick night streets, cracked concrete.
Camera grammar:
- explanation beat: static frontal close-up, very slow push-in, shallow focus, background falls to black.
- reveal: dramatic low angle, wide lens, character small against a giant interior.
- impact: whip pan, speed lines, one held frame, debris frozen mid-air.
- domain expansion: hands rise into a mudra, hold, hard cut to black, the environment dissolves from the edges inward and is replaced by the domain world, volumetric fog, sudden silence.
Domain interior presets (original): void sky (dark cosmos, cyan/violet nebula, one enormous eye-like sphere overhead, no ground); red shrine (crimson-black open-air altar, skulls, torii-like pillars, white slash-cuts); shadow tide (ink-black liquid floor, beast silhouettes rising); iron furnace (basalt, magma cracks, ash); perfect hands (pure black, giant pale clasped hands opening like a flower).

## Sound line
H3-Max generates native audio. Ask only for ambience and score: "low ominous drone", "sub-bass hit then silence", "distant rain on concrete", "taiko hit", "string ostinato rising", "sudden silence". Always "no dialogue".

## Reference images (optional)
`"image": "assets/ref/foo.jpg"` on a scene (or at script top level for all shots) uses that picture as the clip's first frame via image-to-video. Use it on 2-3 character shots, not every shot, or every clip opens on the same pose. Paths are relative to the workspace root. Prepare the image as 16:9 (1280x720) with the subject isolated; the video follows the image's aspect ratio. Describe the subject in `cast` anyway so text-only shots stay consistent.
`"refs": ["assets/ref/a.jpg", ...]` (top level or per scene, up to 9) sends a character sheet to `minimax/h3-max/reference-to-video` instead; the renderer tells the model that Image 1..N are the same character. Add a top-level `"seed"` to keep the look stable across shots. `refs` wins over `image`.

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
