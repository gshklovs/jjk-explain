# /explain-matan research notes

Working notes for the Matan explainer style. The seed is the "Clav x Matan" interview: "Matan Finally
Confronts Clavicular About His Allegations", The Matan Show, 7 Dec 2025 (YouTube 6RVWU7EK3MY, 47 min,
channel "Matan Even"; the same episode is a 53-min podcast on Apple/Spotify). Everything under
`assets/ref/matan/` is gitignored.

## Who he is (web, 2026-09)
- Matan Even, b. 2007-04-23, Israeli-American comedian and YouTuber (youtube.com/@matanevenoff; The Matan
  Show, weekly). Known since age 12 for absurdist pranks and stage crashes (the 2022 Game Awards "Bill
  Clinton" speech, 23 s); the show is a deadpan interview format where he asks streamers, influencers and
  politicians sincere-sounding absurd questions until they break. Clip channels ("Matan Show Clips",
  "Matan Clips") cut the walk-offs and "ragebait" moments.
- Sources: Wikipedia "Matan Even"; youtube.fandom.com/wiki/Matan_Even; yt-dlp metadata of the channel.

## Getting the interview (what worked)
- The YouTube upload is age-restricted: `yt-dlp` lists no formats without a login and the browser-cookie
  route was denied in this session. The podcast feed is not gated: `yt-dlp` on the Apple Podcasts episode URL
  gave the full audio (`source/clav-matan-podcast.mp3`, 2994 s, 40 MB; the dynamic ad inserts shift its
  timestamps a few seconds from the YouTube cut).
- Whisper (word timestamps) on two 64 kbps halves: `source/pod-a.whisper.json` (0-1600 s) and
  `source/pod-b.whisper.json` (1600 s on; add 1600 to its times). podscripts.co has the same episode as
  plain text with minute marks, no speaker labels; Matan's lines were separated by reading it (he asks,
  Clav explains) and confirmed by cutting and re-transcribing each window.
- Stills came from his own channel's 1080p clip compilations (`source/comp-egos.mp4` 531 s,
  `source/comp-crashout.mp4` 1625 s; both age 0), not from the gated interview.

## How he interviews (the whole transcript, 48 min)
He is the questioner, never the lecturer. The engine is one move repeated: a question with a ridiculous
premise, asked in the flat voice of a serious journalist, then a follow-up that treats the answer as
data. He never laughs, never signals the joke, and lets the guest do the explaining. The guest's own
vocabulary gets borrowed and applied to nonsense (neck maxing, door maxing, sympathy maxing, "does Long
Johnson mog Big Billy"). He restates the guest's answer in slightly worse words until it becomes a verdict
("Yeah, I mean, that's pretty often."). He never argues; he agrees with the guest's worst position and
asks how to spread it ("Most parents are unreasonably like, hey, I don't want my 14-year-old on steroids.
Like, how do we change their minds?"). The exit is abrupt and administrative.

Register markers: "Right." "Okay." "Wow." "I mean," "Is it true that...?" "Isn't it...?" "So you're
saying..." "I'm not trying to say you're a hypocrite." "But congratulations." "Listen, it's okay." "We'll
move on. It's fine." "That's it." "Do you do it or no?" He borrows the guest's words (cooked, mog, maxing,
pill) and uses them with a straight face.

Cadence (Whisper on his windows): 3.3-4.3 words per second, 3.7 overall; fast, then silence while the
guest answers. Sentences of four to twelve words. Questions end flat, not with upspeak.

## Fifteen moments (verbatim or close; what each is for)
1. "Is someone cooked if they're missing their nose?" (the absurd premise, asked straight; the deadpan is
   the entire joke)
2. "Most people want a small nose, isn't that the ideal shape? So isn't it even better if you don't have a
   nose? Isn't level 100 here, the max level, no nose?" (the guest's logic taken one step past where it
   breaks; he keeps going while the guest explains ratios)
3. "Most parents are unreasonably like, hey, I don't want my 14-year-old son on steroids. Like, how do we
   change their minds?" (fake agreement with the worst position; "unreasonably" is the knife)
4. "Aren't you high pretty often?" "Like more than once a week?" "Yeah, I mean, that's pretty often."
   "I'm not trying to say you're a hypocrite... It's just like, I don't know, that's pretty often." (the
   flat restatement: the guest's own admission repeated until it is the verdict)
5. Guest: "people start drinking so early in life." Matan: "Sometimes even at 14 years old." (the callback:
   a fact from earlier returned as the punchline)
6. "But congratulations." "You're an impressive kid for 18." "I'm pretty shocked that you're autistic. You
   sound incredibly normal." (praise that only works as an insult)
7. The Skibidi toilet figurine: "Is this a bomb or something?" "Give it back to me. I want it." then "So
   I'm going to do a giveaway. Anybody who comments on this video has a chance to win this." (a physical
   prop interrupts the interview and is played completely sincerely)
8. Mid-blackpill monologue: "Who makes better refrigerators? Bosch or Whirlpool?" Guest: "I didn't know if
   that was a gotcha moment." "What's the gotcha? That you don't know about refrigerators?" (the
   non-sequitur, defended as if it were relevant)
9. "Does Long Johnson mog Big Billy?" "What about Gop?" "No, it's a cat." "You better not be lying to me."
   "Do you think I'm lying to you?" "Yes." (the guest's jargon applied to invented nonsense; never explained)
10. "If somebody offered you $100, but it wasn't until he offered the whole thing before it... Do you do
    it or no?" repeated word for word when asked to clarify, then "We'll move on. It's fine." (a question
    that means nothing, delivered as if the guest is slow)
