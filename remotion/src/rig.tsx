import React from 'react';
export const INK = '#111111';
import { PROJECT } from './project';
export const ACCENT = PROJECT === 'pol' ? '#3FA9F5' : PROJECT === 'fire' ? '#FF5A36' : PROJECT === 'sol' ? '#C9B458' : PROJECT === 'gru' ? '#FF8A1F' : PROJECT === 'pils' ? '#2CC4E8' : PROJECT === 'asc' ? '#9B6BFF' : PROJECT === 'ele' ? '#FFD400' : PROJECT === 'lin' ? '#FF4FA3' : (PROJECT === 'chi' || PROJECT === 'chi2') ? '#17C3B2' : '#8FD23F';
const SK = ['#f0c9a4', '#e0a982', '#c98c63', '#8d5a3b'];
export type View = 'front' | 'three' | 'side' | 'back';
export type Expr = 'smile' | 'happy' | 'surprised' | 'concerned' | 'angry' | 'sad' | 'deadpan' | 'panic';
export type Pose = 'wave' | 'idle' | 'point' | 'hold' | 'cheer' | 'shrug' | 'talk' | 'cross';
export type Outfit = { skin: string; hair?: string; hairStyle?: 'side' | 'curly' | 'bald' | 'bun' | 'short' | 'pony'; hat?: string; torso: string; trim: string; pants: string; shoes: string; kind: 'jacket' | 'hivis' | 'shirt' | 'blazer' | 'knit' | 'vest' | 'dress' | 'hoodie'; stubble?: boolean; glasses?: boolean; stache?: string; brow?: string; kid?: boolean; temples?: boolean; tie?: string };

