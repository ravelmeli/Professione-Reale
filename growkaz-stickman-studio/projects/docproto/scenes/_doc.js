// _doc.js — documentary style: layered flat sets, drawn light, egg-torso cut-out characters
import { E, clamp, lerp, ease, prog, text, FONTS, shade, linGrad, layer } from '/engine/core.js';
import { POSES, walkPose, breathe } from '/engine/rig2d.js';
export { POSES, walkPose, breathe };
export const INK = '#111111', LW = 4.5;
const W = 1920, H = 1080, FLOOR = 690;

// ------------------------------------------------------------ helpers
const stroke = (g, lw = LW) => { g.lineWidth = lw; g.strokeStyle = INK; g.lineJoin = 'round'; g.lineCap = 'round'; g.stroke(); };
const fillst = (g, fill, lw = LW) => { g.fillStyle = fill; g.fill(); if (lw) stroke(g, lw); };
function rr(g, x, y, w, h, r, fill, lw = LW) { g.beginPath(); g.roundRect(x, y, w, h, r); fillst(g, fill, lw); }
function ell(g, x, y, rx, ry, fill, lw = LW, rot = 0) { g.beginPath(); g.ellipse(x, y, rx, ry, rot, 0, 7); fillst(g, fill, lw); }
function poly(g, pts, fill, lw = LW) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); fillst(g, fill, lw); }
function ln(g, pts, lw = LW, col = INK) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.lineWidth = lw; g.strokeStyle = col; g.lineCap = 'round'; g.lineJoin = 'round'; g.stroke(); }
const glow = (g, x, y, r, col, a = 0.5) => { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, col); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.save(); g.globalAlpha *= a; g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); g.restore(); };