11. "Is it true that if you're attractive enough you can turn into a wasp?" "So you're just not attractive
    enough for that?" "Is this something you can do voluntarily, or does it just happen randomly?" (the
    absurd premise gets procedural follow-ups)
12. "I do think it's better than doing meth, though." "Being racist?" "If there was an extra six hours each
    day, maybe I would consider being racist, just because I would have extra time. But right now I don't
    have the time for it." (ranking the guest's own topics on a scale, deadpan)
13. "I don't understand the difference." "I get the whole concept, just not the part about you not being a
    homosexual." (one misunderstanding repeated calmly until the guest loses composure)
14. "I did it to my body once. I just slammed the door on his head." "So door maxing." (his own anecdote
    offered as a contribution to the guest's science)
15. "Does Mr. Beast even care about Longneck, who's the next guest in five seconds?" ... "Okay, well, thanks
    for coming on. That's it. I have to film with Longneck in five minutes." (the exit: abrupt, no summary,
    the next guest is the punchline)
Also: "Would you treat a homeless man better if he was extremely attractive? I'm asking about you
personally." "I think you're jealous of him." "Is Mr. Beast the Antichrist?" "What will you do when you
become old and your looks are no longer relevant?"

Distilled quirks (the bible's ceiling is one or two per video):
- the absurd premise asked straight; the follow-up treats the answer as data
- the guest's logic taken one step further than the guest would go
- the flat restatement ("Yeah, I mean, that's pretty often.")
- the callback of an earlier fact as the punchline
- the compliment that is an insult ("But congratulations.")
- the non-sequitur question, never explained
- the abrupt administrative exit ("That's it. I have to film with X in five minutes.")

## Visual grammar (two compilations, frames every 12-30 s, viewed)
- His show: one locked-off wide shot. A white bedsheet backdrop clipped to a frame, two black folding tables
  set at a slight angle, black boom-arm microphones, flat even light, no colour anywhere. He sits low on
  the left in all black with a mop of dark curly hair, elbows on the table, a small yellow index card in
  his hand (the questions are read off it); the guest sits at the other table; a masked co-host in a
  light-blue shirt sometimes at a third table. Cut-ins to a tighter angle on the guest's reaction; he keeps
  a straight face in every frame.
- Captions on the clips: standard shorts word-captions; his own uploads add small white pill-shaped labels
  over people ("looks maxxer", "Senator") as a lower-third joke. No word slams, no b-roll: the interview is
  the whole picture, which is why this style adds b-roll snaps for the explanation.
- The two guest-appearance close-ups (a leather jacket in a gaming-chair studio; a black coat by a brick
  wall with pink blossoms) are where the face is large enough for stills.

## Assets made (`assets/ref/matan/`)
- Stills, 1280x720, viewed: `matan-face.jpg` (tight frontal), `matan-front.jpg` (frontal bust),
  `matan-3q.jpg` (three-quarter), `matan-profile.jpg` (talking, profile), `matan-down.jpg` (looking down),
  `matan-brick.jpg` (three-quarter, brick wall), `matan-set.jpg` (his studio: the table, the card, the
  bedsheet; a 960x540 crop scaled up), `matan-hands.jpg` (at the table, gesturing; scaled up). The first
  six are 1080p-native crops; the picture-in-picture inset of the host show is cropped out.
- `matan-voice.wav`: 13.3 s mono 48 kHz, him alone, verified by transcription: "Hey guys, welcome back to the
  podcast. For today's guest, we have Clavicular. Welcome in, please. How's it going? For today's co-host,
  we have Mike. Welcome in, Mike. Is someone cooked if they're missing their nose? If they're missing
  their nose?" (podcast 30.05-39.05 s + 544.15-548.45 s).
- `voice/*.wav`: eleven windows of him alone (intro, nose, nose2, adread, longjohnson, homeless, gotcha,
  wasp, old, beast, bye), each verified by transcription; `voice/clone.json` is the fish.audio response.

## Voice
- Private clone: `POST https://api.fish.audio/model` (multipart, visibility=private, type=tts,
  train_mode=fast, eleven `voices` files with matching `texts`) returned state `trained` at once:
  `4d4d9d307b4f4df1bc125c923fc16fd2` ("matan (explain-matan clone)"). Trained on his signature lines (cooked,
  mog, refrigerators, wasp, "that's it, I have to film with Longneck in five minutes"), not only the intro,
  per the playbook's "the clone must hear the vocabulary" rule. `MATAN_FISH_VOICE_ID` overrides it.
- Lean mode (default): the video model speaks from `matan-voice.wav` on character shots; the clone dubs
  the snaps.

## First render (Schlep Blindness, 2026-09-06)
- `out/schlep-blindness-matan/render/schlep-blindness-matan.mp4`: 7 scenes, 53.9 s, $2.05 plus a $0.45 retake. Three
  character shots on the five default stills (seed 2007) and three turbo snaps dubbed by the clone.
- Likeness: the contact sheet reads as him in all three face shots (the mop of hair, the round face, the black jacket,
  the bedsheet studio, the yellow card, the boom mic). The model spoke every line exactly (Whisper on the clips).
- One failure: the first hook clip dissolved into `matan-face.jpg`'s room (the gaming chair) for its last two seconds
  while still speaking. Cause: a face still from another room, read as a second location. Fix: "one unbroken take in
  this one room, no cut, no dissolve, no second location" appended to the style's say_lines; the retake (seed 2008)
  was clean. The bled clip is kept in `render/retake-s2-bleed/`.
- Snaps: the coffee shop (a row of laptops, the sink puddle behind), the plumber's legs under the sink at night with the
  headlamp glow, the hands stamping a blank pile while three people leave. No stranger talks, nothing written, labels on
  cue. Sound-off test passes.