export const heroAt = (age: number): Outfit => {
  const base = { skin: SK[0], hair: '#b8452b', hairStyle: 'side' as const, shoes: '#14141a' };
  if (age <= 24) return { ...base, torso: '#3f9a6a', trim: '#e8e2d0', pants: '#2f3a52', kind: 'hoodie', shoes: '#eceae2' };
  if (age <= 32) return { ...base, torso: '#2d4a7a', trim: '#e0a32e', pants: '#2a2f3c', kind: 'jacket', hat: '#e0a32e', stubble: true };
  if (age <= 42) return { ...base, torso: '#2f7f86', trim: '#ff8c42', pants: '#2a2f3c', kind: 'hivis', hat: '#1f7a8c', stubble: true };
  if (age <= 50) return { ...base, torso: '#dfe8f5', trim: '#dfe8f5', pants: '#2a3550', kind: 'shirt', stubble: true, glasses: true, tie: '#a8362f', temples: true };
  return { ...base, hair: '#9a5a3c', torso: '#1f2a3d', trim: '#c33631', pants: '#2a3550', kind: 'jacket', hat: '#c33631', stubble: true, temples: true };
};
export const polAt = (age: number): Outfit => {
  const base = { skin: SK[1], hair: '#2a1c14', hairStyle: 'short' as const, shoes: '#14141a' };
  if (age <= 26) return { ...base, torso: '#1c3d73', trim: '#3FA9F5', pants: '#16233f', kind: 'jacket', hat: '#1c3d73' };
  if (age <= 34) return { ...base, torso: '#1c3d73', trim: '#3FA9F5', pants: '#16233f', kind: 'jacket', hat: '#16305c', stubble: true };
  if (age <= 42) return { ...base, torso: '#2a4f8f', trim: '#e8e2d0', pants: '#16233f', kind: 'vest', hat: '#16305c', stubble: true, temples: true };
  if (age <= 50) return { ...base, hair: '#5a4a44', torso: '#dfe8f5', trim: '#dfe8f5', pants: '#16233f', kind: 'shirt', stubble: true, glasses: true, tie: '#1c3d73', temples: true };
  return { ...base, hair: '#b8bcc6', torso: '#23314d', trim: '#3FA9F5', pants: '#16233f', kind: 'blazer', glasses: true, tie: '#3FA9F5', temples: true };
};
export const fireAt = (age: number): Outfit => {
  const base = { skin: SK[1], hair: '#3a2418', hairStyle: 'short' as const, shoes: '#14141a' };
  if (age <= 27) return { ...base, torso: '#b3261e', trim: '#ffd23f', pants: '#2a2f3c', kind: 'jacket', hat: '#b3261e' };
  if (age <= 36) return { ...base, torso: '#b3261e', trim: '#ffd23f', pants: '#2a2f3c', kind: 'hivis', hat: '#8e1c16', stubble: true };
  if (age <= 46) return { ...base, torso: '#c4301f', trim: '#e8e2d0', pants: '#1f2430', kind: 'vest', hat: '#8e1c16', stubble: true, temples: true };
  if (age <= 54) return { ...base, hair: '#5a4a44', torso: '#dfe8f5', trim: '#dfe8f5', pants: '#1f2430', kind: 'shirt', stubble: true, glasses: true, tie: '#b3261e', temples: true };
  return { ...base, hair: '#b8bcc6', torso: '#1f2a3d', trim: '#ff5a36', pants: '#1f2430', kind: 'blazer', glasses: true, tie: '#b3261e', temples: true };
};
export const solAt = (age: number): Outfit => {
  const base = { skin: SK[1], hair: '#2a1c14', hairStyle: 'short' as const, shoes: '#2a2218' };
  if (age <= 24) return { ...base, torso: '#5b6b3a', trim: '#c9b458', pants: '#4a5530', kind: 'jacket', hat: '#4a5530' };
  if (age <= 34) return { ...base, torso: '#566637', trim: '#c9b458', pants: '#4a5530', kind: 'jacket', hat: '#3f4a28', stubble: true };
  if (age <= 44) return { ...base, torso: '#66763f', trim: '#e8e2d0', pants: '#4a5530', kind: 'vest', hat: '#3f4a28', stubble: true, temples: true };
  if (age <= 52) return { ...base, hair: '#5a4a44', torso: '#dfe8f5', trim: '#dfe8f5', pants: '#2f3a26', kind: 'shirt', stubble: true, glasses: true, tie: '#3f4a28', temples: true };
  return { ...base, hair: '#b8bcc6', torso: '#2d3a24', trim: '#c9b458', pants: '#2f3a26', kind: 'blazer', glasses: true, tie: '#c9b458', temples: true };
};
export const gruAt = (age: number): Outfit => {
  const base = { skin: SK[1], hair: '#3a2418', hairStyle: 'short' as const, shoes: '#3a2f22' };
  if (age <= 26) return { ...base, torso: '#ff8a1f', trim: '#e8e2d0', pants: '#2f3a52', kind: 'hivis', hat: '#ffd23f' };
  if (age <= 36) return { ...base, torso: '#ff8a1f', trim: '#e8e2d0', pants: '#2f3a52', kind: 'hivis', hat: '#ffd23f', stubble: true };
  if (age <= 46) return { ...base, torso: '#e87a1a', trim: '#ffd23f', pants: '#2a2f3c', kind: 'vest', hat: '#ffffff', stubble: true, temples: true };
  if (age <= 54) return { ...base, hair: '#5a4a44', torso: '#dfe8f5', trim: '#dfe8f5', pants: '#2a2f3c', kind: 'shirt', stubble: true, glasses: true, tie: '#e87a1a', temples: true };
  return { ...base, hair: '#b8bcc6', torso: '#2d3a52', trim: '#ff8a1f', pants: '#2a2f3c', kind: 'blazer', glasses: true, tie: '#ff8a1f', temples: true };
};
export const pilAt = (age: number): Outfit => {
  const base = { skin: SK[1], hair: '#2a1c14', hairStyle: 'short' as const, shoes: '#14141a' };
  if (age <= 21) return { ...base, torso: '#f4f6fa', trim: '#2CC4E8', pants: '#14213d', kind: 'shirt', tie: '#14213d' };
  if (age <= 30) return { ...base, torso: '#f4f6fa', trim: '#d9b04a', pants: '#14213d', kind: 'shirt', tie: '#14213d', hat: '#14213d' };
  if (age <= 42) return { ...base, torso: '#f4f6fa', trim: '#d9b04a', pants: '#14213d', kind: 'shirt', tie: '#14213d', hat: '#14213d', stubble: true };
  return { ...base, hair: '#b8bcc6', torso: '#14213d', trim: '#d9b04a', pants: '#14213d', kind: 'blazer', tie: '#d9b04a', hat: '#14213d', glasses: true, temples: true };
};
export const ascAt = (age: number): Outfit => {
  const base = { skin: SK[2], hair: '#2a1c14', hairStyle: 'short' as const, shoes: '#2a2218' };
  if (age <= 24) return { ...base, torso: '#4a4f66', trim: '#9B6BFF', pants: '#2a2f3c', kind: 'jacket', hat: '#f4f6fa' };
  if (age <= 38) return { ...base, torso: '#4a4f66', trim: '#9B6BFF', pants: '#2a2f3c', kind: 'jacket', hat: '#f4f6fa', stubble: true };
  if (age <= 50) return { ...base, torso: '#5a5f78', trim: '#e8e2d0', pants: '#2a2f3c', kind: 'vest', hat: '#f4f6fa', stubble: true, temples: true };
  return { ...base, hair: '#b8bcc6', torso: '#2d3250', trim: '#9B6BFF', pants: '#2a2f3c', kind: 'blazer', glasses: true, tie: '#9B6BFF', temples: true };
};
export const eleAt = (age: number): Outfit => {
  const base = { skin: SK[0], hair: '#6a3a20', hairStyle: 'short' as const, shoes: '#2a2218' };
  if (age <= 22) return { ...base, torso: '#2a6fb0', trim: '#FFD400', pants: '#2a2f3c', kind: 'hoodie' };
  if (age <= 34) return { ...base, torso: '#2a6fb0', trim: '#FFD400', pants: '#2a2f3c', kind: 'jacket', hat: '#FFD400', stubble: true };
  if (age <= 46) return { ...base, torso: '#2a6fb0', trim: '#e8e2d0', pants: '#2a2f3c', kind: 'vest', hat: '#FFD400', stubble: true, temples: true };
  return { ...base, hair: '#b8bcc6', torso: '#dfe8f5', trim: '#dfe8f5', pants: '#2a2f3c', kind: 'shirt', stubble: true, glasses: true, tie: '#2a6fb0', temples: true };
};
export const linAt = (age: number): Outfit => {
  const base = { skin: SK[0], hair: '#4a2a18', hairStyle: 'short' as const, shoes: '#2a2218' };
  if (age <= 26) return { ...base, torso: '#d9e84a', trim: '#e8e2d0', pants: '#2a3550', kind: 'hivis', hat: '#f4f6fa' };
  if (age <= 40) return { ...base, torso: '#d9e84a', trim: '#e8e2d0', pants: '#2a3550', kind: 'hivis', hat: '#f4f6fa', stubble: true };
  return { ...base, hair: '#b8bcc6', torso: '#d9e84a', trim: '#e8e2d0', pants: '#2a3550', kind: 'vest', hat: '#f4f6fa', stubble: true, glasses: true, temples: true };
};
export const chiAt = (age: number): Outfit => {
  const base = { skin: SK[1], hair: '#2a1c14', hairStyle: 'short' as const, shoes: '#e8e2d0' };
  if (age <= 22) return { ...base, torso: '#e8e2d0', trim: '#17c3b2', pants: '#2a3550', kind: 'hoodie', shoes: '#f4f1ea' };
  if (age <= 32) return { ...base, torso: '#17a8a0', trim: '#e8e2d0', pants: '#17a8a0', kind: 'jacket', hat: '#17a8a0' };
  if (age <= 45) return { ...base, torso: '#17a8a0', trim: '#e8e2d0', pants: '#17a8a0', kind: 'jacket', hat: '#17a8a0', stubble: true, glasses: true };
  return { ...base, hair: '#b8bcc6', torso: '#f4f6fa', trim: '#17c3b2', pants: '#2a3550', kind: 'blazer', glasses: true, tie: '#17c3b2', temples: true };
};
export const CAST: Record<string, (a?: number) => Outfit> = {
  pol: (a = 30) => polAt(a),
  fire: (a = 30) => fireAt(a),
  sol: (a = 30) => solAt(a),
  gru: (a = 30) => gruAt(a),
  pil: (a = 30) => pilAt(a),
  asc: (a = 30) => ascAt(a),
  ele: (a = 30) => eleAt(a),
  lin: (a = 30) => linAt(a),
  chi: (a = 30) => chiAt(a),
  rocco: (a = 30) => heroAt(a),
  ciro: () => ({ skin: SK[1], hairStyle: 'bald', torso: '#7a5a3a', trim: '#e8e2d0', pants: '#2a2a30', shoes: '#14141a', kind: 'vest', stache: '#5a4a3a', brow: '#5a4a3a' }),
  marta: () => ({ skin: SK[2], hair: '#2a1a16', hairStyle: 'curly', torso: '#6a4cc0', trim: '#f3efe6', pants: '#22222c', shoes: '#14141a', kind: 'blazer', glasses: true }),
  dino: () => ({ skin: SK[0], hair: '#d8d8de', hairStyle: 'bald', hat: '#4a4f5c', torso: '#8a6a38', trim: '#e8e2d0', pants: '#3a3a44', shoes: '#14141a', kind: 'knit', stache: '#e8e8ee', brow: '#c8c8d0' }),
  ines: () => ({ skin: SK[1], hair: '#5a2a1a', hairStyle: 'bun', torso: '#e86aa0', trim: '#f4f1ea', pants: '#2a2e45', shoes: '#4a2a3a', kind: 'dress' }),
  luca: () => ({ skin: SK[0], hair: '#b8452b', hairStyle: 'short', torso: '#ffd23f', trim: '#e8e2d0', pants: '#3b3f55', shoes: '#4a2a1a', kind: 'hoodie', kid: true }),
  vik: () => ({ skin: SK[0], hair: '#d9a52e', hairStyle: 'short', hat: '#2a7de1', torso: '#d8d8e0', trim: '#2a7de1', pants: '#2f3447', shoes: '#14141a', kind: 'jacket', stubble: true, stache: '#d9a52e' }),
  agente: () => ({ skin: SK[3], hair: '#17141f', hairStyle: 'short', hat: '#1b3a6b', torso: '#3a5fa0', trim: '#ffd23f', pants: '#1b2a4a', shoes: '#14141a', kind: 'vest', brow: '#17141f' }),
  sara: () => ({ skin: SK[2], hair: '#f2c24a', hairStyle: 'pony', torso: '#3ddc84', trim: '#f4f1ea', pants: '#2a2e45', shoes: '#14141a', kind: 'blazer', glasses: true }),
};
const sh = (hex: string, k: number) => { const n = parseInt(hex.slice(1), 16); const f = (v: number) => Math.max(0, Math.min(255, Math.round(v + (k < 0 ? v * k : (255 - v) * k)))); return `#${[(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => f(v).toString(16).padStart(2, '0')).join('')}`; };

