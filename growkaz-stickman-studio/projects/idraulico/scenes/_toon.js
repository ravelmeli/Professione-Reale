// _toon.js — cartoon full-body characters (white head, thick ink outline), backdrops, icons and overlays.
import { E, clamp, lerp, ease, prog, text, measure, FONTS, shade, alpha, linGrad } from '/engine/core.js';
import { POSES, walkPose } from '/engine/rig2d.js';

export const INK = '#17141f', WHITE = '#f6f8fc';
export const COL = { y: ['#ffd23f', '#2a2218'], r: ['#ff5a4d', '#ffffff'], g: ['#3ddc84', '#10281a'], b: ['#4aa3ff', '#ffffff'], w: ['#ffffff', '#17141f'], p: ['#a35cff', '#ffffff'], k: ['#232a3d', '#ffffff'], o: ['#ff9a2e', '#2a1a08'] };

// ---------------------------------------------------------------- characters
const BODY = {
  nico(o) { // eroe: capelli blu, cambia look con l'età
    const a = o.age || 18; const hair = '#2a7de1';
    if (a <= 18) return { hair, hairStyle: 'short', torso: '#1fb5b0', arms: '#1fb5b0', legs: '#3b4f78', shoes: '#5a3b22', cheeks: true, wet: true };
    if (a <= 25) return { hair, hairStyle: 'spiky', torso: '#ff8c42', arms: '#ff8c42', legs: '#3b3f55', shoes: '#5a3b22', belt: '#8a5a2b', cheeks: true };
    if (a <= 32) return { hair, hairStyle: 'short', hat: 'cap', hatColor: '#d1495b', torso: '#2f3447', arms: '#2f3447', legs: '#2f3447', shoes: '#111', stripes: '#d1495b', stubble: true };
    if (a <= 38) return { hair, hairStyle: 'short', hat: 'hardhat', hatColor: '#ffd23f', torso: '#c7e83a', arms: '#2f3447', legs: '#3b3f55', shoes: '#111', stripes: '#f6f8fc', stubble: true, temples: true };
    return { hair: '#4a7fbf', hairStyle: 'short', hat: 'cap', hatColor: '#1b3a6b', torso: '#1b3a6b', arms: '#1b3a6b', legs: '#3b3f55', shoes: '#111', stubble: true, temples: true, glasses: true };
  },
  baffo: () => ({ hair: '#8a8f99', hairStyle: 'none', torso: '#3a7d44', arms: '#3a7d44', legs: '#2a3a2e', shoes: '#111', stache: '#5a3a22', brows: '#5a3a22', temples: true }),
  elvira: () => ({ hair: '#7a4a2a', hairStyle: 'bob', torso: '#d1495b', arms: '#d1495b', legs: '#2a2e45', shoes: '#4a2a3a', glasses: true, cheeks: true }),
  dante: () => ({ hair: '#f2c24a', hairStyle: 'spiky', torso: '#ffd23f', arms: '#ffd23f', legs: '#2f6fb5', shoes: '#5a3b22', cheeks: true }),
  sofia: () => ({ hair: '#17141f', hairStyle: 'bob', torso: '#ff7aa8', arms: '#ff7aa8', legs: '#2a2e45', shoes: '#111', cheeks: true, glasses: true }),
  anna: () => ({ hair: '#17141f', hairStyle: 'pig', torso: '#e8553d', arms: '#e8553d', legs: '#e8553d', shoes: '#4a2a1a', dress: true, cheeks: true }),
  tommy: () => ({ hair: '#8a5a2b', hairStyle: 'short', torso: '#4aa3ff', arms: '#4aa3ff', legs: '#3b3f55', shoes: '#4a2a1a', cheeks: true, kid: true }),
};

function limb(g, pts, w, col) {
  g.lineCap = 'round'; g.lineJoin = 'round';
  for (const [c, ww] of [[INK, w + 7], [col, w]]) { g.strokeStyle = c; g.lineWidth = ww; g.beginPath(); g.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]); g.stroke(); }
}
function blob(g, x, y, rx, ry, fill, lw = 3.5, rot = 0) { g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, 7); g.fillStyle = fill; g.fill(); if (lw) { g.lineWidth = lw; g.strokeStyle = INK; g.stroke(); } }
function poly(g, pts, fill, lw = 3.5) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); g.fillStyle = fill; g.fill(); if (lw) { g.lineWidth = lw; g.strokeStyle = INK; g.lineJoin = 'round'; g.stroke(); } }
function line(g, pts, lw = 4, col = INK) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.lineWidth = lw; g.strokeStyle = col; g.lineCap = 'round'; g.lineJoin = 'round'; g.stroke(); }
function rrect(g, x, y, w, h, r, fill, lw = 4) { g.beginPath(); g.roundRect(x, y, w, h, r); g.fillStyle = fill; g.fill(); if (lw) { g.lineWidth = lw; g.strokeStyle = INK; g.stroke(); } }

