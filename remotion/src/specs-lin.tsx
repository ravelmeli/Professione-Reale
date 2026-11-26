import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const Lw = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['lin', x, pose, expr, { age, ...ex }];
const C = (who: string, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => [who, x, pose, expr, ex];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const TP = { n: 'tempesta' }; const CA = { n: 'casa' }; const NS = { n: 'strada', truck: false };
const UF = (sign: string, extra: any = {}) => ({ n: 'ufficio', sign, ...extra });
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0';
const NUM = (n: string, k: string, extra: any = {}) => ({ ins: ['dots', DOTS] as [string, string], objs: [ob('num', 960, 380, 0.1, 1.9, 'slam', { text: n }), ob(k, 960, 780, 0.6, 2.4, 'drop', extra)], mv: 'push', grade: 'warm' });
export const SPECS_LIN: Spec[] = [
  sp('0:00.0', { set: TP, cast: [Lw(26, 960, 'point', 'concerned')], objs: [ob('storm', 800, 200, 0.3, 1.2, 'drop'), ob('dollar', 1130, 230, 0.9, 1.2, 'drop')], mv: 'push', fx: 'rain', grade: 'night' }),
  sp('0:04.0', { set: CA, cast: [C('ines', 800, 'wave', 'happy'), C('luca', 1120, 'wave', 'happy', { flip: true })], objs: [ob('house', 960, 300, 0.4, 1.4, 'grow')], mv: 'push', grade: 'warm' }),
  sp('0:05.8', { set: TP, cast: [Lw(26, 960, 'idle', 'deadpan')], objs: [ob('pole', 1140, 400, 0.2, 1.6, 'slide'), ob('lamp', 790, 220, 0.6, 1.1, 'drop')], mv: 'push', fx: 'rain', grade: 'night' }),
  sp('0:07.4', { ...NUM('1', 'chart') }),
  sp('0:09.2', { ins: ['dots', DOTS], objs: [ob('dollar', 960, 460, 0.2, 2.8, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '95.000 $' })], mv: 'push', grade: 'warm' }),
  sp('0:12.6', { ins: ['dots', DOTS], objs: [st('LORDI', 960, 600, 0.3, '#c33631')], mv: 'punch', grade: 'warm' }),
  sp('0:15.6', { set: TP, cast: [Lw(26, 960, 'idle', 'sad')], objs: [ob('bubble', 960, 150, 0.4, 1.4, 'drop', { text: '< 51.000 $' })], mv: 'push', fx: 'rain', grade: 'night' }),
  sp('0:18.4', { set: TP, cast: [Lw(40, 960, 'cheer', 'happy')], objs: [ob('bubble', 960, 150, 0.4, 1.4, 'drop', { text: '> 128.000 $' }), ob('star', 790, 480, 0.9, 1.3, 'grow')], mv: 'push', fx: 'rain', grade: 'warm' }),
  sp('0:21.7', { ins: ['panels', PAN], objs: [ob('doc', 960, 420, 0.2, 2.4, 'drop'), st('BLS 2025', 960, 840, 0.9, '#2a5cd0')], mv: 'pull' }),
  sp('0:25.1', { ...NUM('2', 'storm') }),
  sp('0:27.5', { ins: ['dots', DOTS], objs: [ob('storm', 960, 440, 0.2, 2.4, 'drop'), ob('cross', 960, 860, 0.9, 1.9, 'slam'), ob('dollar', 1140, 860, 1.4, 1.2, 'drop')], mv: 'push', grade: 'night' }),
  sp('0:30.8', { set: TP, cast: [Lw(26, 960, 'point', 'concerned')], objs: [ob('bubble', 960, 150, 0.3, 1.3, 'drop', { text: 'MA…' })], mv: 'push', fx: 'rain', grade: 'night' }),
  sp('0:32.4', { set: NS, cast: [Lw(26, 960, 'idle', 'sad')], objs: [ob('truck', 790, 260, 0.4, 1.1, 'slide', { text: 'LINEE' }), ob('pin', 1140, 240, 0.9, 1.2, 'drop')], mv: 'pan', fx: 'rain', grade: 'night' }),
  sp('0:35.2', { ins: ['panels', PAN], objs: [ob('clock', 790, 420, 0.2, 1.6, 'on', { v: 12 }), ob('cal', 1130, 420, 0.8, 1.5, 'on', { text: 'GIORNI' }), ob('house', 960, 860, 1.4, 1.6, 'grow')], mv: 'pull' }),
  sp('0:38.6', { ...NUM('3', 'clock', { v: 3 }) }),
  sp('0:40.6', { ins: ['dots', DOTS], objs: [ob('clock', 960, 460, 0.2, 2.6, 'on', { v: 3 }), ob('coin', 960, 860, 0.9, 1.8, 'drop')], mv: 'push', grade: 'warm' }),
  sp('0:43.0', { set: UF('CONTRATTO'), cast: [Lw(26, 800, 'idle', 'concerned'), C('marta', 1130, 'talk', 'deadpan', { flip: true })], objs: [ob('doc', 960, 360, 0.6, 1.1, 'drop')], mv: 'push' }),
  sp('0:45.2', { ...NUM('4', 'flag', { text: 'it' }) }),
  sp('0:47.0', { ins: ['panels', PAN], objs: [ob('moon', 790, 420, 0.2, 1.6, 'grow'), ob('cal', 1130, 420, 0.8, 1.5, 'on', { text: 'FESTIVI' }), ob('coin', 960, 860, 1.4, 1.8, 'drop')], mv: 'pull' }),
  sp('0:50.4', { set: CA, cast: [Lw(40, 960, 'hold', 'smile')], objs: [ob('phone', 790, 300, 0.4, 0.8, 'slide'), ob('coin', 1140, 260, 0.9, 1.2, 'drop')], mv: 'push', grade: 'dusk' }),
  sp('0:53.3', { set: UF('CONTRATTO'), cast: [Lw(40, 960, 'point', 'deadpan')], objs: [ob('doc', 960, 130, 0.4, 1.0, 'drop')], mv: 'push' }),
  sp('0:56.9', { ...NUM('5', 'warn') }),
  sp('0:58.7', { set: TP, cast: [Lw(26, 960, 'idle', 'concerned')], objs: [ob('bolt', 790, 220, 0.3, 1.2, 'slam'), ob('pole', 1140, 400, 0.6, 1.4, 'slide')], mv: 'push', fx: 'rain', grade: 'night' }),
  sp('1:01.9', { set: TP, cast: [Lw(26, 960, 'cheer', 'panic')], mv: 'punch', fx: 'rain', grade: 'night' }),
  sp('1:04.3', { set: NN(), cast: [Lw(26, 960, 'idle', 'concerned')], objs: [ob('bulb', 960, 200, 0.4, 1.4, 'drop')], mv: 'push', fx: 'rain', grade: 'night' }),
  sp('1:06.9', { ins: ['dots', DOTS], objs: [ob('dollar', 960, 460, 0.2, 2.4, 'drop'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'CIFRA MAGICA?' })], mv: 'push', grade: 'warm' }),
  sp('1:09.8', { ins: ['panels', PAN], objs: [ob('clock', 790, 460, 0.2, 1.5, 'on', { v: 3 }), ob('warn', 960, 460, 0.8, 1.5, 'slam'), ob('doc', 1130, 460, 1.4, 1.5, 'drop')], mv: 'pull' }),
  sp('1:14.2', { phone: 'sub' }),
];
function NN() { return { n: 'notte', truck: false }; }
