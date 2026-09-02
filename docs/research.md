# /explain skill research (2026-09-02)

## The model you meant
- **`minimax/h3-max/text-to-video` and `/image-to-video` on fal.** Post-trained by fal from MiniMax-H3 (Hailuo 3.0). 5-15 s clips, 480p/768p, native stereo audio (SFX, score, lip-synced dialogue in 11 langs incl. EN/JA). ~3 s inference per 5 s clip, ~15 s for 15 s.
- Price: $0.05/s (480p), $0.08/s (768p). Promo $0.0125 / $0.02 per s until ~Sep 7.
- No reference-to-video on H3-Max yet ("coming soon"). Base `minimax/h3/reference-to-video` has it (9 ref images, 3 videos, 3 audio) but runs 3-4 min/clip at $0.06/s 768p.
- Open weights: base H3 yes (33B, 115-134 GB, license excludes US/EU/UK/KR without application). Mac ports exist (MLX, h3.c) at 18 min per 5 s clip on M4 Pro 64 GB. H3-Max is closed. Not worth running locally.
- Hailuo 2.3 Fast = the older silent, I2V-only tier. Ignore.
- Prompting H3: 7000-char prompt, `[Shot 1]`/`[Shot 2]` multi-shot markers, camera tags, trailing `Sound:` clause, quoted lines for dialogue (~2.5 words/s, one speaker per shot).
- Moderation: named film IP is hard-blocked on official API (error 1026). Anime names unverified. Original characters sidestep this.

