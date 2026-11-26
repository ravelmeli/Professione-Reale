import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const Ch = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['chi', x, pose, expr, { age, ...ex }];
const C = (who: string, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => [who, x, pose, expr, ex];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const SA = { n: 'sala' }; const CA = { n: 'casa' }; const NN = { n: 'notte', truck: false };
const UF = (sign: string, extra: any = {}) => ({ n: 'ufficio', sign, ...extra });
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0';
const NUM = (n: string, k: string, extra: any = {}) => ({ ins: ['dots', DOTS] as [string, string], objs: [ob('num', 960, 380, 0.1, 1.9, 'slam', { text: n }), ob(k, 960, 780, 0.6, 2.4, 'drop', extra)], mv: 'push', grade: 'warm' });
export const SPECS_CHI: Spec[] = [
  sp('0:00.0', { set: SA, cast: [Ch(26, 800, 'point', 'happy'), Ch(50, 1130, 'point', 'smile', { flip: true })], objs: [ob('coin', 960, 200, 0.5, 1.3, 'drop')], mv: 'push' }),
  sp('0:02.6', { set: SA, cast: [Ch(26, 800, 'idle', 'concerned'), Ch(50, 1130, 'idle', 'smile', { flip: true })], objs: [ob('bubble', 960, 170, 0.3, 1.4, 'drop', { text: 'VS' })], mv: 'push' }),
  sp('0:05.1', { ...NUM('1', 'stetho') }),
  sp('0:07.3', { set: UF('LAUREA'), cast: [Ch(26, 800, 'idle', 'smile'), C('marta', 1130, 'hold', 'smile', { flip: true })], objs: [ob('doc', 960, 360, 0.6, 1.1, 'drop')], mv: 'push' }),
  sp('0:09.2', { ins: ['dots', DOTS], objs: [ob('doc', 960, 460, 0.2, 2.6, 'drop'), ob('tick', 960, 860, 0.9, 2, 'slam')], mv: 'push', grade: 'warm' }),
  sp('0:12.3', { set: SA, cast: [Ch(26, 960, 'hold', 'concerned')], objs: [ob('scalpel', 800, 250, 0.4, 1.3, 'drop'), ob('mask', 1140, 250, 0.9, 1.2, 'drop')], mv: 'push' }),
  sp('0:16.4', { ins: ['dots', DOTS], objs: [ob('coin', 960, 440, 0.2, 2.6, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '22.700 €' })], mv: 'push', grade: 'warm' }),
  sp('0:20.0', { ins: ['panels', PAN], objs: [ob('bubble', 960, 420, 0.2, 1.8, 'slam', { text: '+ 2.300 €' }), ob('cal', 960, 860, 0.9, 1.7, 'on', { text: '1-2 ANNO' })], mv: 'pull' }),
  sp('0:23.6', { ins: ['panels', PAN], objs: [ob('bubble', 960, 420, 0.2, 1.8, 'slam', { text: '+ 3.300 €' }), ob('cal', 960, 860, 0.9, 1.7, 'on', { text: '3° ANNO' })], mv: 'pull' }),
  sp('0:25.7', { ins: ['dots', DOTS], objs: [ob('bubble', 960, 440, 0.2, 1.8, 'slam', { text: '25.000 €' }), ob('bubble', 960, 860, 0.9, 1.8, 'slam', { text: '26.000 €' })], mv: 'punch', grade: 'warm' }),
  sp('0:28.9', { set: SA, cast: [Ch(26, 960, 'point', 'deadpan')], objs: [ob('cal', 800, 200, 0.4, 1.4, 'on', { text: '2024/25' })], mv: 'push' }),
  sp('0:32.2', { ins: ['dots', DOTS], objs: [ob('up', 960, 460, 0.2, 2.6, 'drop'), ob('bubble', 960, 860, 0.9, 1.7, 'drop', { text: 'AUMENTI' })], mv: 'push', grade: 'warm' }),
  sp('0:36.1', { ins: ['panels', PAN], objs: [ob('doc', 790, 460, 0.2, 1.6, 'drop'), ob('warn', 1130, 460, 0.8, 1.5, 'slam'), ob('bubble', 960, 860, 1.4, 1.9, 'drop', { text: 'VERIFICA' })], mv: 'pull' }),
  sp('0:39.6', { ...NUM('2', 'star') }),
  sp('0:41.0', { set: SA, cast: [Ch(50, 960, 'idle', 'smile')], objs: [ob('stetho', 800, 250, 0.4, 1.2, 'drop')], mv: 'push', grade: 'warm' }),
  sp('0:42.2', { set: UF('SANITA'), cast: [Ch(50, 800, 'point', 'smile'), C('sara', 1130, 'hold', 'smile', { flip: true })], objs: [ob('doc', 960, 360, 0.6, 1.1, 'drop')], mv: 'push' }),
  sp('0:45.3', { ins: ['dots', DOTS], objs: [ob('coin', 960, 440, 0.2, 2.6, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '~50.000 €' })], mv: 'push', grade: 'warm' }),
  sp('0:48.3', { ins: ['panels', PAN], objs: [ob('cal', 960, 440, 0.2, 2, 'on', { text: '13 MESI' }), ob('doc', 960, 860, 0.9, 1.8, 'drop')], mv: 'pull' }),
  sp('0:50.9', { ins: ['panels', PAN], objs: [ob('doc', 790, 460, 0.2, 1.6, 'drop'), st('CCNL 22-24', 960, 860, 0.9, '#2a5cd0')], mv: 'pull' }),
  sp('0:55.2', { set: SA, cast: [Ch(50, 960, 'idle', 'concerned')], objs: [ob('warn', 800, 220, 0.3, 1.3, 'slam')], mv: 'push', grade: 'dusk' }),
  sp('0:57.0', { ins: ['dots', DOTS], objs: [ob('coin', 760, 520, 0.2, 1.8, 'drop'), ob('coin', 960, 520, 0.7, 1.8, 'drop'), ob('coin', 1160, 520, 1.2, 1.8, 'drop'), ob('bubble', 960, 880, 1.8, 1.7, 'drop', { text: '+ VOCI' })], mv: 'push', grade: 'warm' }),
  sp('1:00.9', { ins: ['dots', DOTS], objs: [ob('cross', 960, 520, 0.2, 2.6, 'slam'), ob('bubble', 960, 880, 0.9, 1.7, 'drop', { text: 'NON INCLUSE' })], mv: 'punch', grade: 'warm' }),
  sp('1:03.4', { ...NUM('3', 'scales') }),
  sp('1:05.2', { set: SA, cast: [Ch(26, 800, 'idle', 'sad'), Ch(50, 1130, 'idle', 'smile', { flip: true })], objs: [ob('bubble', 960, 170, 0.3, 1.5, 'drop', { text: '≈ ×2' })], mv: 'push', grade: 'warm' }),
  sp('1:08.3', { ins: ['panels', PAN], objs: [ob('clock', 760, 480, 0.2, 1.5, 'on', { v: 3 }), ob('moon', 960, 480, 0.8, 1.5, 'grow'), ob('scales', 1160, 480, 1.4, 1.4, 'drop')], mv: 'pull' }),
  sp('1:12.9', { ins: ['dots', DOTS], objs: [ob('cross', 960, 520, 0.2, 2.4, 'slam'), ob('bubble', 960, 880, 0.9, 1.7, 'drop', { text: 'PRIVATO' })], mv: 'push', grade: 'warm' }),
  sp('1:16.4', { ins: ['dots', DOTS], objs: [st('LORDO', 960, 380, 0.2, '#c33631'), st('NETTO', 960, 760, 0.9, '#2a5cd0')], mv: 'punch', grade: 'warm' }),
  sp('1:18.5', { set: SA, cast: [Ch(26, 800, 'idle', 'smile'), Ch(50, 1130, 'idle', 'smile', { flip: true })], objs: [ob('mask', 960, 200, 0.4, 1.3, 'drop')], mv: 'push', grade: 'warm' }),
  sp('1:21.8', { phone: 'sub' }),
];
