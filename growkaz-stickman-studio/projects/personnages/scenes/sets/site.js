import { E, V, mood, layer, rr, seg, circle, linGrad, glow, alpha, shade } from '/engine/core.js';
import * as FX from '/engine/fx2d.js';
export const siteGround = () => E.H * V(0.8, 0.68);
export function site(g, t, cam, o = {}) {
  const M = mood(o.mood || 'golden'), GY = siteGround(), CX = E.W / 2;
  layer(g, cam, 0.3, (g) => {
    g.fillStyle = linGrad(g, 0, -E.H, 0, GY, M.sky); g.fillRect(-E.W, -E.H, E.W * 3, GY + E.H);
    FX.sun(g, CX + 380, GY - 300, 70, '#fff7e6', M.key, 4);
    FX.skyline(g, { x: -200, y: GY, w: E.W + 400, maxH: 420, color: alpha(shade(M.wall, -0.3), 0.8), windowColor: alpha(M.practical, 0.7), seed: 7 });
  });
  layer(g, cam, 0.7, (g) => {
    // crane + scaffolding silhouette
    const kx = CX + 560; g.fillStyle = shade(M.wall, -0.55);
    g.fillRect(kx, GY - 640, 16, 640); g.fillRect(kx - 380, GY - 640, 520, 12);
    seg(g, [[kx - 340, GY - 628], [kx - 340, GY - 470]], 3, shade(M.wall, -0.55)); g.fillRect(kx - 370, GY - 470, 60, 40);
    for (let i = 0; i < 5; i++) { g.fillRect(CX - 900 + i * 90, GY - 330, 8, 330); } g.fillRect(CX - 920, GY - 330, 420, 8); g.fillRect(CX - 920, GY - 190, 420, 8);
    g.fillStyle = linGrad(g, 0, GY - 20, 0, GY + 600, [shade(M.floor, 0.1), M.dark]); g.fillRect(-E.W, GY - 20, E.W * 3, E.H * 2);
    FX.floorLines(g, GY - 20, GY + 600, 'rgba(0,0,0,.2)', 0.07);
  });
  return { GY, CX, M };
}
