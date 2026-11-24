import { PROJECT } from './project';
import React from 'react';
import { Cam, L, W, H, FLOOR, Wall, Floor, WindowView, Clock, Calendar, Sign, Plant, Desk, Cabinet, Shelf, MapPin, Lamp, Truck, Glow, S, Poly, Ln, Defs, Finish, shade } from './kit';
import { INK, ACCENT } from './rig';

export type SetP = { cam: Cam; t: number; cast?: React.ReactNode; fore?: React.ReactNode; lit?: boolean; truck?: boolean; truckX?: number; truckS?: number; halo?: boolean; extra?: React.ReactNode };
const Stars: React.FC<{ t: number }> = ({ t }) => <g>{Array.from({ length: 46 }).map((_, i) => <circle key={i} cx={(i * 211) % 2300 - 200} cy={30 + (i * 53) % 400} r={1.6 + (i % 3) * 0.5} fill="#cfd8f0" opacity={0.55 + 0.4 * Math.sin(t * 2 + i)} />)}</g>;
const Mist: React.FC<{ t: number; y?: number }> = ({ t, y = FLOOR - 10 }) => <g opacity={0.16}>{[0, 1, 2].map((i) => <ellipse key={i} cx={(i * 720 + t * 18 * (i + 1)) % 2400 - 200} cy={y + i * 26} rx={420} ry={24} fill="#cfd8f0" />)}</g>;