## Audio
- **Narrator voice**: do NOT clone Yoshiko Sakakibara (JP narrator / Tengen) or Kirk Thornton (EN dub narrator). Kenjiro Tsuda (Nanami's VA) sued TikTok in Nov 2025 over exactly this kind of AI-narration video; ElevenLabs ToS bans it. Use voice DESIGN from a text description instead.
  - ElevenLabs v3: Voice Design + audio tags `[pause] [long pause] [whispers] [deadpan]`; $0.10/1k chars; `with-timestamps` endpoint gives caption alignment. Best delivery.
  - OpenAI gpt-4o-mini-tts: free-text `instructions`, voices onyx/ash; ~$0.015/min; key already set. Zero-setup fallback.
  - MiniMax speech-2.8: Voice Design $3, emotion param, same key as video.
  - Local: Qwen3-TTS VoiceDesign (Apache 2.0, MLX) or Chatterbox (MIT).
- **H3 native audio**: use for ambience/SFX/score per clip, prompt "no dialogue". Narration as a separate TTS track for consistency across clips. Optionally let characters speak one quoted line via H3 (lip-synced) for the in-fight voice beat.
- **Music**: "the delirious anthem" = OST track "Delirious" (Yoshimasa Terui, S2 Hidden Inventory OST, 2:30), the Gojo vs Toji / Hollow Purple cue. Personal use: fine. Publishing: Content ID claim. Original alternative: ElevenLabs Music (licensed, instrumental cinematic). MiniMax Music API closed to new users Aug 20 2026; Music 3.0 weights are open. Udio unusable (no export).

## Alternatives to H3-Max (if anime look disappoints)
- Kling 3.0: best anime pick in shootouts, JP/EN lip-sync, multi-shot storyboard, "Elements" character refs, ~$0.084-0.112/s.
- Seedance 2.5: 30 s multi-shot per call, free audio, 9 ref images, best with line-art refs, ~$0.24/s 720p on Segmind (cheaper on fal).
- Veo 3.1 Fast: $0.10/s, drifts photoreal, needs "cel-shaded, flat colors" prompting.
- Sora 2: API sunsets 2026-09-24. Skip.

## JJK narrator format (script bible)
- JP narrator = Yoshiko Sakakibara (revealed to be Tengen). EN = Kirk Thornton. Narration was reinstated in S2 ep32 because Shibuya techniques got too complex; narrator says what no character can know.
- Segment beats: (1) hard cut to black / dark-red field or slow push-in on face; (2) brush-kanji title card + English sub; (3) DEFINITION "Cursed Technique: X. It allows the user to..."; (4) MECHANISM rule; (5) GUARANTEE (domain sure-hit); (6) COST / CONDITION (CE drain, activation condition, binding vow); (7) WEAKNESS / COUNTER (domain clash "the more refined domain conquers", Simple Domain, Amplification); (8) snap back to action, character finishes the narrator's sentence.
- Alt voices: Gojo playful lecturer; Nanami dry procedural; Sukuna contemptuous connoisseur; Todo bombastic; Mahito philosophical.
- Meme register: deadpan over-glorification over OST, joke domain at the end, "...with the sole exception of Satoru Gojo, of course."
- Anchor quotes: "Manifesting one's innate domain without closing its barrier is akin to painting a masterpiece on air without a canvas." / "Domain Expansion is the pinnacle of jujutsu... any cursed technique activated within it is a guaranteed hit." / "When two domains clash, the more refined domain will conquer." / Jogo: "I can see everything!! ... And because of that, I can't do anything!" / "Infinity exists everywhere." / "Throughout Heaven and Earth, I alone am the honored one." / 0.2 s Void = six months of information. / Nanami Overtime: output 80-90% on the clock, 110-120% after six. / "The greater the restriction, the greater the reward."
- Visual grammar: hand sign (mudra) -> name spoken -> environment swallowed. Sukuna dark red/skulls/open shrine; Gojo galactic void with giant eye, target frozen; Chimera Shadow black liquid floor; Mahito black void with clasped hands. Title typography: brush calligraphy kanji, white on black or black on red, often vertical.
- OST cues: "Domain Expansion" (S2 D2-4), "Delirious", "Malevolent Shrine", "Awaken", "Thunderclap", "Limitless Cursed Technique", "Hollow Purple".

## Concept -> metaphor taxonomy (the "temperature" knob)
- Cursed energy = raw resource/input. Innate technique = core mechanism (one rule). Extension = sub-feature. Reversal = running it backwards / the dual. Maximum technique = same mechanism at its limit. Domain = system level: environment + guarantee + cost + clash rule + counters. Binding vow = the tradeoff/contract ("greater restriction, greater reward"). Heavenly restriction = innate constraint.
- Tiering: simple concept = technique card only; moderate = technique + extension + weakness; complex = full domain + binding-vow closing beat.
- Temperature: randomize (a) which tier, (b) which narrator register (canonical vs Sukuna-contempt vs Nanami-procedural), (c) cast of 3-4 original archetypes.

## Style vocabulary (no IP names)
"dark shonen anime, 2020s MAPPA-style sharp linework, cel shading, heavy black ink shadows, desaturated navy/black palette, electric blue and crimson cursed-energy glow, thin-line character design, dramatic low angle, slow push-in, rim light, floating white brush-calligraphy title on black". Negative: "realism, cgi, 3d render".

## Orchestration (verified docs)
- Skill layout: `~/.claude/skills/explain/SKILL.md` + `reference.md` (bible above) + `scripts/render.py`. Frontmatter: `allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*)`, `argument-hint`, optional `disable-model-invocation`.
- Interactive flow: Claude writes `script.json` (scenes[]: {kind: title|narration|character|domain, narration, visual_prompt, duration, sound}), then runs render.py: TTS -> fal clips in parallel -> title cards via ffmpeg drawtext/ASS -> concat/xfade -> mix with sidechain ducking -> burn captions.
- Headless: `claude --bare -p "/explain TOPIC" --output-format json --json-schema script.schema.json | jq .structured_output`. Structured output validates with retries.
- Long context is not a problem: a 60 s script is ~150 words; the render pipeline lives in a script, not the context.
- ffmpeg recipes (normalize, concat demuxer, xfade chain, sidechaincompress ducking, loudnorm, subtitles) are in the pipeline agent report; copy into render.py.
- Prior art: danielrosehill/Claude-AI-Video-Producer-Plugin, assafkip/claude-video-editor, fal-ai-community/skills (genmedia CLI), MindStudio HyperFrames+ElevenLabs writeup. None do the JJK format.

## Cost / time per 60 s video
- 7 clips x 8 s x $0.08 = $4.50 (768p regular); $1.12 on promo. TTS ~$0.10. Wall time ~1-2 min with parallel fal calls.

## Test dataset
- `eval/cases.json`: 3 real ELI5 asks from the BerkeleyAIHacks session (fold flywheel, nub vs interviewer, dropping the canonical pass). No "Fortnite terms" asks exist in local Claude Code logs.

## Style bible (copy into reference.md)

### Style lock (always include)
"2D Japanese TV anime, dark modern shonen, 2020s prestige studio look, hand-drawn cel shading, flat color fills, thin clean linework with heavy black ink shadow shapes, painterly matte-painting background, film grain, 24fps anime motion, limited animation with smear frames"
Negative: "3D render, CGI, realistic skin, photographic texture, western cartoon, chibi, pastel, oversaturated, soft airbrush shading, motion blur"

### Palette
Base: desaturated navy, charcoal black, cold grey concrete, muted teal-blue night tint.
Accents per scene: electric cyan-blue energy glow (Limitless-type) / deep crimson and black, blood-red rim light (King-of-Curses-type) / sickly violet-black smoke (cursed spirit) / bone-white on black (title cards).
Aura: translucent wisps of dark smoke with a single-color inner glow, energy outlines as jagged ink strokes.

### Lighting
Hard rim light from one side, face half in black shadow, eyes lit as glowing slits, cold fluorescent/streetlight sources, wet-asphalt reflections, Shibuya-like scramble crossing, neon muted to teal and magenta, empty rain-slick streets, cracked concrete.

### Camera grammar
- Explanation beat: static frontal close-up, very slow push-in on the face, shallow focus, background falls to black.
- Technique reveal: dramatic low-angle, wide lens distortion, character small against giant domain interior.
- Impact: whip pan, speed lines, single held frame on impact, debris frozen mid-air, camera shake.
- Domain expansion: hands rise into a mudra, hold, hard cut to black, environment dissolves from the edges inward and is replaced by the domain world, volumetric fog, sudden silence.
- Time-stop: smear frames, duplicated silhouettes, monochrome inverted flash frame on the hit.

### Title cards (do in post with ffmpeg, not in the model)
Black screen, single line of white brush-calligraphy Japanese text, vertical, slight ink bleed, hard cut with a sub-bass hit, English subtitle in tracking-wide sans beneath. Model renders black card with abstract smoke; text overlaid via ffmpeg with a brush font.

### Domain interior presets (original)
- Void sky: boundless dark cosmos, cyan/violet nebula, a single enormous eye-like sphere overhead, target frozen, no ground plane.
- Red shrine: crimson-black open-air altar with animal skulls and horns, torii-like pillars, no dome, white slash-cuts across the frame.
- Shadow tide: ink-black liquid floods the floor, beast silhouettes rise, low reflective horizon.
- Iron furnace: volcanic interior, basalt, magma cracks, ash particles.
- Perfect hands: pure black, giant pale clasped hands opening like a flower, target suspended in the palm.

### Master prompt template
"2D Japanese dark-shonen TV anime, hand-drawn cel shading, thin linework, heavy black ink shadows, desaturated navy-and-charcoal palette with electric blue energy glow, painterly night-city background with wet asphalt reflections, hard one-sided rim light, dramatic low-angle, slow push-in, film grain, 24fps, [SUBJECT + ACTION]. Negative: 3D, CGI, realistic, photographic, chibi, pastel."

## Original cast (JJK-role analogues)
1. THE BLINDED PRODIGY (Gojo-role): tall young man, silver-white spiky hair, dark cloth band over the eyes, high-collared black long coat over black turtleneck, hands in pockets, lazy smile; band off = pale ice-blue eyes with luminous rings; thin cyan glow bending the air. Voice: playful, condescending, explains while yawning. Tag: "the sorcerer born once in several centuries."
2. THE CROWNED PARASITE (Sukuna-role): lean figure in plain grey kimono, bandaged wrists, black tattoo-like lines under the eyes and across cheeks, faint extra eye-marks on the brow, second cruel mouth-shape in shadow, crimson rim light, short rose-pink hair. Voice: bored contempt, judges technique as art. Tag: "a calamity that was never truly sealed."
3. THE CLOCK-OUT VETERAN (Nanami-role): broad-shouldered man in beige suit and spotted tie, blond hair combed back, tinted rectangular glasses, cloth-wrapped blunt blade, sleeves rolled to the same height, under fluorescent office light. Voice: dry, quantitative, percentages and conditions. Tag: "a man who treats slaughter as paperwork."
4. THE VESSEL (Yuji-role): athletic teenager, salmon-pink undercut, hooded black school uniform with red trim, taped knuckles, honest wide eyes, shadow carries a second silhouette, fights barehanded. Voice: blunt, asks the dumb question. Tag: "an ordinary boy carrying the worst thing in the world."
5. THE SHADOW SUMMONER (Megumi-role, optional): black spiky hair, downturned teal eyes, high-collared dark uniform, hands forming shadow-puppet shapes, ink-black hounds rising from his shadow.
Consistency: generate a front/side/45° sheet still per character with the style lock, feed as first frame (H3-Max I2V) or reference (base H3 reference-to-video).
