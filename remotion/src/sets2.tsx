import React from 'react';
import { PROJECT } from './project';
import { Cam, L, W, H, FLOOR, S, Poly, Ln, Glow, Clock, Calendar, Sign, Truck, Wall, Floor, WindowView, Plant, Desk, Lamp, SIGN, shade } from './kit';
import { INK, ACCENT } from './rig';
import { SetP, Piazzale, Strada, Ufficio, Citta } from './sets';
import { Fx } from './kit2';

const NightSky: React.FC<{ t: number }> = ({ t }) => <g><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="#0d1226" />{Array.from({ length: 46 }).map((_, i) => <circle key={i} cx={(i * 211) % 2300 - 200} cy={30 + (i * 53) % 400} r={1.6 + (i % 3) * 0.5} fill="#cfd8f0" opacity={0.55 + 0.4 * Math.sin(t * 2 + i)} />)}</g>;
const Hills: React.FC<{ col: string; y?: number }> = ({ col, y = 500 }) => <path d={`M -400 ${y + 60} L -100 ${y - 20} L 300 ${y - 30} L 700 ${y + 20} L 1100 ${y - 40} L 1500 ${y} L 2000 ${y - 50} L 2400 ${y + 20} L 2400 ${FLOOR} L -400 ${FLOOR} Z`} fill={col} />;