const ARMS: Record<Pose, { f: number[][]; b: number[][] }> = {
  idle: { f: [[40, -190], [48, -150], [46, -112]], b: [[-40, -190], [-48, -150], [-46, -112]] },
  point: { f: [[40, -196], [86, -206], [130, -210]], b: [[-40, -190], [-48, -150], [-46, -112]] },
  hold: { f: [[40, -190], [62, -150], [78, -170]], b: [[-40, -190], [-52, -150], [-26, -150]] },
  cheer: { f: [[40, -196], [74, -250], [84, -300]], b: [[-40, -196], [-74, -250], [-84, -300]] },
  shrug: { f: [[40, -192], [74, -170], [84, -206]], b: [[-40, -192], [-74, -170], [-84, -206]] },
  talk: { f: [[40, -192], [70, -170], [92, -196]], b: [[-40, -190], [-48, -150], [-46, -112]] },
  wave: { f: [[40, -196], [74, -236], [84, -280]], b: [[-40, -190], [-48, -150], [-46, -112]] },
  cross: { f: [[40, -190], [20, -150], [-24, -168]], b: [[-40, -190], [-20, -150], [24, -164]] },
};

const Mouth: React.FC<{ x: number; y: number; e: Expr }> = ({ x, y, e }) => {
  if (e === 'smile') return <path d={`M ${x - 10} ${y - 2} Q ${x} ${y + 8} ${x + 10} ${y - 2}`} fill="none" stroke={INK} strokeWidth={3.5} strokeLinecap="round" />;
  if (e === 'happy') return <path d={`M ${x - 12} ${y - 3} Q ${x} ${y + 16} ${x + 12} ${y - 3} Z`} fill="#fff" stroke={INK} strokeWidth={3.5} strokeLinejoin="round" />;
  if (e === 'surprised') return <ellipse cx={x} cy={y + 3} rx={5.5} ry={8} fill={INK} />;
  if (e === 'concerned' || e === 'sad') return <path d={`M ${x - 9} ${y + 5} Q ${x} ${y - 3} ${x + 9} ${y + 5}`} fill="none" stroke={INK} strokeWidth={3.5} strokeLinecap="round" />;
  if (e === 'angry') return <path d={`M ${x - 10} ${y + 5} L ${x + 10} ${y + 2}`} stroke={INK} strokeWidth={4} strokeLinecap="round" />;
  if (e === 'panic') return <path d={`M ${x - 10} ${y} L ${x - 5} ${y + 5} L ${x} ${y} L ${x + 5} ${y + 5} L ${x + 10} ${y}`} fill="#fff" stroke={INK} strokeWidth={3} strokeLinejoin="round" />;
  return <path d={`M ${x - 8} ${y + 1} L ${x + 8} ${y + 1}`} stroke={INK} strokeWidth={3.5} strokeLinecap="round" />;
};

