import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, Audio, staticFile } from 'remotion';
import { SPECS_PILS } from './specs-pils';
import { SPECS_ASC } from './specs-asc';
import { SPECS_ELE } from './specs-ele';
import { SPECS_LIN } from './specs-lin';
import { SPECS_CHI } from './specs-chi';
import { PROJECT } from './project';
const ASC = PROJECT === 'asc';
const ELE = PROJECT === 'ele';
const LIN = PROJECT === 'lin';
const CHI = PROJECT === 'chi';
const SPECS = CHI ? SPECS_CHI : LIN ? SPECS_LIN : ELE ? SPECS_ELE : ASC ? SPECS_ASC : SPECS_PILS;
import { drawSpec } from './engine';
import { Defs, Finish, H, clamp, out3 } from './kit';
import type { C, Out } from './beats';
export const FPS = 30;
export const SEND = CHI ? 84.63 : LIN ? 76.39 : ELE ? 73.22 : ASC ? 77.12 : 77.77;
const VW = 607.5; const VX = 960 - VW / 2;
type Item = { s: number; id: string; draw: (c: C) => Out; whip?: boolean };
const build = (): Item[] => {
  const items: Item[] = []; let prev = -0.9;
  SPECS.forEach((sp, i) => { const s = Math.max(sp.a as number, prev + 0.9); items.push({ s, id: `S${i + 1}`, draw: drawSpec(sp, s), whip: sp.whip }); prev = s; });
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
    <Audio src={staticFile(CHI ? 'voce-chi.wav' : LIN ? 'voce-lin.wav' : ELE ? 'voce-ele.wav' : ASC ? 'voce-asc.wav' : 'voce-pils.wav')} />
    {ITEMS.map((it, i) => { const end = i + 1 < ITEMS.length ? ITEMS[i + 1].s : SEND; return <Sequence key={it.id} from={Math.round(it.s * FPS)} durationInFrames={Math.max(1, Math.round((end - it.s) * FPS))}><Beat i={i} /></Sequence>; })}
  </AbsoluteFill>
);
export const SHORT_FRAMES = Math.round(SEND * FPS);
