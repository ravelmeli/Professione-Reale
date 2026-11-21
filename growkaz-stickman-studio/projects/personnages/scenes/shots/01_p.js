import { E, V, registerShot, mood, layer, blurLayer, veil, text, FONTS, alpha } from '/engine/core.js';
import { drawFigure, POSES, posesAt, breathe, bigFace } from '/engine/rig2d.js';
import * as FX from '/engine/fx2d.js';
import { site } from '../sets/site.js';
import { CHARS } from '../cast.js';
registerShot('p1', { draw(g, t) {
  const cam = { z: 1, x: 0 }; const { GY, M } = site(g, t, cam);
  const rim = { color: M.rim, dir: [0, -1], w: 4 };
  layer(g, cam, 1, (g) => CHARS.forEach((c, i) => {
    const x = E.W * (0.075 + i * 0.121), y = GY + 40;
    drawFigure(g, { x, y, s: V(1.85, 1.6), facing: 1, outfit: c.o, pose: breathe(posesAt(t, [[0, 'stand'], [0.5 + i * 0.1, c.pose]]), t, 1, i), prop: c.prop, expr: c.expr, rim, blink: (t + i) % 3 > 2.9 });
    text(g, c.n, x, y + 70, { size: 26, color: '#f4efe6', font: FONTS.ui, weight: 900, spacing: 2 });
    text(g, c.r, x, y + 104, { size: 20, color: alpha('#f4efe6', .75), font: FONTS.ui, weight: 700 });
  }));
  FX.dust(g, t);
} });
registerShot('p2', { draw(g, t) {
  blurLayer(g, 16, (g) => site(g, t, { z: 1.4, x: -120, y: -100 })); veil(g, '#120a10', 0.3);
  const M = mood('golden');
  CHARS.forEach((c, i) => { const col = i % 4, row = Math.floor(i / 4);
    bigFace(g, E.W * (0.14 + col * 0.24), E.H * (0.3 + row * 0.42), V(130, 130), { outfit: c.o, expr: c.expr, look: [Math.sin(t + i) * .4, 0], rimColor: M.rim, rimSide: -1 });
    text(g, c.n, E.W * (0.14 + col * 0.24), E.H * (0.3 + row * 0.42) + 175, { size: 26, color: '#f4efe6', font: FONTS.ui, weight: 900, spacing: 2 }); });
} });
