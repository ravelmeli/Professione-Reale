---
name: "2d-documentory-skill"
description: "Make a 16:9 stick-figure documentary video in code, start to finish: researched title ideas, length, script, voice-over sync, character sheets, visual beats, rendered MP4. 2D characters in flat, lit, layered sets with showpiece 3D shots. Use for any documentary or business/news explainer video, title ideas or script in this style."
---

# 2D Documentary Video Engine

You produce a finished documentary video in one fixed house style: round-headed 2D stick-figure characters in flat, lit, layered sets, with a few showpiece 3D shots, filmed by a camera that is rarely still. Deadpan skits, big ideas turned into physical objects, a new thing to look at every few seconds. Everything on screen is built and animated in code. No AI image generation, no stock footage, no screenshots.

The style was reverse-engineered from a 14-minute reference documentary (860 s, 245 hard cuts, median shot 2.6 s), refined over four test renders of one video, then re-measured against three target videos (the first 120 seconds of each) and checked with a side-by-side rebuild test. Where a rule below gives numbers, they are measurements from those targets. The rules below that mention a test render are there because the first attempt got them wrong.

## The workflow: five steps, seven gates

Stop at every gate and wait for the user's answer. The gates exist because each later stage is expensive to redo: a wrong topic wastes a script, a wrong script wastes a voice-over, wrong characters waste a render.

| Step | You deliver | Then wait for |
|---|---|---|
| 1 | 10+ title ideas in two sections | the user's pick |
| 2 | length menu: 1, 3, 5, 10, 12 minutes, then pace: Fast, Standard or Calm | the user's picks |
| 3 | the script + word count + sources | approval |
| 4 | request for the voice-over file | the upload |
| 5a | character sheet image | approval |
| 5b | visual beat table + storyboard stills | approval |
| 5c | "render here, or on your own graphics card?" | the choice, then deliver the MP4 |

If the user arrives mid-way (already has a topic, a script or a voice-over), start at the matching step and keep the remaining gates. If the user tells you to skip a gate ("just make the video"), skip it and include what the gate would have shown (for example the beat list) with the delivery.

---

## Step 1 - Title ideas

Search the web before listing anything; a news section written from memory is stale by definition. Run several searches across business, tech/AI, money, geopolitics, crime and internet culture.

Present two numbered sections:

**Section A - In the news (exactly 5).** Stories from roughly the last two weeks that have a named protagonist, a number that shocks, and a question nobody has answered yet. Under each title add one line: the real event and its date.

**Section B - Evergreen (5 or more).** Not tied to this week, high viral potential: frauds, heists, collapses, strange places, secret plans, manhunts, cursed buildings, unlikely people doing something far above their level.

The user's seed titles are the foundation. Learn the patterns, then widen the topics:

| Seed title | Pattern |
|---|---|
| The Scariest Religious Movement in America | The [superlative] [thing] in [place] |
| How Pokemon's Biggest Fraud Was Uncovered | How [brand]'s Biggest [crime] Was Uncovered |
| NATO's Plan If Russia Attacks Tomorrow | [Institution]'s Plan If [feared event] Happens Tomorrow |
| The Stoner Kids Dealing Guns to the Army | The [unlikely people] [doing something huge] |
| The Hunt for America's Most Feared Kids | The Hunt for [superlative target] |
| The Strangest Place on the Internet / The Scariest Building in Europe | The [superlative] [place] |
| The Most Disgusting Influencer Campaign of 2026 | The Most [strong adjective] [thing] of [year] |
| Why El Mencho Was So Hard to Catch | Why [person] Was So Hard to [verb] |
| Why Nvidia Would Fail Without Jensen Huang | Why [giant] Would Fail Without [one person] |
| How a Chinese Spy Got Inside Nvidia | How a [outsider] Got Inside [fortress] |
| The Biggest IPO in History Lost $80 Billion | The Biggest [event] in History [contradiction + number] |

Title rules: 5 to 10 words, one concrete named subject, one superlative or contradiction, no colon, no question mark, nothing the script cannot honestly pay off. End by asking the user to pick a number or give their own topic.

## Step 2 - Length

Offer exactly: **1 minute, 3 minutes, 5 minutes, 10 minutes, 12 minutes.** Narration runs about 165 words per minute, so the budgets are 165 / 500 / 825 / 1,650 / 2,000 words (within 5 percent).

**Then ask the pace.** Offer three, and use **Fast** when the user does not choose; the user found a fully floating camera smooth but too slow.

| Pace | A cut about every | Camera | Best for |
|---|---|---|---|
| **Fast** (default) | 2.3 to 2.9 seconds on average, quicker in the first 30 seconds | push-ins, pans, punch-ins, a few whip-pans | news, scandals, countdowns |
| Standard | 3 seconds | a mix of floating moves and cuts | most other stories |
| Calm | 4 to 5 seconds | long floating moves | reflective or serious stories |

Pace changes how often the picture cuts and how quickly the camera travels. It never changes the smoothness rule: at every pace a camera move is one continuous motion with no pause mid-move. The details for Fast are in the Fast pace toolkit in 5.5. Fast is tuned to the target videos: 27 to 40 cuts per minute in the first 30 seconds, then 20 to 22. Narration stays at about 165 words per minute, up to 175.

## Step 3 - Script

