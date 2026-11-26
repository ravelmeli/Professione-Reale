import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const P = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['pil', x, pose, expr, { age, ...ex }];
const Ch = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['chi', x, pose, expr, { age, ...ex }];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const PI = { n: 'pista' }; const CK = { n: 'cockpit' }; const SA = { n: 'sala' };
const UF = (sign: string, extra: any = {}) => ({ n: 'ufficio', sign, ...extra });
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0';
const NUM = (n: string, k: string, extra: any = {}) => ({ ins: ['dots', DOTS] as [string, string], objs: [ob('num', 960, 380, 0.1, 1.9, 'slam', { text: n }), ob(k, 960, 780, 0.6, 2.4, 'drop', extra)], mv: 'push', grade: 'warm' });
export const SPECS_PVC: Spec[] = [
  sp('0:00.0', { set: PI, cast: [P(42, 800, 'point', 'smile'), P(42, 800, 'point', 'smile')].slice(0, 1), objs: [ob('plane', 1140, 250, 0.4, 1.0, 'slide'), ob('bubble', 960, 170, 0.3, 1.2, 'drop', { text: 'VS' })], mv: 'push' }),
  sp('0:01.9', { set: SA, cast: [Ch(50, 960, 'point', 'smile')], objs: [ob('coin', 800, 220, 0.4, 1.3, 'drop'), ob('bubble', 1140, 250, 0.9, 1.3, 'drop', { text: '?' })], mv: 'push' }),
  sp('0:03.3', { ins: ['panels', PAN], objs: [ob('bubble', 960, 440, 0.2, 2.6, 'slam', { text: 'USA' }), ob('bubble', 960, 860, 0.9, 1.8, 'drop', { text: 'DATI USA' })], mv: 'pull' }),
  sp('0:05.0', { ins: ['dots', DOTS], objs: [ob('chart', 960, 460, 0.2, 2.6, 'drop'), ob('tick', 960, 860, 0.9, 1.8, 'slam')], mv: 'push', grade: 'warm' }),
  sp('0:06.7', { ins: ['panels', PAN], objs: [ob('doc', 960, 440, 0.2, 2.4, 'drop'), st('BLS 2025', 960, 860, 0.9, '#2a5cd0')], mv: 'pull' }),
  sp('0:10.4', { ...NUM('1', 'plane') }),
  sp('0:12.6', { ins: ['dots', DOTS], objs: [ob('dollar', 960, 440, 0.2, 2.6, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '232.000 $' })], mv: 'push', grade: 'warm' }),
  sp('0:16.2', { ...NUM('2', 'stetho') }),
  sp('0:18.0', { ins: ['dots', DOTS], objs: [ob('dollar', 960, 440, 0.2, 2.6, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '414.000 $' })], mv: 'push', grade: 'warm' }),
  sp('0:22.3', { ins: ['panels', PAN], objs: [ob('bubble', 960, 440, 0.2, 1.9, 'slam', { text: 'MEDIANE' }), st('LORDE', 960, 860, 0.9, '#c33631')], mv: 'pull' }),
  sp('0:24.7', { set: SA, cast: [Ch(50, 960, 'cheer', 'happy')], objs: [ob('star', 800, 240, 0.4, 1.3, 'grow')], mv: 'push', grade: 'warm' }),
  sp('0:28.1', { ins: ['dots', DOTS], objs: [ob('warn', 960, 460, 0.2, 2.4, 'slam'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'MA…' })], mv: 'punch', grade: 'warm' }),
  sp('0:29.9', { ...NUM('3', 'cal', { text: 'ANNI' }) }),
  sp('0:31.4', { set: SA, cast: [Ch(26, 960, 'hold', 'concerned')], objs: [ob('bubble', 800, 200, 0.3, 1.3, 'drop', { text: '6 + 5' })], mv: 'push' }),
  sp('0:35.7', { set: CK, cast: [P(26, 960, 'hold', 'concerned')], objs: [ob('clock', 800, 220, 0.4, 1.3, 'on', { v: 3 }), ob('bubble', 1140, 250, 0.9, 1.4, 'drop', { text: '1500 ORE' })], mv: 'push' }),
  sp('0:39.8', { ...NUM('4', 'coin') }),
  sp('0:41.8', { set: SA, cast: [Ch(26, 960, 'idle', 'smile')], objs: [ob('coin', 800, 220, 0.4, 1.3, 'drop'), ob('bubble', 1140, 250, 0.9, 1.3, 'drop', { text: '25.000 €' })], mv: 'push', grade: 'warm' }),
  sp('0:46.4', { set: PI, cast: [P(22, 960, 'idle', 'concerned')], objs: [ob('coin', 800, 220, 0.4, 1.3, 'drop'), ob('cross', 1140, 250, 0.9, 1.2, 'slam')], mv: 'push', grade: 'dusk' }),
  sp('0:48.4', { ins: ['dots', DOTS], objs: [ob('coin', 960, 440, 0.2, 2.6, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '90-160 MILA' })], mv: 'push', grade: 'warm' }),
  sp('0:50.6', { ins: ['panels', PAN], objs: [st('STIMA', 960, 460, 0.2, '#c33631'), ob('warn', 960, 860, 0.9, 1.6, 'slam')], mv: 'pull' }),
  sp('0:51.9', { ...NUM('5', 'flag', { text: 'it' }) }),
  sp('0:54.4', { ins: ['panels', PAN], objs: [ob('flag', 960, 440, 0.2, 2.4, 'slide', { text: 'it' }), ob('bubble', 960, 860, 0.9, 1.7, 'drop', { text: 'NON COINCIDONO' })], mv: 'pull' }),
  sp('0:56.8', { ins: ['dots', DOTS], objs: [ob('bubble', 960, 440, 0.2, 2.0, 'slam', { text: '74-80 MILA €' }), ob('warn', 960, 860, 0.9, 1.5, 'slam')], mv: 'push', grade: 'warm' }),
  sp('1:01.7', { set: UF('SANITA'), cast: [Ch(50, 960, 'point', 'smile')], objs: [ob('bubble', 960, 150, 0.3, 1.5, 'drop', { text: '~50.000 €' })], mv: 'push' }),
  sp('1:05.3', { ins: ['panels', PAN], objs: [ob('coin', 760, 480, 0.2, 1.6, 'drop'), ob('coin', 960, 480, 0.7, 1.6, 'drop'), ob('coin', 1160, 480, 1.2, 1.6, 'drop'), ob('bubble', 960, 880, 1.8, 1.6, 'drop', { text: '+ VOCI' })], mv: 'pull' }),
  sp('1:08.5', { ins: ['dots', DOTS], objs: [ob('scales', 960, 460, 0.2, 2.4, 'drop'), ob('cross', 960, 860, 0.9, 1.8, 'slam')], mv: 'push', grade: 'warm' }),
  sp('1:12.3', { set: PI, cast: [P(46, 800, 'idle', 'concerned'), Ch(50, 1130, 'idle', 'concerned', { flip: true })], objs: [ob('bubble', 960, 170, 0.3, 1.5, 'drop', { text: 'CHI?' })], mv: 'push', grade: 'warm' }),
  sp('1:14.3', { ins: ['panels', PAN], objs: [ob('flag', 790, 460, 0.2, 1.4, 'slide', { text: 'it' }), ob('cal', 960, 460, 0.8, 1.4, 'on', { text: 'ANNI' }), ob('coin', 1130, 460, 1.4, 1.4, 'drop')], mv: 'pull' }),
  sp('1:18.2', { ins: ['dots', DOTS], objs: [ob('cross', 960, 460, 0.2, 2.4, 'slam'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'CARRIERA?' })], mv: 'push', grade: 'warm' }),
  sp('1:20.6', { phone: 'sub' }),
];