function prop(g, name, hand, t) {
  const [hx, hy] = hand; g.save(); g.translate(hx, hy);
  if (name === 'tablet') { g.rotate(-0.2); rrect(g, -4, -40, 46, 58, 6, '#2a3350', 3.5); rrect(g, 0, -35, 38, 46, 3, '#8fd6ff', 0); line(g, [[6, -26], [30, -26]], 3, '#fff'); line(g, [[6, -16], [24, -16]], 3, '#fff'); }
  else if (name === 'phone') { rrect(g, 0, -30, 20, 36, 4, '#222', 3); rrect(g, 3, -26, 14, 26, 2, '#8fd6ff', 0); }
  else if (name === 'tester') { rrect(g, -2, -34, 34, 44, 6, '#ffd23f', 3.5); rrect(g, 3, -28, 24, 14, 2, '#2a3a2a', 0); line(g, [[10, -22], [22, -22]], 2.5, '#7dff9a'); blob(g, 14, -2, 5, 5, '#ff5a4d', 2); }
  else if (name === 'screwdriver') { g.rotate(-0.9); rrect(g, -5, -10, 12, 26, 5, '#ff5a4d', 3.5); line(g, [[1, -10], [1, -44]], 5, '#c9ced6'); }
  else if (name === 'coil') { for (let i = 0; i < 3; i++) { g.beginPath(); g.ellipse(14, -10, 22 - i * 5, 20 - i * 4, 0, 0, 7); g.lineWidth = 6; g.strokeStyle = INK; g.stroke(); g.lineWidth = 3; g.strokeStyle = ['#2f7fd0', '#8b5a2b', '#8ccf3a'][i]; g.stroke(); } }
  else if (name === 'clip') { g.rotate(-0.15); rrect(g, -4, -42, 40, 56, 4, '#b98a52', 3.5); rrect(g, 0, -36, 32, 44, 2, '#fff', 0); line(g, [[5, -28], [26, -28]], 2.5, '#888'); line(g, [[5, -20], [26, -20]], 2.5, '#888'); line(g, [[5, -12], [20, -12]], 2.5, '#888'); }
  else if (name === 'keys') { blob(g, 0, 0, 6, 6, '#ffd23f', 2.5); blob(g, 14, 8, 6, 6, '#c9ced6', 2.5); line(g, [[0, 6], [2, 26]], 3); }
  else if (name === 'ladder') { g.rotate(-1.25); rrect(g, -4, -150, 10, 190, 4, '#e9a23b', 3); rrect(g, 34, -150, 10, 190, 4, '#e9a23b', 3); for (let i = 0; i < 6; i++) line(g, [[4, -130 + i * 28], [36, -130 + i * 28]], 5, '#e9a23b'); }
  else if (name === 'doc') { rrect(g, 0, -36, 34, 46, 3, '#fff', 3.5); for (let i = 0; i < 4; i++) line(g, [[6, -26 + i * 9], [28, -26 + i * 9]], 2.5, '#9aa'); }
  else if (name === 'wrench') { g.rotate(-0.9); rrect(g, -6, -8, 12, 84, 5, '#c9ced6', 3.5); g.beginPath(); g.arc(0, -16, 17, 0, 7); g.fillStyle = '#c9ced6'; g.fill(); g.lineWidth = 3.5; g.strokeStyle = INK; g.stroke(); rrect(g, -6, -34, 12, 20, 2, '#2a3350', 0); }
  else if (name === 'box') { rrect(g, -22, -6, 66, 40, 6, '#d1495b', 4); rrect(g, -4, -16, 30, 14, 5, '#9a2a3a', 4); }
  else if (name === 'hammer') { g.rotate(-0.8); rrect(g, -5, -10, 10, 70, 4, '#8a5a2b', 3); rrect(g, -22, -30, 44, 24, 5, '#7a808c', 3.5); }
  else if (name === 'cup') { rrect(g, 0, -20, 24, 28, 6, '#fff', 3.5); line(g, [[24, -14], [34, -8], [24, 0]], 4); line(g, [[8, -26], [8, -34]], 3, '#aab'); line(g, [[16, -26], [16, -36]], 3, '#aab'); }
  g.restore();
}

