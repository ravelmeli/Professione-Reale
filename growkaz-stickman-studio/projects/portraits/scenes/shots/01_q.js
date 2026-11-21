import { E, registerShot, text, FONTS, alpha } from '/engine/core.js';
import { portrait, card } from '../_char.js';
const C = [
 { n: 'Rocco, il nuovo', r: 'Casco giallo troppo grande, gilet arancione', bg: '#2f4a3a', o: { suit: '#e8751a', vest: '#f08a24', badge: '#f2c21a', hat: 'hardhat', hatColor: '#f2c21a', cheeks: true, mouth: 'smile' } },
 { n: 'Mastro Bruno, il caposquadra', r: 'Baffi, cappello grigio, sguardo severo', bg: '#3a3426', o: { suit: '#5a6270', hat: 'cap', hatColor: '#6b6f78', hair: 'bald', hairColor: '#2a2a2e', stache: true, mouth: 'flat', brow: 'angry', squint: true } },
 { n: 'Giada, la sicurezza', r: 'Chignon, occhiali, tablet delle ispezioni', bg: '#2b3550', o: { suit: '#ffffff', collar: '#e8ecef', hat: 'hardhat', hatColor: '#e8ecef', hair: 'bun', hairColor: '#8a3a2a', glasses: true, mouth: 'smile', brow: 'soft' } },
 { n: 'Nonno Tonino, il veterano', r: 'Barba bianca, berretto, ha visto tutto', bg: '#2a3a3a', o: { suit: '#3a6ea5', hat: 'beanie', hatColor: '#d64a33', hair: 'bald', hairColor: '#e5e6ea', beard: true, mouth: 'smile', brow: 'soft', cheeks: true } },
 { n: 'Ing. Valenti, il committente', r: 'Bombetta, cravatta rossa, mai in cantiere', bg: '#3a2430', o: { suit: '#222a3a', tie: '#c8283a', collar: '#ffffff', hat: 'bowler', hatColor: '#1c1c20', hair: 'bald', hairColor: '#1c1c20', mouth: 'smile', squint: true, brow: 'soft' } },
 { n: 'Sara, la carpentiera', r: 'Ricci, occhiali da sole, sorriso largo', bg: '#2a3a2f', o: { suit: '#1ea7a1', collar: '#e8ecef', hair: 'curly', hairColor: '#2b1a12', shades: true, mouth: 'grin', brow: 'soft', cheeks: true } },
];
registerShot('q1', { draw(g, t) {
  g.fillStyle = '#121216'; g.fillRect(0, 0, E.W, E.H);
  C.forEach((c, i) => { const col = i % 3, row = Math.floor(i / 3), w = 400, h = 400, x = 240 + col * 480, y = 40 + row * 520;
    g.save(); g.beginPath(); g.roundRect(x, y, w, h, 18); g.clip(); g.fillStyle = c.bg; g.fillRect(x, y, w, h); portrait(g, x + w / 2, y + 160, 1.0, c.o, t + i); g.restore();
    text(g, c.n, x + w / 2, y + h + 40, { size: 30, color: '#f4efe6', font: FONTS.ui, weight: 900 }); text(g, c.r, x + w / 2, y + h + 76, { size: 21, color: alpha('#f4efe6', .7), font: FONTS.ui, weight: 700 }); });
} });
