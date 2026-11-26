import React from 'react';
import { INK, ACCENT } from './rig';
import '@fontsource/caveat/700.css';
import '@fontsource/anton/400.css';
export const W = 1920, H = 1080, FLOOR = 690;
export const HAND = "Caveat, cursive", SIGN = "Anton, Impact, sans-serif";
export type Cam = { z: number; x: number; y: number };
export const shade = (hex: string, k: number) => { const n = parseInt(hex.slice(1), 16); const f = (v: number) => Math.max(0, Math.min(255, Math.round(v + (k < 0 ? v * k : (255 - v) * k)))); return `#${[(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => f(v).toString(16).padStart(2, '0')).join('')}`; };
export const ease = (t: number) => (t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t));
export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const out3 = (t: number) => 1 - Math.pow(1 - clamp(t), 3);

export const L: React.FC<{ cam: Cam; d: number; blur?: number; children: React.ReactNode }> = ({ cam, d, blur, children }) => {
  const z = 1 + (cam.z - 1) * d;
  return <g filter={blur ? `url(#blur${blur})` : undefined} transform={`translate(960 540) scale(${z}) translate(${-960 - cam.x * d} ${-540 - cam.y * d})`}>{children}</g>;
};
export const Defs: React.FC = () => (
  <defs>
    <radialGradient id="hs" cx="0.38" cy="0.35" r="0.8"><stop offset="0" stopColor="rgba(255,255,255,.12)" /><stop offset="1" stopColor="rgba(120,60,20,.22)" /></radialGradient>
    <filter id="blur5" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" /></filter>
    <filter id="blur8" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="8" /></filter>
    <style>{`.c *{vector-effect:non-scaling-stroke}`}</style>
  </defs>
);
const GR: Record<string, [string, number, number]> = { day: ['#d4d0bf', 0.0, 0.3], night: ['#13192b', 0.35, 0.62], warm: ['#45221d', 0.18, 0.4], dusk: ['#48296a', 0.14, 0.4], sepia: ['#5a4a38', 0.2, 0.4], sea: ['#0b4a7a', 0.38, 0.5] };
export const Finish: React.FC<{ grade: string }> = ({ grade }) => {
  const [col, a, v] = GR[grade] || GR.day;
  return (
    <g>
      <defs><radialGradient id="vg" cx="0.5" cy="0.5" r="0.75"><stop offset="0.6" stopColor="#000" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity={v} /></radialGradient></defs>
      {a > 0 && <rect width={W} height={H} fill={col} opacity={a * 0.55} style={{ mixBlendMode: 'multiply' }} />}
      <rect width={W} height={H} fill="url(#vg)" />
    </g>
  );
};
export const Glow: React.FC<{ x: number; y: number; r: number; c: string; o?: number }> = ({ x, y, r, c, o = 0.5 }) => (
  <g><defs><radialGradient id={`g${x | 0}_${y | 0}_${r | 0}`}><stop offset="0" stopColor={c} stopOpacity={o} /><stop offset="1" stopColor={c} stopOpacity="0" /></radialGradient></defs><circle cx={x} cy={y} r={r} fill={`url(#g${x | 0}_${y | 0}_${r | 0})`} /></g>
);
export const S: React.FC<{ w: number; h: number; x: number; y: number; r?: number; fill: string; sw?: number }> = ({ w, h, x, y, r = 4, fill, sw = 4.5 }) => <rect x={x} y={y} width={w} height={h} rx={r} fill={fill} stroke={INK} strokeWidth={sw} />;
export const Poly: React.FC<{ p: number[][]; fill: string; sw?: number }> = ({ p, fill, sw = 4.5 }) => <path d={`M ${p.map((q) => q.join(' ')).join(' L ')} Z`} fill={fill} stroke={INK} strokeWidth={sw} strokeLinejoin="round" />;
export const Ln: React.FC<{ p: number[][]; sw?: number; c?: string }> = ({ p, sw = 4.5, c = INK }) => <path d={`M ${p.map((q) => q.join(' ')).join(' L ')}`} fill="none" stroke={c} strokeWidth={sw} strokeLinecap="round" strokeLinejoin="round" />;