function hairBack(g, b, c) {
  if (b.hairStyle === 'bun') blob(g, c[0] - 24, c[1] - 40, 15, 15, b.hair, 3.5);
  if (b.hairStyle === 'curly') for (let i = 0; i < 8; i++) { const a = Math.PI * (0.95 + i * 0.15); blob(g, c[0] + Math.cos(a) * 36, c[1] + Math.sin(a) * 34, 13, 13, b.hair, 3.5); }
  if (b.hairStyle === 'pig') { blob(g, c[0] - 38, c[1] - 6, 11, 11, b.hair, 3.5); blob(g, c[0] + 38, c[1] - 6, 11, 11, b.hair, 3.5); }
  if (b.hairStyle === 'bob') { blob(g, c[0], c[1] + 6, 41, 40, b.hair, 3.5); }
}
function head(g, b, c, expr, t, look, seed) {
  const R = b.kid ? 38 : 36;
  g.beginPath(); g.arc(c[0], c[1], R, 0, 7); const gr = g.createRadialGradient(c[0] - 12, c[1] - 14, 4, c[0], c[1], R + 4); gr.addColorStop(0, '#ffffff'); gr.addColorStop(1, '#dfe4ee'); g.fillStyle = gr; g.fill(); g.lineWidth = 4; g.strokeStyle = INK; g.stroke();
  if (b.cheeks) { blob(g, c[0] + 22, c[1] + 12, 7, 4.5, '#f6b4b4', 0); blob(g, c[0] - 4, c[1] + 12, 7, 4.5, '#f6b4b4', 0); }
  if (b.stubble) for (let i = 0; i < 14; i++) { const a = 0.4 + i * 0.2; g.fillStyle = 'rgba(40,30,30,.45)'; g.fillRect(c[0] + 4 + Math.cos(a) * 20 * (0.5 + (i % 3) * 0.2), c[1] + 14 + Math.abs(Math.sin(a * 2)) * 15, 2, 2); }
  const ex = [c[0] - 2 + 8, c[0] + 22 + 4], ey = c[1] - 3, blink = ((t + seed) % 3.4) > 3.28;
  const lk = [clamp(look[0], -1, 1) * 3, clamp(look[1], -1, 1) * 2.5];
  ex.forEach((x, i) => {
    if (blink || expr === 'sleepy') { line(g, [[x - 6, ey], [x + 6, ey]], 4); return; }
    if (expr === 'shock') { blob(g, x, ey, 8.5, 10, '#fff', 3); blob(g, x + lk[0], ey + lk[1], 3, 3, INK, 0); return; }
    blob(g, x + lk[0], ey + lk[1], 5, 6.4, INK, 0); g.fillStyle = '#fff'; g.beginPath(); g.arc(x + lk[0] + 1.8, ey + lk[1] - 2, 1.8, 0, 7); g.fill();
  });
  const bc = b.brows || INK;
  const brow = (x, dy, tilt) => line(g, [[x - 8, ey - 15 + dy - tilt], [x + 8, ey - 15 + dy + tilt]], 3.5, bc);
  if (expr === 'angry') { brow(ex[0], 1, 4); brow(ex[1], 1, -4); }
  else if (expr === 'worried') { brow(ex[0], -1, -4); brow(ex[1], -1, 4); }
  else if (expr === 'shock') { brow(ex[0], -6, 0); brow(ex[1], -6, 0); }
  else if (expr === 'sleepy') { brow(ex[0], 4, 1); brow(ex[1], 4, -1); }
  else brow(ex[0], 0, 0), brow(ex[1], 0, 0);
  const mx = c[0] + 14, my = c[1] + 20;
  if (expr === 'smile') line(g, [[mx - 10, my - 2], [mx - 4, my + 3], [mx + 4, my + 3], [mx + 10, my - 2]], 4);
  else if (expr === 'grin') { g.beginPath(); g.moveTo(mx - 13, my - 4); g.quadraticCurveTo(mx, my + 20, mx + 13, my - 4); g.closePath(); g.fillStyle = '#fff'; g.fill(); g.lineWidth = 3.5; g.strokeStyle = INK; g.stroke(); }
  else if (expr === 'shock') blob(g, mx, my + 2, 6, 8, INK, 0);
  else if (expr === 'worried') line(g, [[mx - 9, my + 5], [mx, my], [mx + 9, my + 5]], 4);
  else if (expr === 'angry') line(g, [[mx - 9, my + 4], [mx, my - 1], [mx + 9, my + 4]], 4.5);
  else line(g, [[mx - 8, my + 1], [mx + 8, my + 1]], 4);
  if (b.stache) { poly(g, [[mx - 18, my - 8], [mx - 2, my - 12], [mx, my - 8], [mx + 2, my - 12], [mx + 18, my - 8], [mx + 10, my], [mx, my - 4], [mx - 10, my]], b.stache, 3); }
  if (b.glasses) { blob(g, ex[0], ey, 13, 13, 'rgba(255,255,255,.3)', 3.5); blob(g, ex[1], ey, 13, 13, 'rgba(255,255,255,.3)', 3.5); line(g, [[ex[0] + 13, ey], [ex[1] - 13, ey]], 3.5); }
  // capelli davanti / copricapo
  const top = c[1] - R;
  if (b.hairStyle === 'short' || b.hairStyle === 'bun' || b.hairStyle === 'curly' || b.hairStyle === 'bob' || b.hairStyle === 'pig') {
    g.beginPath(); g.moveTo(c[0] - R - 1, c[1] - 6); g.quadraticCurveTo(c[0] - R - 4, top - 8, c[0] + 4, top - 6); g.quadraticCurveTo(c[0] + R + 4, top - 6, c[0] + R + 1, c[1] - 8); g.quadraticCurveTo(c[0] + 18, c[1] - 24, c[0] - 6, c[1] - 22); g.quadraticCurveTo(c[0] - 26, c[1] - 24, c[0] - R - 1, c[1] - 6); g.closePath(); g.fillStyle = b.hair; g.fill(); g.lineWidth = 4; g.strokeStyle = INK; g.stroke();
    if (b.temples) { blob(g, c[0] - R + 4, c[1] - 6, 4, 8, '#d8d8e0', 0); }
  }
  if (b.hairStyle === 'spiky') { poly(g, [[c[0] - R, c[1] - 8], [c[0] - R + 4, top - 12], [c[0] - 16, top - 2], [c[0] - 8, top - 26], [c[0] + 4, top - 4], [c[0] + 16, top - 24], [c[0] + 22, top - 2], [c[0] + R, top - 8], [c[0] + R - 2, c[1] - 10], [c[0] + 12, c[1] - 24], [c[0] - 14, c[1] - 24]], b.hair, 4); }
  if (b.hat === 'hardhat') { g.beginPath(); g.moveTo(c[0] - R - 5, c[1] - 12); g.quadraticCurveTo(c[0] - R - 3, top - 22, c[0], top - 22); g.quadraticCurveTo(c[0] + R + 3, top - 22, c[0] + R + 5, c[1] - 12); g.closePath(); g.fillStyle = b.hatColor; g.fill(); g.lineWidth = 4; g.strokeStyle = INK; g.stroke(); rrect(g, c[0] - R - 12, c[1] - 16, 2 * R + 24, 10, 5, b.hatColor, 4); line(g, [[c[0], top - 22], [c[0], c[1] - 16]], 3.5); }
  if (b.hat === 'cap') { g.beginPath(); g.moveTo(c[0] - R - 2, c[1] - 12); g.quadraticCurveTo(c[0] - R, top - 14, c[0] + 4, top - 14); g.quadraticCurveTo(c[0] + R, top - 14, c[0] + R + 2, c[1] - 12); g.closePath(); g.fillStyle = b.hatColor; g.fill(); g.lineWidth = 4; g.strokeStyle = INK; g.stroke(); poly(g, [[c[0] + 6, c[1] - 14], [c[0] + R + 28, c[1] - 8], [c[0] + R + 24, c[1] - 1], [c[0] + 6, c[1] - 6]], b.hatColor, 3.5); if (b.bolt) { poly(g, [[c[0] + 2, top - 6], [c[0] + 12, top - 6], [c[0] + 6, top + 6], [c[0] + 14, top + 6], [c[0], top + 20], [c[0] + 3, top + 9], [c[0] - 4, top + 9]], '#ffd23f', 2); } }
}