// ------------------------------------------------------------ characters
const SKIN = ['#f0c9a4', '#e0a982', '#c98c63', '#8d5a3b'];
const CAST = {
  rocco(o) { const a = o.age || 30; return { skin: SKIN[0], hair: '#b8452b', hairStyle: 'side', torso: a < 40 ? '#3f7a5e' : '#2d4a7a', trim: '#e8e2d0', pants: '#2a2f3c', shoes: '#14141a', kind: a < 40 ? 'jacket' : 'shirt', hat: a >= 24 && a < 40 ? '#e0a32e' : null, stubble: a >= 24, glasses: a >= 40 && a < 50 }; },
  ciro: () => ({ skin: SKIN[1], hair: null, torso: '#7a5a3a', trim: '#e8e2d0', pants: '#2a2a30', shoes: '#14141a', kind: 'vest', stache: '#5a4a3a', brow: '#5a4a3a', age: 'old' }),
  marta: () => ({ skin: SKIN[2], hair: '#2a1a16', hairStyle: 'curly', torso: '#6a4cc0', trim: '#e8e2d0', pants: '#22222c', shoes: '#14141a', kind: 'blazer', glasses: true }),
  dino: () => ({ skin: SKIN[0], hair: '#d8d8de', hairStyle: 'none', torso: '#8a6a38', trim: '#e8e2d0', pants: '#3a3a44', shoes: '#14141a', kind: 'knit', hat: '#4a4f5c', stache: '#e8e8ee', brow: '#c8c8d0' }),
};
function mouth(g, c, expr) {
  const mx = c[0] + 6, my = c[1] + 20;
  if (expr === 'smile' || expr === 'happy') { g.beginPath(); g.moveTo(mx - 9, my - 2); g.quadraticCurveTo(mx, my + 8, mx + 9, my - 2); stroke(g, 3.5); }
  else if (expr === 'surprised') ell(g, mx, my + 2, 5, 7, INK, 0);
  else if (expr === 'sad' || expr === 'concerned') { g.beginPath(); g.moveTo(mx - 8, my + 4); g.quadraticCurveTo(mx, my - 3, mx + 8, my + 4); stroke(g, 3.5); }
  else if (expr === 'angry') { g.beginPath(); g.moveTo(mx - 8, my + 4); g.lineTo(mx + 8, my + 2); stroke(g, 4); }
  else ln(g, [[mx - 7, my + 1], [mx + 7, my + 1]], 3.5);
}
function head(g, b, c, expr, t, look, seed) {
  const R = 42;
  if (b.hairStyle === 'curly') for (let i = 0; i < 9; i++) { const a = Math.PI * (0.9 + i * 0.15); ell(g, c[0] + Math.cos(a) * 40, c[1] + Math.sin(a) * 38 + 4, 15, 15, b.hair, LW * 0.8); }
  g.beginPath(); g.arc(c[0], c[1], R, 0, 7); g.fillStyle = b.skin; g.fill();
  const gr = g.createRadialGradient(c[0] - 10, c[1] - 12, 6, c[0], c[1], R); gr.addColorStop(0, 'rgba(255,255,255,.10)'); gr.addColorStop(1, 'rgba(120,60,20,.22)'); g.fillStyle = gr; g.fill();
  g.beginPath(); g.arc(c[0], c[1], R - 6, 0.25 * Math.PI, 0.95 * Math.PI); g.lineWidth = 6; g.strokeStyle = 'rgba(120,60,20,.20)'; g.stroke();
  g.beginPath(); g.arc(c[0], c[1], R - 4, -0.55 * Math.PI, -0.15 * Math.PI); g.lineWidth = 3; g.strokeStyle = 'rgba(255,255,255,.7)'; g.stroke();
  g.beginPath(); g.arc(c[0], c[1], R, 0, 7); stroke(g);
  // hair
  if (b.hairStyle === 'side') { g.beginPath(); g.moveTo(c[0] - R, c[1] - 4); g.quadraticCurveTo(c[0] - R - 4, c[1] - R - 12, c[0] + 6, c[1] - R - 6); g.quadraticCurveTo(c[0] + R + 4, c[1] - R, c[0] + R, c[1] - 6); g.quadraticCurveTo(c[0] + 14, c[1] - 26, c[0] - 8, c[1] - 24); g.quadraticCurveTo(c[0] - 28, c[1] - 24, c[0] - R, c[1] - 4); fillst(g, b.hair); ln(g, [[c[0] - 14, c[1] - R - 2], [c[0] - 4, c[1] - 28]], 2, 'rgba(0,0,0,.35)'); ln(g, [[c[0] + 4, c[1] - R - 3], [c[0] + 10, c[1] - 28]], 2, 'rgba(0,0,0,.35)'); }
  if (b.hairStyle === 'curly') { g.beginPath(); g.moveTo(c[0] - R, c[1] - 6); g.quadraticCurveTo(c[0] - R, c[1] - R - 10, c[0], c[1] - R - 8); g.quadraticCurveTo(c[0] + R, c[1] - R - 10, c[0] + R, c[1] - 6); g.quadraticCurveTo(c[0], c[1] - 28, c[0] - R, c[1] - 6); fillst(g, b.hair); }
  if (b.stubble) { g.fillStyle = 'rgba(30,20,20,.35)'; g.beginPath(); g.arc(c[0], c[1], R - 2, 0.15 * Math.PI, 0.85 * Math.PI); g.lineTo(c[0] + 18, c[1] + 18); g.lineTo(c[0] - 18, c[1] + 18); g.fill(); }
  // face
  const ex = [c[0] - 2, c[0] + 20], ey = c[1] - 2, blink = ((t + seed) % 3.2) > 3.08;
  const lk = [clamp(look[0], -1, 1) * 3, clamp(look[1], -1, 1) * 2];
  ex.forEach((x) => { if (blink) ln(g, [[x - 5, ey], [x + 5, ey]], 3.5); else if (expr === 'surprised') { ell(g, x, ey, 7, 9, '#fff', 3); ell(g, x + lk[0], ey + lk[1], 2.6, 2.6, INK, 0); } else ell(g, x + lk[0], ey + lk[1], 4.2, 5.6, INK, 0); });
  const bc = b.brow || INK; const brow = (x, dy, tilt) => ln(g, [[x - 8, ey - 16 + dy - tilt], [x + 8, ey - 16 + dy + tilt]], 3, bc);
  if (expr === 'angry') { brow(ex[0], 2, 4); brow(ex[1], 2, -4); } else if (expr === 'sad' || expr === 'concerned') { brow(ex[0], -1, -4); brow(ex[1], -1, 4); } else if (expr === 'surprised') { brow(ex[0], -6, 0); brow(ex[1], -6, 0); } else if (expr === 'deadpan') { brow(ex[0], 0, 0); brow(ex[1], 0, 0); } else { brow(ex[0], 0, 0); brow(ex[1], -1, 0); }
  mouth(g, c, expr);
  if (b.stache) poly(g, [[c[0] - 12, c[1] + 12], [c[0] + 6, c[1] + 8], [c[0] + 26, c[1] + 12], [c[0] + 16, c[1] + 20], [c[0] + 6, c[1] + 15], [c[0] - 4, c[1] + 20]], b.stache, 3);
  if (b.glasses) { ell(g, ex[0], ey, 13, 12, 'rgba(255,255,255,.22)', 3.2); ell(g, ex[1], ey, 13, 12, 'rgba(255,255,255,.22)', 3.2); ln(g, [[ex[0] + 13, ey], [ex[1] - 13, ey]], 3); }
  if (b.hat) { g.beginPath(); g.moveTo(c[0] - R - 2, c[1] - 10); g.quadraticCurveTo(c[0] - R, c[1] - R - 14, c[0] + 4, c[1] - R - 12); g.quadraticCurveTo(c[0] + R, c[1] - R - 14, c[0] + R + 2, c[1] - 10); g.closePath(); fillst(g, b.hat); poly(g, [[c[0] + 8, c[1] - 14], [c[0] + R + 26, c[1] - 8], [c[0] + R + 22, c[1] - 1], [c[0] + 8, c[1] - 5]], shade(b.hat, -0.12), 3.5); ln(g, [[c[0] - 24, c[1] - R - 2], [c[0] - 6, c[1] - R - 8]], 2.5, 'rgba(255,255,255,.5)'); }
}
function torso(g, b, p) {
  const cx = (p.sh[0] + p.hip[0]) / 2, cy = (p.sh[1] + p.hip[1]) / 2 + 4, rx = 38, ry = 60;
  g.save(); g.beginPath(); g.ellipse(cx, cy, rx, ry, 0, 0, 7); g.clip();
  g.fillStyle = b.torso; g.fillRect(cx - rx, cy - ry, 2 * rx, 2 * ry);
  g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(cx - rx, cy + ry - 22, 2 * rx, 22); // hem band
  g.fillStyle = 'rgba(0,0,0,.16)'; g.beginPath(); g.ellipse(cx - 22, cy, 26, ry, 0, 0, 7); g.fill(); // shade
  g.fillStyle = 'rgba(255,255,255,.14)'; g.beginPath(); g.ellipse(cx + 26, cy - 10, 8, ry * 0.7, 0, 0, 7); g.fill(); // rim
  if (b.kind === 'jacket') { ln(g, [[cx + 4, cy - ry + 6], [cx + 4, cy + ry]], 3); rr(g, cx + 10, cy + 8, 18, 14, 3, 'rgba(0,0,0,.12)', 2.5); ln(g, [[cx - 24, cy - 30], [cx + 4, cy - 6], [cx + 4, cy - 30]], 2.5, 'rgba(255,255,255,.55)'); }
  if (b.kind === 'shirt') { poly(g, [[cx - 14, cy - ry + 4], [cx + 4, cy - 30], [cx + 20, cy - ry + 4]], b.trim, 3); for (let i = 0; i < 4; i++) ell(g, cx + 4, cy - 14 + i * 20, 2.5, 2.5, INK, 0); poly(g, [[cx + 1, cy - 34], [cx + 8, cy - 34], [cx + 10, cy + 12], [cx + 4, cy + 18], [cx - 2, cy + 12]], '#a8362f', 2.5); }
  if (b.kind === 'vest') { poly(g, [[cx - 14, cy - ry + 4], [cx + 4, cy - 20], [cx + 22, cy - ry + 4], [cx + 22, cy + 30], [cx - 14, cy + 30]], b.trim, 2.5); ln(g, [[cx + 4, cy - 20], [cx + 4, cy + ry]], 3); for (let i = 0; i < 3; i++) ell(g, cx + 4, cy - 4 + i * 20, 2.5, 2.5, INK, 0); }
  if (b.kind === 'blazer') { poly(g, [[cx - 18, cy - ry + 4], [cx + 4, cy - 6], [cx + 24, cy - ry + 4], [cx + 14, cy - 30], [cx - 6, cy - 30]], '#f3efe6', 2.5); ln(g, [[cx + 4, cy - 6], [cx + 4, cy + ry]], 3); }
  if (b.kind === 'knit') { for (let i = 0; i < 6; i++) ln(g, [[cx - rx + 4, cy - 40 + i * 18], [cx + rx - 4, cy - 36 + i * 18]], 2, 'rgba(0,0,0,.18)'); }
  g.restore(); g.beginPath(); g.ellipse(cx, cy, rx, ry, 0, 0, 7); stroke(g);
}
function prop(g, name, hand) {
  g.save(); g.translate(hand[0], hand[1]);
  if (name === 'clip') { g.rotate(-0.2); rr(g, -4, -40, 40, 54, 4, '#b98a52', 3.5); rr(g, 0, -34, 32, 42, 2, '#f4f1ea', 0); ln(g, [[5, -26], [26, -26]], 2.5, '#888'); ln(g, [[5, -17], [26, -17]], 2.5, '#888'); }
  if (name === 'phone') { rr(g, 0, -30, 20, 36, 4, '#222', 3); rr(g, 3, -26, 14, 26, 2, '#8fd6ff', 0); }
  if (name === 'cup') { rr(g, 0, -20, 24, 28, 6, '#f4f1ea', 3.5); ln(g, [[24, -14], [33, -8], [24, 0]], 3.5); }
  g.restore();
}
export function dchar(g, o) {
  const { x, y, s = 1.5, facing = 1, who = 'rocco', expr = 'neutral', t = 0, look = [0.5, 0], seed = 0 } = o;
  const b = CAST[who](o), p = o.pose || POSES.stand;
  g.save(); g.translate(x, y); g.scale(facing * s, s);
  g.save(); g.globalAlpha *= o.dim ? 0.45 : 0.28; g.fillStyle = '#000'; g.beginPath(); g.ellipse(-14, 4, 62, 11, 0, 0, 7); g.fill(); g.restore(); // cast-line shadow
  // back arm + legs
  ln(g, [p.sh, p.eB, p.hB], 4.5); ell(g, p.hB[0], p.hB[1], 6, 6, b.skin, 3);
  for (const [k, f] of [[p.kB, p.fB], [p.kF, p.fF]]) { ln(g, [p.hip, k, f], 11, INK); ln(g, [p.hip, k, f], 7, b.pants); ell(g, f[0] + 7, f[1] - 2, 15, 7, b.shoes, 3.5); }
  torso(g, b, p);
  ln(g, [p.sh, p.eF, p.hF], 4.5); ell(g, p.hF[0], p.hF[1], 6.5, 6.5, b.skin, 3);
  if (o.prop) prop(g, o.prop, p.hF);
  head(g, b, [p.head[0], p.head[1] - 6], expr, t, look, seed);
  g.restore();
}

