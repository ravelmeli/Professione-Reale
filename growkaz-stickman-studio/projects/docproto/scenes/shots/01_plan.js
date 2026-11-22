import { E, registerShot, layer, ease, text, FONTS } from '/engine/core.js';
import { POSES, breathe } from '/engine/rig2d.js';
import { dchar, dset, finish, truck, walkPose } from '../_doc.js';
const FL = 690;
function mk(g, t, info) {
  const c = { g, t, p: info.p, cam: { z: 1 + 0.09 * info.p, x: -30 * info.p } };
  c.set = (n, o = {}) => dset(g, t, n, o, c.cam);
  c.fig = (who, x, pose = 'stand', o = {}) => layer(g, c.cam, 1, (g) => { const p = pose === 'walk' ? walkPose(t * 7) : (POSES[pose] || pose); dchar(g, { facing: 1, expr: 'neutral', t, seed: x % 7, ...o, who, x, y: o.y ?? FL + 150, pose: pose === 'walk' ? p : breathe(p, t, 1, x * 0.01) }); });
  c.fin = (grade) => finish(g, t, grade);
  return c;
}
const U = [
  (c) => { c.set('piazzale'); c.fig('rocco', 560, 'stand', { age: 24, expr: 'concerned', s: 2.0 }); c.fin('night'); },
  (c) => { c.set('strada'); c.fig('rocco', 600, 'point', { age: 30, expr: 'smile', s: 1.9 }); c.fin('day'); },
  (c) => { c.set('ufficio'); c.fig('rocco', 520, 'holdFront', { age: 46, expr: 'concerned', prop: 'clip', s: 1.9 }); c.fig('marta', 900, 'explain', { facing: -1, expr: 'deadpan', s: 1.9 }); c.fin('day'); },
  (c) => { c.set('casa'); c.fig('rocco', 560, 'wave', { age: 54, expr: 'happy', s: 1.9 }); c.fig('dino', 1000, 'talk', { facing: -1, expr: 'smile', s: 1.9 }); c.fin('warm'); },
  (c) => { c.set('strada', { dusk: true }); c.fig('ciro', 700, 'crossArms', { expr: 'angry', s: 1.9 }); c.fig('rocco', 1100, 'sad', { facing: -1, age: 30, expr: 'surprised', s: 1.9 }); c.fin('dusk'); },
  (c) => { c.set('piazzale', { truck: false }); c.fig('rocco', 700, 'cheer', { age: 54, expr: 'happy', s: 2.2 }); c.fin('night'); },
  // character sheet
  (c) => { const g = c.g; g.fillStyle = '#2a2f3c'; g.fillRect(0, 0, 1920, 1080); [['rocco', 22], ['rocco', 30], ['rocco', 38], ['rocco', 46], ['rocco', 54], ['ciro', 0], ['marta', 0], ['dino', 0]].forEach(([w, a], i) => dchar(g, { x: 150 + i * 230, y: 700, s: 1.3, who: w, age: a, expr: ['smile', 'neutral', 'surprised', 'concerned', 'happy', 'angry', 'deadpan', 'smile'][i], t: c.t, pose: POSES[['stand', 'talk', 'point', 'explain', 'wave', 'crossArms', 'shrug', 'holdFront'][i]] || POSES.stand })); },
];
for (let i = 0; i < 20; i++) { const id = 's' + String(i + 1).padStart(3, '0'); registerShot(id, { draw(g, t, info) { const f = U[info.shot.params?.u]; if (f) f(mk(g, t, info)); } }); }