export function toon(g, o) {
  const { x, y, s = 1.9, facing = 1, who = 'teo', expr = 'smile', t = 0, look = [0.5, 0], alpha: al = 1, seed = 0 } = o;
  const b = BODY[who](o), kid = b.kid, sc = s * (kid ? 0.72 : 1);
  const p = o.pose || POSES.stand;
  g.save(); g.globalAlpha *= al; g.translate(x, y); g.scale(facing * sc, sc);
  g.fillStyle = 'rgba(0,0,0,.22)'; g.beginPath(); g.ellipse(0, 2, 46, 9, 0, 0, 7); g.fill();
  const dk = (c) => shade(c, -0.22);
  const legW = b.dress ? 30 : 25;
  limb(g, [p.hip, p.kB, p.fB], legW, dk(b.legs)); blob(g, p.fB[0] + 8, p.fB[1] - 4, 17, 8, dk(b.shoes), 3.5);
  limb(g, [p.sh, p.eB, p.hB], 22, dk(b.arms)); blob(g, p.hB[0], p.hB[1], 10, 10, '#e6eaf2', 3.5);
  if (b.dress) poly(g, [[p.sh[0] - 14, p.sh[1] + 12], [p.sh[0] + 14, p.sh[1] + 12], [p.hip[0] + 36, p.hip[1] + 52], [p.hip[0] - 36, p.hip[1] + 52]], b.torso, 4);
  limb(g, [[p.sh[0], p.sh[1] - 6], p.hip], 62, b.torso);
  if (b.stripes) { limb(g, [[p.sh[0] - 12, p.sh[1] + 10], [p.hip[0] - 10, p.hip[1] - 6]], 5, b.stripes); limb(g, [[p.sh[0] + 12, p.sh[1] + 10], [p.hip[0] + 10, p.hip[1] - 6]], 5, b.stripes); }
  if (b.strap) { limb(g, [[p.sh[0] - 14, p.sh[1] + 4], [p.hip[0] - 8, p.hip[1] - 12]], 6, b.strap); limb(g, [[p.sh[0] + 14, p.sh[1] + 4], [p.hip[0] + 8, p.hip[1] - 12]], 6, b.strap); }
  if (b.belt) { limb(g, [[p.hip[0] - 22, p.hip[1] - 2], [p.hip[0] + 22, p.hip[1] - 2]], 9, b.belt); rrect(g, p.hip[0] + 10, p.hip[1] - 2, 14, 18, 3, '#ffd23f', 3); }
  limb(g, [p.hip, p.kF, p.fF], legW, b.legs); blob(g, p.fF[0] + 8, p.fF[1] - 4, 17, 8, b.shoes, 3.5);
  limb(g, [p.sh, p.eF, p.hF], 22, b.arms);
  blob(g, p.hF[0], p.hF[1], 10, 10, '#f6f8fc', 3.5);
  if (o.prop) prop(g, o.prop, p.hF, t);
  const c = [p.head[0], p.head[1] - 10];
  g.save(); g.translate(c[0], c[1] + 8); g.scale(1.16, 1.16); g.translate(-c[0], -c[1] - 8); hairBack(g, b, c); head(g, b, c, expr, t, look, seed); g.restore();
  g.restore();
}
export { POSES, walkPose };

