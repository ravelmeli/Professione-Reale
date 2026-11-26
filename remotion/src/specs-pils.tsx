import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const P = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['pil', x, pose, expr, { age, ...ex }];
const C = (who: string, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => [who, x, pose, expr, ex];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const PI = { n: 'pista' }; const CK = { n: 'cockpit' }; const CKN = { n: 'cockpit', night: true };
const UF = (sign: string, extra: any = {}) => ({ n: 'ufficio', sign, ...extra });
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0'; const SKY = '#9fd0e8';
const NUM = (n: string, k: string, extra: any = {}, col = DOTS) => ({ ins: ['dots', col] as [string, string], objs: [ob('num', 960, 380, 0.1, 1.9, 'slam', { text: n }), ob(k, 960, 780, 0.6, 2.4, 'drop', extra)], mv: 'push', grade: 'warm' });
export const SPECS_PILS: Spec[] = [
  sp('0:00.0', { set: PI, cast: [P(19, 960, 'point', 'happy')], objs: [ob('headset', 800, 300, 0.4, 1.4, 'drop')], mv: 'push' }),
  sp('0:01.8', { set: PI, cast: [P(19, 960, 'shrug', 'concerned')], objs: [ob('bubble', 960, 300, 0.4, 1.2, 'drop', { text: '?' })], mv: 'push', grade: 'dusk' }),
  // 1 - visita medica
  sp('0:04.6', { ...NUM('1', 'ecg') }),
  sp('0:07.6', { set: UF('MEDICO'), cast: [P(19, 800, 'idle', 'concerned'), C('sara', 1120, 'hold', 'deadpan', { flip: true })], objs: [ob('ecg', 960, 360, 0.6, 1.1, 'drop')], mv: 'push' }),
  sp('0:10.4', { ins: ['dots', DOTS], objs: [ob('ecg', 960, 520, 0.2, 2.2, 'drop'), ob('cross', 960, 900, 1.0, 2, 'slam')], mv: 'push', grade: 'warm' }),
  sp('0:13.0', { set: PI, cast: [P(19, 960, 'idle', 'sad')], objs: [ob('cal', 800, 280, 0.4, 1.4, 'on', { text: 'OGNI ANNO' })], mv: 'push', grade: 'dusk' }),
  // 2 - costo
  sp('0:16.2', { ...NUM('2', 'coin') }),
  sp('0:18.3', { ins: ['panels', PAN], objs: [ob('coin', 960, 520, 0.2, 2.6, 'drop'), ob('coin', 760, 880, 0.9, 1.8, 'drop'), ob('coin', 1160, 880, 1.3, 1.8, 'drop')], mv: 'pull' }),
  sp('0:22.4', { ins: ['dots', DOTS], objs: [st('STIME', 960, 640, 0.3, '#c33631')], mv: 'punch', grade: 'warm' }),
  sp('0:25.9', { set: PI, cast: [P(19, 960, 'shrug', 'sad')], objs: [ob('house', 800, 300, 0.4, 1.4, 'grow'), ob('cross', 1120, 300, 0.9, 1.1, 'slam')], mv: 'push', grade: 'dusk' }),
  // 3 - ore
  sp('0:28.8', { ...NUM('3', 'doc') }),
  sp('0:31.6', { set: UF('LICENZA'), cast: [P(22, 800, 'idle', 'smile'), C('marta', 1120, 'talk', 'deadpan', { flip: true })], objs: [ob('doc', 960, 360, 0.6, 1.2, 'drop')], mv: 'push' }),
  sp('0:35.8', { ins: ['dots', DOTS], objs: [ob('clock', 960, 520, 0.2, 2.6, 'on', { v: 3 }), ob('bubble', 960, 900, 0.9, 1.9, 'drop', { text: '1500 ORE' })], mv: 'push', grade: 'warm' }),
  sp('0:39.0', { set: PI, cast: [P(22, 960, 'idle', 'deadpan')], objs: [ob('coin', 800, 300, 0.4, 1.4, 'drop'), ob('cross', 1120, 300, 0.9, 1.1, 'slam')], mv: 'push' }),
  // 4 - type rating
  sp('0:42.0', { ...NUM('4', 'plane') }),
  sp('0:44.6', { ins: ['panels', PAN], objs: [ob('plane', 960, 520, 0.2, 2.6, 'slide'), ob('doc', 960, 900, 0.9, 2.2, 'drop')], mv: 'pull' }),
  sp('0:48.4', { set: CK, cast: [P(27, 960, 'hold', 'concerned')], objs: [ob('coin', 800, 300, 0.4, 1.4, 'drop'), ob('yoke', 1120, 900, 0.8, 1.6, 'drop')], mv: 'push' }),
  // 5 - decidere
  sp('0:51.4', { ...NUM('5', 'star') }),
  sp('0:54.5', { set: CK, cast: [P(46, 960, 'point', 'deadpan')], objs: [ob('star', 800, 300, 0.5, 1.4, 'grow')], mv: 'push' }),
  sp('0:56.0', { set: CK, cast: [P(46, 960, 'idle', 'concerned')], objs: [ob('plane', 960, 300, 0.2, 1.4, 'slide')], mv: 'push' }),
  sp('0:58.6', { ins: ['panels', PAN], objs: [ob('plane', 960, 500, 0.2, 2.4, 'slide'), ob('gauge', 760, 880, 0.9, 1.6, 'slam', { v: 0.5 }), ob('cloud', 1160, 880, 1.3, 1.6, 'drop')], mv: 'pull' }),
  sp('1:01.0', { set: CK, cast: [P(46, 960, 'idle', 'deadpan')], objs: [ob('gauge', 800, 300, 0.4, 1.4, 'slam', { v: 0.7 }), ob('cloud', 1120, 300, 0.9, 1.2, 'drop')], mv: 'push' }),
  sp('1:03.8', { set: CKN, cast: [P(46, 960, 'idle', 'sad')], mv: 'push', grade: 'night' }),
  sp('1:06.2', { set: { n: 'casa' }, cast: [C('ines', 780, 'cheer', 'happy'), C('luca', 1100, 'cheer', 'happy', { flip: true })], objs: [ob('cake', 960, 300, 0.5, 1.4, 'grow')], mv: 'push', grade: 'warm' }),
  sp('1:09.8', { set: PI, cast: [P(46, 960, 'idle', 'smile')], objs: [ob('house', 800, 300, 0.4, 1.4, 'grow')], mv: 'push', grade: 'warm' }),
  sp('1:12.6', { set: { n: 'casa' }, cast: [P(46, 800, 'idle', 'sad'), C('luca', 1120, 'wave', 'happy', { flip: true, s: 1.4 })], mv: 'push', grade: 'dusk' }),
  sp('1:15.2', { phone: 'sub' }),
];