export const Head: React.FC<{ o: Outfit; view: View; expr: Expr; look?: number }> = ({ o, view, expr }) => {
  const R = 42; const dx = view === 'front' ? 0 : view === 'three' ? 9 : view === 'side' ? 22 : 0;
  const hair = o.hair || '#555'; const bc = o.brow || INK;
  const eyes = view === 'front' ? [-14, 14] : view === 'three' ? [dx - 8, dx + 18] : view === 'side' ? [dx + 8] : [];
  const ey = -2, mx = view === 'front' ? 0 : dx + (view === 'side' ? 6 : 4), my = 21;
  const brow = (x: number, i: number) => {
    const tilt = expr === 'angry' ? (i === 0 ? 4 : -4) : expr === 'sad' || expr === 'concerned' ? (i === 0 ? -4 : 4) : 0; const dy = expr === 'surprised' ? -7 : expr === 'angry' ? 2 : 0;
    return <path key={i} d={`M ${x - 8} ${ey - 16 + dy - tilt} L ${x + 8} ${ey - 16 + dy + tilt}`} stroke={bc} strokeWidth={3} strokeLinecap="round" />;
  };
  return (
    <g>
      {o.hairStyle === 'curly' && Array.from({ length: 9 }).map((_, i) => { const a = Math.PI * (0.9 + i * 0.15); return <circle key={i} cx={Math.cos(a) * 41} cy={Math.sin(a) * 39 + 4} r={15} fill={hair} stroke={INK} strokeWidth={3.6} />; })}
      {o.hairStyle === 'bun' && <circle cx={view === 'side' ? -30 : -2} cy={-R - 10} r={15} fill={hair} stroke={INK} strokeWidth={4} />}
      {o.hairStyle === 'pony' && <path d={`M ${-R + 6} -20 Q ${-R - 34} 20 ${-R - 8} 60 Q ${-R + 10} 30 ${-R + 14} 0 Z`} fill={hair} stroke={INK} strokeWidth={4} />}
      <circle r={R} fill={o.skin} stroke={INK} strokeWidth={4.5} />
      <circle r={R} fill="url(#hs)" />
      <path d={`M ${-R + 6} 12 A ${R - 6} ${R - 6} 0 0 0 ${R - 6} 16`} fill="none" stroke="rgba(120,60,20,.2)" strokeWidth={6} />
      <path d={`M ${R - 20} ${-R + 10} A ${R - 4} ${R - 4} 0 0 1 ${R - 4} ${-14}`} fill="none" stroke="rgba(255,255,255,.7)" strokeWidth={3} />
      {o.stubble && view !== 'back' && <path d={`M ${-R + 4} 4 Q 0 ${R + 12} ${R - 4} 4 L ${R - 14} 14 Q 0 20 ${-R + 14} 14 Z`} fill="rgba(30,20,20,.3)" />}
      {view !== 'back' && eyes.map((x, i) => expr === 'surprised' || expr === 'panic'
        ? <g key={i}><ellipse cx={x} cy={ey} rx={7.5} ry={9.5} fill="#fff" stroke={INK} strokeWidth={3} /><circle cx={x + 1} cy={ey} r={2.8} fill={INK} /></g>
        : <ellipse key={i} cx={x} cy={ey} rx={4.2} ry={5.6} fill={INK} />)}
      {view !== 'back' && eyes.map((x, i) => brow(x, i))}
      {view !== 'back' && <Mouth x={mx} y={my} e={expr} />}
      {o.stache && view !== 'back' && <path d={`M ${mx - 14} ${my - 8} Q ${mx} ${my - 16} ${mx + 14} ${my - 8} Q ${mx + 8} ${my + 1} ${mx} ${my - 4} Q ${mx - 8} ${my + 1} ${mx - 14} ${my - 8} Z`} fill={o.stache} stroke={INK} strokeWidth={3} />}
      {o.glasses && view !== 'back' && <g fill="rgba(255,255,255,.22)" stroke={INK} strokeWidth={3.2}>{eyes.map((x, i) => <circle key={i} cx={x} cy={ey} r={12.5} />)}{eyes.length > 1 && <path d={`M ${eyes[0] + 12.5} ${ey} L ${eyes[1] - 12.5} ${ey}`} fill="none" />}</g>}
      {/* hair cap */}
      {(o.hairStyle === 'side' || o.hairStyle === 'short' || o.hairStyle === 'bun' || o.hairStyle === 'pony') && !o.hat && <path d={`M ${-R} -4 Q ${-R - 4} ${-R - 12} 6 ${-R - 6} Q ${R + 4} ${-R} ${R} -6 Q 14 -26 -8 ${view === 'back' ? 20 : -24} Q -28 ${view === 'back' ? 30 : -24} ${-R} -4 Z`} fill={hair} stroke={INK} strokeWidth={4.5} />}
      {view === 'back' && (o.hairStyle !== 'bald') && <circle r={R - 1} fill={hair} stroke={INK} strokeWidth={4.5} />}
      {view === 'back' && o.hairStyle === 'bald' && <circle r={R - 1} fill={o.skin} stroke={INK} strokeWidth={4.5} />}
      {o.hat && <g><path d={`M ${-R - 2} -10 Q ${-R} ${-R - 14} 4 ${-R - 12} Q ${R} ${-R - 14} ${R + 2} -10 Z`} fill={o.hat} stroke={INK} strokeWidth={4.5} /><path d={`M ${view === 'back' ? -30 : 8} -14 L ${view === 'back' ? 30 : R + 26} -8 L ${view === 'back' ? 26 : R + 22} -1 L ${view === 'back' ? -26 : 8} -5 Z`} fill={sh(o.hat, -0.14)} stroke={INK} strokeWidth={3.5} /></g>}
      {o.temples && view !== 'back' && <ellipse cx={-R + 4} cy={-6} rx={4} ry={8} fill="#d8d8e0" />}
    </g>
  );
};