// ---------------------------------------------------------------- icons
export function icon(g, name, x, y, sz = 90, o = {}) {
  const k = sz / 100, c = o.color; g.save(); g.translate(x, y); g.scale(k, k);
  const st = (fill, lw = 6) => { g.fillStyle = fill; g.fill(); g.lineWidth = lw; g.strokeStyle = INK; g.lineJoin = 'round'; g.stroke(); };
  if (name === 'bolt') { g.beginPath(); [[-18, -50], [26, -50], [4, -6], [30, -6], [-24, 52], [-6, 6], [-30, 6]].forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath(); st(c || '#ffd23f'); }
  else if (name === 'bulb') { if (o.on !== false) { g.globalAlpha *= 0.35; g.fillStyle = '#ffe9a0'; g.beginPath(); g.arc(0, -10, 80, 0, 7); g.fill(); g.globalAlpha /= 0.35; } g.beginPath(); g.arc(0, -14, 32, 0, 7); st(o.on === false ? '#8a8f9c' : '#ffe27a'); rrect(g, -16, 14, 32, 22, 5, '#c9ced6', 5); }
  else if (name === 'lock') { g.beginPath(); g.arc(0, -16, 22, Math.PI, 0); g.lineWidth = 12; g.strokeStyle = INK; g.stroke(); g.lineWidth = 6; g.strokeStyle = '#c9ced6'; g.stroke(); rrect(g, -32, -16, 64, 52, 10, c || '#ffd23f', 6); blob(g, 0, 8, 6, 6, INK, 0); }
  else if (name === 'warn') { g.beginPath(); [[0, -48], [50, 38], [-50, 38]].forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath(); st(c || '#ffd23f'); g.fillStyle = INK; g.fillRect(-4, -20, 8, 34); g.beginPath(); g.arc(0, 26, 5, 0, 7); g.fill(); }
  else if (name === 'doc') { rrect(g, -34, -46, 68, 92, 6, '#fff', 6); for (let i = 0; i < 5; i++) line(g, [[-22, -26 + i * 16], [i === 4 ? 4 : 22, -26 + i * 16]], 4, '#8a93a6'); }
  else if (name === 'coin') { g.beginPath(); g.arc(0, 0, 42, 0, 7); st(c || '#ffd23f'); g.fillStyle = INK; g.font = '800 46px Fredoka'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('€', 0, 3); }
  else if (name === 'plug') { rrect(g, -26, -20, 52, 44, 8, c || '#e8ecf2', 6); line(g, [[-12, -20], [-12, -44]], 9); line(g, [[12, -20], [12, -44]], 9); line(g, [[0, 24], [0, 54], [30, 70]], 8); }
  else if (name === 'clock') { g.beginPath(); g.arc(0, 0, 42, 0, 7); st('#fff'); line(g, [[0, 0], [0, -26]], 6); line(g, [[0, 0], [20, 10]], 6); }
  else if (name === 'phone') { rrect(g, -24, -42, 48, 84, 10, '#2a3350', 6); rrect(g, -18, -32, 36, 56, 4, '#8fd6ff', 0); if (o.ring) { for (let i = 1; i <= 2; i++) { g.beginPath(); g.arc(0, 0, 44 + i * 14 + Math.sin(o.ring * 12) * 3, -0.7, 0.7); g.lineWidth = 5; g.strokeStyle = '#ff5a4d'; g.stroke(); g.beginPath(); g.arc(0, 0, 44 + i * 14 + Math.sin(o.ring * 12) * 3, Math.PI - 0.7, Math.PI + 0.7); g.stroke(); } } }
  else if (name === 'heart') { g.beginPath(); g.moveTo(0, 36); g.bezierCurveTo(-60, -4, -34, -50, 0, -20); g.bezierCurveTo(34, -50, 60, -4, 0, 36); st(c || '#ff5a6e'); }
  else if (name === 'tick') { g.beginPath(); g.arc(0, 0, 44, 0, 7); st(c || '#3ddc84'); line(g, [[-22, 2], [-6, 20], [24, -16]], 11, '#fff'); }
  else if (name === 'cross') { g.beginPath(); g.arc(0, 0, 44, 0, 7); st(c || '#ff5a4d'); line(g, [[-20, -20], [20, 20]], 11, '#fff'); line(g, [[20, -20], [-20, 20]], 11, '#fff'); }
  else if (name === 'sun') { for (let i = 0; i < 10; i++) { const a = i * 0.628; line(g, [[Math.cos(a) * 44, Math.sin(a) * 44], [Math.cos(a) * 62, Math.sin(a) * 62]], 8, '#ffb02e'); } g.beginPath(); g.arc(0, 0, 34, 0, 7); st('#ffd23f'); }
  else if (name === 'cal') { rrect(g, -42, -40, 84, 80, 10, '#fff', 6); rrect(g, -42, -40, 84, 24, 10, c || '#ff5a4d', 6); for (let i = 0; i < 6; i++) blob(g, -26 + (i % 3) * 26, -2 + Math.floor(i / 3) * 22, 6, 6, '#8a93a6', 0); }
  else if (name === 'house') { poly(g, [[-52, -4], [0, -50], [52, -4]], c || '#ff5a4d', 6); rrect(g, -38, -4, 76, 56, 4, '#fff', 6); rrect(g, -9, 18, 18, 34, 3, '#8a5a2b', 4); }
  else if (name === 'van') { rrect(g, -96, -54, 150, 90, 12, '#f6f8fc', 6); poly(g, [[54, -30], [96, -30], [118, 6], [118, 36], [54, 36]], '#f6f8fc', 6); poly(g, [[62, -22], [92, -22], [108, 4], [62, 4]], '#8fd6ff', 4); for (const wx of [-56, 76]) { g.beginPath(); g.arc(wx, 38, 20, 0, 7); st('#2a2e3d'); g.beginPath(); g.arc(wx, 38, 8, 0, 7); g.fillStyle = '#c9ced6'; g.fill(); } g.save(); g.translate(-22, -10); g.scale(0.5, 0.5); g.beginPath(); [[-18, -50], [26, -50], [4, -6], [30, -6], [-24, 52], [-6, 6], [-30, 6]].forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath(); st('#ffd23f', 8); g.restore(); }
  else if (name === 'drop') { g.beginPath(); g.moveTo(0, -56); g.bezierCurveTo(46, 0, 40, 44, 0, 48); g.bezierCurveTo(-40, 44, -46, 0, 0, -56); st(c || '#4aa3ff'); blob(g, -14, 12, 7, 12, 'rgba(255,255,255,.7)', 0); }
  else if (name === 'wrench') { g.rotate(-0.7); rrect(g, -9, -8, 18, 90, 8, '#c9ced6', 6); g.beginPath(); g.arc(0, -26, 28, 0, 7); st('#c9ced6'); rrect(g, -9, -62, 18, 30, 2, '#2a3350', 0); }
  else if (name === 'gauge') { g.beginPath(); g.arc(0, 0, 56, 0, 7); st('#fff'); for (let i = 0; i <= 8; i++) { const a = Math.PI * (0.75 + i * 0.1875); line(g, [[Math.cos(a) * 42, Math.sin(a) * 42], [Math.cos(a) * 50, Math.sin(a) * 50]], 4, '#555'); } const v = o.v ?? 0.5, a = Math.PI * (0.75 + v * 1.5); line(g, [[0, 0], [Math.cos(a) * 40, Math.sin(a) * 40]], 6, '#ff5a4d'); g.beginPath(); g.arc(0, 0, 7, 0, 7); g.fillStyle = INK; g.fill(); }
  else if (name === 'flame') { g.beginPath(); g.moveTo(0, -54); g.bezierCurveTo(40, -10, 44, 20, 0, 46); g.bezierCurveTo(-44, 20, -40, -10, 0, -54); st(c || '#ff7a1a'); g.beginPath(); g.moveTo(0, -8); g.bezierCurveTo(20, 8, 20, 26, 0, 38); g.bezierCurveTo(-20, 26, -20, 8, 0, -8); g.fillStyle = '#ffd23f'; g.fill(); }
  else if (name === 'snow') { for (let i = 0; i < 3; i++) { const a = i * Math.PI / 3; line(g, [[Math.cos(a) * 48, Math.sin(a) * 48], [-Math.cos(a) * 48, -Math.sin(a) * 48]], 9, INK); } for (let i = 0; i < 3; i++) { const a = i * Math.PI / 3; line(g, [[Math.cos(a) * 46, Math.sin(a) * 46], [-Math.cos(a) * 46, -Math.sin(a) * 46]], 5, c || '#bfe6ff'); } }
  else if (name === 'faucet') { rrect(g, -50, -10, 70, 26, 10, '#c9ced6', 6); rrect(g, 8, -10, 22, 66, 8, '#c9ced6', 6); rrect(g, -12, -36, 24, 26, 6, '#4aa3ff', 5); }
  else if (name === 'radiator') { for (let i = 0; i < 6; i++) rrect(g, -60 + i * 20, -40, 16, 80, 8, '#f6f8fc', 5); line(g, [[-62, -22], [62, -22]], 4, INK); if (o.warm) { for (let i = 0; i < 3; i++) line(g, [[-30 + i * 30, -52], [-24 + i * 30, -80]], 6, '#ff7a1a'); } }
  g.restore();
}

