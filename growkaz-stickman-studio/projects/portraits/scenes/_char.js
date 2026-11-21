// Personnage "cartoon contour" : tête blanche, contour épais, aplats de couleur.
const INK = '#15131a', SKIN = '#eef0f6';
function path(g, pts) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.closePath(); }
function fillStroke(g, fill, lw = 5) { g.fillStyle = fill; g.fill(); g.lineWidth = lw; g.strokeStyle = INK; g.lineJoin = 'round'; g.lineCap = 'round'; g.stroke(); }
function ell(g, x, y, rx, ry, fill, lw = 5) { g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); fillStroke(g, fill, lw); }
function line(g, pts, lw = 6) { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(p[0], p[1]) : g.moveTo(p[0], p[1])); g.lineWidth = lw; g.strokeStyle = INK; g.lineCap = 'round'; g.lineJoin = 'round'; g.stroke(); }
export function portrait(g, x, y, s, o, t = 0) {
  g.save(); g.translate(x, y + Math.sin(t * 2) * 3 * s); g.scale(s, s);
  const bob = Math.sin(t * 2.4) * 2;
  // corps + bras
  ell(g, -78, 205, 24, 62, o.suit, 5); ell(g, 78, 205, 24, 62, o.suit, 5);
  g.beginPath(); g.moveTo(-70, 120); g.quadraticCurveTo(-92, 300, -84, 330); g.lineTo(84, 330); g.quadraticCurveTo(92, 300, 70, 120); g.closePath(); fillStroke(g, o.suit);
  if (o.vest) { path(g, [[-46, 150], [-12, 330], [-60, 330]]); fillStroke(g, o.vest, 4); path(g, [[46, 150], [12, 330], [60, 330]]); fillStroke(g, o.vest, 4); g.fillStyle = '#e8ecef'; g.fillRect(-60, 270, 120, 14); g.fillRect(-48, 296, 96, 10); }
  if (o.tie) { path(g, [[-12, 150], [12, 150], [18, 250], [0, 275], [-18, 250]]); fillStroke(g, o.tie, 4); }
  if (o.collar) { path(g, [[-14, 120], [-44, 150], [-14, 176]]); fillStroke(g, o.collar, 4); path(g, [[14, 120], [44, 150], [14, 176]]); fillStroke(g, o.collar, 4); }
  g.fillStyle = SKIN; g.fillRect(-18, 100, 36, 30); g.lineWidth = 5; g.strokeStyle = INK; g.strokeRect(-18, 100, 36, 30);
  g.save(); g.translate(0, bob);
  const hr = o.round || 92;
  // cheveux arrière / barbe arrière
  if (o.hair === 'curly') for (let i = 0; i < 9; i++) { const a = Math.PI * (1.0 + i * 0.125); ell(g, Math.cos(a) * 88, -10 + Math.sin(a) * 88, 28, 28, o.hairColor); }
  if (o.hair === 'bun') ell(g, 50, -108, 40, 40, o.hairColor);
  // tête
  g.beginPath(); g.ellipse(0, 0, hr, hr * 1.04, 0, 0, 7); fillStroke(g, SKIN, 6);
  if (o.cheeks) { ell(g, -52, 34, 16, 10, '#f6b9b9', 0); ell(g, 52, 34, 16, 10, '#f6b9b9', 0); }
  // yeux
  const ex = o.eyeGap || 34, ey = -6, sq = o.squint;
  [-1, 1].forEach((d) => { if (sq) line(g, [[d * ex - 14, ey], [d * ex + 14, ey - 4 * d]], 7); else { ell(g, d * ex, ey, 9, 11, INK, 0); g.fillStyle = '#fff'; g.beginPath(); g.arc(d * ex + 3, ey - 4, 3, 0, 7); g.fill(); } });
  // sourcils
  const br = o.brow || 'soft';
  [-1, 1].forEach((d) => { const bx = d * ex; if (br === 'angry') line(g, [[bx - d * 18, ey - 30 - 8], [bx + d * 14, ey - 20]], 8); else if (br === 'raised') line(g, [[bx - 14, ey - 30], [bx, ey - 38], [bx + 14, ey - 30]], 6); else line(g, [[bx - 14, ey - 28], [bx + 14, ey - 28 - (d < 0 ? 3 : 0)]], 6); });
  // nez
  line(g, [[-3, 12], [0, 22], [5, 22]], 4);
  // bouche
  const m = o.mouth || 'smile';
  if (m === 'smile') line(g, [[-22, 46], [-8, 56], [8, 56], [22, 46]], 6);
  else if (m === 'grin') { g.beginPath(); g.moveTo(-26, 44); g.quadraticCurveTo(0, 82, 26, 44); g.closePath(); fillStroke(g, '#fff', 5); }
  else if (m === 'flat') line(g, [[-16, 52], [16, 52]], 6);
  else if (m === 'frown') line(g, [[-20, 58], [0, 48], [20, 58]], 6);
  else if (m === 'o') ell(g, 0, 52, 9, 11, INK, 0);
  if (o.stache) { path(g, [[-32, 38], [-6, 34], [0, 40], [6, 34], [32, 38], [20, 50], [0, 44], [-20, 50]]); fillStroke(g, o.hairColor, 4); }
  if (o.beard) { g.beginPath(); g.moveTo(-86, 20); g.quadraticCurveTo(-70, 110, 0, 112); g.quadraticCurveTo(70, 110, 86, 20); g.quadraticCurveTo(50, 62, 0, 56); g.quadraticCurveTo(-50, 62, -86, 20); fillStroke(g, o.hairColor, 5); line(g, [[-20, 56], [0, 50], [20, 56]], 0); }
  if (o.glasses) { ell(g, -ex, ey, 24, 24, 'rgba(255,255,255,.35)', 5); ell(g, ex, ey, 24, 24, 'rgba(255,255,255,.35)', 5); line(g, [[-ex + 24, ey], [ex - 24, ey]], 5); }
  if (o.shades) { ell(g, -ex, ey, 26, 20, INK, 4); ell(g, ex, ey, 26, 20, INK, 4); line(g, [[-ex + 24, ey], [ex - 24, ey]], 6); }
  // cheveux avant / coiffes
  const hc = o.hairColor || '#3a2a20';
  if (o.hair === 'short') { g.beginPath(); g.moveTo(-90, -20); g.quadraticCurveTo(-96, -110, 0, -104); g.quadraticCurveTo(96, -110, 90, -20); g.quadraticCurveTo(60, -62, 0, -58); g.quadraticCurveTo(-60, -62, -90, -20); fillStroke(g, hc, 6); }
  if (o.hair === 'bun' || o.hair === 'curly') { g.beginPath(); g.moveTo(-90, -14); g.quadraticCurveTo(-96, -112, 0, -106); g.quadraticCurveTo(96, -112, 90, -14); g.quadraticCurveTo(40, -70, 0, -62); g.quadraticCurveTo(-40, -70, -90, -14); fillStroke(g, hc, 6); }
  if (o.hair === 'bald') { ell(g, -92, 6, 14, 26, hc, 5); ell(g, 92, 6, 14, 26, hc, 5); }
  if (o.hat === 'hardhat') { g.beginPath(); g.moveTo(-100, -34); g.quadraticCurveTo(-96, -128, 0, -126); g.quadraticCurveTo(96, -128, 100, -34); g.closePath(); fillStroke(g, o.hatColor || '#f2c21a', 6); g.fillStyle = o.hatColor || '#f2c21a'; g.fillRect(-118, -38, 236, 16); g.lineWidth = 5; g.strokeStyle = INK; g.strokeRect(-118, -38, 236, 16); line(g, [[0, -126], [0, -40]], 5); }
  if (o.hat === 'cap') { g.beginPath(); g.moveTo(-94, -30); g.quadraticCurveTo(-96, -118, 0, -114); g.quadraticCurveTo(96, -118, 94, -30); g.closePath(); fillStroke(g, o.hatColor, 6); path(g, [[-10, -34], [120, -26], [112, -12], [-10, -20]]); fillStroke(g, o.hatColor, 5); }
  if (o.hat === 'bowler') { ell(g, 0, -64, 130, 16, o.hatColor, 6); g.beginPath(); g.moveTo(-74, -66); g.quadraticCurveTo(-80, -150, 0, -150); g.quadraticCurveTo(80, -150, 74, -66); g.closePath(); fillStroke(g, o.hatColor, 6); g.fillStyle = '#a58a3c'; g.fillRect(-76, -92, 152, 14); }
  if (o.hat === 'beanie') { g.beginPath(); g.moveTo(-96, -26); g.quadraticCurveTo(-104, -134, 0, -134); g.quadraticCurveTo(104, -134, 96, -26); g.closePath(); fillStroke(g, o.hatColor, 6); g.fillStyle = shadeC(o.hatColor); g.fillRect(-98, -44, 196, 22); ell(g, 0, -140, 22, 22, shadeC(o.hatColor), 5); }
  g.restore(); g.restore();
}
function shadeC(c) { return c; }
export function card(g, x, y, w, h, bg, name, role) {
  g.save(); g.beginPath(); g.roundRect(x, y, w, h, 18); g.fillStyle = bg; g.fill(); g.restore();
  return () => {};
  g.save(); g.fillStyle = '#f4efe6'; g.font = '900 26px sans-serif'; g.textAlign = 'left'; g.fillText(name, x, y + h + 40); g.fillStyle = 'rgba(244,239,230,.65)'; g.font = '700 20px sans-serif'; g.fillText(role, x, y + h + 70); g.restore();
}
