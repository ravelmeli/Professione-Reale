import React from 'react';
import { Cam, W, H, FLOOR, BlackCard, ChapterCard, Calendar, Sign, Truck, S, Ln, Poly, Clock, SIGN, HAND, out3, clamp, ease, Wall, L } from './kit';
import { Char } from './rig';
import { INK, ACCENT } from './rig';
import { AnySet } from './sets2';
import { Obj, ObjSpec, Fx, wt } from './kit2';
import { Insert } from './sets';
import { TopMap, Card, Phone } from './beats';
import type { C, Out } from './beats';

export type CastSpec = [string, number, string?, string?, any?];
export type Spec = { a: string | number; set?: any; cast?: CastSpec[]; objs?: any[]; mv?: string; grade?: string; fx?: string; card?: string; chap?: [string, string]; ins?: [string, string]; top?: boolean; phone?: string; sh3d?: 'border' | 'fleet'; whip?: boolean; cardDelay?: number; typed?: string; glow?: string; note?: string };
const camFor = (mv: string | undefined, p: number, t: number): Cam => {
  switch (mv) {
    case 'pull': return { z: 1.12 - 0.12 * p, x: 0, y: 0 };
    case 'pan': return { z: 1.04, x: -80 + 160 * p, y: 0 };
    case 'panl': return { z: 1.04, x: 80 - 160 * p, y: 0 };
    case 'still': return { z: 1 + 0.015 * p, x: 0, y: 0 };
    case 'punch': return { z: 1 + 0.03 * p + (t > 0.9 ? 0.09 : 0), x: 0, y: 0 };
    case 'wide': return { z: 0.9 + 0.08 * p, x: 0, y: 0 };
    case 'low': return { z: 1.06 + 0.04 * p, x: 0, y: -40 };
    case 'up': return { z: 1.05, x: 0, y: 60 - 120 * p };
    default: return { z: 1 + 0.1 * p, x: -20 * p, y: 0 };
  }
};
export const drawSpec = (sp: Spec, s0: number): ((c: C) => Out) => (c) => {
  const grade = sp.grade || 'day';
  if (sp.card) return { grade, black: true, node: <BlackCard text={sp.card} t={Math.max(0, c.t - (sp.cardDelay || 0))} size={sp.card.length > 24 ? 120 : 150} cps={sp.card.length > 24 ? 17 : 19} /> };
  if (sp.chap) return { grade, black: true, node: <ChapterCard text={sp.chap[0]} sub={sp.chap[1]} /> };
  const cam = camFor(sp.mv, c.p, c.t);
  const objs = (sp.objs || []).map((o: any, i: number) => { const at = typeof o.a === 'string' ? wt(o.a, s0) - s0 : (o.a ?? o.at ?? 0); return <Obj key={i} o={{ ...o, at }} t={c.t} g={c.g} />; });
  const fx = sp.fx ? <Fx kind={sp.fx} t={c.g} /> : null;
  if (sp.phone) {
    const press = clamp((c.t - 0.35) / 0.4) * (1 - clamp((c.t - 1.0) / 0.5));
    return { grade: 'night', node: <Insert cam={cam} col="#1d2a44" glow="#e5392b"><PhoneScreen mode={sp.phone} t={c.t} press={press} /></Insert> };
  }
  if (sp.top) return { grade, node: <g><TopMap route={1}>{null}</TopMap><L cam={cam} d={1}>{objs}</L></g> };
  if (sp.ins) return { grade, node: <g><Insert cam={cam} wall={sp.ins[0] as any} col={sp.ins[1]} glow={sp.glow}>{objs}</Insert>{fx}</g> };
  const hy = (typeof sp.set === 'object' && sp.set.n === 'cabina') || sp.set === 'cabina' ? 940 : FLOOR + 160;
  const cast = <g>{(sp.cast || []).map(([who, x, pose, expr, ex = {}], i) => <Char key={i} who={who} x={x} y={ex.y ?? hy} s={ex.s ?? 1.9} pose={(pose as any) || 'idle'} expr={(expr as any) || 'smile'} flip={!!ex.flip} view={ex.view} age={ex.age} />)}</g>;
  return { grade, node: <g><AnySet spec={sp.set || 'piazzale'} cam={cam} t={c.g} cast={cast} /><L cam={cam} d={1.05}>{objs}</L>{fx}</g> };
};
const PhoneScreen: React.FC<{ mode: string; t: number; press: number }> = ({ mode, t, press }) => {
  if (mode === 'sub') return <Phone x={960} y={560} s={1.25} press={press} />;
  const txt = mode === 'comment' ? 'La cosa più dura è…' : 'Quale professione?';
  const n = Math.floor(Math.max(0, t - 0.3) * 14);
  return (
    <g transform="translate(960 560) scale(1.25)"><S x={-170} y={-330} w={340} h={660} r={42} fill="#1d1f27" sw={8} /><S x={-150} y={-300} w={300} h={600} r={26} fill="#f4f1ea" sw={3} />
      <text y={-230} textAnchor="middle" fontFamily={SIGN} fontSize={30} fill="#2a2f3c" letterSpacing={2}>{mode === 'comment' ? 'COMMENTI' : 'PROSSIMO VIDEO'}</text>
      <S x={-120} y={-190} w={240} h={110} r={14} fill="#fff" sw={3} /><text x={-104} y={-120} fontFamily={HAND} fontWeight={700} fontSize={34} fill="#2a2f3c">{txt.slice(0, n)}{n % 2 ? '|' : ''}</text>
      {mode !== 'comment' && [['wrench', -80], ['house', 0], ['fuel', 80]].map(([k, x]: any, i) => <circle key={i} cx={x} cy={20} r={30} fill={['#e0a32e', '#c33631', '#2f7f86'][i]} stroke={INK} strokeWidth={4} />)}
      <S x={-90} y={150} w={180} h={64} r={14} fill="#e5392b" sw={3} /><text y={194} textAnchor="middle" fontFamily={SIGN} fontSize={34} fill="#fff" letterSpacing={2}>{mode === 'comment' ? 'INVIA' : 'SCEGLI'}</text>
    </g>
  );
};