// ---------------------------------------------------------------- backdrops (1920x1080, ground y = 880)
export const GY = 880;
function sky(g, a, b) { g.fillStyle = linGrad(g, 0, 0, 0, E.H, [a, b]); g.fillRect(-300, -300, E.W + 600, E.H + 600); }
function floor(g, col, y = GY - 20) { g.fillStyle = col; g.fillRect(-300, y, E.W + 600, E.H - y + 400); g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(-300, y, E.W + 600, 8); }
function wireBundle(g, x, y, t, cols) { cols.forEach((c, i) => { const sw = Math.sin(t * 1.6 + i) * 6; g.beginPath(); g.moveTo(x + i * 14, y); g.bezierCurveTo(x + i * 14 + sw, y + 80, x + i * 14 - 30 + sw, y + 160 + i * 14, x + i * 14 - 10 + i * 6, y + 250 + i * 10); g.lineWidth = 12; g.strokeStyle = INK; g.lineCap = 'round'; g.stroke(); g.lineWidth = 7; g.strokeStyle = c; g.stroke(); }); }
export function panel(g, x, y, t, open = true, hot = false) {
  rrect(g, x, y, 560, 620, 12, '#8f9aa3', 7); rrect(g, x + 30, y + 30, 500, 560, 8, '#2a2f38', 5);
  for (let r = 0; r < 4; r++) for (let i = 0; i < 8; i++) { const on = (r * 8 + i) % 5 !== 0; rrect(g, x + 52 + i * 58, y + 60 + r * 128, 40, 90, 5, on ? '#e8ecf2' : '#ff5a4d', 4); rrect(g, x + 60 + i * 58, y + (on ? 70 : 118) + r * 128, 24, 34, 3, '#2a2f38', 0); }
  if (hot) { g.save(); g.globalAlpha *= 0.5 + 0.3 * Math.sin(t * 14); rrect(g, x + 30, y + 30, 500, 560, 8, 'rgba(255,90,70,.35)', 0); g.restore(); }
  wireBundle(g, x + 90, y + 590, t, ['#8b5a2b', '#2f7fd0', '#8ccf3a', '#222']);
}
export function backdrop(g, t, name, o = {}) {
  const W = E.W, H = E.H;
  if (name === 'quadro') { sky(g, '#2b4a52', '#1d3338'); floor(g, '#16252a'); panel(g, 1120, 150, t, true, o.hot); icon(g, 'warn', 300, 300, 120); }
  else if (name === 'cantiere') { sky(g, '#566474', '#3d4756'); g.fillStyle = '#2d3440'; g.fillRect(-300, -300, W + 600, 380); for (let i = 0; i < 4; i++) { g.fillStyle = '#6b7788'; g.fillRect(180 + i * 480, 80, 26, H); } rrect(g, 1290, 180, 240, 120, 8, '#9fd0ff', 6); floor(g, '#363e4a'); icon(g, 'warn', 1560, 560, 90); }
  else if (name === 'casa') { sky(g, '#e2c6a4', '#d2b08a'); floor(g, '#8a6a4f'); rrect(g, 1250, 190, 340, 640, 16, '#f2f5f9', 7); line(g, [[1250, 470], [1590, 470]], 6); rrect(g, 1560, 300, 12, 70, 5, '#8a93a6', 3); rrect(g, 220, 220, 260, 220, 10, '#2a3a58', 7); rrect(g, 236, 236, 228, 188, 6, o.dark ? '#14203a' : '#a9dcff', 0); icon(g, 'bulb', 860, 230, 96, { on: o.lamp !== false }); line(g, [[860, 150], [860, 80]], 5); }
  else if (name === 'fabbrica') { sky(g, '#323946', '#252a35'); floor(g, '#3a3f4d'); for (let i = 0; i < 4; i++) { rrect(g, 120 + i * 420, 330, 300, 440, 12, '#59647a', 7); rrect(g, 150 + i * 420, 365, 240, 130, 8, '#1e2431', 5); const run = !(o.stop); blob(g, 190 + i * 420, 560, 18, 18, run ? '#3ddc84' : '#ff5a4d', 4); blob(g, 250 + i * 420, 560, 18, 18, run ? '#ffd23f' : '#4a1e1a', 4); } g.fillStyle = '#ffd23f'; for (let i = 0; i < 24; i++) g.fillRect(-60 + i * 90, GY - 20, 46, 14); if (o.stop) { g.save(); g.globalAlpha *= 0.15 + 0.15 * Math.sin(t * 10); g.fillStyle = '#ff2a1a'; g.fillRect(0, 0, W, H); g.restore(); } }
  else if (name === 'ufficio') { sky(g, '#cdd7e4', '#b8c4d6'); floor(g, '#7a6650'); rrect(g, 1180, 150, 520, 330, 10, '#2a3a58', 7); rrect(g, 1196, 166, 488, 298, 6, '#bfe3ff', 0); for (let i = 0; i < 6; i++) { g.fillStyle = '#8da4c4'; g.fillRect(1210 + i * 78, 310 - (i % 3) * 40, 56, 150 + (i % 3) * 40); } rrect(g, 940, 700, 760, 40, 8, '#8a5a2b', 6); rrect(g, 980, 740, 24, 120, 3, '#6a4220', 4); rrect(g, 1640, 740, 24, 120, 3, '#6a4220', 4); rrect(g, 240, 190, 260, 190, 6, '#fff', 6); line(g, [[270, 240], [470, 240]], 5, '#9aa'); line(g, [[270, 280], [440, 280]], 5, '#9aa'); }
  else if (name === 'notte') { sky(g, '#141a33', '#0c1124'); floor(g, '#1a2038'); rrect(g, 1180, 160, 440, 360, 10, '#0a0e1c', 7); blob(g, 1500, 260, 44, 44, '#fff3c4', 5); for (let i = 0; i < 12; i++) blob(g, 1220 + (i * 97) % 380, 200 + (i * 53) % 280, 3, 3, '#fff', 0); rrect(g, 200, 640, 820, 200, 14, '#3a4a7a', 7); rrect(g, 200, 590, 180, 80, 14, '#e8ecf2', 6); rrect(g, 1100, 700, 160, 180, 8, '#4a3a2a', 6); }
  else if (name === 'strada') { sky(g, '#7fa6d6', '#f3c88c'); for (let i = 0; i < 7; i++) { g.fillStyle = ['#5a6580', '#6a7592', '#4e5873'][i % 3]; g.fillRect(i * 290 - 40, 280 + (i % 3) * 60, 250, 700); for (let r = 0; r < 6; r++) for (let c = 0; c < 3; c++) { g.fillStyle = '#ffe9a8'; g.fillRect(i * 290 + 12 + c * 76, 320 + (i % 3) * 60 + r * 100, 44, 56); } } floor(g, '#3a3f4d', GY - 20); g.fillStyle = '#ffd23f'; for (let i = 0; i < 12; i++) g.fillRect(i * 180, GY + 50, 90, 10); }
  else if (name === 'bagno') { sky(g, '#a9d9ea', '#8cc4d8'); g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 3; for (let x = 0; x < W; x += 110) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, GY - 20); g.stroke(); } for (let y = 0; y < GY - 20; y += 110) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); } floor(g, '#6f879b'); rrect(g, 1280, 330, 360, 36, 16, '#fbfcfe', 6); rrect(g, 1420, 366, 80, 380, 10, '#eef2f7', 6); rrect(g, 1450, 740, 20, 50, 4, '#c9ced6', 4); line(g, [[1460, 790], [1460, 840]], 10, '#c9ced6'); rrect(g, 1340, 150, 240, 150, 10, '#d8eef7', 6); const dp = (t * 1.3) % 1; if (o.leak !== false) { blob(g, 1460, 820 + dp * 30, 6, 9, '#4aa3ff', 2); } const lv = o.flood ?? 0.5; g.save(); g.globalAlpha *= 0.75; g.fillStyle = '#4aa3ff'; g.beginPath(); g.moveTo(-60, GY + 110); for (let x = -60; x <= W + 60; x += 40) g.lineTo(x, GY - 10 - 50 * lv + Math.sin(x * 0.02 + t * 2.4) * 8); g.lineTo(W + 60, GY + 220); g.lineTo(-60, GY + 220); g.closePath(); g.fill(); g.restore(); }
  else if (name === 'caldaia') { sky(g, '#d9c9aa', '#cdb892'); floor(g, '#7a6650'); rrect(g, 1560, 230, 300, 420, 14, '#f6f8fc', 7); rrect(g, 1590, 270, 240, 90, 8, '#1e2431', 5); text(g, o.temp || '60°', 1710, 316, { size: 54, color: '#7dff9a', font: FONTS.title, weight: 800 }); blob(g, 1630, 410, 12, 12, o.fault ? '#ff5a4d' : '#3ddc84', 4); blob(g, 1680, 410, 12, 12, '#ffd23f', 4); for (const [xx, cc] of [[1610, '#ff5a4d'], [1710, '#4aa3ff'], [1800, '#4aa3ff']]) { rrect(g, xx, 650, 22, 200, 4, cc, 4); } rrect(g, 1590, 120, 22, 110, 4, '#ff5a4d', 4); rrect(g, 1800, 120, 22, 110, 4, '#4aa3ff', 4); for (let i = 0; i < 7; i++) rrect(g, 190 + i * 40, 520, 34, 300, 14, '#f6f8fc', 6); if (o.warm) { g.save(); g.globalAlpha *= 0.25 + 0.1 * Math.sin(t * 3); g.fillStyle = '#ff9a2e'; g.fillRect(150, 300, 360, 520); g.restore(); } if (o.gauge != null) icon(g, 'gauge', 760, 330, 120, { v: o.gauge }); }
  else if (name === 'tubi') { sky(g, '#2a3040', '#1c212e'); [['#c97b43', 150], ['#4aa3ff', 330], ['#e8ecf2', 510], ['#9aa3b2', 690]].forEach(([c, y], i) => { rrect(g, -60, y, W + 120, 70, 35, '#0e1118', 0); rrect(g, -60, y - 4, W + 120, 62, 31, c, 6); line(g, [[0, y + 14], [W, y + 14]], 6, 'rgba(255,255,255,.35)'); rrect(g, 380 + i * 360, y - 14, 60, 90, 8, shade(c, -0.2), 6); }); floor(g, '#171b26', GY - 20); }
  else if (name === 'luce') { sky(g, '#0b1230', '#1b2447'); for (let i = 0; i < 9; i++) { g.fillStyle = '#10182f'; g.fillRect(i * 230 - 20, 260 + (i % 4) * 70, 200, 700); for (let r = 0; r < 7; r++) for (let c = 0; c < 3; c++) { const idx = i * 21 + r * 3 + c, on = (o.p ?? 1) * 1.15 > ((idx * 37) % 100) / 100; g.fillStyle = on ? '#ffe08a' : '#1c2542'; g.fillRect(i * 230 + 14 + c * 62, 300 + (i % 4) * 70 + r * 92, 40, 54); } } floor(g, '#0a1022'); }
  else { sky(g, '#1a2740', '#101a2c'); g.fillStyle = 'rgba(255,255,255,.05)'; for (let x = 40; x < W; x += 80) for (let y = 40; y < H; y += 80) g.fillRect(x, y, 3, 3); }
}