// ------------------------------------------------------------ pattern fills
function wallPattern(g, kind, y0, y1, col) {
  g.save(); g.beginPath(); g.rect(-300, y0, W + 600, y1 - y0); g.clip(); const dk = shade(col, -0.10);
  if (kind === 'panels') { for (let x = -300; x < W + 300; x += 220) ln(g, [[x, y0], [x, y1]], 3, dk); ln(g, [[-300, y0 + (y1 - y0) * 0.62], [W + 300, y0 + (y1 - y0) * 0.62]], 3, dk); }
  else if (kind === 'dots') { g.fillStyle = dk; for (let y = y0 + 20; y < y1; y += 56) for (let x = -300 + ((y / 56) % 2) * 28; x < W + 300; x += 56) { g.beginPath(); g.arc(x, y, 4, 0, 7); g.fill(); } }
  else if (kind === 'corrugated') { for (let x = -300; x < W + 300; x += 34) ln(g, [[x, y0], [x, y1]], 3, dk); }
  else if (kind === 'brick') { for (let y = y0, r = 0; y < y1; y += 44, r++) { ln(g, [[-300, y], [W + 300, y]], 3, dk); for (let x = -300 + (r % 2) * 70; x < W + 300; x += 140) ln(g, [[x, y], [x, y + 44]], 3, dk); } }
  else if (kind === 'stripes') { for (let x = -300; x < W + 300; x += 90) { g.fillStyle = dk; g.fillRect(x, y0, 44, y1 - y0); } }
  g.restore();
}
function floorPattern(g, kind, y0, col) {
  g.save(); g.beginPath(); g.rect(-300, y0, W + 600, H + 300 - y0); g.clip(); const dk = shade(col, -0.12);
  if (kind === 'planks') { for (let y = y0 + 40; y < H + 100; y += 56) ln(g, [[-300, y], [W + 300, y]], 3, dk); for (let y = y0, r = 0; y < H + 100; y += 56, r++) for (let x = -300 + (r % 3) * 150; x < W + 300; x += 450) ln(g, [[x, y], [x, y + 56]], 3, dk); }
  else if (kind === 'asphalt') { for (let i = 0; i < 40; i++) { g.fillStyle = dk; g.fillRect((i * 331) % (W + 200) - 100, y0 + 60 + (i * 97) % 300, 40 + (i * 13) % 50, 4); } g.fillStyle = '#c9c4a0'; for (let i = 0; i < 8; i++) g.fillRect(i * 300 - 60, y0 + 190, 170, 10); }
  else if (kind === 'checker') { for (let r = 0; r < 8; r++) for (let c = -3; c < 22; c++) if ((r + c) % 2) { g.fillStyle = dk; g.fillRect(c * 120 + (r % 2) * 0, y0 + r * 50, 120, 50); } }
  g.restore();
}
function windowView(g, x, y, w, h, view, t) {
  rr(g, x, y, w, h, 4, '#9fd0ff', 8); g.save(); g.beginPath(); g.rect(x + 6, y + 6, w - 12, h - 12); g.clip();
  const gr = linGrad(g, 0, y, 0, y + h, view === 'night' ? ['#13192B', '#2a2f55'] : view === 'dusk' ? ['#f0b789', '#db747a'] : ['#8fc6f0', '#dff0ff']); g.fillStyle = gr; g.fillRect(x, y, w, h);
  g.fillStyle = view === 'night' ? '#0e1226' : '#6f9a8a'; g.beginPath(); g.moveTo(x, y + h * 0.7); for (let i = 0; i <= 6; i++) g.lineTo(x + i * w / 6, y + h * (0.55 + 0.1 * Math.sin(i * 1.7))); g.lineTo(x + w, y + h); g.lineTo(x, y + h); g.fill();
  if (view === 'night') for (let i = 0; i < 6; i++) { g.fillStyle = '#ffe08a'; g.fillRect(x + 20 + i * w / 7, y + h * 0.62 + (i % 2) * 14, 8, 10); }
  else { ell(g, x + w * 0.7 + Math.sin(t * 0.3) * 6, y + h * 0.25, 28, 10, 'rgba(255,255,255,.8)', 0); }
  g.restore(); ln(g, [[x + w / 2, y], [x + w / 2, y + h]], 6); ln(g, [[x, y + h / 2], [x + w, y + h / 2]], 6); rr(g, x, y, w, h, 4, null, 8);
}