export const Torso: React.FC<{ o: Outfit; view: View }> = ({ o, view }) => {
  const rx = view === 'front' ? 38 : view === 'three' ? 34 : view === 'side' ? 26 : 38, ry = 60, cy = -150;
  const cx = view === 'three' ? 3 : view === 'side' ? 4 : 0;
  const id = `clip-${o.kind}-${view}`;
  const f = view !== 'back';
  return (
    <g>
      <clipPath id={id}><ellipse cx={cx} cy={cy} rx={rx} ry={ry} /></clipPath>
      <g clipPath={`url(#${id})`}>
        <rect x={cx - rx} y={cy - ry} width={2 * rx} height={2 * ry} fill={o.torso} />
        <rect x={cx - rx} y={cy + ry - 22} width={2 * rx} height={22} fill="rgba(0,0,0,.2)" />
        <ellipse cx={cx - 22} cy={cy} rx={26} ry={ry} fill="rgba(0,0,0,.16)" />
        <ellipse cx={cx + 26} cy={cy - 10} rx={8} ry={ry * 0.7} fill="rgba(255,255,255,.14)" />
        {o.kind === 'jacket' && f && <g><path d={`M ${cx + 4} ${cy - ry + 4} L ${cx + 4} ${cy + ry}`} stroke={INK} strokeWidth={3} /><rect x={cx + 10} y={cy + 8} width={18} height={14} rx={3} fill="rgba(0,0,0,.14)" stroke={INK} strokeWidth={2.5} /><path d={`M ${cx - 24} ${cy - 30} L ${cx + 4} ${cy - 6} L ${cx + 4} ${cy - 30}`} fill="none" stroke="rgba(255,255,255,.55)" strokeWidth={2.5} /></g>}
        {o.kind === 'hoodie' && f && <g><path d={`M ${cx - 16} ${cy - ry + 2} Q ${cx} ${cy - 24} ${cx + 18} ${cy - ry + 2}`} fill={sh(o.torso, -0.2)} stroke={INK} strokeWidth={3} /><path d={`M ${cx - 6} ${cy - 30} L ${cx - 6} ${cy - 6} M ${cx + 8} ${cy - 30} L ${cx + 8} ${cy - 6}`} stroke={INK} strokeWidth={2.5} /><rect x={cx - 22} y={cy + 14} width={44} height={22} rx={5} fill="rgba(0,0,0,.14)" stroke={INK} strokeWidth={2.5} /></g>}
        {o.kind === 'hivis' && f && <g><rect x={cx - rx} y={cy - 28} width={2 * rx} height={10} fill={o.trim} /><rect x={cx - rx} y={cy + 12} width={2 * rx} height={10} fill={o.trim} /><path d={`M ${cx - 22} ${cy - ry} L ${cx - 12} ${cy + ry} M ${cx + 22} ${cy - ry} L ${cx + 12} ${cy + ry}`} stroke="#ff8c42" strokeWidth={10} /><path d={`M ${cx + 2} ${cy - ry + 4} L ${cx + 2} ${cy + ry}`} stroke={INK} strokeWidth={3} /></g>}
        {o.kind === 'shirt' && f && <g><path d={`M ${cx - 14} ${cy - ry + 4} L ${cx + 4} ${cy - 30} L ${cx + 20} ${cy - ry + 4} Z`} fill="#fff" stroke={INK} strokeWidth={3} />{o.tie && <path d={`M ${cx + 1} ${cy - 34} L ${cx + 8} ${cy - 34} L ${cx + 10} ${cy + 12} L ${cx + 4} ${cy + 18} L ${cx - 2} ${cy + 12} Z`} fill={o.tie} stroke={INK} strokeWidth={2.5} />}{[0, 1, 2].map((i) => <circle key={i} cx={cx + 4} cy={cy + 24 + i * 12} r={2.4} fill={INK} />)}<rect x={cx + 14} y={cy - 4} width={16} height={16} rx={2} fill="rgba(0,0,0,.1)" stroke={INK} strokeWidth={2} /></g>}
        {o.kind === 'vest' && f && <g><path d={`M ${cx - 14} ${cy - ry + 4} L ${cx + 4} ${cy - 20} L ${cx + 22} ${cy - ry + 4} L ${cx + 22} ${cy + 30} L ${cx - 14} ${cy + 30} Z`} fill={o.trim} stroke={INK} strokeWidth={2.5} /><path d={`M ${cx + 4} ${cy - 20} L ${cx + 4} ${cy + ry}`} stroke={INK} strokeWidth={3} />{[0, 1, 2].map((i) => <circle key={i} cx={cx + 4} cy={cy - 4 + i * 20} r={2.4} fill={INK} />)}</g>}
        {o.kind === 'blazer' && f && <g><path d={`M ${cx - 18} ${cy - ry + 4} L ${cx + 4} ${cy - 6} L ${cx + 24} ${cy - ry + 4} L ${cx + 14} ${cy - 30} L ${cx - 6} ${cy - 30} Z`} fill={o.trim} stroke={INK} strokeWidth={2.5} /><path d={`M ${cx + 4} ${cy - 6} L ${cx + 4} ${cy + ry}`} stroke={INK} strokeWidth={3} /></g>}
        {o.kind === 'knit' && f && [0, 1, 2, 3, 4, 5].map((i) => <path key={i} d={`M ${cx - rx + 4} ${cy - 40 + i * 18} L ${cx + rx - 4} ${cy - 36 + i * 18}`} stroke="rgba(0,0,0,.2)" strokeWidth={2} />)}
        {o.kind === 'dress' && <path d={`M ${cx - rx} ${cy + 20} L ${cx + rx} ${cy + 20}`} stroke="rgba(255,255,255,.4)" strokeWidth={6} />}
        {!f && <g><path d={`M ${cx - 20} ${cy - ry + 2} Q ${cx} ${cy - 40} ${cx + 20} ${cy - ry + 2}`} fill={sh(o.torso, -0.15)} stroke={INK} strokeWidth={3} /><path d={`M ${cx} ${cy - 40} L ${cx} ${cy + ry}`} stroke="rgba(0,0,0,.35)" strokeWidth={2.5} /></g>}
      </g>
      <ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke={INK} strokeWidth={4.5} />
    </g>
  );
};

