// Personnage "cartoon contour" : tête blanche, contour épais, aplats de couleur.
const INK = '#15131a', SKIN = '#eef0f6';
function path(g, pts) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); }
function fillStroke(g, fill, lw = 5) { g.fillStyle = fill; g.fill(); g.lineWidth = lw; g.strokeStyle = INK; g.lineJoin = 'round'; g.lineCap = 'round'; g.stroke(); }
function ell(g, x, y, rx, ry, fill, lw = 5) { g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); fillStroke(g, fill, lw); }
function line(g, pts, lw = 6) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.lineWidth = lw; g.strokeStyle = INK; g.lineCap = 'round'; g.lineJoin = 'round'; g.stroke(); }
export function portrait(g, x, y, s, o, t = 0) {
  g.save(); g.translate(x, y); g.scale(s, s);
  const bob = Math.sin(t * 2.2) * 2.5, hc = o.hairColor || '#4a2f22', ex = 27, ey = 6;
  // bras (capsules écartées)
  [-1, 1].forEach((d) => { g.save(); g.translate(d * 88, 205); g.rotate(d * -0.12); g.beginPath(); g.roundRect(-20, -62, 40, 130, 20); fillStroke(g, o.suit, 5); g.restore(); });
  // buste
  g.beginPath(); g.roundRect(-66, 128, 132, 190, 30); fillStroke(g, o.suit, 5);
  if (o.vest) { path(g, [[-40, 134], [-8, 318], [-66, 318], [-66, 160]]); fillStroke(g, o.vest, 4); path(g, [[40, 134], [8, 318], [66, 318], [66, 160]]); fillStroke(g, o.vest, 4); g.fillStyle = '#e8ecef'; g.fillRect(-64, 262, 128, 12); }
  path(g, [[-14, 130], [14, 130], [16, 280], [0, 300], [-16, 280]]); fillStroke(g, '#f4f4f8', 4);
  if (o.tie) { path(g, [[-9, 150], [9, 150], [13, 250], [0, 268], [-13, 250]]); fillStroke(g, o.tie, 3); }
  if (o.badge) { g.fillStyle = o.badge; g.fillRect(34, 190, 24, 14); g.lineWidth = 3; g.strokeStyle = INK; g.strokeRect(34, 190, 24, 14); }
  g.save(); g.translate(0, bob);
  if (o.hair === 'bun') ell(g, 60, -112, 38, 38, hc);
  if (o.hair === 'curly') for (let i = 0; i < 9; i++) { const a = Math.PI * (1.0 + i * 0.125); ell(g, Math.cos(a) * 98, -8 + Math.sin(a) * 98, 28, 28, hc); }
  // tête : grand cercle blanc légèrement dégradé
  const gr = g.createRadialGradient(-30, -40, 10, 0, 0, 110); gr.addColorStop(0, '#ffffff'); gr.addColorStop(1, '#dde1ea');
  g.beginPath(); g.arc(0, 0, 100, 0, 7); fillStroke(g, gr, 6);
  if (o.cheeks) { ell(g, -58, 36, 14, 9, '#f6b9b9', 0); ell(g, 58, 36, 14, 9, '#f6b9b9', 0); }
  // yeux
  [-1, 1].forEach((d) => { if (o.squint) line(g, [[d * ex - 14, ey + 2], [d * ex + 14, ey - 3 * d]], 7); else { ell(g, d * ex, ey, 9, 12, INK, 0); g.fillStyle = '#fff'; g.beginPath(); g.arc(d * ex + 3, ey - 4, 2.6, 0, 7); g.fill(); } });
  const br = o.brow || 'none';
  [-1, 1].forEach((d) => { const bx = d * ex; if (br === 'angry') line(g, [[bx - d * 20, ey - 40], [bx + d * 14, ey - 26]], 8); else if (br === 'raised') line(g, [[bx - 14, ey - 32], [bx, ey - 40], [bx + 14, ey - 32]], 5); else if (br === 'soft') line(g, [[bx - 14, ey - 30], [bx, ey - 34], [bx + 14, ey - 30]], 5); });
  const m = o.mouth || 'smile';
  if (m === 'smile') line(g, [[-20, 44], [-8, 52], [8, 52], [20, 44]], 6);
  else if (m === 'grin') { g.beginPath(); g.moveTo(-26, 42); g.quadraticCurveTo(0, 82, 26, 42); g.closePath(); fillStroke(g, '#fff', 5); }
  else if (m === 'flat') line(g, [[-16, 52], [16, 52]], 6);
  else if (m === 'o') ell(g, 0, 52, 8, 11, INK, 0);
  if (o.stache) { path(g, [[-34, 36], [-6, 32], [0, 38], [6, 32], [34, 36], [22, 50], [0, 42], [-22, 50]]); fillStroke(g, hc, 4); }
  if (o.beard) { g.beginPath(); g.moveTo(-96, 16); g.quadraticCurveTo(-80, 112, 0, 114); g.quadraticCurveTo(80, 112, 96, 16); g.quadraticCurveTo(52, 60, 0, 54); g.quadraticCurveTo(-52, 60, -96, 16); fillStroke(g, hc, 5); line(g, [[-16, 54], [0, 48], [16, 54]], 5); }
  if (o.glasses) { ell(g, -ex, ey, 24, 24, 'rgba(255,255,255,.3)', 5); ell(g, ex, ey, 24, 24, 'rgba(255,255,255,.3)', 5); line(g, [[-ex + 24, ey], [ex - 24, ey]], 5); }
  if (o.shades) { ell(g, -ex, ey, 26, 19, INK, 4); ell(g, ex, ey, 26, 19, INK, 4); line(g, [[-ex + 24, ey], [ex - 24, ey]], 6); }
  if (o.hair === 'short' || o.hair === 'bun' || o.hair === 'curly') { g.beginPath(); g.moveTo(-99, -14); g.quadraticCurveTo(-104, -112, 0, -106); g.quadraticCurveTo(104, -112, 99, -14); g.quadraticCurveTo(50, -64, 0, -56); g.quadraticCurveTo(-50, -64, -99, -14); fillStroke(g, hc, 6); }
  if (o.hat === 'hardhat') { g.beginPath(); g.moveTo(-104, -30); g.quadraticCurveTo(-100, -132, 0, -130); g.quadraticCurveTo(100, -132, 104, -30); g.closePath(); fillStroke(g, o.hatColor, 6); g.fillStyle = o.hatColor; g.fillRect(-122, -34, 244, 16); g.lineWidth = 5; g.strokeStyle = INK; g.strokeRect(-122, -34, 244, 16); line(g, [[0, -130], [0, -36]], 5); }
  if (o.hat === 'cap') { g.beginPath(); g.moveTo(-98, -26); g.quadraticCurveTo(-100, -122, 0, -118); g.quadraticCurveTo(100, -122, 98, -26); g.closePath(); fillStroke(g, o.hatColor, 6); path(g, [[-10, -30], [124, -22], [116, -8], [-10, -16]]); fillStroke(g, o.hatColor, 5); }
  if (o.hat === 'bowler') { ell(g, 0, -68, 134, 16, o.hatColor, 6); g.beginPath(); g.moveTo(-78, -70); g.quadraticCurveTo(-84, -156, 0, -156); g.quadraticCurveTo(84, -156, 78, -70); g.closePath(); fillStroke(g, o.hatColor, 6); g.fillStyle = '#a58a3c'; g.fillRect(-80, -96, 160, 14); }
  if (o.hat === 'beanie') { g.beginPath(); g.moveTo(-100, -22); g.quadraticCurveTo(-108, -138, 0, -138); g.quadraticCurveTo(108, -138, 100, -22); g.closePath(); fillStroke(g, o.hatColor, 6); ell(g, 0, -144, 22, 22, o.hatColor, 5); g.fillStyle = 'rgba(0,0,0,.18)'; g.fillRect(-101, -46, 202, 22); }
  g.restore(); g.restore();
}
function shadeC(c) { return c; }
export function card(g, x, y, w, h, bg, name, role) {
  g.save(); g.beginPath(); g.roundRect(x, y, w, h, 18); g.fillStyle = bg; g.fill(); g.restore();
  return () => {};
  g.save(); g.fillStyle = '#f4efe6'; g.font = '900 26px sans-serif'; g.textAlign = 'left'; g.fillText(name, x, y + h + 40); g.fillStyle = 'rgba(244,239,230,.65)'; g.font = '700 20px sans-serif'; g.fillText(role, x, y + h + 70); g.restore();
}