// ------------------------------------------------------------ props (drawn silhouettes)
export function truck(g, x, y, s = 1, o = {}) {
  g.save(); g.translate(x, y); g.scale(s, s);
  g.save(); g.globalAlpha *= 0.3; g.fillStyle = '#000'; g.beginPath(); g.ellipse(40, 8, 300, 16, 0, 0, 7); g.fill(); g.restore();
  rr(g, -330, -250, 460, 220, 8, o.trailer || '#d9d4c4', LW); for (let i = 0; i < 9; i++) ln(g, [[-310 + i * 50, -246], [-310 + i * 50, -34]], 2.5, 'rgba(0,0,0,.18)');
  rr(g, -330, -250, 460, 26, 8, o.accent || '#8FD23F', LW); text(g, o.name || 'TRASPORTI', -100, -118, { size: 46, color: '#2a2f3c', font: FONTS.title, weight: 800, spacing: 4 });
  poly(g, [[140, -190], [250, -190], [310, -110], [310, -30], [140, -30]], o.cab || '#c33631', LW); poly(g, [[156, -176], [236, -176], [282, -112], [156, -112]], '#9fd0ff', LW); ln(g, [[196, -176], [196, -112]], 3);
  rr(g, 296, -80, 22, 40, 5, '#f6e08a', 3.5); if (o.lights !== false) glow(g, 330, -60, 140, 'rgba(255,240,170,1)', 0.7);
  rr(g, -330, -30, 640, 18, 4, '#2a2f3c', LW);
  for (const wx of [-250, -190, 40, 210]) { ell(g, wx, 0, 36, 36, '#1d1f27', LW); ell(g, wx, 0, 15, 15, '#c9ced6', 3); }
  g.restore();
}
const lamp = (g, x, y, t, col = '#ffe2a0') => { ln(g, [[x, y], [x, FLOOR + 10]], 9); ln(g, [[x, y], [x + 40, y]], 7); rr(g, x + 20, y - 4, 44, 16, 6, '#3a3f4d', 4); glow(g, x + 42, y + 8, 260, col, 0.55); g.save(); g.globalAlpha *= 0.14; g.fillStyle = col; g.beginPath(); g.moveTo(x + 30, y + 14); g.lineTo(x - 130, FLOOR + 150); g.lineTo(x + 210, FLOOR + 150); g.fill(); g.restore(); };
const clock = (g, x, y, r = 34) => { ell(g, x, y, r, r, '#f4f1ea', 5); ln(g, [[x, y], [x, y - r * 0.6]], 4); ln(g, [[x, y], [x + r * 0.45, y + r * 0.2]], 4); };
const calendar = (g, x, y) => { rr(g, x, y, 70, 82, 4, '#f4f1ea', 4); rr(g, x, y, 70, 22, 4, '#c33631', 4); for (let i = 0; i < 6; i++) ell(g, x + 14 + (i % 3) * 21, y + 40 + Math.floor(i / 3) * 20, 4, 4, '#8a8f9c', 0); };
const sign = (g, x, y, w, str, col = '#f4f1ea', fg = '#2a2f3c', size = 34) => { rr(g, x, y, w, size + 30, 6, col, 4.5); text(g, str, x + w / 2, y + (size + 30) / 2 + 2, { size, color: fg, font: FONTS.title, weight: 800 }); };
const plant = (g, x, y) => { poly(g, [[x - 26, y], [x + 26, y], [x + 20, y - 50], [x - 20, y - 50]], '#a0583a', 4); for (let i = 0; i < 5; i++) { g.beginPath(); g.ellipse(x + (i - 2) * 16, y - 80 - (i % 2) * 16, 11, 34, (i - 2) * 0.35, 0, 7); fillst(g, '#4f8a4a', 3.5); } };
const desk = (g, x, y, w) => { rr(g, x, y, w, 26, 4, '#6e4726', LW); rr(g, x + 20, y + 26, 22, 120, 3, '#5a3a1e', LW); rr(g, x + w - 42, y + 26, 22, 120, 3, '#5a3a1e', LW); };
const cabinet = (g, x, y) => { rr(g, x, y, 110, 210, 6, '#8d99a6', LW); for (let i = 0; i < 3; i++) { ln(g, [[x, y + 70 * (i + 1) - 10], [x + 110, y + 70 * (i + 1) - 10]], 3.5); rr(g, x + 40, y + 30 + i * 70, 30, 8, 3, '#2a2f3c', 3); } };
const shelf = (g, x, y, w) => { rr(g, x, y, w, 14, 3, '#6e4726', 4); for (let i = 0; i < 5; i++) rr(g, x + 14 + i * 40, y - 46, 30, 46, 3, ['#c33631', '#4A6B6E', '#e0a32e', '#2C3E50', '#8FD23F'][i], 3.5); };
const mapPin = (g, x, y) => { rr(g, x, y, 190, 130, 3, '#e9e2c8', 4); ln(g, [[x + 20, y + 90], [x + 70, y + 50], [x + 110, y + 80], [x + 170, y + 30]], 3, '#2C3E50'); ell(g, x + 70, y + 50, 7, 7, '#c33631', 3); ell(g, x + 170, y + 30, 7, 7, '#c33631', 3); };