export const Piazzale: React.FC<SetP> = ({ cam, t, cast, fore, lit = true, truck = true, truckX = 760, truckS = 0.9, halo = false, extra }) => (
  <g>
    <L cam={cam} d={0.3}><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="#0d1226" /><Stars t={t} /><path d={`M -400 520 L -100 450 L 200 480 L 520 420 L 900 470 L 1300 430 L 1700 480 L 2100 440 L 2400 500 L 2400 ${FLOOR} L -400 ${FLOOR} Z`} fill="#10162a" /></L>
    <L cam={cam} d={0.55}>
      <S x={1180} y={240} w={560} h={450} r={4} fill="#2a3350" /><Wall kind="corr" col="#2a3350" y0={244} y1={686} />
      <S x={1290} y={360} w={340} h={330} r={3} fill={lit ? '#f0d58a' : '#12162a'} />{lit && [1, 2, 3, 4, 5].map((i) => <Ln key={i} p={[[1290, 360 + i * 55], [1630, 360 + i * 55]]} sw={3} c="rgba(0,0,0,.25)" />)}
      <Sign x={1300} y={262} w={320} text={PROJECT === 'fire' || PROJECT === 'sol' ? 'CASERMA' : 'MAGAZZINO'} bg="#2a2f3c" fg="#f4f1ea" size={40} />
      {lit && <path d="M 1290 690 L 1630 690 L 1760 900 L 1160 900 Z" fill="#f0d58a" opacity={0.18} />}
    </L>
    <L cam={cam} d={0.8}>
      <Floor kind="asphalt" col="#1c2238" />
      <Lamp x={250} y={170} />
      {truck && <Truck x={truckX} y={FLOOR + 40} s={truckS} halo={halo} />}
      <Mist t={t} />
    </L>
    {extra}
    <L cam={cam} d={1}>{cast}</L>
    <L cam={cam} d={1.6} blur={5}><g><ellipse cx={1760} cy={FLOOR + 330} rx={70} ry={12} fill="rgba(0,0,0,.3)" /><S x={1730} y={FLOOR + 120} w={60} h={210} r={8} fill="#c33631" /><S x={1722} y={FLOOR + 160} w={76} h={20} r={4} fill="#f4f1ea" /></g></L>
    {fore}
  </g>
);
export const Strada: React.FC<SetP & { dusk?: boolean }> = ({ cam, t, cast, truck = true, truckX = 1100, truckS = 0.8, dusk }) => (
  <g>
    <L cam={cam} d={0.3}><defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1">{dusk ? <><stop offset="0" stopColor="#48296a" /><stop offset="0.6" stopColor="#db747a" /><stop offset="1" stopColor="#f0b789" /></> : <><stop offset="0" stopColor="#6aa7e0" /><stop offset="1" stopColor="#dff0ff" /></>}</linearGradient></defs><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="url(#sk)" /><circle cx={1500} cy={380} r={90} fill={dusk ? '#ffd9a0' : '#fff6cf'} />{[0, 1, 2, 3].map((i) => <ellipse key={i} cx={300 + i * 420 + (t * 8) % 60} cy={160 + (i % 2) * 60} rx={120} ry={28} fill="rgba(255,255,255,.75)" />)}</L>
    <L cam={cam} d={0.45}><path d={`M -400 560 L -100 480 L 300 470 L 700 520 L 1100 460 L 1500 500 L 2000 450 L 2400 520 L 2400 ${FLOOR} L -400 ${FLOOR} Z`} fill={dusk ? '#4a3a5a' : '#8aaec0'} /></L>
    <L cam={cam} d={0.6}><rect x={-400} y={600} width={W + 800} height={100} fill={dusk ? '#3a4a3a' : '#5b8a58'} />{Array.from({ length: 14 }).map((_, i) => { const x = i * 160 - ((t * 120) % 160); return <g key={i}><Ln p={[[x, 600], [x, 560]]} sw={6} /><ellipse cx={x} cy={552} rx={22} ry={28} fill="#3d6b3d" stroke={INK} strokeWidth={3.5} /></g>; })}</L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#3a3f4d" /><rect x={-400} y={FLOOR - 4} width={W + 800} height={6} fill="#f4f1ea" />{Array.from({ length: 12 }).map((_, i) => <rect key={i} x={i * 200 - ((t * 400) % 200)} y={FLOOR + 170} width={110} height={12} fill="#e0a32e" />)}{truck && <Truck x={truckX} y={FLOOR + 120} s={truckS} />}</L>
    <L cam={cam} d={1}>{cast}</L>
  </g>
);
export const Ufficio: React.FC<SetP & { sign?: string; view?: 'day' | 'night' | 'dusk' }> = ({ cam, t, cast, fore, sign, view = 'day' }) => (
  <g>
    <L cam={cam} d={0.35}><Wall kind="dots" col="#c9c1a8" /><WindowView x={1180} y={140} w={420} h={330} view={view} t={t} /></L>
    <L cam={cam} d={0.6}><Clock x={700} y={170} h={9} m={20} /><Calendar x={150} y={150} /><MapPin x={360} y={140} /><Shelf x={880} y={330} w={260} /><Cabinet x={1650} y={FLOOR - 210} /><Plant x={90} y={FLOOR} />{sign && <Sign x={760} y={250} w={340} text={sign} bg="#2C3E50" fg="#f4f1ea" size={36} />}</L>
    <L cam={cam} d={0.8}><Floor kind="planks" col="#7a5a3a" /><Desk x={1000} y={FLOOR - 120} w={520} /></L>
    <L cam={cam} d={1}>{cast}</L>
    <L cam={cam} d={1.5} blur={5}><g><Plant x={-30} y={FLOOR + 330} /></g></L>
    {fore}
  </g>
);
export const Citta: React.FC<SetP & { kind?: 'depot' | 'negozio' | 'cantiere' }> = ({ cam, t, cast, fore, kind = 'depot', truck = true, truckX = 1200, truckS = 0.7, extra }) => (
  <g>
    <L cam={cam} d={0.3}><defs><linearGradient id="sk2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6aa7e0" /><stop offset="1" stopColor="#dff0ff" /></linearGradient></defs><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="url(#sk2)" />{[0, 1, 2].map((i) => <ellipse key={i} cx={300 + i * 600 + (t * 8) % 60} cy={150 + (i % 2) * 60} rx={120} ry={28} fill="rgba(255,255,255,.8)" />)}</L>
    <L cam={cam} d={0.45}>{Array.from({ length: 9 }).map((_, i) => <g key={i}><rect x={i * 300 - 200} y={300 + (i % 3) * 50} width={240} height={FLOOR - 300 - (i % 3) * 50} fill={['#8a9bb0', '#9fb0a2', '#b0a08a'][i % 3]} stroke={INK} strokeWidth={4} />{Array.from({ length: 4 }).map((_, r) => <rect key={r} x={i * 300 - 170} y={340 + (i % 3) * 50 + r * 70} width={50} height={40} fill="#f0e3a0" stroke={INK} strokeWidth={3} />)}</g>)}</L>
    <L cam={cam} d={0.65}>
      {kind === 'negozio' && <g><S x={120} y={330} w={760} h={360} r={4} fill="#e8d9b8" /><Wall kind="stripes" col="#e8d9b8" y0={334} y1={686} /><Poly p={[[100, 330], [900, 330], [940, 420], [60, 420]]} fill="#c33631" /><Sign x={330} y={440} w={300} text="NEGOZIO" bg="#f4f1ea" size={44} /><S x={160} y={500} w={140} h={190} r={4} fill="#9fd0ff" /></g>}
      {kind === 'cantiere' && <g><Ln p={[[100, 330], [100, 690], [700, 690], [700, 330], [100, 330]]} sw={6} /><Ln p={[[100, 330], [700, 690]]} sw={5} /><Ln p={[[700, 330], [100, 690]]} sw={5} /><Ln p={[[100, 460], [700, 460]]} sw={5} /><Ln p={[[900, 690], [900, 140], [1300, 140]]} sw={14} /><Ln p={[[900, 140], [1020, 300]]} sw={7} /><Sign x={780} y={560} w={300} text="CANTIERE" bg="#e0a32e" size={44} /></g>}
      {kind === 'depot' && <g><S x={140} y={380} w={700} h={310} r={4} fill="#5a6a80" /><Wall kind="corr" col="#5a6a80" y0={384} y1={686} /><Sign x={300} y={300} w={380} text="DEPOSITO" bg="#2a2f3c" fg="#f4f1ea" size={44} /></g>}
    </L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 40} width={W + 800} height={H} fill="#8a8f98" /><rect x={-400} y={FLOOR + 40} width={W + 800} height={H} fill="#3a3f4d" /><rect x={-400} y={FLOOR + 36} width={W + 800} height={8} fill="#f4f1ea" />{truck && <Truck x={truckX} y={FLOOR + 140} s={truckS} />}{extra}</L>
    <L cam={cam} d={1}>{cast}</L>
    {fore}
  </g>
);
export const Insert: React.FC<{ cam: Cam; wall?: 'corr' | 'dots' | 'brick' | 'panels'; col?: string; floor?: boolean; children?: React.ReactNode; glow?: string }> = ({ cam, wall = 'corr', col = '#2a3350', floor = false, children, glow }) => (
  <g><L cam={cam} d={0.4}><Wall kind={wall} col={col} y0={-400} y1={H + 400} /></L>{glow && <Glow x={960} y={540} r={700} c={glow} o={0.35} />}<L cam={cam} d={1}>{children}</L></g>
);
