import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, Audio, staticFile } from 'remotion';
import { BEATS, BEAT_END } from './beats';
import { Defs, Finish, W, H } from './kit';
const FPS = 30;
const Beat: React.FC<{ i: number }> = ({ i }) => {
  const f = useCurrentFrame(); const b = BEATS[i]; const end = i + 1 < BEATS.length ? BEATS[i + 1].s : BEAT_END; const dur = end - b.s; const t = f / FPS;
  const o = b.draw({ t, dur, p: Math.min(1, t / dur), g: b.s + t });
  return <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ background: '#000' }}><Defs /><g className="c">{o.node}</g>{!o.black && <Finish grade={o.grade} />}</svg>;
};
export const DocFirst90: React.FC = () => (
  <AbsoluteFill style={{ background: '#000' }}>
    <Audio src={staticFile('voce.wav')} />
    {BEATS.map((b, i) => { const end = i + 1 < BEATS.length ? BEATS[i + 1].s : BEAT_END; return <Sequence key={b.id} from={Math.round(b.s * FPS)} durationInFrames={Math.max(1, Math.round((end - b.s) * FPS))}><Beat i={i} /></Sequence>; })}
  </AbsoluteFill>
);
export const FIRST90_FRAMES = Math.round(BEAT_END * FPS);