// ------------------------------------------------------------ sets (elevation: back wall / mid props / cast line / foreground)
const GRADE = { day: ['#d4d0bf', 0.0, 0.35], night: ['#13192b', 0.35, 0.62], warm: ['#45221d', 0.18, 0.4], dusk: ['#48296a', 0.14, 0.4] };
export function dset(g, t, name, o = {}, cam = { z: 1, x: 0 }) {
  const L = (depth, fn) => layer(g, cam, depth, fn);
  if (name === 'ufficio') {
    L(0.35, () => { g.fillStyle = '#c9c1a8'; g.fillRect(-400, -300, W + 800, FLOOR + 300); wallPattern(g, 'dots', -300, FLOOR, '#c9c1a8'); windowView(g, 1180, 140, 420, 330, o.view || 'day', t); });
    L(0.6, () => { clock(g, 700, 170); calendar(g, 150, 150); mapPin(g, 360, 140); shelf(g, 880, 330, 260); cabinet(g, 1650, FLOOR - 210); plant(g, 90, FLOOR); sign(g, 760, 260, 0, ''); });
    L(0.8, () => { g.fillStyle = '#7a5a3a'; g.fillRect(-400, FLOOR, W + 800, H); floorPattern(g, 'planks', FLOOR, '#7a5a3a'); desk(g, 1000, FLOOR - 120, 520); });
    o._glow = null;
  } else if (name === 'piazzale') {
    L(0.35, () => { const gr = linGrad(g, 0, -300, 0, FLOOR, ['#0A0C18', '#1d2748']); g.fillStyle = gr; g.fillRect(-400, -300, W + 800, FLOOR + 300); for (let i = 0; i < 40; i++) ell(g, (i * 211) % W, 40 + (i * 53) % 320, 2, 2, '#cfd8f0', 0); g.fillStyle = '#10162a'; g.beginPath(); g.moveTo(-400, 520); for (let i = 0; i <= 10; i++) g.lineTo(-400 + i * 280, 450 - 60 * Math.abs(Math.sin(i * 1.3))); g.lineTo(W + 400, FLOOR); g.lineTo(-400, FLOOR); g.fill(); });
    L(0.55, () => { rr(g, 1180, 240, 560, 450, 4, '#2a3350', LW); wallPattern(g, 'corrugated', 244, 686, '#2a3350'); rr(g, 1290, 360, 340, 330, 3, o.lit === false ? '#12162a' : '#f0d58a', LW); for (let i = 1; i < 6; i++) ln(g, [[1290, 360 + i * 55], [1630, 360 + i * 55]], 3, 'rgba(0,0,0,.25)'); sign(g, 1300, 260, 320, 'MAGAZZINO', '#2a2f3c', '#f4f1ea', 40); });
    L(0.8, () => { g.fillStyle = '#1c2238'; g.fillRect(-400, FLOOR, W + 800, H); floorPattern(g, 'asphalt', FLOOR, '#1c2238'); lamp(g, 250, 170, t); if (o.truck !== false) truck(g, 720, FLOOR + 40, 0.9, { lights: false }); });
  } else if (name === 'strada') {
    L(0.3, () => { const gr = linGrad(g, 0, -300, 0, FLOOR, o.dusk ? ['#48296a', '#db747a', '#f0b789'] : ['#6aa7e0', '#dff0ff']); g.fillStyle = gr; g.fillRect(-400, -300, W + 800, FLOOR + 300); ell(g, 1500, 360, 90, 90, o.dusk ? '#ffd9a0' : '#fff6cf', 0); for (let i = 0; i < 4; i++) ell(g, 300 + i * 420 + ((t * 8) % 60), 160 + (i % 2) * 60, 120, 28, 'rgba(255,255,255,.75)', 0); });
    L(0.45, () => { g.fillStyle = o.dusk ? '#4a3a5a' : '#8aaec0'; g.beginPath(); g.moveTo(-400, 560); for (let i = 0; i <= 8; i++) g.lineTo(-400 + i * 330, 470 - 80 * Math.abs(Math.sin(i * 1.1))); g.lineTo(W + 400, FLOOR); g.lineTo(-400, FLOOR); g.fill(); });
    L(0.6, () => { g.fillStyle = o.dusk ? '#3a4a3a' : '#5b8a58'; g.fillRect(-400, 600, W + 800, 100); for (let i = 0; i < 14; i++) { ln(g, [[(i * 160 - ((t * 120) % 160)), 600], [(i * 160 - ((t * 120) % 160)), 560]], 6); ell(g, (i * 160 - ((t * 120) % 160)), 552, 22, 28, '#3d6b3d', 3.5); } });
    L(0.8, () => { g.fillStyle = '#3a3f4d'; g.fillRect(-400, FLOOR - 20, W + 800, H); g.fillStyle = '#f4f1ea'; g.fillRect(-400, FLOOR - 4, W + 800, 6); for (let i = 0; i < 12; i++) { g.fillStyle = '#e0a32e'; g.fillRect(i * 200 - ((t * 400) % 200), FLOOR + 170, 110, 12); } truck(g, 1100 + Math.sin(t * 2) * 3, FLOOR + 120, 0.8); });
  } else if (name === 'casa') {
    L(0.35, () => { g.fillStyle = '#d9b68a'; g.fillRect(-400, -300, W + 800, FLOOR + 300); wallPattern(g, 'stripes', -300, FLOOR, '#d9b68a'); windowView(g, 160, 150, 360, 300, 'dusk', t); glow(g, 1500, 200, 380, '#ffd9a0', 0.5); });
    L(0.6, () => { clock(g, 760, 170); rr(g, 940, 130, 150, 110, 4, '#f4f1ea', 4); ell(g, 1015, 185, 30, 30, '#8FD23F', 3); sign(g, 1360, 120, 0, ''); rr(g, 1480, 280, 260, 410, 8, '#e8e4da', LW); ln(g, [[1480, 460], [1740, 460]], 4); rr(g, 1710, 340, 10, 70, 4, '#8a8f9c', 3); plant(g, 760, FLOOR); });
    L(0.8, () => { g.fillStyle = '#8a6a4a'; g.fillRect(-400, FLOOR, W + 800, H); floorPattern(g, 'checker', FLOOR, '#8a6a4a'); desk(g, 1000, FLOOR - 120, 360); glow(g, 1500, FLOOR + 80, 330, '#ffd9a0', 0.4); });
  }
  // light pools & lamp discs are baked per set above
}
export function finish(g, t, grade = 'day', cam = {}) {
  const [col, a, v] = GRADE[grade] || GRADE.day;
  g.save(); g.globalCompositeOperation = 'multiply'; g.globalAlpha = 0.28; g.fillStyle = col === '#d4d0bf' ? '#ffffff' : col; g.fillRect(0, 0, W, H); g.restore();
  const gr = g.createRadialGradient(W / 2, H / 2, Math.hypot(W, H) * 0.5 * 0.45, W / 2, H / 2, Math.hypot(W, H) * 0.5); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, `rgba(0,0,0,${v})`); g.fillStyle = gr; g.fillRect(0, 0, W, H);
}