// ---------- wall / floor patterns
export const Wall: React.FC<{ kind: 'dots' | 'panels' | 'corr' | 'brick' | 'stripes' | 'plain'; col: string; y0?: number; y1?: number }> = ({ kind, col, y0 = -300, y1 = FLOOR }) => {
  const dk = shade(col, -0.1); const items: React.ReactNode[] = [];
  if (kind === 'dots') for (let y = y0 + 24; y < y1; y += 56) for (let x = -300 + ((y / 56) % 2) * 28; x < W + 300; x += 56) items.push(<circle key={`${x}_${y}`} cx={x} cy={y} r={4} fill={dk} />);
  if (kind === 'panels') { for (let x = -300; x < W + 300; x += 220) items.push(<Ln key={x} p={[[x, y0], [x, y1]]} sw={3} c={dk} />); items.push(<Ln key="h" p={[[-300, y1 - 200], [W + 300, y1 - 200]]} sw={3} c={dk} />); }
  if (kind === 'corr') for (let x = -300; x < W + 300; x += 34) items.push(<Ln key={x} p={[[x, y0], [x, y1]]} sw={3} c={dk} />);
  if (kind === 'brick') for (let y = y0, r = 0; y < y1; y += 44, r++) { items.push(<Ln key={`r${y}`} p={[[-300, y], [W + 300, y]]} sw={3} c={dk} />); for (let x = -300 + (r % 2) * 70; x < W + 300; x += 140) items.push(<Ln key={`b${x}_${y}`} p={[[x, y], [x, y + 44]]} sw={3} c={dk} />); }
  if (kind === 'stripes') for (let x = -300; x < W + 300; x += 90) items.push(<rect key={x} x={x} y={y0} width={44} height={y1 - y0} fill={dk} />);
  return <g><rect x={-400} y={y0} width={W + 800} height={y1 - y0} fill={col} />{items}</g>;
};
export const Floor: React.FC<{ kind: 'planks' | 'asphalt' | 'checker' | 'tiles'; col: string }> = ({ kind, col }) => {
  const dk = shade(col, -0.13); const it: React.ReactNode[] = [];
  if (kind === 'planks') for (let y = FLOOR + 40; y < H + 100; y += 56) { it.push(<Ln key={y} p={[[-300, y], [W + 300, y]]} sw={3} c={dk} />); for (let x = -300 + ((y / 56) % 3) * 150; x < W + 300; x += 450) it.push(<Ln key={`${x}_${y}`} p={[[x, y], [x, y + 56]]} sw={3} c={dk} />); }
  if (kind === 'asphalt') { for (let i = 0; i < 40; i++) it.push(<rect key={i} x={(i * 331) % (W + 200) - 100} y={FLOOR + 60 + (i * 97) % 300} width={40 + (i * 13) % 50} height={4} fill={dk} />); for (let i = 0; i < 8; i++) it.push(<rect key={`m${i}`} x={i * 300 - 60} y={FLOOR + 190} width={170} height={10} fill="#c9c4a0" />); }
  if (kind === 'checker') for (let r = 0; r < 8; r++) for (let c = -3; c < 22; c++) if ((r + c) % 2) it.push(<rect key={`${r}_${c}`} x={c * 120} y={FLOOR + r * 50} width={120} height={50} fill={dk} />);
  if (kind === 'tiles') for (let r = 0; r < 8; r++) { it.push(<Ln key={r} p={[[-300, FLOOR + r * 50], [W + 300, FLOOR + r * 50]]} sw={3} c={dk} />); for (let c = -3; c < 22; c++) it.push(<Ln key={`${r}_${c}`} p={[[c * 130 + (r % 2) * 65, FLOOR + r * 50], [c * 130 + (r % 2) * 65, FLOOR + r * 50 + 50]]} sw={3} c={dk} />); }
  return <g><rect x={-400} y={FLOOR} width={W + 800} height={H} fill={col} />{it}</g>;
};
export const WindowView: React.FC<{ x: number; y: number; w: number; h: number; view: 'day' | 'night' | 'dusk'; t?: number }> = ({ x, y, w, h, view, t = 0 }) => {
  const id = `wv${x}${y}`; const top = view === 'night' ? '#13192B' : view === 'dusk' ? '#f0b789' : '#8fc6f0', bot = view === 'night' ? '#2a2f55' : view === 'dusk' ? '#db747a' : '#dff0ff';
  return (
    <g>
      <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={top} /><stop offset="1" stopColor={bot} /></linearGradient><clipPath id={`${id}c`}><rect x={x} y={y} width={w} height={h} /></clipPath></defs>
      <g clipPath={`url(#${id}c)`}><rect x={x} y={y} width={w} height={h} fill={`url(#${id})`} /><path d={`M ${x} ${y + h * 0.7} Q ${x + w * 0.3} ${y + h * 0.45} ${x + w * 0.55} ${y + h * 0.65} T ${x + w} ${y + h * 0.6} L ${x + w} ${y + h} L ${x} ${y + h} Z`} fill={view === 'night' ? '#0e1226' : '#6f9a8a'} />
        {view === 'night' ? [0, 1, 2, 3, 4].map((i) => <rect key={i} x={x + 24 + i * w / 5.6} y={y + h * 0.66 + (i % 2) * 12} width={8} height={10} fill="#ffe08a" />) : <ellipse cx={x + w * 0.7 + Math.sin(t) * 6} cy={y + h * 0.25} rx={34} ry={11} fill="rgba(255,255,255,.85)" />}
      </g>
      <S x={x} y={y} w={w} h={h} r={4} fill="none" sw={8} /><Ln p={[[x + w / 2, y], [x + w / 2, y + h]]} sw={6} /><Ln p={[[x, y + h / 2], [x + w, y + h / 2]]} sw={6} />
    </g>
  );
};

