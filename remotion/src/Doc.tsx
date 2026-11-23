import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, Audio, staticFile } from 'remotion';
import { BEATS as BEATS_CAM } from './beats';
import { SPECS as SPECS_CAM } from './specs';
import { SPECS_POL } from './specs-pol';
import { PROJECT } from './project';
const POL = PROJECT === 'pol';
const BEATS = POL ? [] : BEATS_CAM;
const SPECS = POL ? SPECS_POL : SPECS_CAM;
import { drawSpec } from './engine';
import { wt } from './kit2';
import { Defs, Finish, W, H, clamp, out3 } from './kit';
import { Showpiece } from './three3d';
import type { C, Out } from './beats';
export const FPS = 30;
export const END = POL ? 557.28 : 552.36;
type Item = { s: number; id: string; draw: (c: C) => Out; whip?: boolean; sh3d?: 'border' | 'fleet'; grade?: string };
export const buildItems = (): Item[] => {
  const items: Item[] = BEATS.map((b) => ({ s: b.s, id: b.id, draw: b.draw }));
  let prev = BEATS.length ? BEATS[BEATS.length - 1].s : -0.9;
  SPECS.forEach((sp, i) => {
    const s = typeof sp.a === 'number' ? sp.a : wt(sp.a, prev + 0.45);
    items.push({ s: Math.max(s, prev + 0.9), id: `N${i + 1}`, draw: drawSpec(sp, s), whip: sp.whip, sh3d: sp.sh3d, grade: sp.grade });
    prev = Math.max(s, prev + 0.9);
  });
  return items;
};
export const ITEMS = buildItems();
const Beat: React.FC<{ i: number }> = ({ i }) => {
  const f = useCurrentFrame(); const it = ITEMS[i]; const end = i + 1 < ITEMS.length ? ITEMS[i + 1].s : END; const dur = end - it.s; const t = f / FPS;
  const c: C = { t, dur, p: Math.min(1, t / dur), g: it.s + t };
  if (it.sh3d) return (<AbsoluteFill><Showpiece kind={it.sh3d} p={c.p} t={c.g} /><svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: 'absolute', left: 0, top: 0 }}><Finish grade={it.grade || 'day'} /></svg></AbsoluteFill>);
  const o = it.draw(c);
  const k = it.whip ? clamp(f / 9) : 1; const wx = (1 - out3(k)) * 520; const blur = (1 - out3(k)) * 38;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ background: '#000' }}>
      <Defs /><defs><filter id="mbx" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation={`${blur} 0`} /></filter></defs>
      <g filter={blur > 0.5 ? 'url(#mbx)' : undefined} transform={`translate(${wx} 0)`}><g className="c">{o.node}</g>{!o.black && <Finish grade={o.grade} />}</g>
    </svg>
  );
};
export const DocFull: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <Audio src={staticFile(POL ? 'voce-pol.wav' : 'voce.wav')} />
    {ITEMS.map((it, i) => { const end = i + 1 < ITEMS.length ? ITEMS[i + 1].s : END; return <Sequence key={it.id} from={Math.round(it.s * FPS)} durationInFrames={Math.max(1, Math.round((end - it.s) * FPS))}><Beat i={i} /></Sequence>; })}
  </AbsoluteFill>
);
export const FULL_FRAMES = Math.round(END * FPS);
