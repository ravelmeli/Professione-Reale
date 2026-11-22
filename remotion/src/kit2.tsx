import React from 'react';
import { Cam, L, W as CW, H, FLOOR, S, Poly, Ln, Glow, Clock, Calendar, Sign, Truck, Wall, Floor, WindowView, Plant, Desk, Lamp, SIGN, ease, clamp, out3, shade } from './kit';
import { INK, ACCENT } from './rig';
import words from './words.json';

export const WORDS: { w: string; s: number }[] = (words as any).words.map((x: any) => ({ w: String(x.word || x.text).toLowerCase().replace(/[^\w'àèéìòù]/g, ''), s: x.start }));
export const wt = (q: string, after = 0): number => { const k = q.toLowerCase(); const r = WORDS.find((x) => x.s >= after - 0.05 && x.w.startsWith(k)); return r ? r.s : after; };

// ---------------------------------------------------------- icons / objects
export type ObjSpec = { k: string; x: number; y: number; s?: number; at?: number; e?: 'slide' | 'drop' | 'slam' | 'grow' | 'on'; text?: string; col?: string; v?: number };
const Moon = () => <g><circle r={40} fill="#fff3c4" stroke={INK} strokeWidth={4.5} /><circle cx={16} cy={-8} r={34} fill="#10162a" /></g>;
const Heart = () => <path d="M 0 36 C -60 -4 -34 -50 0 -20 C 34 -50 60 -4 0 36 Z" fill="#e5392b" stroke={INK} strokeWidth={5} />;
const KINDS: Record<string, (o: ObjSpec, t: number) => React.ReactNode> = {
  clock: (o) => <Clock x={0} y={0} r={50} h={o.v ?? 4} m={0} />,
  cal: (o) => <Calendar x={-36} y={-42} label={o.text} />,
  tacho: (o, t) => <g><circle r={60} fill="#f4f1ea" stroke={INK} strokeWidth={6} />{Array.from({ length: 24 }).map((_, i) => <Ln key={i} p={[[Math.cos(i * Math.PI / 12) * 46, Math.sin(i * Math.PI / 12) * 46], [Math.cos(i * Math.PI / 12) * 56, Math.sin(i * Math.PI / 12) * 56]]} sw={3} />)}<path d="M 0 0 L 40 0 A 40 40 0 0 1 -22 33 Z" fill={ACCENT} stroke={INK} strokeWidth={3} /><Ln p={[[0, 0], [Math.cos(t) * 48, Math.sin(t) * 48]]} sw={5} c="#c33631" /></g>,
  truck: (o) => <Truck x={0} y={40} s={0.35} name={o.text || 'TRASPORTI'} lights={false} />,
  crate: () => <g><S x={-46} y={-34} w={92} h={72} r={6} fill="#d9a45c" /><Ln p={[[-46, -8], [46, -8]]} sw={4} /><Ln p={[[-46, 16], [46, 16]]} sw={4} /></g>,
  doc: () => <g><S x={-38} y={-50} w={76} h={100} r={6} fill="#f4f1ea" />{[0, 1, 2, 3].map((i) => <Ln key={i} p={[[-24, -30 + i * 20], [i === 3 ? 4 : 24, -30 + i * 20]]} sw={3.5} c="#8a8f9c" />)}</g>,
  coin: () => <g><circle r={44} fill="#e0a32e" stroke={INK} strokeWidth={5} /><text y={16} textAnchor="middle" fontFamily={SIGN} fontSize={52} fill="#111">€</text></g>,
  fuel: () => <g><S x={-34} y={-52} w={68} h={104} r={10} fill="#c33631" /><S x={-22} y={-40} w={44} h={30} r={4} fill="#9fd0ff" sw={3} /><Ln p={[[34, -30], [56, -20], [56, 20], [48, 36]]} sw={7} /></g>,
  wheel: () => <g><circle r={52} fill="none" stroke={INK} strokeWidth={16} /><circle r={52} fill="none" stroke="#3a3f55" strokeWidth={9} /><Ln p={[[-52, 0], [52, 0]]} sw={8} c="#3a3f55" /><Ln p={[[0, 0], [0, 52]]} sw={8} c="#3a3f55" /></g>,
  flag: (o) => { const cols: Record<string, string[]> = { fr: ['#2a5cd0', '#fff', '#e5392b'], it: ['#2fa84f', '#fff', '#e5392b'], de: ['#17141f', '#e5392b', '#ffd23f'], es: ['#e5392b', '#ffd23f', '#e5392b'], at: ['#e5392b', '#fff', '#e5392b'] }; const c = cols[o.text || 'it']; const v = o.text === 'fr' || o.text === 'it'; return <g><Ln p={[[-60, -42], [-60, 100]]} sw={8} />{c.map((cc, i) => <rect key={i} x={v ? -56 + i * 37 : -56} y={v ? -40 : -40 + i * 26} width={v ? 38 : 112} height={v ? 78 : 27} fill={cc} />)}<rect x={-56} y={-40} width={112} height={78} fill="none" stroke={INK} strokeWidth={5} /></g>; },
  mount: () => <g><Poly p={[[-80, 40], [-24, -50], [6, -10], [30, -56], [86, 40]]} fill="#8a93a6" /><Poly p={[[-34, -30], [-24, -50], [-12, -30], [-24, -24]]} fill="#fff" sw={0} /><Poly p={[[18, -36], [30, -56], [42, -36], [30, -30]]} fill="#fff" sw={0} /></g>,
  snow: () => <g>{[0, 1, 2].map((i) => <Ln key={i} p={[[Math.cos(i * Math.PI / 3) * 50, Math.sin(i * Math.PI / 3) * 50], [-Math.cos(i * Math.PI / 3) * 50, -Math.sin(i * Math.PI / 3) * 50]]} sw={9} c="#bfe6ff" />)}</g>,
  barrier: () => <g><S x={-74} y={-10} w={148} h={22} r={6} fill="#fff" />{[0, 1, 2, 3].map((i) => <rect key={i} x={-64 + i * 36} y={-8} width={18} height={18} fill="#e5392b" />)}<S x={-92} y={-34} w={22} h={92} r={5} fill="#8a93a6" /></g>,
  bed: () => <g><S x={-62} y={0} w={124} h={30} r={6} fill="#8a5a2b" /><S x={-58} y={-24} w={116} h={28} r={8} fill="#4aa3ff" /><S x={-58} y={-32} w={36} h={20} r={8} fill="#fff" sw={3.5} /></g>,
  house: () => <g><Poly p={[[-60, -4], [0, -56], [60, -4]]} fill="#c33631" /><S x={-44} y={-4} w={88} h={64} r={4} fill="#f4f1ea" /><S x={-10} y={20} w={20} h={40} r={3} fill="#6e4726" sw={3.5} /></g>,
  family: () => <g><circle cx={-26} cy={-30} r={14} fill="#f4f1ea" stroke={INK} strokeWidth={4.5} /><S x={-40} y={-14} w={28} h={46} r={10} fill="#e86aa0" /><circle cx={26} cy={-30} r={14} fill="#f4f1ea" stroke={INK} strokeWidth={4.5} /><S x={12} y={-14} w={28} h={46} r={10} fill="#4aa3ff" /><circle cy={-4} r={10} fill="#f4f1ea" stroke={INK} strokeWidth={4.5} /><S x={-9} y={8} w={18} h={28} r={8} fill="#ffd23f" /></g>,
  cake: () => <g><S x={-44} y={-4} w={88} h={48} r={8} fill="#ffb3c7" />{[-1, 0, 1].map((i) => <g key={i}><Ln p={[[i * 24, -6], [i * 24, -32]]} sw={7} c="#4aa3ff" /><ellipse cx={i * 24} cy={-40} rx={6} ry={9} fill="#ffb02e" stroke={INK} strokeWidth={3} /></g>)}</g>,
  heart: () => <Heart />,
  moon: () => <Moon />,
  warn: () => <g><Poly p={[[0, -52], [54, 40], [-54, 40]]} fill="#ffd23f" /><rect x={-4} y={-22} width={8} height={36} fill={INK} /><circle cy={28} r={5} fill={INK} /></g>,
  tick: () => <g><circle r={46} fill="#3ddc84" stroke={INK} strokeWidth={5} /><Ln p={[[-22, 2], [-6, 22], [26, -18]]} sw={11} c="#fff" /></g>,
  cross: () => <g><circle r={46} fill="#e5392b" stroke={INK} strokeWidth={5} /><Ln p={[[-20, -20], [20, 20]]} sw={11} c="#fff" /><Ln p={[[20, -20], [-20, 20]]} sw={11} c="#fff" /></g>,
  wrench: () => <g transform="rotate(-40)"><S x={-9} y={-6} w={18} h={96} r={8} fill="#c9ced6" /><circle cy={-26} r={28} fill="#c9ced6" stroke={INK} strokeWidth={5} /><rect x={-9} y={-64} width={18} height={30} fill="#222836" /></g>,
  tire: () => <g><circle r={50} fill="#1d1f27" stroke={INK} strokeWidth={5} /><circle r={24} fill="#c9ced6" stroke={INK} strokeWidth={4} /></g>,
  pin: () => <g><path d="M 0 52 C -52 -4 -40 -52 0 -52 C 40 -52 52 -4 0 52 Z" fill="#e5392b" stroke={INK} strokeWidth={5} /><circle cy={-16} r={15} fill="#fff" /></g>,
  sign: (o) => <Sign x={-(o.text!.length * 13 + 30)} y={-30} w={o.text!.length * 26 + 60} text={o.text!} bg={o.col || '#f4f1ea'} fg={o.col === '#c33631' || o.col === '#2a2f3c' ? '#f4f1ea' : '#2a2f3c'} size={o.s ? 34 : 34} />,
  stamp: (o) => <g transform="rotate(-8)"><rect x={-(o.text!.length * 15 + 30)} y={-40} width={o.text!.length * 30 + 60} height={80} rx={12} fill="none" stroke={o.col || '#c33631'} strokeWidth={8} /><text y={16} textAnchor="middle" fontFamily={SIGN} fontSize={48} fill={o.col || '#c33631'} letterSpacing={3}>{o.text}</text></g>,
  phone: (o) => <g><S x={-60} y={-110} w={120} h={220} r={18} fill="#1d1f27" sw={5} /><S x={-52} y={-98} w={104} h={196} r={10} fill="#f4f1ea" sw={0} />{o.text === 'ring' && <g><path d="M 78 -40 q 20 40 0 80" fill="none" stroke="#e5392b" strokeWidth={6} /><path d="M 98 -60 q 30 60 0 120" fill="none" stroke="#e5392b" strokeWidth={6} /></g>}<S x={-40} y={20} w={80} h={30} r={8} fill="#e5392b" sw={3} /></g>,
  gauge: (o) => { const a = Math.PI * (0.75 + (o.v ?? 0.5) * 1.5); return <g><circle r={60} fill="#f4f1ea" stroke={INK} strokeWidth={6} /><Ln p={[[0, 0], [Math.cos(a) * 42, Math.sin(a) * 42]]} sw={6} c="#c33631" /><circle r={7} fill={INK} /></g>; },
  chart: () => <g><S x={-70} y={-50} w={140} h={100} r={6} fill="#f4f1ea" />{[0, 1, 2, 3].map((i) => <rect key={i} x={-52 + i * 30} y={30 - (20 + i * 14)} width={20} height={20 + i * 14} fill={['#e0a32e', '#e0a32e', '#8FD23F', '#8FD23F'][i]} stroke={INK} strokeWidth={3} />)}</g>,
  chartdown: () => <g><S x={-70} y={-50} w={140} h={100} r={6} fill="#f4f1ea" /><Ln p={[[-52, -20], [-20, 0], [10, -6], [50, 34]]} sw={7} c="#c33631" /></g>,
  tiles: () => <g />,
  boxes: () => <g><S x={-40} y={-10} w={80} h={56} r={4} fill="#d9a45c" /><S x={-26} y={-52} w={64} h={44} r={4} fill="#c88f48" /></g>,
  fridge: () => <g><S x={-44} y={-90} w={88} h={180} r={8} fill="#e8e4da" /><Ln p={[[-44, -20], [44, -20]]} sw={4} /></g>,
  ticket: () => <g><S x={-60} y={-34} w={120} h={68} r={8} fill="#ffd23f" /><text y={14} textAnchor="middle" fontFamily={SIGN} fontSize={38} fill="#111">№ 42</text></g>,
  helmet: () => <g><path d="M -44 10 Q -44 -44 0 -44 Q 44 -44 44 10 Z" fill="#ffd23f" stroke={INK} strokeWidth={5} /><S x={-52} y={8} w={104} h={14} r={6} fill="#ffd23f" /></g>,
  lic: (o) => <g><S x={-230} y={-140} w={460} h={280} r={22} fill="#f4f1ea" /><S x={-230} y={-140} w={460} h={60} r={22} fill="#2C3E50" /><text x={-200} y={-96} fontFamily={SIGN} fontSize={34} fill="#f4f1ea" letterSpacing={3}>{o.text}</text><S x={-200} y={-50} w={110} h={130} r={10} fill="#9fd0ff" /><circle cx={-145} cy={-10} r={26} fill="#f0c9a4" stroke={INK} strokeWidth={4} /><Ln p={[[-60, -30], [180, -30]]} sw={4} c="#8a8f9c" /><Ln p={[[-60, 10], [140, 10]]} sw={4} c="#8a8f9c" /><circle cx={140} cy={80} r={44} fill={ACCENT} stroke={INK} strokeWidth={5} /><text x={140} y={98} textAnchor="middle" fontFamily={SIGN} fontSize={o.col && o.col.length > 2 ? 36 : 56} fill="#111">{o.col}</text></g>,
  ladder: () => <g />,
};
export const Obj: React.FC<{ o: ObjSpec; t: number; g: number }> = ({ o, t }) => {
  const at = o.at ?? 0; const k = (t - at); const e = o.e ?? 'slide'; if (k < 0) return null;
  const f = KINDS[o.k]; if (!f) return null; const s = o.s ?? 1.6;
  let tx = 0, ty = 0, sc = 1, op = 1, rot = 0;
  if (e === 'slide') { const d = o.x < 960 ? -1 : 1; tx = (1 - out3(k / 0.17)) * d * 900; }
  if (e === 'drop') { ty = -(1 - out3(k / 0.25)) * 700; }
  if (e === 'slam') { sc = 1 + (1 - out3(k / 0.2)) * 0.7; rot = (1 - out3(k / 0.2)) * 6; op = clamp(k * 12); }
  if (e === 'grow') { ty = (1 - out3(k / 0.33)) * 160; op = clamp(k * 8); }
  if (e === 'on') { op = k > 0 ? 1 : 0; sc = 1 + Math.max(0, 0.1 - k) * 1; }
  return <g transform={`translate(${o.x + tx} ${o.y + ty}) rotate(${rot}) scale(${s * sc})`} opacity={op}>{f(o, t)}{e === 'drop' && k > 0.2 && k < 0.5 && [-1, 0, 1].map((i) => <circle key={i} cx={i * 34} cy={50} r={10 * (1 - (k - 0.2) / 0.3)} fill="#fff" opacity={0.7} />)}</g>;
};

// ---------------------------------------------------------- effects (seeded, subtle)
export const Fx: React.FC<{ kind: string; t: number; o?: number }> = ({ kind, t, o = 1 }) => {
  const rnd = (i: number) => ((Math.sin(i * 127.1) * 43758.5453) % 1 + 1) % 1;
  if (kind === 'rain') return <g opacity={0.55 * o}>{Array.from({ length: 70 }).map((_, i) => { const x = rnd(i) * 2100 - 100, y = ((rnd(i + 9) * 1200 + t * 900) % 1300) - 100; return <Ln key={i} p={[[x, y], [x - 14, y + 44]]} sw={3} c="#cfe3ff" />; })}</g>;
  if (kind === 'snow') return <g opacity={0.9 * o}>{Array.from({ length: 80 }).map((_, i) => { const x = (rnd(i) * 2100 + Math.sin(t + i) * 24) % 2000, y = ((rnd(i + 5) * 1200 + t * 150) % 1250) - 80; return <circle key={i} cx={x} cy={y} r={3 + rnd(i + 3) * 4} fill="#fff" />; })}</g>;
  if (kind === 'dust') return <g opacity={0.5 * o}>{Array.from({ length: 30 }).map((_, i) => <circle key={i} cx={(rnd(i) * 1900 + Math.sin(t * 0.6 + i) * 30)} cy={(rnd(i + 4) * 900 + t * 12 * (1 + rnd(i))) % 1000} r={2 + rnd(i + 2) * 3} fill="#fff6cf" />)}</g>;
  if (kind === 'smoke') return <g opacity={0.5 * o}>{Array.from({ length: 6 }).map((_, i) => { const k = ((t * 0.5 + i / 6) % 1); return <circle key={i} cx={1500 + Math.sin(k * 5 + i) * 30 + k * 60} cy={520 - k * 420} r={22 + k * 50} fill="#d8dbe4" opacity={1 - k} />; })}</g>;
  if (kind === 'sparks') return <g opacity={o}>{Array.from({ length: 14 }).map((_, i) => { const k = ((t * 1.4 + rnd(i)) % 1); return <circle key={i} cx={960 + (rnd(i + 1) - 0.5) * 300 + k * (rnd(i + 2) - 0.5) * 300} cy={600 - k * 240 + k * k * 220} r={4 * (1 - k)} fill="#ffd23f" />; })}</g>;
  if (kind === 'mist') return <g opacity={0.2 * o}>{[0, 1, 2].map((i) => <ellipse key={i} cx={(i * 720 + t * 20 * (i + 1)) % 2400 - 200} cy={FLOOR + i * 30} rx={440} ry={26} fill="#cfd8f0" />)}</g>;
  if (kind === 'flicker') return <rect width={CW} height={H} fill="#fff" opacity={(Math.sin(t * 40) > 0.85 ? 0.06 : 0) * o} />;
  return null;
};