const Arm: React.FC<{ pts: number[][]; skin: string; sleeve?: string }> = ({ pts, skin }) => (
  <g><path d={`M ${pts[0][0]} ${pts[0][1]} L ${pts[1][0]} ${pts[1][1]} L ${pts[2][0]} ${pts[2][1]}`} fill="none" stroke={INK} strokeWidth={4.5} strokeLinecap="round" strokeLinejoin="round" /><circle cx={pts[2][0]} cy={pts[2][1]} r={7} fill={skin} stroke={INK} strokeWidth={3} /></g>
);

export const Char: React.FC<{ who: string; age?: number; view?: View; expr?: Expr; pose?: Pose; x?: number; y?: number; s?: number; flip?: boolean; shadow?: boolean }> = ({ who, age, view = 'front', expr = 'smile', pose = 'idle', x = 0, y = 0, s = 1, flip = false, shadow = true }) => {
  const o = CAST[who](age); const k = o.kid ? 0.74 : 1; const a = ARMS[pose] || ARMS.idle;
  const legX = view === 'side' ? [-8, 10] : view === 'three' ? [-14, 16] : [-16, 16];
  const hx = view === 'three' ? 3 : view === 'side' ? 4 : 0;
  return (
    <g transform={`translate(${x} ${y}) scale(${flip ? -s * k : s * k} ${s * k})`} className="c">
      {shadow && <ellipse cx={-14} cy={4} rx={60} ry={10} fill="rgba(0,0,0,.28)" />}
      {view !== 'side' && <Arm pts={a.b} skin={o.skin} />}
      {legX.map((lx, i) => <g key={i}><path d={`M ${lx * 0.7} -100 L ${lx} -50 L ${lx} -8`} fill="none" stroke={INK} strokeWidth={11} strokeLinecap="round" /><path d={`M ${lx * 0.7} -100 L ${lx} -50 L ${lx} -8`} fill="none" stroke={o.pants} strokeWidth={7} strokeLinecap="round" /><ellipse cx={lx + (view === 'side' ? 7 : 4)} cy={-3} rx={view === 'side' ? 15 : 12} ry={7} fill={o.shoes} stroke={INK} strokeWidth={3.5} /></g>)}
      <Torso o={o} view={view} />
      <Arm pts={view === 'side' ? [[4, -190], [24, -150], [30, -112]].map((p, i) => (pose === 'idle' ? p : a.f[i])) : a.f} skin={o.skin} />
      <g transform={`translate(${hx} -262)`}><Head o={o} view={view} expr={expr} /></g>
      {expr === 'panic' && <path d={`M ${hx + 46} -300 q 6 10 0 16 q -6 -6 0 -16`} fill="#8fd6ff" stroke={INK} strokeWidth={2.5} />}
    </g>
  );
};
export const HeadDefs: React.FC = () => (
  <defs><radialGradient id="hs" cx="0.38" cy="0.35" r="0.8"><stop offset="0" stopColor="rgba(255,255,255,.12)" /><stop offset="1" stopColor="rgba(120,60,20,.22)" /></radialGradient><style>{`.c *{vector-effect:non-scaling-stroke}`}</style></defs>
);
