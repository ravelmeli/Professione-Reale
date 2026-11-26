import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, Audio, staticFile } from 'remotion';
import { SPECS_PILS } from './specs-pils';
import { drawSpec } from './engine';
import { Defs, Finish, H, clamp, out3 } from './kit';
import type { C, Out } from './beats';
export const FPS = 30;
export const SEND = 77.77;
const VW = 607.5; const VX = 960 - VW / 2;
type Item = { s: number; id: string; draw: (c: C) => Out; whip?: boolean };
const build = (): Item[] => {
  const items: Item[] = []; let prev = -0.9;
  SPECS_PILS.forEach((sp, i) => { const s = Math.max(sp.a as number, prev + 0.9); items.push({ s, id: `S${i + 1}`, draw: drawSpec(sp, s), whip: sp.whip }); prev = s; });
  return items;
};
const ITEMS = build();
const Beat: React.FC<{ i: number }> = ({ i }) => {
  const f = useCurrentFrame(); const it = ITEMS[i]; const end = i + 1 < ITEMS.length ? ITEMS[i + 1].s : SEND; const dur = end - it.s; const t = f / FPS;
  const c: C = { t, dur, p: Math.min(1, t / dur), g: it.s + t };
  const o = it.draw(c);
  return (
    <svg width={1080} height={1920} viewBox={`${VX} 0 ${VW} ${H}`} style={{ background: '#000' }}>
      <Defs /><g className="c">{o.node}</g>{!o.black && <Finish grade={o.grade} />}
    </svg>
  );
};
export const ShortDoc: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <Audio src={staticFile('voce-pils.wav')} />
    {ITEMS.map((it, i) => { const end = i + 1 < ITEMS.length ? ITEMS[i + 1].s : SEND; return <Sequence key={it.id} from={Math.round(it.s * FPS)} durationInFrames={Math.max(1, Math.round((end - it.s) * FPS))}><Beat i={i} /></Sequence>; })}
  </AbsoluteFill>
);
export const SHORT_FRAMES = Math.round(SEND * FPS);
