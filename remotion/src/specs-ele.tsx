import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const E = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['ele', x, pose, expr, { age, ...ex }];
const C = (who: string, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => [who, x, pose, expr, ex];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const Q = { n: 'quadro' }; const CA = { n: 'casa' };
const UF = (sign: string, extra: any = {}) => ({ n: 'ufficio', sign, ...extra });
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0';
const NUM = (n: string, k: string, extra: any = {}) => ({ ins: ['dots', DOTS] as [string, string], objs: [ob('num', 960, 380, 0.1, 1.9, 'slam', { text: n }), ob(k, 960, 780, 0.6, 2.4, 'drop', extra)], mv: 'push', grade: 'warm' });
export const SPECS_ELE: Spec[] = [
  sp('0:00.0', { set: Q, cast: [E(19, 960, 'point', 'happy')], objs: [ob('tester', 790, 250, 0.4, 1.3, 'drop'), ob('bolt', 1140, 260, 0.9, 1.1, 'slam')], mv: 'push' }),
  sp('0:02.6', { set: Q, cast: [E(19, 960, 'shrug', 'concerned')], objs: [ob('bubble', 960, 170, 0.3, 1.3, 'drop', { text: '€ ?' })], mv: 'push', grade: 'dusk' }),
  sp('0:05.2', { ...NUM('1', 'doc') }),
  sp('0:07.0', { set: UF('CONTRATTO'), cast: [E(19, 800, 'idle', 'concerned'), C('marta', 1120, 'talk', 'deadpan', { flip: true })], objs: [ob('doc', 960, 360, 0.6, 1.1, 'drop')], mv: 'push' }),
  sp('0:09.4', { ins: ['panels', PAN], objs: [ob('doc', 790, 420, 0.2, 1.5, 'drop'), ob('doc', 1130, 420, 0.8, 1.5, 'drop'), ob('doc', 790, 840, 1.4, 1.5, 'drop'), ob('doc', 1130, 840, 2.0, 1.5, 'drop')], mv: 'pull' }),
  sp('0:12.6', { set: UF('TABELLE'), cast: [E(19, 960, 'point', 'deadpan')], objs: [ob('chart', 960, 120, 0.4, 1.0, 'drop')], mv: 'push' }),
  sp('0:15.8', { ...NUM('2', 'wrench') }),
  sp('0:17.2', { set: Q, cast: [E(19, 800, 'hold', 'concerned'), E(40, 1130, 'point', 'smile', { flip: true })], objs: [ob('tester', 960, 130, 0.5, 1.1, 'drop')], mv: 'push' }),
  sp('0:19.6', { ins: ['dots', DOTS], objs: [ob('bubble', 960, 420, 0.2, 2.2, 'slam', { text: '% QUALIFICATO' }), ob('chartdown', 960, 860, 0.9, 2, 'drop')], mv: 'push', grade: 'warm' }),
  sp('0:22.7', { ins: ['panels', PAN], objs: [ob('bubble', 960, 420, 0.2, 1.8, 'slam', { text: '< 50%' }), ob('warn', 960, 860, 1.0, 1.8, 'slam')], mv: 'pull' }),
  sp('0:25.2', { ins: ['dots', DOTS], objs: [ob('up', 960, 460, 0.2, 2.6, 'drop'), ob('cal', 960, 860, 0.9, 1.7, 'on', { text: 'ANNI' })], mv: 'push', grade: 'warm' }),
  sp('0:28.9', { ...NUM('3', 'scales') }),
  sp('0:31.5', { ins: ['dots', DOTS], objs: [st('LORDO', 960, 380, 0.2, '#c33631'), ob('doc', 960, 800, 0.8, 2, 'drop')], mv: 'punch', grade: 'warm' }),
  sp('0:34.4', { ins: ['dots', DOTS], objs: [st('NETTO', 960, 380, 0.2, '#2a5cd0'), ob('coin', 960, 800, 0.8, 2, 'drop')], mv: 'punch', grade: 'warm' }),
  sp('0:36.9', { ...NUM('4', 'plug') }),
  sp('0:38.2', { set: CA, cast: [E(30, 960, 'idle', 'deadpan')], objs: [ob('bubble', 960, 170, 0.3, 1.3, 'drop', { text: 'BASE' })], mv: 'push' }),
  sp('0:40.0', { ins: ['panels', PAN], objs: [ob('clock', 790, 420, 0.2, 1.6, 'on', { v: 10 }), ob('fuel', 1130, 420, 0.8, 1.5, 'drop'), ob('coin', 960, 860, 1.4, 1.8, 'drop')], mv: 'pull' }),
  sp('0:43.2', { ins: ['dots', DOTS], objs: [ob('coin', 960, 520, 0.2, 2.8, 'slam'), ob('star', 960, 860, 0.9, 1.6, 'grow')], mv: 'push', grade: 'warm' }),
  sp('0:45.6', { ...NUM('5', 'star') }),
  sp('0:47.0', { set: Q, cast: [E(22, 960, 'idle', 'smile')], objs: [ob('tester', 790, 250, 0.4, 1.3, 'drop')], mv: 'push' }),
  sp('0:49.3', { set: Q, cast: [E(22, 770, 'idle', 'smile', { s: 1.5 }), E(32, 960, 'idle', 'smile', { s: 1.5 }), E(46, 1150, 'idle', 'smile', { s: 1.5, flip: true })], mv: 'wide', grade: 'warm' }),
  sp('0:54.0', { set: UF('IMPIANTO'), cast: [E(46, 800, 'point', 'smile'), C('marta', 1130, 'hold', 'smile', { flip: true })], objs: [ob('doc', 960, 360, 0.6, 1.2, 'drop')], mv: 'push' }),
  sp('0:57.3', { ins: ['dots', DOTS], objs: [ob('doc', 960, 420, 0.2, 2.4, 'drop'), ob('bubble', 960, 840, 0.9, 1.7, 'drop', { text: 'DM 37/2008' })], mv: 'push', grade: 'warm' }),
  sp('1:00.6', { set: Q, cast: [E(22, 960, 'idle', 'happy')], objs: [ob('bolt', 790, 250, 0.4, 1.1, 'slam'), ob('bulb', 1140, 250, 0.9, 1.2, 'drop')], mv: 'push', grade: 'warm' }),
  sp('1:03.6', { set: CA, cast: [E(40, 960, 'idle', 'smile')], objs: [ob('star', 790, 250, 0.5, 1.2, 'grow')], mv: 'push', grade: 'warm' }),
  sp('1:08.1', { ins: ['panels', PAN], objs: [ob('doc', 790, 420, 0.2, 1.6, 'drop'), ob('tick', 1130, 420, 0.8, 1.4, 'slam'), ob('bubble', 960, 860, 1.4, 1.9, 'drop', { text: 'LIVELLO %' })], mv: 'pull' }),
  sp('1:10.6', { phone: 'sub' }),
];