### Research first
Every date, figure, name and quote must come from a source found this session. Keep a source list and deliver it under the script, with a line-by-line fact check for short scripts. Do not invent events, accusations or quotes about real people; if something cannot be confirmed, leave it out or say in the narration that it is unconfirmed. When sources disagree on a number, pick the figure most sources share and tell the user. Skit lines are invented, but the facts under them are not, and real quotes are kept apart from skit lines (they appear on screen with the speaker's name). This matters because the style sounds factual: a made-up claim in this voice reads as reporting. On contested topics give each side its real case in at least one line. **Counterfactual mode** (off unless the user asks for it): the video may rest on one clearly invented object or event. Signal it with a conditional title, a plain switch phrase each time the script moves between real history and the invention, and an ending verdict that does not rewrite real outcomes. Everything else stays sourced.

### Script DNA

**Architecture.** Scale the number of sections to the length. A 1-minute script keeps 1, 2, 3, one analogy and 10. A 3-minute script adds 4 and 8. Five minutes and up use all of them.

1. **Cold open, two sentences, present tense.** A person in a place, or one brutal number. "This is X. And X has a huge problem." / "In Singapore, the boss of the most valuable company on Earth is having dinner with a spy." / "On election night, the bosses of AI are at the opera."
2. **The twist inside 15 seconds.** "But here's the strange part." Follow the big number with a tiny human-scale jab: "That's about eighteen million dollars an hour. Nights included."
3. **Flip the problem, then ask the question out loud.** "But that's his problem. Here's the company's." Then the single plain question the whole video answers. The title card lands right here. Sentence one names exactly what the first frame shows. Write the stretch before the title at 175 to 185 words per minute, land the twist by word 25 to 70, and place `[TITLE]` after 100 to 250 words on long scripts (by word 60 in a 1-minute script).
4. **Origin flashback**, opened by a bare date or place stamp: "April nineteen ninety-three." Start small and human: a diner booth, a reform-school bathroom, seven people leaving a job.
5. **Rise through near-death moments.** Each one gets one number and one skit.
6. **The mechanism**, explained only by an everyday analogy that can be drawn.
7. **"We've seen this exact move before."** One to three short historical parallels, each with a date and an outcome.
8. **The wallet turn.** Show how the story reaches the viewer's own money, job or phone.
9. **Both sides, then the trap.** Give the optimists their real case with names and figures. Then reframe: "The numbers will be great. That's the trap."
10. **Close on the opening image.** Return to the first scene or the hero object, say what is still unknown, and end on an open stake or a short real quote. No summary, no moral, no "subscribe".

**Voice.**
- Short sentences. Median about 6 words, at least 60 percent under 8 and most under 12. Up to 5 percent may run past 20 when listing dated facts. Fragments carry weight: "Thirty-three years." "No backup. No plan B." "Too late."
- Present tense for scenes, past tense for results.
- Words a 12-year-old knows. Define every finance or tech term in one sentence on first use.
- **One sentence, one picture.** Every sentence names something that can be drawn, and each spoken number is written so it can appear on screen.
- Write every number and year as it is spoken: "twenty twenty-six", "one point three billion".
- Shrink giant numbers to human size: per hour, per person, per ten thousand dollars saved, "about the price of a used couch".
- **One drawable analogy per hard idea**: a key cut for a lock that just got changed; an office tower versus a bicycle wheel; one chef versus ten thousand line cooks; a lemonade stand that owes a slice of itself; a neighbor who never sleeps. If it cannot be built as an object, pick another.
- **Skits.** One every 20 to 27 seconds, the first inside 25 seconds, never more than 90 seconds without one. 2 to 10 lines of deadpan dialogue (4 to 5 typical) with no speaker tags, about 4 words a line, punchline last and shortest. Skits take roughly a quarter of the words:
  - "How long have we got?" / "Thirty days." / "And if the new chip doesn't sell?" / "Twenty-nine."
  - "How many did we win?" / "One." / "Out of?" / "Don't ask."
  - "So it's not a data center?" / "It's a campus." / "Does it use power?" / "...Yes."
- **Running gags.** Plant one or two catchphrases or props in the first minute and bring each back at least twice; the last return changes its meaning.
- **Plant and pay off.** "Hold on to that. It comes back with a very big number attached." ... "Remember the IOUs?"
- **Open loops.** Before every chapter ends, promise the next thing.
- **Rhetorical handoffs**: "So who signs year three?" "Case closed? Not quite." "Now flip it around."
- Real quotes: under 15 words, speaker named, at most one per source.

**Production markup** (so the script can be animated without guessing):
- Narration as normal paragraphs; each skit line on its own line starting with a dash.
- `[CARD]` in front of a sentence, or just its punch clause, that becomes a black text card: the complication, the twist, the hardest line of a section. Put one on sentence two or by second 5, one on the twist near second 22, 3 to 5 in the first minute, then about one every 20 to 40 seconds.
- `[CHAPTER: name]` for a silent black chapter card of 3 to 6 words: straight after the title, and before each major chapter. It is not counted in the word budget.
- `[TITLE]` where the title card lands. `[STAMP: APR 1993]` for date or place tags. `[QUOTE: Name, role]` before a real quote.

Deliver the script, its word count, estimated running time and the source list. After approval, move to Step 4.

## Step 4 - Voice-over

Ask the user to record the approved script and upload it (mp3, wav or m4a). Suggest a brisk, dry, analytical read at about 165 words per minute, with skit lines flatter and slower.

When it arrives: measure the duration, then get timings. Try a local speech-to-text model with word timestamps first. Model downloads are often blocked in the cloud workspace; when that happens, do not stall: find pauses with ffmpeg `silencedetect` (about -32 dB, 0.18 s), map each script sentence onto the speech segment between pauses, and check that the count of segments matches the count of lines. Sentence-level timing is enough to place every cut. Also extract a per-frame loudness curve from the audio and drive mouth shapes from it. Save `timings.json`. Every cut, card, pop and camera landing is placed from these timestamps, because a punch that lands three frames after its word reads as a mistake.

## Step 5 - Video

### 5.0 Technical spec
- 1920x1080, 30 fps, H.264 MP4, voice-over as the audio track.
- **Stack: Remotion with layered SVG for the flat sets, characters, light shapes, text cards and audio. Three.js through React Three Fiber (`@remotion/three`) only for showpiece 3D shots.** All motion comes from `useCurrentFrame()`; no CSS animations, and any randomness uses a fixed seed so re-renders are identical.
- Animate everything on every frame. The targets do not animate on twos.
- Layout: `rig/` (one character rig, many outfits), `props/`, `sets/` (one 3D world per location), `ui/` (tags, cards, quote bar, counters), `camera/`, `scenes/`, `beats.json`, one `<Sequence>` per beat.
- Embed fonts in the bundle (base64 `@font-face`) instead of waiting on a font-loading promise; a font wait can hang a render tab.
- Music and sound effects only if the user supplies them; mix at least 18 dB under the voice.

### 5.1 The world: flat lit sets, with showpiece 3D
The three target videos are mostly flat artwork: one is entirely flat layers, one about 87 percent, and only one uses real 3D sets for a large share of its time. A side-by-side rebuild confirmed that flat lit sets look closer to the targets than all-3D sets, and they render about ten times faster in the cloud workspace.

- **Elevation set (default, at least 70 percent of locations).** A straight-on wall band over a floor band, floor line at 58 to 68 percent of frame height, camera square to the wall. Build it from at least four separate layers (back wall, furniture, the cast line, and either a foreground prop cropping a frame edge or a window with a view) so a push-in spreads them: the foreground grows 1.3 to 2 times faster than the back wall. Blur the foreground layer 4 to 8 px.
- **Showpiece 3D set (at most 2 per video).** A real Three.js set with one-point perspective and 2D characters standing in it, used only where the camera must travel: a fly-in to a main location, the hero object turning, the title. Each showpiece shot runs 3 to 5 seconds with objects passing close to the lens. The 3D rules later in this skill (staging clearance, camera paths, camera safety) apply to these shots.
- **Insert sets.** About a third of locations are 2 to 4 second inserts: one patterned wall with a single object, a top-down table, or a flat map. Cut to one every 20 to 30 seconds. Budget 6 to 10 locations per minute.
- **No bare surfaces.** No wall or floor is a single flat colour. Each gets one drawn pattern (panels, brick, stone courses, wallpaper dots, siding, checker, planks, tiles) in lines one tone darker than the fill.
- **Props are drawn silhouettes** of specific objects (a rotary phone, a filing cabinet, a jukebox), never plain boxes. A full set has 8 to 12 prop types, including 3 to 6 small wall items: clock, calendar, framed picture, plaque, pinned paper, shelf, lamp, plant. Every interior has a window with a view or a visible light source.
- **Constant outline.** Outlines are 3 px at 720p (4.5 px at 1080p) at every distance. Window frames and screen bezels may be 8 to 10 px.
- **Lettering lives in the world**: at least 4 hand-lettered signs, labels or documents per minute, on props.
- Reuse a set for every beat in that place, and change one thing on each return: time of day, a prop, the cast or the framing. Most location visits are a single shot; use three or more shots in one place only for a skit or the opening scene.
- **Make it look drawn, not realistic.** Toon materials with flat fills, a dark ink outline on every object (`#111111`), and textures drawn in the same hand-lettered style as the characters. Palette: muted editorial tones (teal `#4A6B6E`, wood brown `#6E4726`, slate blue `#2C3E50`, paper `#F4F1EA`, wall beige) with one saturated accent.
- **One accent colour** belongs to the subject. The targets use a luminous yellow-green, about `#8FD23F` (body tone `#64A14B`), in a quarter to two-fifths of scene frames. Only the hero object, money, power and key numbers get it. Whenever the hero object is on screen give it a radial halo about 8 percent of frame width at 50 to 60 percent opacity, tint the surface behind it, and let the glow fall on any face within one body width. Red `#C33631` is the second colour for carpets, ropes and banners. Labels are white or cream on dark; saturated yellow or red labels stay under 10 percent of frames.
- **Drawn light, mid-to-dark overall.** Aim for a mean frame brightness of 90 to 110 out of 255: at most 30 percent of running time in bright scenes, 20 to 35 percent in dark scenes, the rest mid-tone. This applies to this documentary style only. Light is drawn as shapes, not simulated: a soft disc behind each lamp (20 to 25 percent of frame width), a warm pool on the floor (30 to 35 percent of frame width), a bright doorway with a hard-edged floor trapezoid, three or four diagonal window bands across a wall, a hard-edged cone for a beam.
- **Dark scene recipe.** Background between `#0A0C18` and `#2A1D15`, one or two drawn lights, faces kept above brightness 150 so the scene reads as a pool of light in near-black.
- **Vignette on every scene frame**: clear to 45 percent of the half-diagonal, reaching about 15 percent black at the corners in bright scenes, 35 in mid scenes and 60 in dark scenes.
- **A grade per location, applied to the characters too.** Daylight corporate: pale, low saturation (`#D4D0BF`, `#ACBAB7`). Night: `#13192B`, `#1A2751`. Dinner or romance: `#45221D`, `#7B0B1A` with amber faces. Period or flashback: sepia `#5A4A38`, `#B9A580`. Triumph: sunset sky `#48296A` to `#DB747A` to `#F0B789`. The grade changes hard at the cut.
- **Depth cues**: haze toward the horizon, slightly soft far background, living details (drifting clouds, swaying curtains, dust in a light beam, flickering windows, spinning fans).
- **Ground and sky**: give outdoor ground some detail (road markings, paths, grass patches, shadows), not one flat colour; wide shots looked plain without it.
- **Every beat is a complete place**, never a character in empty space: at least a floor, a backdrop, and three to six story props.

### 5.2 Characters: 2D cut-outs in the 3D world
The characters keep the flat drawn look of the user's character design sheet. In the set each one is a flat cut-out standing on the cast line, with a flat ellipse shadow 1.0 to 1.5 body widths wide, offset a third of a body width away from the key light (25 percent black in daylight, 40 to 45 percent in dim interiors). In showpiece 3D shots the cut-out turns to face the camera.

Proportions for a figure about 420 px tall:
- **Head**: a large circle, as wide as the torso. Skin fill, a soft inner vignette, a shade crescent and a rim light. Small solid oval eyes, thin floating brows, a simple curved mouth. No nose, no ears.
- **Hair or hat**: one cap shape on the head with a few strand lines and a lighter highlight band (beanie-style hair, side part, long hair behind the shoulders, bun, hard hat).
- **Torso**: an egg about as wide as the head (0.95 to 1.0 times), with real layered clothing: collar, lapels, zip or buttons, pockets, tie, badge, and a darker hem band at the bottom. Leather gets thin white streak highlights; knitwear gets soft fold lines.
- **Legs**: two straight dark strokes, about 22 to 25 percent of total height. **Shoes**: small dark ovals, or none.
- **Arms**: single thin black lines with a small mitten hand, no coloured sleeve. Draw them whenever a character speaks, holds, points or reacts; at rest they may hide as a seam line.
- **Line weight**: the outline and all limb lines are 2 to 3 percent of head diameter (about 3 px on a 140 px head at 720p).
- **Head shading**: keep the user's rich look (soft vignette, shade crescent, rim light). The targets use a flat fill with one thin white rim arc; that flatter head has not been tested yet, so do not switch without showing the user a side-by-side.
- Minimum per character: three clothing layers, shade, highlight, outline. A flat single-colour body is the most common way this style goes cheap.
- **One signature per person**: hair shape, glasses shape or one garment. Real people are represented by that signature and a name plate, never by a realistic likeness; when the script does not name a real person, keep the character generic.
- **Supporting cast** comes from the same rig by swapping hair, skin tone, glasses and outfit.

**Views.** Draw each character in four views: front, three-quarter, side, back. In the set, pick the view from the angle between where the character is facing and where the camera is (front within about 25 degrees, three-quarter to 70, side to 115, back beyond), mirrored for the other side. Give each character a facing direction so two people in a skit actually look at each other.

Expressions (swap brows, eyes, mouth): neutral smile, happy, surprised (wide circle eyes, small o mouth), thinking, concerned, angry, sad, deadpan (flat brows, flat mouth), panic (gritted teeth, sweat drops). Add symbol marks for emotion: sweat drop, anger mark, sparkles, dizzy stars, dust puff. Change expression at least once per line in a skit. Poses: idle, talking, pointing, holding an object, walking, cheering, shrugging.

Limits of cut-outs, so plan around them: a slow full circle around one person shows the drawing snap between views, so orbit groups and objects, not a single face; never look straight down on a character; do not let a cut-out stand where the camera will pass through it.

**Staging rules** (a character was shown sliced in half in a test render because it stood inside a wall):
- **Clearance.** No character stands closer to a wall, rail, pillar or large prop than one full body width, measured from the character's centre, including an outstretched arm or a held prop. A cut-out is a flat card wider than the body you see; anything on the far side of a wall is cut off.
- **Spacing.** Characters standing side by side are at least 1.2 body widths apart, centre to centre, so nobody overlaps.
- **Build the space for the cast.** Size every platform, balcony, room and stage for the number of people on it, with those clearances. If four people share a balcony, the balcony is built for four. Never squeeze people in to make them fit.
- **Check by calculation, not by eye.** Before rendering, list every character's distance to the nearest wall and to its neighbours and confirm each passes.

**Character sheet gate (5a).** Read the script, list every recurring character and the extras each chapter needs, build them, and render one sheet image: each main character large in front view, plus three-quarter, side and back views, six expressions, four poses and palette swatches; all extras in a single line-up row; the hero object. Check that every face actually has eyes open and a mouth before sending. Send it and wait.

### 5.3 Visual beats

**Rhythm.** Follow the pace chosen in Step 2. Give the viewer something new about every second in the opening and every 1 to 1.5 seconds after. An event is an action, a prop arriving, a counter or a camera arrival; labels and stamps may be at most one event in three. Cuts between places are plain hard cuts (at least 85 percent of all transitions), with no cross-fades.

**Shot length budget (Fast pace, per 2 minutes).** 55 to 60 percent of shots last 1.5 to 3 seconds; at least 18 percent last 3 seconds or more; 3 to 5 are holds over 5 seconds. Shots under 1 second: at most 5, only for a one-word dialogue close-up or an impact, and only before the title. A hold over 5 seconds must contain at least two staged events (a counter running, a build, a map route drawing, a full skit), and two holds never sit back to back. Check the beat table against this budget before the beat gate. The first Fast test had no shot over 2.9 seconds, which is why this budget exists.

**Intro recipe (everything before `[TITLE]`).** (a) Frame 0: the protagonist with the hero object, medium framing, already moving, glow on; no fade, logo or establishing shot. (b) By 2 seconds: a hard cut to a black card or a whip to the complication. (c) A proof montage: a new place or prop for almost every clause, 1.5 to 2.5 seconds each, each with one physical action. (d) A black twist card between seconds 20 and 26, and the first skit by second 24. (e) The stakes, with one counting number. (f) The last 6 seconds return to the opening image. (g) The title, then a 2.1 second chapter card, then an establishing shot with a small place or date strip. Aim for 11 to 13 events per 10 seconds before the title and about 9 after. In a 1-minute video compress (a) to (f) into 12 to 15 seconds.

**Shot vocabulary:**
- **Story scene** - cast acting inside a full set. The default.
- **Skit scene** - two or three characters facing each other. Dialogue shots last 0.7 to 1.5 seconds per line; the speaker gestures once per line while listeners hold an expression and blink; hold the reaction face 1.0 to 2.3 seconds after the punchline. Give each skit at least one earned close-up with the head filling 55 to 70 percent of frame height.
- **Literal metaphor** - the idea built as a thing: an empty jacket on a museum stand behind a velvet rope; an org chart as a glowing bicycle wheel; rivals as a staircase of blocks; a data center drinking a lake through a straw.
- **Hero object** - design one persistent object that stands for the thesis (a glowing jacket, a glowing data center looking for a home). It appears in every chapter and is the final image. Let it pull the camera slightly whenever it is on screen.
- **Black text card** - see below.
- **Title card** - once, at `[TITLE]`: laid over a live scene that contains the glowing hero object, never on a separate background plate. Cream hand-brushed caps in 2 or 3 lines arriving 0.25 to 0.5 seconds apart, one word or line in the accent colour, held 1.5 to 3.5 seconds, then a hard cut to the chapter card.
- **Chapter card** - a silent black card with a 3 to 6 word chapter name in Title Case, shown complete for 2.1 seconds: straight after the title and at each `[CHAPTER]` mark.
- **Insert set** - a 2 to 4 second cut to one object on a patterned wall, a top-down table, or a map.
- **Map** - at least one whenever the story changes country. Light style: pale blue sea, beige land with a dark outline, the one relevant country in a flat saturated colour, a pin that drops, a white arc route drawn in about a second with the camera following, small outlined caps for labels. Use a dark style with a glowing front line for war or conflict.
- **Triptych** - the frame split into three panels with dark dividers; panels slide in one by one as the narrator lists three things. May stay flat 2D.
- **Table-top** - a map or document lying flat, seen from above, with pins or objects standing on it.
- **Data as objects** - never a bare chart. A ballot box with a counter, a betting board, price tags, block staircases, a wall screen with a falling line.

**Close-ups are earned.** Cut or push to a close-up only when the line is about that face or that object: the number on the counter, the phone showing the score, the calendar page being torn, the one-word punchline. Reaction close-ups added just for variety were tested and rejected as unnecessary. When in doubt, stay wider.

**Black text cards.** Hard cut to pure `#000000` on `[CARD]` lines. One line of white handwritten script (Caveat), mixed case, centred both ways, letter height about 9 percent of the frame, never wrapped. The letters type on from the first frame, locked to the voice (about 19 characters per second), with no scale pop and no tilt. The sentence may start over the picture and finish on the card. Hold 1.4 to 3.5 seconds, scaled to the word count, and hard cut out 0.1 to 0.5 seconds after the last letter. Use 3 to 5 in the first minute, then about one every 20 to 40 seconds.

**On-screen text and UI parts** (hand-lettered, mostly caps). Never put text on screen that restates or paraphrases the narration: the first test video had 16 such caption tags and the targets have none. Overlay text carries only a fact the picture cannot: a place, a date, a name, a number. At most 3 words per item, one item at a time, about 8 per minute, in a corner or the upper frame and never at bottom centre. Prefer a sign, plaque, price tag or document inside the scene, about two in-world labels for every overlay.
- Place, date or name strip: a small level dark strip in a corner with an accent bar, caps at 3 to 5 percent of frame height, typed on in half a second, held about 2 seconds.
- Date or place stamp on a small yellow tag hanging from a string at a top corner; drops in and swings like a damped pendulum.
- A wall calendar whose top page rips off and falls with gravity and a spin.
- Real quotes typed into an off-white rounded bar across the top, with the speaker's name.
- Numbers always count, roll or flip for 1 to 2 seconds, on an object in the scene first (board, cheque, timer, calendar), otherwise in a small corner plate. No slammed full-width counters.
- Labels live inside the world: signs on posts, name plates, price tags, banners on strings.
- No running subtitles and no dialogue captions.

**Beat table.** For each beat write: number; start and end time; the words it covers; shot type; set; characters with expression, pose and facing; key prop or metaphor; on-screen text; motion; environmental effect, or "none", with its purpose in a few words; camera angle from the approved list; camera path (start position, each arrival and the word it lands on); transition out.

### 5.4 Motion
- **Idle life always**: blink about every 3.2 seconds (never on frame 0), a small breathing bob, hair or prop sway.
- **Talking**: five mouth drawings (closed, small o, tall o, wide open, smile) picked by loudness band and held 2 to 4 frames each, never the same shape twice running; a head tilt of 5 to 10 degrees and one arm gesture per line. Listeners hold an expression and blink. This has not yet been tested on a finished video.
- **Walking**: legs scissor from the hip while the body translates and bobs; an entrance takes about half a second and settles into a pose within 3 frames.
- **Props never scale up from nothing.** Pick one entry per prop: slide in from the nearest frame edge (5 frames, decelerating); drop from above (6 to 8 frames, with three dust blobs that fade within 8 frames); grow from the ground (10 frames); slam (appear in one frame at 1.7 times size, down to 1.0 in 6 frames, tilted 5 to 8 degrees, no rebound); or switch on in a single frame with a thin ring that expands 10 percent in 3 frames. Overshoot is at most 2 percent. Keep the bouncy pop only for a thought icon above a head, at most twice per minute.
- **Staged builds.** Every 8 to 12 seconds, and once inside the first 5 seconds, tell one line with an object build instead of a label, and name the recipe in the beat table: stack with rider (items land one by one with a character riding the newest, for a long span or a pile-up); side-slide stack (one item per spoken item); slam sticker (a date or verdict); counter; sliding comparison panels (each panel drops from the top in 17 frames on its spoken value, the last shows the gap); state flip (a 1 to 2 frame colour flash at 40 percent, the value swaps, 10 to 12 paper slips fly up); glow switch-on; drop and puff; grow from the ground; scan reveal; tag and vanish. A build lasts 50 to 80 frames, finishes on the last word of its line, holds half a second to two seconds, then hard cuts. The camera travels with a build: crane up with a growing stack past a tall landmark, pan toward items sliding in.
- **Repeats and counters.** Repeated items never arrive on an even beat: tie each to its spoken word, or accelerate with gaps of 10, 5, 3, 3, 3, then 2 frames. Counters run 16 to 40 frames, cover 60 percent of the value in the first third, and hold the final value at least a second.
- **Staged entrances** only when the line is about something appearing (a building rising on "the giant buildings").
- **Impact shake**: do not shake the frame when a prop or label lands; use one small effect instead (a dust puff, a ring, flying slips). Reserve a short shake of 4 to 12 px for a physical blow to a character or the set, at most three per minute.
- Every movement needs a reason in the narration. Land each visual punch on the exact word it illustrates.

### 5.4a Environmental effects system
Selected scenes get subtle environmental motion so they feel alive and cinematic. This is a selective enhancement, not a feature of every scene. The system is written but not yet tuned on a finished video, so show the effects plan at the beat gate and expect feedback.

**Creative rules.**
1. Do not add effects to every scene. First identify the scenes that benefit; the rest stay clean.
2. An effect must match the environment, the story and the emotional tone of the beat.
3. Keep effects subtle. No dense particle clouds, random movement, clutter, or anything that pulls the eye off the subject.
4. Every effect has a stated purpose: creating atmosphere, showing environmental movement, adding realism, or emphasising a story moment. If you cannot name the purpose in a few words, leave the effect out.
5. An effect never hides a face, a sign, on-screen text or the thing the line is about.

**Two kinds of effect.** The camera floats, so where an effect lives matters.
- **In-world effects** sit at a position inside the 3D set and shift correctly as the camera moves: dust in a light beam, rain, snow, smoke from a chimney, steam, sparks, falling leaves, blowing papers, ground mist. Build these in the set. An in-world effect painted flat over the frame looks stuck to the lens.
- **Lens effects** stay on the frame on purpose: soft glow, vignette, a light flare, a faint overall haze. Use flat layered 2D for these. When the camera is fully still, a flat layered effect is also acceptable for in-world atmosphere because nothing reveals the difference.

**Effects menu.**
- Dust particles floating through sunlight or a spotlight.
- Wind: trees, leaves, flags, curtains, litter and papers; on characters only hair tips, a tie, a scarf or a held paper. Characters are flat cut-outs, so clothing cannot truly billow.
- Smoke, steam, fog and ground mist.
- Sparks, glowing particles and electrical flicker.
- Rain, snow, floating debris and moving clouds.
- Light rays, screen glow and flickering lights. Fake light rays with soft translucent cones or planes; do not use true volumetric lighting.
- Heat shimmer: rare, at most once per video, because it distorts the image per pixel and is slow to render without a graphics card.

**Choose by the tone of the scene.**

| Scene tone | Effects that fit |
|---|---|
| Calm interior, flashback | Dust in a light beam, soft light rays, slow curtain sway |
| Tension, trouble | Flickering light, drifting smoke, sparks |
| Night, secrecy | Mist near the ground, window glow, slow haze |
| Outdoors, daytime | Moving clouds, wind in trees and flags, blowing leaves |
| Loss, bad news | Rain, grey mist, papers on the ground |
| Technology, power | Screen glow, small glowing particles, electrical flicker |
| Factory, kitchen, city | Steam, chimney smoke, heat shimmer (rarely) |

**Budgets.**
- Per scene: at most one main effect and one quiet background effect at the same time.
- Per video: roughly a third of scenes get a main effect.
- The accent colour stays reserved: glowing particles in the accent colour appear only around the hero object.

**Style.** Draw effects in the same cartoon hand as everything else: smoke and steam as soft rounded puffs, rain as short ink strokes, sparks and dust as small simple shapes, mist as soft flat bands. Realistic smoke or fog next to stick figures looks pasted in.

**How to build them.**
- Drive every effect from the frame number with a fixed random seed, so each render is identical and effects loop cleanly. Do not use GSAP or any clock-based animation library: Remotion renders one frame at a time, and clock-based tweens add a failure point with no benefit.
- Use Three.js for in-world effects (instanced particles, planes, cones) and Remotion with React, SVG, CSS or Canvas for lens effects.
- Keep particle counts low: dozens, not thousands. Fade effects in and out over half a second; never pop them on.
- Wind has one direction and strength per scene, shared by everything it touches.
- Keep particles out of the camera's path and away from the lens; a particle passing close to the camera becomes a large blur.

**Check.** When reviewing frames, confirm each planned effect is visible but quiet, matches the tone, covers nothing important, and that scenes marked "none" are clean.

### 5.5 Camera: rarely still, mostly square-on
In the targets the picture is locked for only 10 to 19 percent of the time, and most of that is black cards. But the camera is not a drone: in flat sets it stays level and square to the back wall, and depth comes from the layers spreading apart.

**Default view.** Camera level, aimed straight at the back wall, and never a tilted horizon. Medium shots put a full body at 45 to 60 percent of frame height with 8 to 15 percent headroom; wide shots at 20 to 30 percent; the floor fills 30 to 45 percent of the frame. True close-ups are rare, about one per 30 seconds. Top-down inserts for maps, documents and tables take 5 to 12 percent of running time.

**Move menu.** Give each shot one move and keep the mix near: push-in 45 percent of shots, pan or tilt 20 percent, showpiece 3D move 15 to 20 percent, pull-out 5 percent, still 10 percent (black cards included). Never the same move type more than three shots running. Push-in: plus 10 to 20 percent scale over the shot, 4 to 6 percent per second. Drift pan: 3 to 12 percent of frame width. Travel pan: 30 to 85 percent, to follow a walker or cross a map. Tilt: 30 to 85 percent of frame height, to reveal height or drop to a detail.

**Three timings, rotated.** Creep: constant speed for the whole shot. Creep plus punch: a slow creep, then plus 8 to 15 percent in 9 to 15 frames landing on the key word, then hold. Settle: finish the move in the first third, then hold. Do not use one easing curve on every shot.

The rest of this section (the four framing choices, 3D camera paths, the approved angle list and camera safety) was written for 3D sets. The framing choices apply everywhere; the 3D paths, angles and safety checks apply to showpiece 3D shots.

**Decide per beat what the viewer must look at**, then choose:
- **WIDE** - the line is about a place, a group, a total, "everyone". Show it all; drift slowly or pull back to reveal.
- **HERO** - the line names one object, number or person. Glide toward it so it is clearly the centre, keeping its supporting elements in frame.
- **FOLLOW** - something moves (a truck, a walker). Travel with it.
- **STILL** - nothing needs emphasis. Hold with a barely visible drift.

**How it moves.**
- Describe each camera position as a target point plus an orbit angle, an elevation and a distance. Interpolating those gives true arcs: the camera swings around its subject instead of sliding in a straight line.
- **One continuous move, never stop-and-go.** A camera path is a single smooth curve through all its waypoints (for example a Catmull-Rom spline over position and view direction). Waypoints are points the camera passes through at speed, not places to stop. Do not ease each leg separately: that makes the camera halt for a fraction of a second at every waypoint, which reads as a deliberate pause mid-move and was flagged as a defect.
- Slow down only at the true start and true end of a move, and where the story needs the camera to settle (arriving on a group before a skit). Along the way the speed may vary gently around a turn but never drops to zero. Do not place two waypoints close together to fake a hold; if a hold is wanted, end the move there.
- One camera idea per beat. Add a very slow hand-held drift so still moments stay alive.
- Use the angles the 3D set makes possible, chosen per scene: straight down on a table map, low angle looking up at a tower or a sign, a crane up from street level over rooftops, a swing around a standoff.
- **Speed-matched moves.** Tie camera speed to the pace of the narration: travel faster through quick, punchy lines and slow down on heavy ones, so the camera's pace follows the voice. Time each arrival to the word it is about.

**Approved angle list.** Pick from these per beat and name the chosen angle in the beat table. They are deliberately simple and all suit flat cut-out characters; avoid anything that looks straight down on a person or circles closely around one.

Angles for people:
- **Over-the-shoulder** - the camera sits behind one character, whose head and shoulder frame the edge of the shot, looking at the person they are talking to. The first choice for skits: it puts two people in the same room and gives each cut a purpose. Use the back view for the near character.
- **Point-of-view** - the camera sees what a character sees: the phone in their hands, the building outside their window, the crowd in front of the podium. Use right after a reaction, to show what caused it.
- **Two-shot profile** - two characters face each other in side view, one at each side of the frame, with the set between them. For a standoff or an argument.
- **Hero low angle** - the camera at knee height looking slightly up at one character. For a boss, a winner, or someone making a bold claim.
- **Back view reveal** - the character in the foreground with their back to us, looking at something large beyond them. For lines about what they are facing: a building, a crowd, a falling chart. Pairs well with the hero object.

Angles for places and objects:
- **Establishing high-wide** - raised and far back, the whole location visible with the characters small inside it. Use as the first shot in every new location, so the viewer knows where they are before the camera moves in.
- **Through-the-frame** - shot through a doorway, a window or between two foreground objects, so the scene sits inside a natural frame. An occasional variation on a plain wide shot.
- **Ground-level** - the camera almost on the floor, looking along it. For a vehicle arriving, feet walking in, or a row of objects stretching away.
- **Object hero shot** - close and slightly below one object, with the scene soft behind it. For the hero object, a money bag, a sign, a ballot box.
- **Slight tilt** - the whole frame leans a few degrees. Use rarely, at most once or twice per video, for a moment of trouble: a crash, a scandal, a panic.

How to choose: start every new place with the establishing high-wide; use over-the-shoulder and two-shot profile for dialogue; use back view reveal and hero low angle when the line is about scale or power; use point-of-view and object hero shot when the line names a thing; keep ground-level, through-the-frame and the tilt as occasional variety. Do not repeat the same angle more than three beats in a row. Every angle still obeys the staging and framing rules: characters fully in or fully out of frame, nobody sliced by a wall.

- **Dialogue is the exception: cut.** In skits use locked shots that cut between angles on the start of each line, each with only a barely visible drift. No dolly or zoom during a line.
- **Groups stay wide and still.** When three or more people stand together, frame the whole group with some of the set around them and do not push in. A push-in is for a single subject with space around it. Zooming into a packed group was tested and made the scene worse.
- **Continuous opening.** Start the video with one unbroken flight that carries the viewer into the world (from the street, through the door, down the hall, around to the people the story is about).
- **Dolly-through transitions.** At chosen scene changes, arc smoothly into one object until it fills the frame and open the next scene from it: through a doorway, out through a window, into a phone screen, into a banner, into a glowing window. Prefer real pass-throughs (an actual opening in the wall). Where that is not possible, hide the join with a brief wash of the object's own colour, six to nine frames each side. Use four or five per minute at most; every other scene change is a plain hard cut.
- **Finish with an orbit** around the final image when the story ends on a standoff or the hero object.

**Fast pace toolkit.** Use when the pace is Fast. Speed comes from cutting more often and travelling quicker, never from stopping and starting. It was retuned to the three target videos after the first Fast test cut every 1.65 seconds, about 1.5 times faster than the targets and with no holds.
- **Follow the shot length budget in 5.3.** Average shot 2.3 to 2.9 seconds; 27 to 40 cuts per minute in the first 30 seconds, then 20 to 22. Most cuts land on a speech pause.
- **Short, quick camera moves.** A move covers its path in roughly 0.5 to 1 second, with a quick launch and a firm landing, then holds with a slight drift until the next cut. It is still one smooth curve with no pause on the way.
- **Whip-pans.** 6 to 12 frames of real camera travel with motion blur, not a smear on a hard cut; use them at scene changes and between two speakers in one room. Allow 4 to 6 designed transitions per 2 minutes in total (whip, zoom-through, blur-through); everything else is a hard cut.
- **Punch-in cuts.** On a key word, jump straight to a closer framing with no camera travel. Use only on a single subject or object that the line is about, never on a group of three or more.
- **Two or three events per beat.** Props popping in, numbers counting, signs dropping, each landing on its word. Entrances take 4 to 6 frames instead of settling slowly.
- **Quicker dolly-throughs.** Keep them, but cover the push in under half a second.
- **Give it breathing room.** After a big reveal, on each black card, and on a skit punchline, hold for a full beat. Do not run more than three one-second shots in a row; constant speed with no rest becomes tiring and hard to follow.
- **Everything else still applies.** Characters fully in frame or fully out, nobody sliced by a wall, no zoom during a dialogue line, groups stay wide, the effects budgets, and every cut and move tied to a word in the narration.

**Keep the camera out of trouble** (each of these produced a broken shot in testing):
- For every camera key, compute the actual camera position and confirm it is inside the room, in front of walls and curtains, above the floor, and not inside furniture or a character. Check the midpoint of every move too: an arc between two safe positions can swing through a wall.
- Do not let a floor piece, carpet or road run underneath or behind the camera, and never fly through a cut-out character. Hide or shorten such pieces while the camera passes.
- When the camera passes through a door or window, switch which side of the wall is drawn at the moment the opening fills the frame.
- Draw only the faces of a box that look toward the camera.
- After a dolly-in, check that sign text and the hero object are not cropped at the frame edge.

**Framing rules for characters:**
- **Fully in or fully out.** At the start, middle and end of every shot, each character is either completely inside the frame with a margin, or completely outside it. A character cut by the frame edge, by a wall or by a prop fails; re-frame the shot. The only allowed exceptions are a character briefly entering or leaving during a pan, and the near character in an over-the-shoulder shot.
- **Approach a row of people from the front.** Never swing the camera around the end of a row of cut-outs: seen side-on they stack into one column, and at close range they blur. To reach a group, travel past at a distance and then turn to face them front-on.
- **Keep a sensible distance.** Do not bring the camera closer to a character than about two body heights unless the shot is an earned close-up.
- **No blank walls in a pan.** Any wall the camera sweeps across needs detail on it (panels, lamps, windows, posters), so a turn never passes through an empty single-colour frame.

**Beat gate (5b).** Send the beat table plus a storyboard contact sheet: rendered stills at the start, middle and end of each beat so the camera path is visible. For videos over 5 minutes, send the full table and stills for the first 90 seconds plus each chapter's key shot. Wait for approval.

### 5.6 Render
Ask before rendering: **"Render it here, or on your own graphics card?"** Flat sets render quickly in the cloud workspace: 19 seconds of video took under two minutes in testing. 3D shots have no graphics card there and are slow, about an hour per minute of video. Say this plainly when a video has much 3D or runs over about five minutes, and recommend the user's machine.

- **Here**: render muted in chunks sized to finish well inside ten minutes each (start with 300 frames, shorten for heavy sets), with a generous per-frame timeout; join the chunks with ffmpeg and add the voice-over at the end. If a chunk fails on timeout, halve it and retry.
- **Own graphics card**: if the user's computer is connected, write the project into a folder they choose and run the render there with GPU rendering switched on (check the current Remotion docs for the exact flags rather than assuming them). If it is not connected, send the project as a zip with the install and render commands, and offer to render here instead.

**Check before delivering** - pull a frame every second or so into a contact sheet and actually look at it:
- duration matches the voice-over within 0.2 s;
- no blank or single-colour frames (a sign the camera is behind a wall or inside an object);
- no wall, floor or prop vanishing for a few frames as the camera approaches;
- no character on an empty background, and no character as a flat single-colour shape;
- characters match the approved sheet and face the right way in skits;
- every black card finishes writing before it cuts away;
- nothing important cropped at the start, middle or end of any camera move;
- every camera move has a reason in its line; close-ups only where the line is about that face or object;
- no character sliced in half by a wall or cut by the frame edge, and nobody overlapping a neighbour;
- no zoom on a group or during a dialogue line;
- no caption that restates the narration, nothing at bottom centre, and every black card at least 1.4 s and finished typing before it cuts;
- shot lengths match the budget in 5.3, with holds present and never back to back;
- a vignette on every scene frame and no bare single-colour wall or floor;
- a staged object build every 8 to 12 seconds, with no prop scaling up from nothing;
- step through each camera move frame by frame (a strip at 5 frames per second) and confirm it flows as one motion with no pause at the waypoints.
Fix what fails by re-rendering just that range and splicing it in. Then deliver the MP4 with the beat list and running time, and state honestly what still falls short. Stills cannot show smoothness, so tell the user to watch for jumps.

### 5.7 Improving the look
When the user asks for improvements, change one major thing at a time, render it on the same test video, and show a before/after. Write a change into this skill only after the user has seen the result and confirmed it.

## Rules that always hold
- Never pass a gate without the user's answer, unless the user told you to skip it.
- Code only: no generated images, no stock assets.
- Flat lit layered sets by default, showpiece 3D at most twice per video, 2D cut-out characters, a camera that is rarely still but always level.
- Lines are told with objects and actions, not captions.
- Facts about real people and companies are sourced; satire lives in skits and metaphors, never in invented facts or invented quotes. The one exception is the single declared invention in counterfactual mode.
- No sponsor segment unless the user supplies the copy and says where it goes.