// ---------- props (drawn silhouettes)
export const Clock: React.FC<{ x: number; y: number; r?: number; h?: number; m?: number }> = ({ x, y, r = 36, h = 4, m = 0 }) => {
  const ha = (h % 12) / 12 * 2 * Math.PI - Math.PI / 2 + (m / 60) * Math.PI / 6, ma = (m / 60) * 2 * Math.PI - Math.PI / 2;
  return <g><circle cx={x} cy={y} r={r} fill="#f4f1ea" stroke={INK} strokeWidth={5} />{Array.from({ length: 12 }).map((_, i) => { const a = i * Math.PI / 6; return <Ln key={i} p={[[x + Math.cos(a) * r * 0.82, y + Math.sin(a) * r * 0.82], [x + Math.cos(a) * r * 0.92, y + Math.sin(a) * r * 0.92]]} sw={2.5} />; })}<Ln p={[[x, y], [x + Math.cos(ha) * r * 0.5, y + Math.sin(ha) * r * 0.5]]} sw={4.5} /><Ln p={[[x, y], [x + Math.cos(ma) * r * 0.75, y + Math.sin(ma) * r * 0.75]]} sw={3.5} /></g>;
};
export const Calendar: React.FC<{ x: number; y: number; label?: string }> = ({ x, y, label }) => <g><S x={x} y={y} w={72} h={84} fill="#f4f1ea" /><S x={x} y={y} w={72} h={24} fill="#c33631" />{label && <text x={x + 36} y={y + 62} textAnchor="middle" fontFamily={SIGN} fontSize={28} fill="#2a2f3c">{label}</text>}{!label && [0, 1, 2, 3, 4, 5].map((i) => <circle key={i} cx={x + 16 + (i % 3) * 20} cy={y + 44 + Math.floor(i / 3) * 20} r={4} fill="#8a8f9c" />)}</g>;
export const Sign: React.FC<{ x: number; y: number; w: number; text: string; bg?: string; fg?: string; size?: number }> = ({ x, y, w, text, bg = '#f4f1ea', fg = '#2a2f3c', size = 34 }) => <g><S x={x} y={y} w={w} h={size + 28} r={6} fill={bg} /><text x={x + w / 2} y={y + size + 6} textAnchor="middle" fontFamily={SIGN} fontSize={size} fill={fg} letterSpacing={2}>{text}</text></g>;
export const Plant: React.FC<{ x: number; y: number }> = ({ x, y }) => <g><Poly p={[[x - 26, y], [x + 26, y], [x + 20, y - 50], [x - 20, y - 50]]} fill="#a0583a" />{[0, 1, 2, 3, 4].map((i) => <ellipse key={i} cx={x + (i - 2) * 16} cy={y - 84 - (i % 2) * 16} rx={11} ry={34} transform={`rotate(${(i - 2) * 20} ${x + (i - 2) * 16} ${y - 84 - (i % 2) * 16})`} fill="#4f8a4a" stroke={INK} strokeWidth={3.5} />)}</g>;
export const Desk: React.FC<{ x: number; y: number; w: number }> = ({ x, y, w }) => <g><S x={x} y={y} w={w} h={26} fill="#6e4726" /><S x={x + 20} y={y + 26} w={22} h={120} fill="#5a3a1e" /><S x={x + w - 42} y={y + 26} w={22} h={120} fill="#5a3a1e" /></g>;
export const Cabinet: React.FC<{ x: number; y: number }> = ({ x, y }) => <g><S x={x} y={y} w={110} h={210} r={6} fill="#8d99a6" />{[0, 1, 2].map((i) => <g key={i}><Ln p={[[x, y + 70 * (i + 1) - 10], [x + 110, y + 70 * (i + 1) - 10]]} sw={3.5} /><S x={x + 40} y={y + 30 + i * 70} w={30} h={8} r={3} fill="#2a2f3c" sw={3} /></g>)}</g>;
export const Shelf: React.FC<{ x: number; y: number; w: number }> = ({ x, y, w }) => <g><S x={x} y={y} w={w} h={14} r={3} fill="#6e4726" sw={4} />{[0, 1, 2, 3, 4].map((i) => <S key={i} x={x + 14 + i * 40} y={y - 46} w={30} h={46} r={3} fill={['#c33631', '#4A6B6E', '#e0a32e', '#2C3E50', '#8FD23F'][i]} sw={3.5} />)}</g>;
export const MapPin: React.FC<{ x: number; y: number }> = ({ x, y }) => <g><S x={x} y={y} w={190} h={130} r={3} fill="#e9e2c8" /><Ln p={[[x + 20, y + 90], [x + 70, y + 50], [x + 110, y + 80], [x + 170, y + 30]]} sw={3} c="#2C3E50" /><circle cx={x + 70} cy={y + 50} r={7} fill="#c33631" stroke={INK} strokeWidth={3} /></g>;
export const Lamp: React.FC<{ x: number; y: number; col?: string }> = ({ x, y, col = '#ffe2a0' }) => (
  <g><Ln p={[[x, y], [x, FLOOR + 10]]} sw={9} /><Ln p={[[x, y], [x + 40, y]]} sw={7} /><S x={x + 20} y={y - 4} w={44} h={16} r={6} fill="#3a3f4d" sw={4} /><Glow x={x + 42} y={y + 8} r={280} c={col} o={0.55} /><path d={`M ${x + 30} ${y + 14} L ${x - 140} ${FLOOR + 150} L ${x + 220} ${FLOOR + 150} Z`} fill={col} opacity={0.13} /><ellipse cx={x + 42} cy={FLOOR + 110} rx={230} ry={46} fill={col} opacity={0.14} /></g>
);
export const Truck: React.FC<{ x: number; y: number; s?: number; lights?: boolean; halo?: boolean; name?: string; flip?: boolean }> = ({ x, y, s = 1, lights = true, halo = false, name = 'TRASPORTI', flip = false }) => (
  <g transform={`translate(${x} ${y}) scale(${flip ? -s : s} ${s})`}>
    {halo && <Glow x={0} y={-130} r={420} c={ACCENT} o={0.65} />}
    <ellipse cx={40} cy={8} rx={300} ry={16} fill="rgba(0,0,0,.3)" />
    <S x={-330} y={-250} w={460} h={220} r={8} fill="#d9d4c4" />
    {Array.from({ length: 9 }).map((_, i) => <Ln key={i} p={[[-310 + i * 50, -246], [-310 + i * 50, -34]]} sw={2.5} c="rgba(0,0,0,.18)" />)}
    <S x={-330} y={-250} w={460} h={26} r={8} fill={ACCENT} />
    <text x={-100} y={-104} textAnchor="middle" fill="#2a2f3c" fontSize={56} fontFamily={SIGN} letterSpacing={4}>{name}</text>
    <Poly p={[[140, -190], [250, -190], [310, -110], [310, -30], [140, -30]]} fill="#c33631" />
    <Poly p={[[156, -176], [236, -176], [282, -112], [156, -112]]} fill="#9fd0ff" /><Ln p={[[196, -176], [196, -112]]} sw={3} />
    <S x={296} y={-80} w={22} h={40} r={5} fill="#f6e08a" sw={3.5} />
    {lights && <g><Glow x={330} y={-60} r={170} c="#fff0aa" o={0.8} /><path d="M 318 -76 L 700 -150 L 700 20 L 318 -44 Z" fill="#fff0aa" opacity={0.18} /></g>}
    <S x={-330} y={-30} w={640} h={18} r={4} fill="#2a2f3c" />
    {[-250, -190, 40, 210].map((wx) => <g key={wx}><circle cx={wx} cy={0} r={36} fill="#1d1f27" stroke={INK} strokeWidth={4.5} /><circle cx={wx} cy={0} r={15} fill="#c9ced6" stroke={INK} strokeWidth={3} /></g>)}
  </g>
);

// ---------- text cards
export const Typed: React.FC<{ text: string; t: number; cps?: number; size?: number }> = ({ text, t, cps = 19, size = 150 }) => <text x={W / 2} y={H / 2 + size * 0.3} textAnchor="middle" fontFamily={HAND} fontWeight={700} fontSize={size} fill="#fff">{text.slice(0, Math.max(0, Math.floor(t * cps)))}</text>;
export const BlackCard: React.FC<{ text: string; t: number; cps?: number; size?: number }> = ({ text, t, cps, size }) => <g><rect width={W} height={H} fill="#000" /><Typed text={text} t={t} cps={cps} size={size} /></g>;
export const ChapterCard: React.FC<{ text: string; sub?: string }> = ({ text, sub }) => <g><rect width={W} height={H} fill="#000" /><text x={W / 2} y={H / 2 - 10} textAnchor="middle" fontFamily={SIGN} fontSize={120} fill="#F4F1EA" letterSpacing={6}>{text}</text>{sub && <text x={W / 2} y={H / 2 + 110} textAnchor="middle" fontFamily={SIGN} fontSize={80} fill={ACCENT} letterSpacing={4}>{sub}</text>}</g>;
