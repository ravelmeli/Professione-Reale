import { E, V, registerShot, mood, layer, blurLayer, veil, ease, prog, text, FONTS, alpha, clamp } from '/engine/core.js';
import { drawFigure, POSES, posesAt, breathe, bigFace } from '/engine/rig2d.js';
import * as FX from '/engine/fx2d.js';
import * as UI from '/engine/ui2d.js';
import { site } from '../sets/site.js';
import { ROCCO, ELIA, GIADA, CAPO, SARA, NARR } from '../cast.js';

registerShot('c1', { draw(g, t) {
  const cam = { z: 1 + 0.04 * t / 4, x: -20 };
  const { GY, M } = site(g, t, cam);
  const rim = { color: M.rim, dir: [0, -1], w: 4 };
  const cast = [[ROCCO, 'ROCCO', 'operaio'], [ELIA, 'ELIA', 'pilota'], [GIADA, 'GIADA', 'ingegnera'], [CAPO, 'IL CAPO', 'datore'], [SARA, 'SARA', 'infermiera'], [NARR, 'NARRATORE', 'voce']];
  layer(g, cam, 1, (g) => {
    cast.forEach(([o, n, r], i) => {
      const x = E.W * (0.12 + i * 0.152);
      drawFigure(g, { x, y: GY + 40, s: V(2.15, 2.0), facing: 1, outfit: o, pose: breathe(posesAt(t, [[0, 'stand'], [1 + i * .2, i % 2 ? 'wave' : 'explain'], [3, 'stand']]), t, 1, i), expr: 'smile', rim, blink: (t + i) % 3 > 2.9 });
      text(g, n, x, GY + 130, { size: 34, color: '#f4efe6', font: FONTS.ui, weight: 900, spacing: 2 });
      text(g, r, x, GY + 172, { size: 26, color: alpha('#f4efe6', .7), font: FONTS.ui, weight: 700 });
    });
  });
  FX.dust(g, t);
} });
registerShot('c2', { draw(g, t) {
  const cam = { z: 1.1 + 0.08 * t / 4, x: -60 };
  const { GY, M } = site(g, t, cam, { mood: 'golden' });
  layer(g, cam, 1, (g) => {
    drawFigure(g, { x: E.W * 0.36, y: GY + 40, s: V(2.1, 1.9), facing: 1, outfit: ROCCO, pose: breathe(posesAt(t, [[0, 'ready'], [1.2, 'point'], [3, 'explain']]), t), expr: 'determined', rim: { color: M.rim, dir: [0, -1], w: 5 } });
    drawFigure(g, { x: E.W * 0.62, y: GY + 40, s: V(1.8, 1.6), facing: -1, outfit: CAPO, pose: breathe(POSES.crossArms, t, 1, 2), expr: 'neutral', rim: { color: M.rim, dir: [0, -1], w: 5 } });
  });
  FX.dust(g, t, { count: 50 });
  UI.bigLine(g, t, { str: 'OPERAIO COMUNE · 1.100 € LORDI', dur: 4, y: E.H * 0.2, size: V(64, 60) });
} });
registerShot('c3', { draw(g, t) {
  blurLayer(g, 14, (g) => site(g, t, { z: 1.4, x: -120, y: -100 })); veil(g, '#120a10', 0.35);
  const M = mood('golden');
  bigFace(g, E.W * 0.34, E.H * 0.58, V(320, 340), { outfit: ROCCO, expr: t > 2 ? 'surprised' : 'determined', look: [0.2, -0.2], rimColor: M.rim, rimSide: -1 });
  bigFace(g, E.W * 0.74, E.H * 0.58, V(240, 260), { outfit: ELIA, expr: 'smile', look: [-0.2, -0.1], rimColor: M.rim, rimSide: 1 });
} });