// ---------------------------------------------------------------- overlays
function pop(t, at, d = 0.38) { return ease.outBack(prog(t, at, at + d)); }
export function chip(g, str, x, y, t, at, c = 'y', size = 46, o = {}) {
  const k = pop(t, at); if (k <= 0.01) return; const [bg, fg] = COL[c] || COL.y; const w = measure(g, str, size, FONTS.title, 800) + 56, h = size + 34;
  g.save(); g.translate(x, y); g.scale(k, k); if (o.rot) g.rotate(o.rot); rrect(g, -w / 2 + 4, -h / 2 + 6, w, h, h / 2, 'rgba(0,0,0,.35)', 0); rrect(g, -w / 2, -h / 2, w, h, h / 2, bg, 6); text(g, str, 0, 3, { size, color: fg, font: FONTS.title, weight: 800 }); g.restore();
}
export function banner(g, t, n, name, sub) {
  const k = ease.outBack(prog(t, 0.05, 0.6)); g.save(); g.translate(E.W / 2, 200 - (1 - k) * 340);
  rrect(g, -560, -110, 1120, 230, 34, '#14202f', 8); rrect(g, -560, -110, 1120, 70, 34, '#ffd23f', 8);
  text(g, 'LIVELLO ' + n, 0, -73, { size: 56, color: '#17141f', font: FONTS.title, weight: 800, spacing: 6 });
  text(g, name, 0, 36, { size: name.length > 18 ? 62 : 76, color: '#ffffff', font: FONTS.title, weight: 800 });
  if (sub) text(g, sub, 0, 96, { size: 30, color: '#9fb6d8', font: FONTS.ui, weight: 800, spacing: 2 }); g.restore();
}
export function card(g, t, at, x, y, w, title, rows, accent = '#ffd23f') {
  const k = pop(t, at); if (k <= 0.01) return; const rh = 74, h = 90 + rows.length * rh;
  g.save(); g.translate(x, y); g.scale(k, k); rrect(g, -w / 2 + 6, -h / 2 + 8, w, h, 24, 'rgba(0,0,0,.35)', 0); rrect(g, -w / 2, -h / 2, w, h, 24, '#14202f', 7); rrect(g, -w / 2, -h / 2, w, 70, 24, accent, 7);
  text(g, title, 0, -h / 2 + 37, { size: 38, color: '#17141f', font: FONTS.title, weight: 800 });
  rows.forEach((r, i) => { const yy = -h / 2 + 70 + 14 + i * rh + rh / 2; if (r[3] != null && t < r[3]) return; text(g, r[0], -w / 2 + 34, yy, { size: 36, color: '#cfe0ff', font: FONTS.ui, weight: 800, align: 'left' }); if (r[1]) text(g, r[1], w / 2 - 34, yy, { size: 40, color: r[2] || '#ffd23f', font: FONTS.title, weight: 800, align: 'right' }); });
  g.restore();
}
export function stamp(g, str, x, y, t, at, col = '#ff5a4d', rot = -0.1, size = 78) {
  const p = prog(t, at, at + 0.22); if (p <= 0) return; const k = 1 + (1 - ease.out(p)) * 1.2; g.save(); g.translate(x, y); g.rotate(rot); g.scale(k, k); g.globalAlpha *= clamp(p * 3);
  const w = measure(g, str, size, FONTS.title, 800) + 64; g.lineWidth = 10; g.strokeStyle = col; g.beginPath(); g.roundRect(-w / 2, -size * 0.8, w, size * 1.6, 18); g.stroke(); text(g, str, 0, 4, { size, color: col, font: FONTS.title, weight: 800, spacing: 3 }); g.restore();
}
export function bubble(g, str, x, y, t, at, tail = [0, 90], size = 42) {
  const k = pop(t, at); if (k <= 0.01) return; const w = measure(g, str, size, FONTS.title, 800) + 60, h = size + 50;
  g.save(); g.translate(x, y); g.scale(k, k); g.beginPath(); g.roundRect(-w / 2, -h / 2, w, h, 30); g.moveTo(-14, h / 2 - 2); g.lineTo(tail[0], tail[1] + h / 2); g.lineTo(18, h / 2 - 2); g.fillStyle = '#fff'; g.fill(); g.lineWidth = 6; g.strokeStyle = INK; g.lineJoin = 'round'; g.stroke();
  g.fillStyle = '#fff'; g.fillRect(-16, h / 2 - 8, 36, 12); text(g, str, 0, 3, { size, color: INK, font: FONTS.title, weight: 800 }); g.restore();
}
export function iconPop(g, name, x, y, sz, t, at, o = {}) { const k = pop(t, at); if (k <= 0.01) return; icon(g, name, x, y, sz * k, { ...o, ring: o.ring ? t : 0 }); }
export function button(g, t, at) {
  const k = pop(t, at, 0.5); if (k <= 0.01) return; g.save(); g.translate(E.W * 0.7, 480); g.scale(k * (1 + 0.03 * Math.sin(t * 5)), k * (1 + 0.03 * Math.sin(t * 5)));
  rrect(g, -270, -80, 540, 160, 40, '#ff2d2d', 8); g.fillStyle = '#fff'; g.beginPath(); g.moveTo(-200, -38); g.lineTo(-200, 38); g.lineTo(-140, 0); g.closePath(); g.fill();
  text(g, 'ISCRIVITI', 30, 4, { size: 74, color: '#fff', font: FONTS.title, weight: 800, spacing: 3 }); g.restore();
}
