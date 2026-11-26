import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const A = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['asc', x, pose, expr, { age, ...ex }];
const C = (who: string, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => [who, x, pose, expr, ex];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const AT = { n: 'atrio' }; const TR = { n: 'tromba' };
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0'; const LIL = '#b9a8e8';
export const SPECS_ASC: Spec[] = [
  sp('0:00.0', { set: AT, cast: [A(24, 960, 'point', 'happy')], objs: [ob('dollar', 790, 230, 0.3, 1.4, 'slam'), ob('dollar', 1130, 260, 0.9, 1.2, 'slam')], mv: 'push' }),
  sp('0:02.4', { ins: ['dots', DOTS], objs: [ob('gradcap', 960, 520, 0.2, 2.6, 'drop'), ob('cross', 960, 860, 0.9, 2.2, 'slam')], mv: 'push', grade: 'warm' }),
  sp('0:04.9', { ins: ['panels', PAN], objs: [ob('pc', 960, 360, 0.2, 2, 'drop'), ob('cross', 960, 520, 0.8, 1.2, 'slam'), ob('chart', 960, 880, 1.6, 2, 'drop'), ob('cross', 1100, 880, 2.2, 1.2, 'slam')], mv: 'pull' }),
  sp('0:07.8', { set: AT, cast: [A(30, 960, 'point', 'smile')], objs: [ob('lift', 800, 320, 0.3, 1.6, 'grow')], mv: 'push' }),
  sp('0:10.6', { ins: ['dots', DOTS], objs: [ob('dollar', 960, 380, 0.2, 2.6, 'slam'), ob('bubble', 960, 800, 0.8, 1.9, 'drop', { text: '110.000 $' })], mv: 'push', grade: 'warm' }),
  sp('0:14.2', { ins: ['dots', DOTS], objs: [st('LORDI', 960, 600, 0.3, '#c33631')], mv: 'punch', grade: 'warm' }),
  sp('0:17.5', { ins: ['panels', PAN], objs: [ob('doc', 960, 400, 0.2, 2.4, 'drop'), st('BLS 2025', 960, 840, 0.9, '#2a5cd0')], mv: 'pull' }),
  sp('0:21.3', { set: AT, cast: [A(30, 960, 'idle', 'concerned')], objs: [ob('warn', 800, 520, 0.3, 1.4, 'slam'), ob('bubble', 960, 170, 0.9, 1.4, 'drop', { text: 'MEDIANA' })], mv: 'push', grade: 'dusk' }),
  sp('0:24.2', { ins: ['dots', DOTS], objs: [ob('chartdown', 960, 520, 0.2, 2.6, 'drop'), ob('bubble', 960, 880, 0.9, 1.7, 'drop', { text: '50%' })], mv: 'push', grade: 'warm' }),
  sp('0:27.4', { set: AT, cast: [A(24, 960, 'idle', 'sad')], objs: [ob('bubble', 960, 170, 0.4, 1.5, 'drop', { text: '< 60.000 $' })], mv: 'push', grade: 'dusk' }),
  sp('0:31.1', { set: AT, cast: [A(50, 960, 'cheer', 'happy')], objs: [ob('bubble', 960, 170, 0.4, 1.5, 'drop', { text: '> 158.000 $' }), ob('star', 790, 480, 0.9, 1.3, 'grow')], mv: 'push', grade: 'warm' }),
  sp('0:34.8', { set: AT, cast: [A(18, 960, 'shrug', 'concerned')], objs: [ob('bubble', 960, 170, 0.3, 1.3, 'drop', { text: '?' })], mv: 'push' }),
  sp('0:36.2', { ins: ['panels', PAN], objs: [ob('doc', 960, 460, 0.2, 2.6, 'drop'), ob('tick', 960, 860, 0.9, 2, 'slam')], mv: 'pull' }),
  sp('0:38.6', { set: TR, cast: [A(18, 800, 'hold', 'concerned'), A(45, 1130, 'point', 'smile', { flip: true })], objs: [ob('wrench', 960, 200, 0.4, 1.3, 'drop')], mv: 'push' }),
  sp('0:42.3', { ins: ['dots', DOTS], objs: [ob('wrench', 960, 400, 0.2, 2.6, 'drop'), ob('tick', 960, 800, 1.0, 1.8, 'slam')], mv: 'push', grade: 'warm' }),
  sp('0:46.0', { ins: ['panels', PAN], objs: [ob('lift', 960, 380, 0.2, 2, 'grow'), ob('escal', 960, 800, 0.9, 1.6, 'slide')], mv: 'pull' }),
  sp('0:48.8', { set: TR, cast: [A(30, 960, 'hold', 'concerned')], objs: [ob('ladder', 760, 520, 0.4, 2.2, 'slide')], mv: 'push', grade: 'dusk' }),
  sp('0:52.0', { ins: ['dots', DOTS], objs: [ob('up', 960, 460, 0.2, 2.6, 'drop'), ob('bubble', 960, 860, 0.9, 1.7, 'drop', { text: 'USA' })], mv: 'push', grade: 'warm' }),
  sp('0:55.7', { ins: ['dots', DOTS], objs: [ob('bubble', 960, 520, 0.2, 1.9, 'slam', { text: '+6%' }), ob('cal', 960, 860, 0.9, 1.7, 'on', { text: '2035' })], mv: 'punch', grade: 'warm' }),
  sp('0:58.8', { set: AT, cast: [A(30, 960, 'point', 'deadpan')], objs: [ob('bubble', 960, 170, 0.4, 1.5, 'drop', { text: 'DATI USA' })], mv: 'push' }),
  sp('1:00.5', { ins: ['panels', PAN], objs: [ob('flag', 960, 520, 0.2, 2.4, 'slide', { text: 'it' }), ob('bubble', 960, 880, 0.9, 1.6, 'drop', { text: 'CIFRE DIVERSE' })], mv: 'pull' }),
  sp('1:04.3', { set: AT, cast: [A(24, 960, 'idle', 'deadpan')], objs: [ob('dollar', 790, 200, 0.3, 1.3, 'drop'), ob('clock', 1130, 200, 0.9, 1.2, 'on', { v: 9 })], mv: 'push', grade: 'dusk' }),
  sp('1:07.1', { ins: ['panels', PAN], objs: [ob('cal', 790, 520, 0.2, 1.5, 'on', { text: 'ANNI' }), ob('doc', 960, 520, 0.9, 1.5, 'drop'), ob('scales', 1130, 520, 1.5, 1.3, 'drop')], mv: 'pull' }),
  sp('1:10.6', { set: AT, cast: [A(50, 960, 'idle', 'smile')], mv: 'push', grade: 'warm' }),
  sp('1:12.4', { set: AT, cast: [A(50, 960, 'idle', 'surprised')], objs: [ob('lift', 800, 320, 0.2, 1.6, 'grow'), ob('warn', 1130, 330, 0.8, 1.4, 'slam')], mv: 'punch', grade: 'dusk' }),
  sp('1:14.6', { phone: 'sub' }),
];
