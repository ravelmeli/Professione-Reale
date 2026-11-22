---
name: professione-reale-style
description: House visual style for the "Professione Reale" channel (La tua vita a ogni livello come [professione]). Use whenever making, planning or reviewing a video/short for this channel: it applies the 2D documentary skill (layered flat lit sets, egg-torso cut-out characters, no running captions) adapted to the channel's standing rules.
---
# Professione Reale — style

1. Read `docs/stile-professione-reale.md` (adaptations, conflicts, engine status) AND `docs/2d-documentary-skill-ORIGINAL.md` (the exact original rules: sections 5.0–5.7 and "Rules that always hold"). Apply every rule of the original; where the adaptation file says otherwise, the adaptation wins.
2. Channel rules that always win: never invent figures; state lordo/netto; flag uncertain numbers; Italian narration/signs; long = 16:9, shorts = 9:16; long scripts have 3 subscribe CTAs (start, ~2/3 before the last level, end with comment question + "which profession next"), spoken AND shown on screen — the original skill's "no subscribe" ban is lifted by the user; a unique cast and hero object per profession; one accent colour per profession.
3. No running subtitles. Numbers/places/names go on in-world signs, name plates, stamps, black cards.
4. Keep the gates: character sheet (5a), beat table + stills (5b, first 90 s + one key shot per level for long videos), render choice (5c). The user records the voice; align with Whisper + script, cut duplicated takes.
5. Engine: Remotion + SVG layers + `@remotion/three` for ≤ 2 showpiece 3D shots, project in `remotion/` (Chromium at /opt/pw-browsers/chromium, GL swangle; see remotion/remotion.config.ts). Visual reference prototype: `growkaz-stickman-studio/projects/docproto/scenes/_doc.js`. Check the "À construire" list in the adaptation file before rendering and build the missing parts; verify with a contact sheet and the 5.6 checklist before delivering.
