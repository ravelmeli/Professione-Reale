import { Spec, CastSpec } from './engine';
const T = (s: string): number => { const [m, r] = s.split(':'); return Number(m) * 60 + Number(r); };
const Ch = (age: number, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => ['chi', x, pose, expr, { age, ...ex }];
const C = (who: string, x: number, pose = 'idle', expr = 'smile', ex: any = {}): CastSpec => [who, x, pose, expr, ex];
const st = (text: string, x: number, y: number, a: number, col?: string) => ({ k: 'stamp', x, y, text, a, col, e: 'slam' });
const ob = (k: string, x: number, y: number, a: number, s = 1.8, e: any = 'slide', extra: any = {}) => ({ k, x, y, a, s, e, ...extra });
const SA = { n: 'sala' }; const NN = { n: 'notte', truck: false };
const UF = (sign: string, extra: any = {}) => ({ n: 'ufficio', sign, ...extra });
const sp = (t: string, s: Omit<Spec, 'a'>): Spec => ({ a: T(t), ...s });
const DOTS = '#c9c1a8'; const PAN = '#7aa3a0';
const YEAR = (n: string, k: string, extra: any = {}) => ({ ins: ['dots', DOTS] as [string, string], objs: [ob('bubble', 960, 380, 0.1, 2.3, 'slam', { text: `ANNO ${n}` }), ob(k, 960, 780, 0.6, 2.4, 'drop', extra)], mv: 'push', grade: 'warm' });
export const SPECS_CHI2: Spec[] = [
  sp('0:00.0', { set: UF('UNIVERSITA'), cast: [Ch(19, 960, 'idle', 'smile')], objs: [ob('book', 790, 200, 0.4, 1.3, 'drop')], mv: 'push' }),
  sp('0:02.2', { ins: ['panels', PAN], objs: [ob('book', 960, 440, 0.2, 2.4, 'drop'), ob('bubble', 960, 860, 0.9, 2, 'drop', { text: '6 ANNI' })], mv: 'pull' }),
  sp('0:04.8', { ins: ['panels', PAN], objs: [ob('scalpel', 960, 440, 0.2, 2.4, 'drop'), ob('bubble', 960, 860, 0.9, 2, 'drop', { text: '5 ANNI' })], mv: 'pull' }),
  sp('0:07.8', { set: SA, cast: [Ch(19, 800, 'idle', 'smile'), Ch(50, 1130, 'idle', 'smile', { flip: true })], objs: [ob('bubble', 960, 170, 0.3, 1.5, 'drop', { text: '20 ANNI' })], mv: 'push' }),
  sp('0:10.9', { ...YEAR('1', 'book') }),
  sp('0:14.0', { ins: ['dots', DOTS], objs: [ob('coin', 960, 460, 0.2, 2.6, 'drop'), ob('cross', 960, 860, 0.9, 2.2, 'slam')], mv: 'push', grade: 'warm' }),
  sp('0:16.8', { set: UF('UNIVERSITA'), cast: [Ch(22, 960, 'shrug', 'concerned')], objs: [ob('bubble', 960, 150, 0.3, 1.4, 'drop', { text: 'E ORA?' })], mv: 'push', grade: 'dusk' }),
  sp('0:20.8', { ...YEAR('7', 'scalpel') }),
  sp('0:25.0', { set: SA, cast: [Ch(27, 960, 'hold', 'concerned')], objs: [ob('cal', 800, 200, 0.4, 1.4, 'on', { text: '5 ANNI' }), ob('mask', 1140, 230, 0.9, 1.2, 'drop')], mv: 'push' }),
  sp('0:27.3', { set: SA, cast: [Ch(28, 960, 'idle', 'deadpan')], objs: [ob('coin', 800, 220, 0.4, 1.3, 'drop')], mv: 'push', grade: 'dusk' }),
  sp('0:30.2', { ins: ['dots', DOTS], objs: [ob('coin', 960, 440, 0.2, 2.6, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '25.000 €' })], mv: 'push', grade: 'warm' }),
  sp('0:33.6', { ins: ['panels', PAN], objs: [ob('bubble', 960, 440, 0.2, 1.9, 'slam', { text: '26.000 €' }), ob('cal', 960, 860, 0.9, 1.7, 'on', { text: '3° ANNO' })], mv: 'pull' }),
  sp('0:36.9', { ins: ['dots', DOTS], objs: [ob('up', 960, 460, 0.2, 2.6, 'drop'), ob('bubble', 960, 860, 0.9, 1.7, 'drop', { text: 'AUMENTI' })], mv: 'push', grade: 'warm' }),
  sp('0:39.1', { ins: ['panels', PAN], objs: [ob('doc', 790, 460, 0.2, 1.6, 'drop'), ob('warn', 1130, 460, 0.8, 1.5, 'slam'), ob('bubble', 960, 860, 1.4, 1.9, 'drop', { text: 'VERIFICA' })], mv: 'pull' }),
  sp('0:40.7', { ...YEAR('12', 'stetho') }),
  sp('0:43.8', { set: UF('SANITA'), cast: [Ch(35, 800, 'point', 'smile'), C('sara', 1130, 'hold', 'smile', { flip: true })], objs: [ob('doc', 960, 360, 0.6, 1.1, 'drop')], mv: 'push' }),
  sp('0:47.0', { ins: ['dots', DOTS], objs: [ob('coin', 960, 440, 0.2, 2.6, 'slam'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '~50.000 €' })], mv: 'push', grade: 'warm' }),
  sp('0:49.6', { ins: ['panels', PAN], objs: [ob('cal', 960, 440, 0.2, 2, 'on', { text: '13 MESI' }), ob('doc', 960, 860, 0.9, 1.8, 'drop')], mv: 'pull' }),
  sp('0:52.6', { set: SA, cast: [Ch(35, 960, 'idle', 'concerned')], objs: [ob('warn', 800, 220, 0.3, 1.3, 'slam')], mv: 'push', grade: 'dusk' }),
  sp('0:53.8', { ins: ['dots', DOTS], objs: [ob('coin', 760, 520, 0.2, 1.8, 'drop'), ob('coin', 960, 520, 0.7, 1.8, 'drop'), ob('coin', 1160, 520, 1.2, 1.8, 'drop'), ob('bubble', 960, 880, 1.6, 1.7, 'drop', { text: '+ VOCI' })], mv: 'push', grade: 'warm' }),
  sp('0:56.6', { ...YEAR('27', 'cal', { text: '15 ANNI' }) }),
  sp('1:01.0', { ins: ['dots', DOTS], objs: [ob('bubble', 960, 440, 0.2, 1.9, 'slam', { text: '6.500 €' }), ob('bubble', 960, 860, 0.9, 1.5, 'drop', { text: 'POSIZIONE' })], mv: 'push', grade: 'warm' }),
  sp('1:05.4', { ins: ['panels', PAN], objs: [ob('tick', 960, 460, 0.2, 2.4, 'slam'), ob('bubble', 960, 860, 0.9, 1.6, 'drop', { text: 'VALUTAZIONE' })], mv: 'pull' }),
  sp('1:09.4', { ins: ['panels', PAN], objs: [ob('doc', 790, 460, 0.2, 1.6, 'drop'), ob('warn', 1130, 460, 0.8, 1.5, 'slam'), ob('bubble', 960, 860, 1.4, 1.9, 'drop', { text: 'VERIFICA' })], mv: 'pull' }),
  sp('1:13.3', { ...YEAR('31', 'scales') }),
  sp('1:16.4', { set: SA, cast: [Ch(48, 800, 'idle', 'smile'), Ch(50, 1130, 'point', 'smile', { flip: true })], objs: [ob('bubble', 960, 170, 0.3, 1.5, 'drop', { text: 'O…' })], mv: 'push' }),
  sp('1:19.6', { set: UF('DIREZIONE'), cast: [Ch(55, 960, 'point', 'smile')], objs: [ob('star', 790, 220, 0.5, 1.3, 'grow')], mv: 'push' }),
  sp('1:23.0', { ins: ['dots', DOTS], objs: [ob('up', 960, 460, 0.2, 2.4, 'drop'), ob('bubble', 960, 860, 0.9, 1.9, 'drop', { text: '+530 €/MESE' })], mv: 'push', grade: 'warm' }),
  sp('1:27.0', { ins: ['panels', PAN], objs: [ob('moon', 790, 460, 0.2, 1.6, 'grow'), ob('clock', 960, 460, 0.8, 1.5, 'on', { v: 3 }), ob('scales', 1130, 460, 1.4, 1.4, 'drop')], mv: 'pull' }),
  sp('1:30.9', { ins: ['dots', DOTS], objs: [ob('cross', 960, 520, 0.2, 2.6, 'slam'), ob('bubble', 960, 880, 0.9, 1.7, 'drop', { text: 'PRIVATO' })], mv: 'push', grade: 'warm' }),
  sp('1:34.1', { ins: ['dots', DOTS], objs: [st('LORDO', 960, 380, 0.2, '#c33631'), st('NETTO', 960, 760, 0.9, '#2a5cd0')], mv: 'punch', grade: 'warm' }),
  sp('1:36.3', { set: UF('UNIVERSITA'), cast: [Ch(19, 960, 'idle', 'smile')], objs: [ob('book', 790, 200, 0.4, 1.3, 'drop')], mv: 'push' }),
  sp('1:39.7', { set: SA, cast: [Ch(50, 960, 'idle', 'smile')], objs: [ob('mask', 800, 230, 0.4, 1.2, 'drop')], mv: 'push', grade: 'warm' }),
  sp('1:43.0', { set: SA, cast: [Ch(56, 960, 'idle', 'sad')], mv: 'push', grade: 'dusk' }),
  sp('1:45.2', { phone: 'sub' }),
];
