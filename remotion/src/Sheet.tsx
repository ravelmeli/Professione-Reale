import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Char, Head, HeadDefs, ACCENT, INK, Expr, Pose, View, CAST } from './rig';

const T: React.FC<{ x: number; y: number; children: React.ReactNode; size?: number; anchor?: 'start' | 'middle' }> = ({ x, y, children, size = 26, anchor = 'start' }) => (
  <text x={x} y={y} fill="#F4F1EA" fontSize={size} fontFamily="Impact, 'Arial Black', sans-serif" letterSpacing={2} textAnchor={anchor}>{children}</text>
);
const Truck: React.FC<{ x: number; y: number; s: number }> = ({ x, y, s }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} className="c">
    <defs><radialGradient id="hh"><stop offset="0" stopColor={ACCENT} stopOpacity="0.75" /><stop offset="1" stopColor={ACCENT} stopOpacity="0" /></radialGradient></defs>
    <circle cx={0} cy={-130} r={260} fill="url(#hh)" />
    <ellipse cx={40} cy={8} rx={300} ry={16} fill="rgba(0,0,0,.35)" />
    <rect x={-330} y={-250} width={460} height={220} rx={8} fill="#d9d4c4" stroke={INK} strokeWidth={4.5} />
    {Array.from({ length: 9 }).map((_, i) => <path key={i} d={`M ${-310 + i * 50} -246 L ${-310 + i * 50} -34`} stroke="rgba(0,0,0,.18)" strokeWidth={2.5} />)}
    <rect x={-330} y={-250} width={460} height={26} rx={8} fill={ACCENT} stroke={INK} strokeWidth={4.5} />
    <text x={-100} y={-104} textAnchor="middle" fill="#2a2f3c" fontSize={52} fontFamily="Impact, sans-serif" letterSpacing={4}>TRASPORTI</text>
    <path d="M 140 -190 L 250 -190 L 310 -110 L 310 -30 L 140 -30 Z" fill="#c33631" stroke={INK} strokeWidth={4.5} strokeLinejoin="round" />
    <path d="M 156 -176 L 236 -176 L 282 -112 L 156 -112 Z" fill="#9fd0ff" stroke={INK} strokeWidth={4.5} />
    <rect x={296} y={-80} width={22} height={40} rx={5} fill="#f6e08a" stroke={INK} strokeWidth={3.5} />
    <rect x={-330} y={-30} width={640} height={18} rx={4} fill="#2a2f3c" stroke={INK} strokeWidth={4.5} />
    {[-250, -190, 40, 210].map((wx) => <g key={wx}><circle cx={wx} cy={0} r={36} fill="#1d1f27" stroke={INK} strokeWidth={4.5} /><circle cx={wx} cy={0} r={15} fill="#c9ced6" stroke={INK} strokeWidth={3} /></g>)}
  </g>
);
export const Sheet: React.FC = () => {
  const ages = [22, 30, 38, 46, 54];
  const looks: [string, string][] = [['22', 'APPRENDISTA'], ['30', 'AUTISTA NAZIONALE'], ['38', 'INTERNAZIONALE'], ['46', 'CAPO TRAFFICO'], ['54', 'PADRONCINO']];
  const views: View[] = ['front', 'three', 'side', 'back'];
  const exprs: Expr[] = ['smile', 'happy', 'surprised', 'concerned', 'angry', 'sad', 'deadpan', 'panic'];
  const poses: Pose[] = ['idle', 'point', 'hold', 'cheer', 'shrug', 'cross'];
  const extras = ['ciro', 'marta', 'dino', 'ines', 'luca', 'vik', 'agente', 'sara'];
  const names: Record<string, string> = { ciro: 'CIRO · capo', marta: 'MARTA · traffico', dino: 'DINO · veterano', ines: 'INES · moglie', luca: 'LUCA · figlio', vik: 'VIK · autista', agente: 'AGENTE', sara: 'SARA · medico' };
  const sw = ['#111111', '#4A6B6E', '#6E4726', '#2C3E50', '#F4F1EA', '#C33631', ACCENT, '#13192B', '#e0a32e', '#b8452b'];
  return (
    <AbsoluteFill style={{ background: '#222836' }}>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080">
        <HeadDefs />
        <T x={40} y={56} size={44}>CAMIONISTA · SCHEDA PERSONAGGI</T>
        <T x={40} y={90} size={22}>ROCCO — IL PROTAGONISTA ATTRAVERSO I 5 LIVELLI (SEGNO: CAPELLI ROSSI)</T>
        {ages.map((a, i) => <g key={a}><Char who="rocco" age={a} x={120 + i * 215} y={500} s={0.98} expr={i === 4 ? 'happy' : 'smile'} /><T x={120 + i * 215} y={540} size={16} anchor="middle">{looks[i][1]}</T></g>)}
        <T x={1190} y={90} size={22}>4 VISTE · FRONTE / 3/4 / PROFILO / DIETRO</T>
        {views.map((v, i) => <Char key={v} who="rocco" age={30} view={v} x={1260 + i * 170} y={500} s={0.9} />)}
        <path d="M 1150 100 L 1150 560" stroke="#3a4156" strokeWidth={2} />
        <T x={40} y={610} size={22}>8 ESPRESSIONI</T>
        {exprs.map((e, i) => <g key={e} transform={`translate(${75 + i * 118} 700) scale(1.15)`} className="c"><Head o={CAST.rocco(22)} view="front" expr={e} /><text y={72} textAnchor="middle" fill="#F4F1EA" fontSize={14} letterSpacing={1}>{e.toUpperCase()}</text></g>)}
        <rect x={0} y={607} width={1000} height={160} fill="rgba(34,40,54,0)" />
        <T x={1010} y={600} size={22}>6 POSE</T>
        {poses.map((p, i) => <Char key={p} who="rocco" age={30} pose={p} x={1060 + i * 140} y={780} s={0.52} />)}
        <T x={40} y={830} size={22}>COMPARSE (STESSO RIG)</T>
        {extras.map((e, i) => <g key={e}><Char who={e} x={85 + i * 140} y={1030} s={0.5} /><T x={85 + i * 140} y={1062} size={14} anchor="middle">{names[e]}</T></g>)}
        <T x={1230} y={830} size={22}>OGGETTO EROE · ALONE ACCENTO</T>
        <Truck x={1560} y={985} s={0.55} />
        {sw.map((c, i) => <rect key={i} x={1220 + i * 46} y={1030} width={40} height={30} rx={4} fill={c} stroke={INK} strokeWidth={3} />)}
      </svg>
    </AbsoluteFill>
  );
};
