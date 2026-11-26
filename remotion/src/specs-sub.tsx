import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const D = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['sub', x, pose, expr, { age, ...ex }];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const FD = { n: 'fondale' }; const PI = { n: 'pista' };
const UF = (sign: string, extra: any = {}) => ({ n: 'ufficio', sign, ...extra });
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0'; const SEA = '#2a6fa8';
const NUM = (n: string, k: string, extra: any = {}) => ({ ins: ['dots', SEA] as [string, string], objs: [ob('num', 960, 380, 0.1, 1.9, 'slam', { text: n }), ob(k, 960, 780, 0.6, 2.4, 'drop', extra)], mv: 'push', grade: 'sea' });
export const SPECS_SUB: Spec[] = [
  sp('0:00.0', { set: FD, cast: [D(28, 960, 'point', 'concerned')], objs: [ob('diverhelm', 790, 220, 0.3, 1.1, 'drop'), ob('arc', 1140, 300, 0.9, 1.3, 'slide')], mv: 'push', grade: 'sea' }),
  sp('0:03.8', { ins: ['panels', SEA], objs: [ob('cross', 960, 460, 0.2, 2.2, 'slam'), ob('bubble', 960, 860, 0.9, 1.8, 'drop', { text: 'SQUALI?' })], mv: 'punch', grade: 'sea' }),
  sp('0:06.0', { set: FD, cast: [D(28, 960, 'idle', 'deadpan')], objs: [ob('bubble', 960, 170, 0.3, 1.4, 'drop', { text: 'BUIO?' })], mv: 'push', grade: 'sea' }),
  sp('0:08.0', { ...NUM('1', 'bolt') }),
  sp('0:10.2', { set: FD, cast: [D(28, 960, 'hold', 'concerned')], objs: [ob('arc', 800, 280, 0.4, 1.3, 'slide')], mv: 'push', grade: 'sea' }),
  sp('0:13.1', { ins: ['dots', SEA], objs: [ob('bolt', 960, 460, 0.2, 2.8, 'slam'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'SCOSSA' })], mv: 'punch', grade: 'sea' }),
  sp('0:16.4', { ins: ['panels', SEA], objs: [ob('plug', 960, 460, 0.2, 2.2, 'drop'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'ISOLARE' })], mv: 'pull', grade: 'sea' }),
  sp('0:19.8', { ins: ['dots', SEA], objs: [ob('arc', 960, 460, 0.2, 2.2, 'slide'), ob('tick', 960, 860, 0.9, 1.8, 'slam')], mv: 'push', grade: 'sea' }),
  sp('0:23.2', { ...NUM('2', 'gaspocket') }),
  sp('0:25.6', { ins: ['dots', SEA], objs: [ob('gaspocket', 960, 480, 0.2, 2.4, 'grow'), ob('bubble', 960, 880, 0.9, 1.6, 'drop', { text: 'IDROGENO' })], mv: 'push', grade: 'sea' }),
  sp('0:28.6', { set: FD, cast: [D(28, 960, 'idle', 'panic')], objs: [ob('gaspocket', 800, 260, 0.3, 1.2, 'grow'), ob('warn', 1140, 260, 0.9, 1.3, 'slam')], mv: 'punch', grade: 'sea' }),
  sp('0:32.1', { ins: ['panels', SEA], objs: [ob('gaspocket', 760, 460, 0.2, 1.6, 'grow'), ob('cross', 1160, 460, 0.8, 1.6, 'slam'), ob('bubble', 960, 860, 1.4, 1.8, 'drop', { text: 'PRECAUZIONI' })], mv: 'pull', grade: 'sea' }),
  sp('0:35.4', { ...NUM('3', 'depth') }),
  sp('0:38.1', { set: FD, cast: [D(28, 960, 'cheer', 'concerned')], objs: [ob('depth', 800, 300, 0.3, 1.0, 'drop')], mv: 'pull', grade: 'sea' }),
  sp('0:41.1', { ins: ['dots', SEA], objs: [ob('clock', 960, 460, 0.2, 2.4, 'on', { v: 3 }), ob('bubble', 960, 860, 0.9, 1.7, 'drop', { text: 'SOSTE' })], mv: 'push', grade: 'sea' }),
  sp('0:43.6', { ins: ['panels', SEA], objs: [ob('chamber', 960, 480, 0.2, 2.2, 'slide'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'IPERBARICA' })], mv: 'pull', grade: 'sea' }),
  sp('0:46.5', { set: FD, cast: [D(28, 960, 'shrug', 'concerned')], objs: [ob('bubble', 960, 170, 0.3, 1.4, 'drop', { text: 'QUALE?' })], mv: 'push', grade: 'sea' }),
  sp('0:50.0', { ins: ['dots', SEA], objs: [ob('scales', 960, 460, 0.2, 2.4, 'drop'), ob('bubble', 960, 860, 0.9, 1.7, 'drop', { text: 'NO CLASSIFICA' })], mv: 'push', grade: 'sea' }),
  sp('0:52.8', { ins: ['panels', SEA], objs: [ob('bolt', 760, 480, 0.2, 1.6, 'slam'), ob('gaspocket', 960, 480, 0.8, 1.3, 'grow'), ob('depth', 1160, 480, 1.4, 1.1, 'drop')], mv: 'pull', grade: 'sea' }),
  sp('0:55.4', { set: FD, cast: [D(28, 960, 'idle', 'concerned')], objs: [ob('bolt', 790, 240, 0.3, 1.0, 'slam'), ob('gaspocket', 960, 200, 0.7, 1.0, 'grow'), ob('depth', 1150, 260, 1.1, 0.9, 'drop')], mv: 'push', grade: 'sea' }),
  sp('0:59.8', { ins: ['dots', SEA], objs: [ob('bubble', 960, 480, 0.2, 2.2, 'slam', { text: '%?' }), ob('warn', 960, 860, 0.9, 1.8, 'slam')], mv: 'punch', grade: 'sea' }),
  sp('1:03.3', { ins: ['panels', SEA], objs: [ob('cross', 960, 460, 0.2, 2.4, 'slam'), ob('bubble', 960, 860, 0.9, 1.7, 'drop', { text: 'NO FONTE' })], mv: 'pull', grade: 'sea' }),
  sp('1:06.9', { set: FD, cast: [D(28, 960, 'point', 'deadpan')], objs: [ob('water', 800, 260, 0.3, 1.0, 'slide'), ob('bubble', 1140, 250, 0.8, 1.3, 'drop', { text: 'AD UMIDO' })], mv: 'push', grade: 'sea' }),
  sp('1:10.1', { ins: ['panels', SEA], objs: [ob('chamber', 960, 460, 0.2, 2.2, 'slide'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'CAMERA SECCA' })], mv: 'pull', grade: 'sea' }),
  sp('1:14.0', { set: FD, cast: [D(40, 960, 'idle', 'smile')], objs: [ob('wave', 790, 230, 0.4, 1.0, 'slide'), ob('bubble', 1140, 250, 0.9, 1.3, 'drop', { text: 'NAVI' })], mv: 'push', grade: 'sea' }),
  sp('1:18.5', { phone: 'sub' }),
];