export const Cabina: React.FC<SetP & { night?: boolean; speed?: number }> = ({ cam, t, cast, night, speed = 1 }) => {
  const sp = (t * speed) % 1;
  return (
    <g>
      <L cam={cam} d={0.3}>{night ? <NightSky t={t} /> : <><defs><linearGradient id="cs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6aa7e0" /><stop offset="1" stopColor="#dff0ff" /></linearGradient></defs><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="url(#cs)" /></>}<Hills col={night ? '#10162a' : '#8aaec0'} /></L>
      <L cam={cam} d={0.55}><rect x={-400} y={560} width={W + 800} height={200} fill={night ? '#1d3028' : '#5b8a58'} /><Poly p={[[900, 560], [1020, 560], [1500, 900], [420, 900]]} fill={night ? '#232a3c' : '#3a3f4d'} />{[0, 1, 2, 3, 4, 5].map((i) => { const k = (i + sp) / 6, y = 560 + k * k * 330, w = 6 + k * 36; return <rect key={i} x={960 - w / 2} y={y} width={w} height={6 + k * 30} fill={night ? '#ffe08a' : '#f4f1ea'} />; })}</L>
      <L cam={cam} d={1}>{cast}</L>
      <L cam={cam} d={1.25}><rect x={-400} y={780} width={W + 800} height={500} fill="#2a2e3d" stroke={INK} strokeWidth={4.5} /><rect x={-400} y={760} width={W + 800} height={40} fill="#1b1e28" /><circle cx={1250} cy={1000} r={190} fill="none" stroke={INK} strokeWidth={50} /><circle cx={1250} cy={1000} r={190} fill="none" stroke="#4a4f66" strokeWidth={36} /><Ln p={[[1060, 1000], [1440, 1000]]} sw={32} c="#4a4f66" /><circle cx={1250} cy={1000} r={46} fill="#4a4f66" stroke={INK} strokeWidth={5} /><circle cx={560} cy={880} r={56} fill="#f4f1ea" stroke={INK} strokeWidth={6} /><Ln p={[[560, 880], [596, 860]]} sw={6} c="#c33631" /></L>
      <rect x={0} y={0} width={W} height={60} fill="#1b1e28" /><rect x={0} y={0} width={70} height={H} fill="#1b1e28" /><rect x={W - 70} y={0} width={70} height={H} fill="#1b1e28" />
    </g>
  );
};
export const Area: React.FC<SetP> = ({ cam, t, cast, fore }) => (
  <g>
    <L cam={cam} d={0.3}><NightSky t={t} /><Hills col="#10162a" y={470} /></L>
    <L cam={cam} d={0.55}><S x={1250} y={330} w={520} h={360} r={4} fill="#2a3350" /><Wall kind="brick" col="#2a3350" y0={334} y1={686} /><Sign x={1300} y={360} w={420} text={PROJECT !== 'cam' ? 'BAR' : 'AREA DI SERVIZIO'} bg="#2a2f3c" fg={ACCENT} size={38} /><S x={1330} y={470} w={150} h={220} r={3} fill="#f0d58a" /><S x={1520} y={480} w={190} h={110} r={3} fill="#f0d58a" /></L>
    <L cam={cam} d={0.8}><Floor kind="asphalt" col="#1c2238" /><Lamp x={160} y={170} /><Lamp x={1040} y={170} />{PROJECT === 'cam' && [0, 1].map((i) => <Truck key={i} x={420 + i * 560} y={FLOOR + 70} s={0.42} lights={false} />)}<Fx kind="mist" t={t} /></L>
    <L cam={cam} d={1}>{cast}</L>{fore}
  </g>
);
export const Frontiera: React.FC<SetP & { a?: string; b?: string }> = ({ cam, t, cast, fore, truck = false, truckX = 400 }) => (
  <g>
    <L cam={cam} d={0.3}><defs><linearGradient id="fs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#8fc6f0" /><stop offset="1" stopColor="#e9f4ff" /></linearGradient></defs><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="url(#fs)" />{[0, 1, 2].map((i) => <ellipse key={i} cx={300 + i * 600 + (t * 8) % 60} cy={170 + (i % 2) * 70} rx={120} ry={28} fill="rgba(255,255,255,.85)" />)}<Hills col="#7aa48f" y={440} /></L>
    <L cam={cam} d={0.55}><S x={1280} y={330} w={260} h={360} r={6} fill="#e8ecf2" /><S x={1300} y={360} w={220} h={120} r={6} fill="#9fd0ff" /><Sign x={1290} y={290} w={240} text="DOGANA" bg="#2C3E50" fg="#f4f1ea" size={34} /></L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#4a4f5c" /><rect x={-400} y={FLOOR - 4} width={W + 800} height={6} fill="#f4f1ea" />{[0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => <rect key={i} x={i * 220 - 60} y={FLOOR + 180} width={120} height={12} fill="#e0a32e" />)}<g transform="translate(1000 690)"><S x={-80} y={-70} w={300} h={22} r={6} fill="#fff" />{[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-70 + i * 56} y={-68} width={28} height={18} fill="#e5392b" />)}<S x={-100} y={-100} w={30} h={110} r={5} fill="#8a93a6" /></g>{truck && <Truck x={truckX} y={FLOOR + 120} s={0.75} />}</L>
    <L cam={cam} d={1}>{cast}</L>{fore}
  </g>
);
export const Neve: React.FC<SetP & { closed?: boolean }> = ({ cam, t, cast, closed }) => (
  <g>
    <L cam={cam} d={0.3}><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="#c8d6e6" /><path d={`M -400 700 L -100 280 L 160 520 L 500 220 L 900 600 L 1260 260 L 1700 640 L 2000 420 L 2400 700 Z`} fill="#9fb3c8" stroke={INK} strokeWidth={4.5} />{[[-100, 280], [500, 220], [1260, 260]].map(([x, y], i) => <Poly key={i} p={[[x, y], [x - 70, y + 100], [x + 70, y + 100]]} fill="#fff" sw={0} />)}</L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 40} width={W + 800} height={H} fill="#eef3fa" /><rect x={-400} y={FLOOR + 80} width={W + 800} height={200} fill="#6a707e" />{[0, 1, 2, 3, 4, 5, 6].map((i) => <rect key={i} x={i * 300 - 80} y={FLOOR + 170} width={120} height={12} fill="#e0a32e" />)}{closed && <g transform="translate(1150 690)"><S x={-100} y={-80} w={260} h={24} r={6} fill="#fff" />{[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-90 + i * 50} y={-78} width={26} height={20} fill="#e5392b" />)}<S x={-120} y={-130} w={28} h={150} r={5} fill="#8a93a6" /><g transform="translate(-30 -250)"><Poly p={[[0, -50], [60, 44], [-60, 44]]} fill="#e5392b" /><rect x={-34} y={0} width={68} height={14} fill="#fff" /></g></g>}</L>
    <L cam={cam} d={1}>{cast}</L>
    <Fx kind="snow" t={t} />
  </g>
);
export const Officina: React.FC<SetP> = ({ cam, t, cast, truck = true, truckX = 1300, truckS = 0.8 }) => (
  <g>
    <L cam={cam} d={0.35}><Wall kind="panels" col="#3a4358" y0={-300} y1={FLOOR} /><S x={160} y={120} w={640} h={200} r={6} fill="#566178" /><Sign x={230} y={160} w={400} text="OFFICINA" bg="#e0a32e" size={64} /><S x={1180} y={140} w={520} h={300} r={6} fill="#566178" /></L>
    <L cam={cam} d={0.6}>{[0, 1, 2].map((i) => <g key={i} transform={`translate(${260 + i * 150} ${420 + i * 20})`}><circle r={64} fill="#17141f" stroke={INK} strokeWidth={5} /><circle r={26} fill="#c9ced6" stroke={INK} strokeWidth={4} /></g>)}{[0, 1, 2, 3].map((i) => <Ln key={i} p={[[1200 + i * 130, 160], [1200 + i * 130, 420]]} sw={4} c="#3a4358" />)}<g transform="translate(1300 300)"><g transform="rotate(-40)"><S x={-9} y={-6} w={18} h={96} r={8} fill="#c9ced6" /><circle cy={-26} r={28} fill="#c9ced6" stroke={INK} strokeWidth={5} /></g></g></L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR} width={W + 800} height={H} fill="#4a4f5c" /><rect x={-400} y={FLOOR - 4} width={W + 800} height={8} fill="#2a2f3c" />{truck && <Truck x={truckX} y={FLOOR + 110} s={truckS} lights={false} />}<Fx kind="sparks" t={t} o={0.6} /></L>
    <L cam={cam} d={1}>{cast}</L>
  </g>
);
export const Casa: React.FC<SetP> = ({ cam, t, cast, fore }) => (
  <g>
    <L cam={cam} d={0.35}><Wall kind="stripes" col="#d9b68a" y0={-300} y1={FLOOR} /><WindowView x={160} y={150} w={360} h={300} view="dusk" t={t} /><Glow x={1500} y={200} r={420} c="#ffd9a0" o={0.55} /></L>
    <L cam={cam} d={0.6}><Clock x={760} y={170} h={7} m={10} /><S x={940} y={130} w={150} h={110} r={4} fill="#f4f1ea" /><circle cx={1015} cy={185} r={30} fill="#8FD23F" stroke={INK} strokeWidth={3} /><S x={1480} y={280} w={260} h={410} r={8} fill="#e8e4da" /><Ln p={[[1480, 460], [1740, 460]]} sw={4} /><Plant x={780} y={FLOOR} /></L>
    <L cam={cam} d={0.8}><Floor kind="checker" col="#8a6a4a" /><Desk x={1000} y={FLOOR - 120} w={360} /><Glow x={1500} y={FLOOR + 80} r={340} c="#ffd9a0" o={0.4} /></L>
    <L cam={cam} d={1}>{cast}</L>{fore}
  </g>
);
export const Bunk: React.FC<SetP> = ({ cam, t, cast }) => (
  <g>
    <L cam={cam} d={0.4}><Wall kind="panels" col="#2a2f45" y0={-300} y1={FLOOR} /><S x={1300} y={140} w={380} h={240} r={14} fill="#0d1226" /><circle cx={1500} cy={230} r={34} fill="#fff3c4" stroke={INK} strokeWidth={4} />{[0, 1, 2, 3, 4].map((i) => <circle key={i} cx={1340 + i * 70} cy={170 + (i % 2) * 120} r={3} fill="#cfd8f0" />)}</L>
    <L cam={cam} d={0.7}><rect x={-400} y={FLOOR} width={W + 800} height={H} fill="#1c2036" /><S x={160} y={FLOOR - 130} w={900} h={130} r={10} fill="#3a4a7a" /><S x={160} y={FLOOR - 170} w={260} h={60} r={20} fill="#e8ecf2" /><Glow x={560} y={FLOOR - 200} r={420} c="#ffe2a0" o={0.35} /></L>
    <L cam={cam} d={1}>{cast}</L>
  </g>
);
export const StradaNight: React.FC<SetP> = ({ cam, t, cast, truck = true, truckX = 1100 }) => {
  const sp = (t * 400) % 200;
  return (
    <g>
      <L cam={cam} d={0.3}><NightSky t={t} /><circle cx={1500} cy={260} r={60} fill="#fff3c4" /></L>
      <L cam={cam} d={0.5}><Hills col="#10162a" y={480} /></L>
      <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#1c2238" /><rect x={-400} y={FLOOR - 4} width={W + 800} height={5} fill="#c9d4f0" />{Array.from({ length: 12 }).map((_, i) => <rect key={i} x={i * 200 - sp} y={FLOOR + 170} width={110} height={11} fill="#ffe08a" />)}{truck && <Truck x={truckX} y={FLOOR + 120} s={0.8} />}</L>
      <L cam={cam} d={1}>{cast}</L>
    </g>
  );
};
export const Pista: React.FC<SetP> = ({ cam, t, cast }) => (
  <g>
    <L cam={cam} d={0.3}><defs><linearGradient id="pk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#4f9fe0" /><stop offset="1" stopColor="#dff0ff" /></linearGradient></defs><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="url(#pk)" />{[0, 1, 2].map((i) => <ellipse key={i} cx={(i * 760 + t * 12) % 2300 - 200} cy={150 + i * 70} rx={180} ry={40} fill="#fff" opacity={0.85} />)}</L>
    <L cam={cam} d={0.5}><Hills col="#8aaec0" y={520} /><S x={1180} y={330} w={110} h={260} r={4} fill="#c9ced6" /><S x={1140} y={290} w={190} h={60} r={8} fill="#2a2f3c" /><S x={1160} y={300} w={150} h={34} r={4} fill="#9fd0e8" /><S x={500} y={470} w={560} h={130} r={6} fill="#aeb6c4" /><S x={520} y={490} w={520} h={46} r={3} fill="#9fd0e8" /></L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#4a4f5c" />{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => <rect key={i} x={i * 300 - 100} y={FLOOR + 130} width={170} height={14} fill="#f4f1ea" />)}<g transform={`translate(${1130 - (t * 20) % 40} ${FLOOR - 40}) scale(0.5)`}><Poly p={[[-190, 0], [-170, -60], [150, -60], [220, -20], [220, 20], [-190, 20]]} fill="#f4f6fa" /><Poly p={[[-190, -60], [-250, -150], [-210, -150], [-130, -60]]} fill="#2CC4E8" /><Poly p={[[-20, -10], [60, -10], [-80, 90], [-120, 90]]} fill="#dfe8f5" /><circle cx={-60} cy={-30} r={9} fill="#9fd0e8" stroke={INK} strokeWidth={3} /><circle cx={0} cy={-30} r={9} fill="#9fd0e8" stroke={INK} strokeWidth={3} /><circle cx={60} cy={-30} r={9} fill="#9fd0e8" stroke={INK} strokeWidth={3} /></g></L>
    <L cam={cam} d={1}>{cast}</L>
  </g>
);
export const Cockpit: React.FC<SetP & { night?: boolean }> = ({ cam, t, cast, night }) => (
  <g>
    <L cam={cam} d={0.3}><defs><linearGradient id="ck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={night ? '#0d1226' : '#2f86d6'} /><stop offset="1" stopColor={night ? '#1d2a44' : '#cfe8ff'} /></linearGradient></defs><rect x={-400} y={-300} width={W + 800} height={H + 600} fill="url(#ck)" />{[0, 1, 2, 3].map((i) => <ellipse key={i} cx={(i * 640 - t * 120 * (1 + i * 0.3) + 4000) % 2600 - 300} cy={220 + i * 110} rx={210} ry={46} fill="#fff" opacity={night ? 0.2 : 0.9} />)}</L>
    <L cam={cam} d={1}>{cast}</L>
    <L cam={cam} d={1.2}><rect x={-400} y={760} width={W + 800} height={500} fill="#262b3a" stroke={INK} strokeWidth={4.5} /><rect x={-400} y={740} width={W + 800} height={40} fill="#171b27" />{[0, 1, 2, 3, 4].map((i) => <g key={i}><circle cx={520 + i * 220} cy={880} r={64} fill="#0d1226" stroke={INK} strokeWidth={5} /><circle cx={520 + i * 220} cy={880} r={52} fill="#10223a" /><Ln p={[[520 + i * 220, 880], [520 + i * 220 + 40 * Math.cos(t * (1 + i * 0.3)), 880 + 40 * Math.sin(t * (1 + i * 0.3))]]} sw={5} c="#2CC4E8" /></g>)}<rect x={0} y={0} width={110} height={H} fill="#171b27" /><rect x={W - 110} y={0} width={110} height={H} fill="#171b27" /></L>
  </g>
);
export const Atrio: React.FC<SetP> = ({ cam, t, cast }) => (
  <g>
    <L cam={cam} d={0.4}><Wall kind="panels" col="#cfd3dc" y0={-300} y1={FLOOR} /><S x={600} y={150} w={720} h={540} r={6} fill="#aeb6c4" /><S x={630} y={180} w={330} h={510} r={3} fill="#d9dee8" /><S x={960} y={180} w={330} h={510} r={3} fill="#d9dee8" /><Ln p={[[960, 180], [960, 690]]} sw={5} /><S x={800} y={96} w={320} h={44} r={8} fill="#0d1226" /><text x={960} y={130} textAnchor="middle" fontFamily="Anton, Impact, sans-serif" fontSize={34} fill="#9B6BFF">{String(1 + Math.floor((t * 0.6) % 9))}</text><S x={1370} y={380} w={34} h={80} r={6} fill="#2a2f3c" /><circle cx={1387} cy={405} r={7} fill="#9B6BFF" /></L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#8a8f98" />{[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => <rect key={i} x={i * 260 - 120} y={FLOOR - 20} width={4} height={H} fill="#6a6f78" />)}</L>
    <L cam={cam} d={1}>{cast}</L>
  </g>
);
export const Tromba: React.FC<SetP> = ({ cam, t, cast }) => (
  <g>
    <L cam={cam} d={0.4}><rect x={-400} y={-300} width={W + 800} height={H + 600} fill="#1b1f2c" />{[700, 1220].map((x) => <g key={x}><S x={x - 14} y={-300} w={28} h={H + 600} r={2} fill="#3a3f4d" />{Array.from({ length: 12 }).map((_, i) => <rect key={i} x={x - 22} y={i * 110 - 40} width={44} height={10} fill="#5a6070" />)}</g>)}<Ln p={[[960, -300], [960, 500]]} sw={6} c="#8a8f98" /><S x={900} y={470} w={120} h={90} r={6} fill="#aeb6c4" /></L>
    <L cam={cam} d={0.8}>{[0, 1, 2, 3].map((i) => <rect key={i} x={-300 + i * 700} y={0} width={14} height={H} fill="#2a2f3c" />)}<rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#3a3f4d" /></L>
    <L cam={cam} d={1}>{cast}</L>
  </g>
);
export const Quadro: React.FC<SetP> = ({ cam, t, cast }) => (
  <g>
    <L cam={cam} d={0.4}><Wall kind="brick" col="#8a8f98" y0={-300} y1={FLOOR} /><S x={640} y={120} w={640} h={470} r={8} fill="#c9ced6" /><S x={664} y={144} w={592} h={422} r={4} fill="#aeb6c4" />{[0, 1, 2].map((r) => [0, 1, 2, 3, 4, 5].map((c) => <g key={`${r}${c}`}><S x={690 + c * 92} y={180 + r * 120} w={64} h={86} r={4} fill="#2a2f3c" /><S x={704 + c * 92} y={196 + r * 120} w={36} h={26} r={3} fill={(c + r) % 3 === 0 ? '#FFD400' : '#e8e2d0'} /></g>))}<Ln p={[[640, 80], [640, 120]]} sw={5} /><path d="M 1280 300 q 90 20 80 120 q -10 90 60 140" fill="none" stroke="#3b6ae0" strokeWidth={9} /><path d="M 1280 330 q 60 30 60 100 q 0 70 40 110" fill="none" stroke="#c33631" strokeWidth={9} /></L>
    <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#5a5f6a" />{[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => <rect key={i} x={i * 260 - 120} y={FLOOR - 20} width={4} height={H} fill="#454a55" />)}</L>
    <L cam={cam} d={1}>{cast}</L>
  </g>
);
export const Tempesta: React.FC<SetP> = ({ cam, t, cast }) => {
  const fl = Math.sin(t * 5.3) > 0.93;
  return (
    <g>
      <L cam={cam} d={0.3}><defs><linearGradient id="tp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#1b2238" /><stop offset="1" stopColor="#4a5470" /></linearGradient></defs><rect x={-400} y={-300} width={W + 800} height={FLOOR + 300} fill="url(#tp)" />{[0, 1, 2, 3].map((i) => <ellipse key={i} cx={(i * 620 + t * 40) % 2400 - 200} cy={120 + (i % 2) * 90} rx={260} ry={60} fill="#2a3048" />)}{fl && <Poly p={[[1100, 0], [1040, 150], [1090, 150], [1020, 340], [1150, 120], [1100, 120], [1160, 0]]} fill="#fff3c4" />}</L>
      <L cam={cam} d={0.55}><rect x={-400} y={FLOOR - 120} width={W + 800} height={H} fill="#2a3a30" />{[0, 1, 2].map((i) => <g key={i}><S x={300 + i * 700} y={FLOOR - 560} w={26} h={560} r={3} fill="#5a4636" /><S x={230 + i * 700} y={FLOOR - 540} w={166} h={14} r={3} fill="#5a4636" /></g>)}<path d={`M -100 ${FLOOR - 540} Q 300 ${FLOOR - 470} 530 ${FLOOR - 540} Q 960 ${FLOOR - 470} 1230 ${FLOOR - 540} Q 1660 ${FLOOR - 470} 1930 ${FLOOR - 540}`} fill="none" stroke={INK} strokeWidth={4} /></L>
      <L cam={cam} d={0.8}><rect x={-400} y={FLOOR - 20} width={W + 800} height={H} fill="#3a4a3a" /></L>
      <L cam={cam} d={1}>{cast}</L>
      <rect x={-400} y={-300} width={W + 800} height={H + 600} fill="#fff" opacity={fl ? 0.12 : 0} />
    </g>
  );
};
export const AnySet: React.FC<{ spec: any; cam: Cam; t: number; cast: React.ReactNode }> = ({ spec, cam, t, cast }) => {
  const n = typeof spec === 'string' ? spec : spec.n; const o = typeof spec === 'string' ? {} : spec;
  const p = { cam, t, cast, ...o };
  switch (n) {
    case 'piazzale': return <Piazzale {...p} />;
    case 'strada': return <Strada {...p} />;
    case 'ufficio': return <Ufficio {...p} />;
    case 'depot': return <Citta {...p} kind="depot" />;
    case 'negozio': return <Citta {...p} kind="negozio" />;
    case 'cantiere': return <Citta {...p} kind="cantiere" />;
    case 'cabina': return <Cabina {...p} />;
    case 'area': return <Area {...p} />;
    case 'frontiera': return <Frontiera {...p} />;
    case 'neve': return <Neve {...p} />;
    case 'officina': return <Officina {...p} />;
    case 'casa': return <Casa {...p} />;
    case 'bunk': return <Bunk {...p} />;
    case 'notte': return <StradaNight {...p} />;
    case 'pista': return <Pista {...p} />;
    case 'atrio': return <Atrio {...p} />;
    case 'quadro': return <Quadro {...p} />;
    case 'tempesta': return <Tempesta {...p} />;
    case 'tromba': return <Tromba {...p} />;
    case 'cockpit': return <Cockpit {...p} />;
    default: return <Piazzale {...p} />;
  }
};
