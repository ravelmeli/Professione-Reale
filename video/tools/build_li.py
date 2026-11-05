"""v3 — « La tua vita dopo 15 anni da camionista », 9:16.
Décors vivants qui s'enrichissent mot à mot (connecteurs animés, compteurs, tampons, badges),
règle de carrière, sorties « le décor recule », sous-titres flous→nets avec mot clé qui rougit
au moment où il est dit, nappe ambiante continue et effets sonores variés.
Usage (depuis video/) : python3 tools/build3.py   ->  video/v3/
"""
import os, re, json, shutil, difflib, math
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'vli')
CUT = os.path.join(ROOT, 'assets', 'cut-eli')
SFXSRC = os.path.join(ROOT, '..', '.claude', 'skills', 'media-use', 'audio', 'assets', 'sfx')
AUDSRC = os.path.join(ROOT, 'assets', 'audio')
VOICE = '/root/.claude/uploads/91729ddc-3274-50e3-9f11-8e52419e14ce/280557de-Generated_Audio_October_24_2026_-_5_04PM.wav'
SCRIPT = os.path.join(ROOT, '..', 'scripts', 'elettricista-vs-idraulico-short.txt')
SRT = os.path.join(ROOT, '..', 'scripts', 'eli-scenes.srt')
TOTAL = 85.5
W, H = 1080, 1920
CAP_Y = 1365
K_IMG, K_BOX = 1.2, 1.12
ZB = 1290
SFX2SRC = os.path.join(ROOT, 'assets', 'sfx2')
RED, GOLD, GREEN, INK, GREY, BLUE = '#ff4d6d', '#ffd166', '#3ddc97', '#ffffff', '#9aa0d8', '#6f7bff'
OVER = 0.32   # recouvrement entre deux décors

# ------------------------------------------------------------------ temps et mots
def parse_srt(path):
    out = []
    for blk in open(path, encoding='utf-8').read().strip().split('\n\n'):
        l = blk.split('\n')
        a, b = l[1].split(' --> ')
        f = lambda s: int(s[:2]) * 3600 + int(s[3:5]) * 60 + int(s[6:8]) + int(s[9:]) / 1000
        out.append((f(a), f(b), ' '.join(l[2:])))
    return out

SC = parse_srt(SRT)
NUMW = set('milleseicentocinquanta duecento venticinque sessanta trenta ottanta'.split())
norm = lambda t: re.sub(r"[^\w]", "", t.lower().replace("l'", "l"))
WW = [[d['w'], d['s'], d['e']] for d in json.load(open(os.path.join(HERE, 'words-eli.json')))]
swords = [w for l in open(SCRIPT, encoding='utf-8') if l.strip() for w in l.split()]
st = ['NUM' if norm(w) in NUMW else norm(w) for w in swords]
wt = ['NUM' if re.fullmatch(r'[\d.,]+', w[0]) else norm(w[0]) for w in WW]
sm = difflib.SequenceMatcher(None, st, wt, autojunk=False)
TW = [None] * len(swords)
for b in sm.get_matching_blocks():
    for k in range(b.size):
        TW[b.a + k] = (WW[b.b + k][1], WW[b.b + k][2])
known = [i for i, x in enumerate(TW) if x]
for i in range(len(TW)):
    if TW[i] is None:
        p = max([j for j in known if j < i], default=None)
        n = min([j for j in known if j > i], default=None)
        if p is None: TW[i] = (0.0, 0.2)
        elif n is None: TW[i] = (TW[p][1], TW[p][1] + .3)
        else:
            f = (i - p) / (n - p); t = TW[p][1] + (TW[n][0] - TW[p][1]) * f; TW[i] = (t, t + .25)

_p = 0.0
for i in range(len(TW)):
    a, b = TW[i]; a = max(a, _p); b = max(b, a + .12); TW[i] = (a, b); _p = a + .01

class Beat:
    pass
BEATS = []
cum = 0
for k, (s, e, text) in enumerate(SC, 1):
    b = Beat(); b.n, b.s, b.e, b.text = k, s, e, text
    nw = len(text.split())
    b.words = [(swords[cum + i], TW[cum + i][0], TW[cum + i][1]) for i in range(nw)]
    cum += nw
    BEATS.append(b)
assert cum == len(swords)
for i, b in enumerate(BEATS):          # bornes de plan recalées sur les mots réellement dits
    b.s = 0.0 if i == 0 else b.words[0][1]
for i, b in enumerate(BEATS):
    b.e = BEATS[i + 1].s if i + 1 < len(BEATS) else round(b.words[-1][2] + .35, 3)
_f = lambda t: '%02d:%02d:%02d,%03d' % (t // 3600, t % 3600 // 60, t % 60, round((t % 1) * 1000))
open(os.path.join(ROOT, '..', 'scripts', 'eli-scenes-aligned.srt'), 'w', encoding='utf-8').write(
    '\n'.join(f'{b.n}\n{_f(b.s)} --> {_f(b.e)}\n{b.text}\n' for b in BEATS))

def T(beat, word=None, off=0.0):
    """instant absolu (s) où le mot est dit dans le plan `beat` ; sans mot : début du plan."""
    b = BEATS[beat - 1]
    if word is None:
        return round(b.s + off, 3)
    k = norm(word)
    for w, t0, t1 in b.words:
        if norm(w).startswith(k) or norm(w).startswith('l' + k):
            return round(max(b.s, t0) + off, 3)
    raise SystemExit(f'mot introuvable: {word!r} dans le plan {beat}: {b.text}')

# ------------------------------------------------------------------ assets
for d in ('assets/img', 'assets/sfx', 'assets/sfx2', 'assets/audio', 'compositions'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
SIZE = {}
for f in os.listdir(CUT):
    im = Image.open(os.path.join(CUT, f)); im.thumbnail((1100, 1100))
    im.save(os.path.join(OUT, 'assets', 'img', f), optimize=True); SIZE[f[:-4]] = im.size
shutil.copy(os.path.join(AUDSRC, 'voce_eli_norm.wav'), os.path.join(OUT, 'assets', 'voce.wav'))
for f in ('bed.wav', 'sweep.wav', 'music.wav'):
    shutil.copy(os.path.join(AUDSRC, f), os.path.join(OUT, 'assets', 'audio', f))
for f in os.listdir(AUDSRC):
    if f.startswith('countup-'): shutil.copy(os.path.join(AUDSRC, f), os.path.join(OUT, 'assets', 'audio', f))
SFXDUR = {k: v['duration'] for k, v in json.load(open(os.path.join(SFXSRC, 'manifest.json'))).items()}
SFXDUR['sweep'] = 0.9
for D in ('0.8', '1.1', '1.4'): SFXDUR[f'countup-{D}'] = float(D) + .1
SFX2 = set()
for f in os.listdir(SFX2SRC):
    if f.endswith('.mp3'):
        n = f[:-4]; SFX2.add(n)
        shutil.copy(os.path.join(SFX2SRC, f), os.path.join(OUT, 'assets', 'sfx2', f))
        SFXDUR[n] = round(float(__import__('subprocess').run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(SFX2SRC, f)], capture_output=True, text=True).stdout.strip()), 3)
for f in os.listdir(SFXSRC):
    if f.endswith('.mp3') or f == 'CREDITS.md':
        shutil.copy(os.path.join(SFXSRC, f), os.path.join(OUT, 'assets', 'sfx', f))

# ------------------------------------------------------------------ DSL
SFXLOG = []     # (t_abs, name, volume)
_rot = {'pop': 0, 'impact': 0}
def sfx(t, name, vol=.33):
    SFXLOG.append((round(t, 3), name, vol))

def ticks(t, dur, n=None, vol=.14):
    n = n or max(4, int(dur / .12))
    for i in range(n):
        sfx(t + i * dur / n, 'click-soft', vol)

def pop_sfx(t, vol=.3):
    seq = ['pop', 'ping', 'click-soft', 'pop']
    sfx(t, seq[_rot['pop'] % 4], vol); _rot['pop'] += 1

def impact_sfx(t):
    sfx(t, 'stamp', .5); sfx(t + .02, 'impact-bass-1' if _rot['impact'] % 2 == 0 else 'impact-bass-2', .26); _rot['impact'] += 1

def count_sfx(t, dur):
    d = min((0.8, 1.1, 1.4), key=lambda x: abs(x - dur))
    sfx(t, f'countup-{d}', .3)

class Stage:
    def __init__(self, sid, b0, b1, ruler=None):
        self.id, self.b0, self.b1 = sid, b0, b1
        self.t0 = BEATS[b0 - 1].s
        self.t1 = BEATS[b1 - 1].e
        self.items, self.paths, self.counters, self.punches = [], [], [], []
        self.zt = 300 if sid in ('s1', 's13') else 470
        self.n = 0
    def _id(self, p):
        self.n += 1
        return f'{self.id}-{p}{self.n}'
    # --- éléments
    def img(self, name, cx, cy, h=None, w=None, enter='pop', at=None, until=None, rot=0, z=3, drift=0.03, flash=False, snd=True, dim=None):
        self.items.append(dict(k='img', id=self._id('i'), name=name, cx=cx, cy=cy, h=h, w=w, enter=enter,
                               at=self.t0 if at is None else at, until=until, rot=rot, z=z, drift=drift, flash=flash, snd=snd, dim=dim))
    def box(self, html, cx, cy, w, h, enter='pop', at=None, until=None, rot=0, z=4, flash=False, snd='pop', cls='', dim=None):
        self.items.append(dict(k='box', id=self._id('b'), html=html, cx=cx, cy=cy, w=w, h=h, enter=enter,
                               at=self.t0 if at is None else at, until=until, rot=rot, z=z, flash=flash, snd=snd, cls=cls, drift=0, dim=dim))
    def tag(self, text, cx, cy, w=520, color='blue', **kw):
        self.box(f'<div class="gtag {color}"><i class="dot"></i>{text}</div>', cx, cy, w, 84, **kw)
    def stamp(self, text, cx, cy, w=560, rot=-8, size=62, color=RED, **kw):
        kw.setdefault('snd', 'impact'); kw.setdefault('flash', True)
        self.box(f'<div class="stamp" style="font-size:{size}px;color:{color};border-color:{color}">{text}</div>', cx, cy, w, int(size * 1.9), rot=rot, **kw)
    def badge(self, kind, cx, cy, at, size=84, **kw):
        sym, col = ('✓', GREEN) if kind == 'ok' else ('✕', RED)
        kw.setdefault('snd', 'ping' if kind == 'ok' else 'click')
        self.box(f'<div class="badge" style="background:{col};box-shadow:0 0 30px {col}"><span>{sym}</span></div>', cx, cy, size, size, at=at, flash=True, z=8, **kw)
    def tiles(self, letters, cx, cy, at, size=84, gap=10):
        n = len(letters); w = n * size + (n - 1) * gap
        tid = self._id('t')
        t = ''.join(f'<div class="tile" id="{tid}-{i}" style="width:{size}px;height:{int(size*1.12)}px"><b style="font-size:{int(size*.52)}px">{c}</b></div>' for i, c in enumerate(letters))
        self.items.append(dict(k='tiles', id=self._id('tl'), html=f'<div class="tiles" style="gap:{gap}px">{t}</div>', cx=cx, cy=cy, w=w, h=int(size * 1.12),
                               at=at, until=None, rot=0, z=4, enter='none', flash=False, snd=None, cls='', drift=0, dim=None, count=n, tid=tid))
    def panel(self, title, rows, cx, cy, w=560, at=None, until=None, **kw):
        rh = 100
        h = 92 + rh * len(rows) + 22
        html = f'<div class="glass"><div class="gtag blue small"><i class="dot"></i>{title}</div>'
        pid = self._id('p')
        for j, r in enumerate(rows):
            rid = f'{pid}-r{j}'
            val = r.get('fmt', '{n}').replace('{n}', fmtn(r.get('frm', 0))) if 'to' in r else r['value']
            cls = 'rv strike' if r.get('strike') else 'rv'
            html += (f'<div class="row" id="{rid}"><span class="rl">{r["label"]}</span>'
                     f'<span class="{cls}" id="{rid}-v" style="color:{r.get("color", INK)}">{val}</span></div>')
            if 'to' in r:
                self.counters.append(dict(el=f'{rid}-v', frm=r.get('frm', 0), to=r['to'], fmt=r.get('fmt', '{n}'),
                                          t=r.get('at', at if at is not None else self.t0) + .1, dur=r.get('dur', 1.1)))
            if r.get('at') is not None and r['at'] > (at if at is not None else self.t0) + .2:
                self.counters.append(dict(row=rid, t=r['at']))
        html += '</div>'
        kw.setdefault('snd', 'pop')
        self.items.append(dict(k='box', id=pid, html=html, cx=cx, cy=cy, w=w, h=h, enter=kw.pop('enter', 'pop'),
                               at=self.t0 if at is None else at, until=until, rot=0, z=4, flash=False, snd=kw['snd'], cls='', drift=0, dim=kw.get('dim')))
    def bignum(self, fmt, to, cx, cy, at, frm=0, dur=1.2, size=150, color=GOLD, sub='', w=640, h=None, until=None, **kw):
        nid = self._id('n')
        html = (f'<div class="num" id="{nid}-v" style="font-size:{size}px;color:{color}">{fmt.replace("{n}", fmtn(frm))}</div>' +
                (f'<div class="sub" style="font-size:40px">{sub}</div>' if sub else ''))
        self.counters.append(dict(el=f'{nid}-v', frm=frm, to=to, fmt=fmt, t=at + .08, dur=dur))
        self.items.append(dict(k='box', id=nid, html=html, cx=cx, cy=cy, w=w, h=h or int(size * 1.5 + (60 if sub else 0)), enter=kw.get('enter', 'pop'), at=at, until=until,
                               rot=0, z=4, flash=False, snd=kw.get('snd', 'pop'), cls='', drift=0, dim=None))
    def conn(self, x1, y1, x2, y2, at, color=GREEN, dur=.55, bend=0.0, dot=True, until=None):
        pid = self._id('c')
        self.paths.append(dict(id=pid, pts=(x1, y1, x2, y2, bend), color=color, at=at, dur=dur, dot=dot, until=until))
        sfx(at, 'swipe', .16)
    def punch(self, t, kind='zoom'):
        self.punches.append((t, kind))
    def flash_at(self, cx, cy, at, size=260, color='rgba(255,255,255,.75)'):
        self.items.append(dict(k='flash', id=self._id('f'), cx=cx, cy=cy, w=size, h=size, at=at, color=color))

def fmtn(n):
    s = f'{int(round(n)):,}'.replace(',', '.')
    return s

# ------------------------------------------------------------------ STORYBOARD
STAGES = []
def stage(sid, b0, b1):
    s = Stage(sid, b0, b1); STAGES.append(s); return s

LX, RX = 238, 715            # colonne du personnage / colonne de droite
# ---- S1 : accroche -----------------------------------------------------------------
s = stage('s1', 1, 3)
s.img('mat_head', 540, 700, h=900, enter='none', at=0.0, until=0.46, drift=0.0, snd=False)
s.img('mat_op', 190, 760, h=430, enter='pop', at=.42, snd=False)
s.img('paolo_arms', 890, 760, h=430, enter='pop', at=.5, snd=False)
s.tag('elettricista', 190, 1050, 340, 'blue', at=T(1, 'Elettricista'))
s.tag('idraulico', 890, 1050, 300, 'gold', at=T(1, 'idraulico'))
s.box('<div class="num" style="font-size:230px;color:#ffd166">?</div>', 540, 700, 220, 260, at=T(1, 'guadagna'), until=T(2, 'Partiamo'))
s.tag('dipendenti', 540, 540, 340, 'blue', at=T(2, 'dipendenza'), until=T(3, 'Spesso'))
s.tag('stesso contratto', 540, 540, 460, 'gold', at=T(3, 'stesso'))
s.tag('impianti', 540, 670, 300, 'blue', at=T(3, 'impianti'))
s.punch(.44, 'zoom'); s.punch(T(1, 'guadagna'))
sfx(.02, 'camera-shutter', .5); sfx(.40, 'whoosh-deep', .4); sfx(.43, 'impact-bass-1', .42)

# ---- S2 : minimo lordo ---------------------------------------------------------------------------
s = stage('s2', 4, 7)
s.img('mat_op', 190, 760, h=430, enter='left', at=T(4))
s.img('paolo_arms', 890, 760, h=430, enter='right', at=T(4))
s.panel('operaio specializzato', [dict(label='LORDO', fmt='≈ {n} €', to=1650, frm=0, at=T(5, 'milleseicentocinquanta'), dur=1.1, color=GOLD)],
        540, 600, w=480, at=T(4, 'Operaio'), until=T(6, 'Lordi'))
s.img('soldi', 540, 880, h=200, enter='pop', at=T(5, 'euro'), until=T(6, 'Lordi'))
s.stamp('LORDO', 540, 620, 440, rot=-7, size=84, at=T(6, 'Lordi'), until=T(7, 'Stesso'))
s.tag('prima delle tasse', 540, 880, 500, 'red', at=T(6, 'prima'), until=T(7, 'Stesso'))
s.tag('stesso minimo', 540, 620, 420, 'green' if False else 'gold', at=T(7, 'minimo'))
s.badge('ok', 540, 800, T(7, 'minimo', .3), size=110)
s.punch(T(5, 'milleseicentocinquanta')); s.punch(T(6, 'Lordi'), 'shake'); sfx(T(5, 'milleseicentocinquanta', 1.0), 'cash-register', .3)

# ---- S3 : un caso reale ----------------------------------------------------------------------------
s = stage('s3', 8, 10)
s.img('mat_op', 190, 760, h=430, enter='none', at=T(8), snd=False)
s.img('paolo_arms', 890, 760, h=430, enter='none', at=T(8), snd=False)
s.tag('un caso reale', 540, 540, 420, 'blue', at=T(8, 'caso'))
s.bignum('+{n} €', 200, 540, 760, at=T(9, 'duecento'), dur=1.0, size=96, color=GREEN, sub='IDRAULICO', w=380)
s.tag('un solo esempio', 540, 1010, 460, 'red', at=T(10, 'esempio'))
s.badge('no', 540, 880, T(10, 'regola'), size=100)
s.punch(T(9, 'duecento')); s.punch(T(10, 'regola'))

# ---- S4 : rischio, tensione, acqua e gas --------------------------------------------------------------
s = stage('s4', 11, 13)
s.img('cartello', 540, 650, h=330, enter='pop', at=T(11, 'rischio'), until=T(12, 'elettricista'))
s.img('mat_spark', 200, 760, h=430, enter='left', at=T(12, 'elettricista'))
s.tag('tensione', 200, 1050, 300, 'red', at=T(12, 'tensione'))
s.img('paolo_splash', 850, 760, w=440, enter='right', at=T(13, 'idraulico'))
s.tag('acqua e gas', 840, 1050, 420, 'blue', at=T(13, 'acqua'))
s.punch(T(11, 'rischio'), 'shake'); s.punch(T(12, 'tensione')); s.punch(T(13, 'gas'))
sfx(T(12, 'tensione'), 'glass-ping', .3)

# ---- S5 : abilitazione, rischio in busta paga ------------------------------------------------------
s = stage('s5', 14, 15)
s.img('mat_hat', 190, 760, h=430, enter='left', at=T(14))
s.img('paolo_wrench', 890, 760, h=430, enter='right', at=T(14))
s.img('certificato', 540, 700, w=380, enter='pop', at=T(14, 'abilitazione'), until=T(15, 'Il'))
s.badge('ok', 540, 560, T(14, 'abilitazione', .3), size=100, until=T(15, 'Il'))
s.tag('abilitazione', 540, 950, 440, 'gold', at=T(14, 'abilitazione'), until=T(15, 'Il'))
s.stamp('RISCHIO', 540, 640, 360, rot=-7, size=64, at=T(15, 'rischio'))
s.tag('non in busta paga', 540, 900, 520, 'red', at=T(15, 'busta'))
s.punch(T(14, 'abilitazione')); s.punch(T(15, 'rischio'), 'shake')

# ---- S6 : la propria ditta, tariffa -------------------------------------------------------------------
s = stage('s6', 16, 18)
s.img('mat_owner', 190, 760, h=430, enter='left', at=T(16))
s.img('paolo_box', 890, 760, h=430, enter='right', at=T(16))
s.img('furgone', 540, 700, w=380, enter='pop', at=T(16, 'ditta'), until=T(17, 'Qui'))
s.tag('la tua ditta', 540, 950, 380, 'gold', at=T(16, 'ditta'), until=T(17, 'Qui'))
s.stamp('CONTRATTO', 540, 640, 460, rot=-6, size=64, at=T(17, 'contratto'), until=T(18, 'Conta'))
s.badge('no', 540, 860, T(17, 'conta'), size=110, until=T(18, 'Conta'))
s.tag('la tariffa', 540, 640, 340, 'gold', at=T(18, 'tariffa'))
s.img('soldi', 540, 880, h=220, enter='pop', at=T(18, 'chiedere'))
s.punch(T(17, 'contratto'), 'shake'); s.punch(T(18, 'tariffa'))

# ---- S7 : tariffa oraria, diritto di chiamata, urgenze ------------------------------------------------
s = stage('s7', 19, 21)
s.img('mat_owner', 190, 760, h=430, enter='none', at=T(19), snd=False)
s.img('paolo_phone', 890, 760, h=430, enter='none', at=T(19), snd=False)
s.panel("tariffa all'ora", [dict(label='DA', fmt='{n} €', to=25, frm=0, at=T(19, 'venticinque'), dur=.8, color=GOLD),
                            dict(label='A', fmt='{n} €', to=60, frm=0, at=T(19, 'sessanta'), dur=.8, color=GREEN)],
        540, 600, w=480, at=T(19, 'media'), until=T(20, 'Il'))
s.panel('diritto di chiamata', [dict(label='DA', fmt='{n} €', to=30, frm=0, at=T(20, 'trenta'), dur=.8, color=GOLD),
                                dict(label='A', fmt='{n} €', to=80, frm=0, at=T(20, 'ottanta'), dur=.8, color=GREEN)],
        540, 600, w=480, at=T(20, 'chiamata'), until=T(21, 'Per'))
s.bignum('×{n}', 2, 540, 620, at=T(21, 'doppio'), frm=1, dur=.7, size=210, color=RED, sub='URGENZE', w=480)
s.tag('stime', 540, 1000, 240, 'gold', at=T(21, 'doppio', .3))
s.punch(T(19, 'sessanta')); s.punch(T(20, 'ottanta')); s.punch(T(21, 'doppio'), 'shake'); sfx(T(20, 'ottanta', .9), 'cash-register', .3)

# ---- S8 : stime, città, clienti, stagione -------------------------------------------------------------------
s = stage('s8', 22, 23)
s.img('mat_owner', 190, 760, h=430, enter='left', at=T(22))
s.img('paolo_box', 890, 760, h=430, enter='right', at=T(22))
s.stamp('STIME', 540, 600, 400, rot=-6, size=84, color=GOLD, at=T(22, 'stime'), until=T(23, 'Dipendono'))
s.tag('città', 540, 540, 240, 'blue', at=T(23, 'città'))
s.tag('clienti', 540, 670, 260, 'gold', at=T(23, 'clienti'))
s.tag('stagione', 540, 800, 300, 'red', at=T(23, 'stagione'))
s.punch(T(22, 'stime'), 'shake')

# ---- S9 : costi, giornate senza chiamate, costo nascosto -----------------------------------------------------
s = stage('s9', 24, 26)
s.img('furgone', 190, 700, w=320, enter='left', at=T(24, 'furgone'), until=T(25, 'E'))
s.img('cacciaviti', 500, 700, h=230, enter='drop', at=T(24, 'attrezzi'), until=T(25, 'E'))
s.img('assicurazione', 890, 700, h=240, enter='right', at=T(24, 'assicurazione'), until=T(25, 'E'))
s.tag('furgone', 190, 900, 260, 'red', at=T(24, 'furgone', .1), until=T(25, 'E'))
s.tag('attrezzi', 480, 900, 260, 'red', at=T(24, 'attrezzi', .1), until=T(25, 'E'))
s.tag('assicurazione', 890, 900, 340, 'red', at=T(24, 'assicurazione', .1), until=T(25, 'E'))
s.img('paolo_boiler', 540, 780, w=620, enter='pop', at=T(25, 'giornate'))
s.tag('nessuna chiamata', 540, 520, 480, 'red', at=T(25, 'chiamata'), until=T(26, 'Il'))
s.tag('costo nascosto', 540, 520, 480, 'red', at=T(26, 'costo'))
s.stamp('NESSUNA GARANZIA', 540, 1130, 640, rot=-5, size=48, at=T(26, 'garantisce'))
s.punch(T(25, 'giornate')); s.punch(T(26, 'costo')); sfx(T(26, 'costo'), 'heartbeat', .3)

# ---- S10 : la domanda giusta --------------------------------------------------------------------------------
s = stage('s10', 27, 28)
s.img('mat_owner', 190, 760, h=430, enter='left', at=T(27))
s.img('paolo_box', 890, 760, h=430, enter='right', at=T(27))
s.tag('non è il mestiere', 540, 540, 500, 'red', at=T(27, 'mestiere'), until=T(28, 'quanti'))
s.badge('no', 540, 700, T(27, 'mestiere', .3), size=110, until=T(28, 'quanti'))
s.tag('quanti clienti?', 540, 540, 460, 'gold', at=T(28, 'clienti'))
s.img('paolo_phone', 540, 800, h=380, enter='pop', at=T(28, 'quanti'))
s.punch(T(27, 'mestiere')); s.punch(T(28, 'clienti'))

# ---- S11 : dipendente vs titolare ---------------------------------------------------------------------------------
s = stage('s11', 29, 30)
s.img('mat_op', 190, 760, h=430, enter='left', at=T(29))
s.img('paolo_arms', 890, 760, h=430, enter='right', at=T(29))
s.tag('dipendente', 540, 540, 340, 'blue', at=T(29, 'dipendente'), until=T(30, 'Da'))
s.box('<div class="num" style="font-size:210px;color:#ffd166">≈</div>', 540, 740, 240, 260, at=T(29, 'uguale'), until=T(30, 'Da'))
s.tag('quasi uguale', 540, 960, 380, 'gold', at=T(29, 'uguale'), until=T(30, 'Da'))
s.tag('titolare', 540, 540, 300, 'gold', at=T(30, 'titolare'))
s.box('<div class="arrow" style="font-size:200px">▲</div>', 540, 750, 240, 240, at=T(30, 'meglio'), snd='ping')
s.tag('chi lavora meglio', 540, 960, 480, 'green' if False else 'blue', at=T(30, 'meglio'))
s.punch(T(29, 'uguale')); s.punch(T(30, 'meglio'))

# ---- S12 : poche fonti, due preventivi -------------------------------------------------------------------------------
s = stage('s12', 31, 32)
s.stamp('POCHE FONTI', 540, 620, 520, rot=-6, size=72, at=T(31, 'fonti'), until=T(32, 'Chiedi'))
s.tag('prudenza', 540, 880, 320, 'red', at=T(31, 'prudente'), until=T(32, 'Chiedi'))
s.img('preventivi', 540, 700, w=420, enter='pop', at=T(32, 'preventivi'))
s.tag('due preventivi scritti', 540, 1010, 560, 'gold', at=T(32, 'preventivi'))
s.badge('ok', 540, 540, T(32, 'scritti'), size=100)
s.punch(T(31, 'fonti'), 'shake'); s.punch(T(32, 'preventivi'))

# ---- S13 : iscriviti -----------------------------------------------------------------------------------------------------
s = stage('s13', 33, 33)
s.img('paolo_head', 540, 700, h=900, enter='pop', at=T(33), drift=0.0)
s.box('<div style="position:relative;width:100%;height:100%"><img src="assets/img/campanella.png" style="width:100%;display:block;filter:drop-shadow(0 14px 22px rgba(0,0,0,.5))"><div class="cta" style="position:absolute;left:50%;top:33%;width:46%;font-size:34px">ISCRIVITI</div></div>',
      800, 1030, 460, 282, enter='pop', at=T(33, 'Iscriviti'), z=9, snd=None)
sfx(T(33, 'Iscriviti'), 'notification', .4)
s.punch(T(33), 'zoom')

# ------------------------------------------------------------------ sous-titres
def captions(bt):
    toks = bt.text.split(' ')
    marks = CAPMARK[bt.n]
    assert len(marks) == len(bt.words)
    out = [(w, m, t0) for (w, t0, t1), m in zip(bt.words, marks)]
    chunks, cur = [], []
    def flush():
        if cur: chunks.append(list(cur)); cur.clear()
    for word, em, t0 in out:
        cur_len = len(' '.join(x[0] for x in cur))
        if cur and cur_len + 1 + len(word) > 24: flush()
        cur.append((word, em, t0))
        if re.search(r'[.,?!]$', word) and len(' '.join(x[0] for x in cur)) >= 9: flush()
    flush()
    merged = []
    for c in chunks:
        if merged and len(c) == 1 and len(c[0][0]) <= 4 and len(' '.join(x[0] for x in merged[-1] + c)) <= 24:
            merged[-1] += c
        else:
            merged.append(c)
    res = []
    for i, c in enumerate(merged):
        ts = c[0][2] if i else bt.s
        te = merged[i + 1][0][2] if i + 1 < len(merged) else bt.e
        res.append((max(ts - 0.04, bt.s) if i else bt.s, te, c))
    return res

CAPEMPH = {1: 'guadagna', 2: 'dipendenza', 3: 'stesso contratto', 4: 'Operaio', 5: 'milleseicentocinquanta lordi', 6: 'Lordi tasse', 7: 'stesso minimo',
 8: 'reale lidraulico', 9: 'duecento', 10: 'solo esempio regola', 11: 'rischio cambia', 12: 'tensione', 13: 'acqua gas', 14: 'labilitazione',
 15: 'rischio busta', 16: 'ditta', 17: 'contratto', 18: 'tariffa', 19: 'venticinque sessanta', 20: 'trenta ottanta', 21: 'doppio', 22: 'stime',
 23: 'città clienti stagione', 24: 'furgone attrezzi assicurazione', 25: 'chiamata', 26: 'costo nascosto lavoro', 27: 'mestiere', 28: 'clienti',
 29: 'dipendente uguale', 30: 'titolare meglio', 31: 'poche prudente', 32: 'preventivi', 33: 'Iscriviti'}
CAPMARK = {}
for n, c in CAPEMPH.items():
    ks = {norm(x) for x in c.split()}
    CAPMARK[n] = [norm(w) in ks for w in BEATS[n - 1].text.split(' ')]
    assert len(CAPMARK[n]) == len(BEATS[n - 1].words), n

# ------------------------------------------------------------------ CSS
CSS = """
  #root { position:absolute; inset:0; font-family:'Montserrat',sans-serif; color:#fff; }
  .stage { position:absolute; inset:0; transform-origin:50% 45%; }
  .item { position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .item img.pic { width:100%; height:100%; object-fit:contain; display:block; filter:url(#boil-STAGE) drop-shadow(0 16px 24px rgba(0,0,0,.45)); }
  .bx { position:absolute; left:0; top:0; transform-origin:0 0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .bx:has(> .gtag) { flex-direction:row; }
  .item img.pic.fade { -webkit-mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); }
  .halo { width:100%; height:100%; border-radius:50%; }
  .num { font-weight:900; line-height:1; letter-spacing:-.02em; text-align:center; white-space:nowrap; text-shadow:0 0 40px rgba(255,255,255,.18); }
  .sub { font-weight:800; letter-spacing:.08em; text-align:center; color:#cdd3ff; margin-top:6px; }
  .stamp { font-family:'Playfair Display',serif; border:7px solid; border-radius:14px; padding:6px 22px; font-weight:900; letter-spacing:.07em; text-align:center; background:rgba(11,11,46,.5); white-space:nowrap; box-shadow:0 0 30px rgba(255,77,109,.25); }
  .gtag { display:inline-flex; align-items:center; gap:12px; padding:13px 30px; border-radius:999px; font-weight:800; font-size:36px; white-space:nowrap;
          background:rgba(40,44,120,.66); border:3px solid rgba(150,160,255,.55); box-shadow:0 0 36px rgba(111,123,255,.35); color:#fff; }
  .gtag.red { background:rgba(90,22,52,.7); border-color:rgba(255,77,109,.7); box-shadow:0 0 36px rgba(255,77,109,.35); }
  .gtag.gold { background:rgba(84,60,10,.7); border-color:rgba(255,209,102,.75); box-shadow:0 0 36px rgba(255,209,102,.3); }
  .gtag.small { font-size:28px; padding:8px 22px; align-self:flex-start; margin-bottom:4px; }
  .gtag .dot { width:14px; height:14px; border-radius:50%; background:#ff4d6d; box-shadow:0 0 12px #ff4d6d; flex:none; }
  .glass { width:100%; height:100%; border-radius:36px; padding:22px 26px; background:linear-gradient(180deg,rgba(60,64,160,.55),rgba(24,26,92,.66));
           border:3px solid rgba(150,160,255,.45); box-shadow:0 26px 52px rgba(0,0,0,.45), inset 0 0 44px rgba(120,130,255,.14); display:flex; flex-direction:column; }
  .glass .row { display:flex; justify-content:space-between; align-items:center; padding:10px 20px; margin-top:8px; border-radius:20px; background:rgba(14,16,70,.58); border:2px solid rgba(150,160,255,.18); height:92px; }
  .glass .rl { font-weight:800; font-size:28px; letter-spacing:.1em; color:#b8bdf0; }
  .glass .rv { font-weight:900; font-size:46px; white-space:nowrap; }
  .glass .rv.strike { text-decoration:line-through; text-decoration-thickness:5px; }
  .tiles { display:flex; justify-content:center; width:100%; }
  .tile { border-radius:20px; background:linear-gradient(180deg,#ffe28a,#f2b83c); display:flex; align-items:center; justify-content:center; box-shadow:0 8px 20px rgba(0,0,0,.4); }
  .tile b { font-weight:900; color:#2a2308; }
  .badge { width:100%; height:100%; border-radius:50%; display:flex; align-items:center; justify-content:center; border:4px solid rgba(255,255,255,.85); }
  .badge span { font-weight:900; font-size:52px; color:#fff; line-height:1; }
  .flash { width:100%; height:100%; border-radius:50%; border:6px solid; box-sizing:border-box; }
  .arrow { font-weight:900; font-size:96px; color:#3ddc97; text-shadow:0 0 30px rgba(61,220,151,.6); line-height:1; }
  .ring { position:relative; width:100%; height:100%; }
  .ring svg { width:100%; height:100%; }
  .ring-bg { fill:none; stroke:#2a2f7a; stroke-width:16; }
  .ring-fg { fill:none; stroke:#ffd166; stroke-width:16; stroke-linecap:round; stroke-dasharray:540.4; stroke-dashoffset:540.4; filter:drop-shadow(0 0 8px rgba(255,209,102,.7)); }
  .ringtxt { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .spark { color:#ffd166; text-shadow:0 0 36px rgba(255,209,102,.85); line-height:1; }
  .paper { width:100%; height:100%; background:#f4ecd8; border-radius:20px; padding:36px 42px; box-shadow:0 22px 46px rgba(0,0,0,.5); color:#3b3328; }
  .paper .ph { font-weight:900; font-size:42px; letter-spacing:.12em; margin-bottom:26px; color:#5a4a33; }
  .paper .pl { height:18px; border-radius:99px; background:#d8cdb2; margin:22px 0; width:100%; }
  .paper .pl.s { width:68%; }
  .paper .hl { border:7px solid rgba(255,77,109,0); display:flex; justify-content:space-between; align-items:center; margin:28px 0; padding:16px 22px; border-radius:18px; font-weight:800; font-size:32px; }
  .paper .hl b { font-size:50px; color:#ff4d6d; white-space:nowrap; }
  .bar { width:100%; height:100%; background:#2a2f7a; border-radius:99px; overflow:hidden; border:5px solid #6f7bff; }
  .barfill { width:100%; height:100%; background:linear-gradient(90deg,#ffd166,#ff8a4d); transform-origin:left center; }
  .phone { width:100%; height:100%; background:#1b1d4a; border:12px solid #9aa0c8; border-radius:50px; overflow:hidden; display:flex; align-items:flex-end; justify-content:center; box-shadow:0 0 54px rgba(100,160,255,.45); }
  .phone .kid { width:132%; max-width:none; margin-bottom:-4%; }
  .opt { width:100%; height:100%; border-radius:30px; background:rgba(42,47,122,.8); border:5px solid #6f7bff; display:flex; flex-direction:row; align-items:center; justify-content:space-between; padding:0 30px; gap:10px; box-shadow:0 0 30px rgba(111,123,255,.3); }
  .opt.gold { background:rgba(90,64,12,.74); border-color:#ffd166; box-shadow:0 0 30px rgba(255,209,102,.3); }
  .opt .otitle { font-weight:900; font-size:40px; letter-spacing:.06em; }
  .opt img { height:150px; }
  .or { font-weight:900; font-size:44px; letter-spacing:.2em; color:#cdd3ff; text-align:center; background:rgba(60,60,170,.5); border-radius:999px; padding:6px 24px; border:2px solid rgba(150,160,255,.4); }
  .chart { width:100%; height:100%; display:flex; align-items:flex-end; justify-content:space-around; gap:50px; }
  .chart .col { flex:1; height:100%; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; }
  .chart .b { width:76%; border-radius:22px 22px 0 0; transform-origin:bottom center; }
  .chart .gr { height:100%; background:linear-gradient(180deg,#5af0b0,#1fa974); box-shadow:0 0 40px rgba(61,220,151,.3); }
  .chart .rd { height:22%; background:linear-gradient(180deg,#ff7a93,#d62d52); }
  .chart .lbl { margin-top:18px; font-weight:900; font-size:40px; letter-spacing:.08em; }
  .meter { width:100%; height:100%; border-radius:34px; padding:22px 30px; background:linear-gradient(180deg,rgba(60,64,160,.55),rgba(24,26,92,.66)); border:3px solid rgba(150,160,255,.45); }
  .meter .mlab { font-weight:800; font-size:28px; letter-spacing:.12em; color:#b8bdf0; margin-bottom:14px; }
  .meter .mtrack { height:46px; border-radius:99px; background:#171a63; border:3px solid #6f7bff; overflow:hidden; }
  .meter .mfill { width:100%; height:100%; background:linear-gradient(90deg,#3ddc97,#b5f06a); transform-origin:left center; }
  .roadbox { overflow:hidden; }
  .road { position:absolute; left:0; right:0; top:30px; bottom:30px; background:#14163f; border-top:6px solid #3a3f95; border-bottom:6px solid #3a3f95; }
  .dash { position:absolute; left:-30%; right:-30%; top:50%; height:10px; background:repeating-linear-gradient(90deg,#ffd166 0 70px,transparent 70px 140px); }
  .cta { font-weight:900; font-size:50px; letter-spacing:.06em; color:#fff; text-shadow:0 4px 10px rgba(120,40,0,.6); text-align:center; white-space:nowrap; }
  svg.conn { position:absolute; inset:0; width:1080px; height:1920px; z-index:2; overflow:visible; }
  svg.conn path { fill:none; stroke-width:7; stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; }
  .hg { position:absolute; top:322px; width:300px; }
  .hlab { font-weight:800; font-size:28px; letter-spacing:.08em; color:#b8bdf0; margin-bottom:8px; white-space:nowrap; }
  .htr { height:18px; border-radius:99px; background:rgba(23,26,99,.8); border:2px solid rgba(111,123,255,.55); overflow:hidden; }
  .hfill { width:100%; height:100%; border-radius:99px; transform-origin:left center; }
  .cap { position:absolute; left:0; width:1080px; text-align:center; font-weight:800; font-size:58px; line-height:1.15; text-transform:uppercase; white-space:nowrap; text-shadow:0 5px 16px rgba(0,0,0,.7); z-index:30; }
  .cap b.k { font-weight:900; display:inline-block; }
  .rl-line { position:absolute; left:90px; top:236px; width:900px; height:6px; border-radius:3px; background:rgba(150,160,255,.35); }
  .rl-fill { position:absolute; left:90px; top:236px; height:6px; border-radius:3px; background:linear-gradient(90deg,#6f7bff,#ff4d6d); width:0; box-shadow:0 0 14px rgba(255,77,109,.6); }
  .rl-tick { position:absolute; top:226px; width:4px; height:26px; border-radius:2px; background:rgba(180,188,255,.55); }
  .rl-num { position:absolute; top:262px; width:80px; margin-left:-40px; text-align:center; font-weight:800; font-size:28px; color:#aab0ee; }
  .rl-dot { position:absolute; top:217px; width:44px; height:44px; margin-left:-22px; border-radius:50%; background:#ff4d6d; border:4px solid #fff; box-shadow:0 0 28px #ff4d6d; }
  .rl-lab { position:absolute; top:148px; width:300px; margin-left:-150px; text-align:center; }
"""

def build_stage(S, prev_end_overlap=True):
    dur = round(min(S.t1 - S.t0 + OVER, TOTAL - S.t0), 3)
    ex_end = round(S.t1 - S.t0, 3)       # fin « logique » du décor, relative
    html, js = [], []
    sid = S.id
    html.append(f'<svg width="0" height="0" style="position:absolute"><filter id="boil-{sid}" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence id="boilt-{sid}" type="fractalNoise" baseFrequency="0.018 0.022" numOctaves="2" seed="1" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.4"/></filter></svg>')
    html.append(f'<div class="stage clip" id="{sid}-stage" data-start="0" data-duration="{dur}" data-track-index="1"><div class="stage" id="{sid}-pun"><div class="stage" id="{sid}-cam">')
    js.append(f'(function(){{var o={{v:0}},t=document.getElementById("boilt-{sid}");tl.to(o,{{v:{int(dur * 8)},duration:{dur},ease:"steps({int(dur * 8)})",onUpdate:function(){{t.setAttribute("seed",String(1+Math.floor(o.v)%23));}}}},0);}})();')
    for (pt, kind) in S.punches:
        pr = round(pt - S.t0, 3)
        if kind == 'zoom':
            js.append(f'tl.to("#{sid}-pun",{{scale:1.1,duration:.08,ease:"power3.out"}},{pr:.3f});')
            js.append(f'tl.to("#{sid}-pun",{{scale:1,duration:.45,ease:"expo.out"}},{pr + .08:.3f});')
        else:
            js.append(f'tl.to("#{sid}-pun",{{x:16,y:-10,rotation:.8,duration:.04,ease:"none"}},{pr:.3f});')
            for k_, (xx, yy, rr) in enumerate([(-14, 12, -.7), (12, -8, .5), (-9, 7, -.4), (6, -4, .2), (0, 0, 0)]):
                js.append(f'tl.to("#{sid}-pun",{{x:{xx},y:{yy},rotation:{rr},duration:.045,ease:"none"}},{pr + .04 + k_ * .045:.3f});')
    js.append(f'tl.fromTo("#{sid}-cam",{{scale:1,y:0}},{{scale:1.06,y:-24,duration:{dur},ease:"none"}},0);')
    # connecteurs
    if S.paths:
        html.append(f'<svg class="conn clip" id="{sid}-svg" data-start="0" data-duration="{dur}" data-track-index="2" viewBox="0 0 1080 1920">')
        for p in S.paths:
            rel = round(p['at'] - S.t0, 3)
            gl = f'filter:drop-shadow(0 0 7px {p["color"]})'
            X1, Y1, X2, Y2, BD = p['pts']
            X1, X2 = 540 + (X1 - 540) * 1.1, 540 + (X2 - 540) * 1.1
            Y1, Y2 = 790 + (Y1 - 700) * 1.2, 790 + (Y2 - 700) * 1.2
            DX = X2 - X1
            p['end'] = (X2, Y2)
            d_ = f'M{X1:.0f} {Y1:.0f} C{X1 + DX * .5:.0f} {Y1 + BD:.0f} {X1 + DX * .5:.0f} {Y2 - BD:.0f} {X2:.0f} {Y2:.0f}'
            html.append(f'<path id="{p["id"]}" d="{d_}" pathLength="1" stroke="{p["color"]}" style="{gl}"/>')
            if p['dot'] and p.get('end'):
                html.append(f'<circle id="{p["id"]}-d" cx="{X2:.0f}" cy="{Y2:.0f}" r="12" fill="{p["color"]}" opacity="0" style="{gl}"/>')
                js.append(f'tl.fromTo("#{p["id"]}-d",{{opacity:0,scale:.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.25,ease:"back.out(2)"}},{rel + p["dur"] - .05:.3f});')
            js.append(f'tl.fromTo("#{p["id"]}",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{p["dur"]},ease:"power2.inOut"}},{rel:.3f});')
            if p.get('until'):
                ur = round(p['until'] - S.t0 - .3, 3)
                js.append(f'tl.to("#{p["id"]}",{{opacity:0,duration:.28,ease:"power2.in"}},{ur:.3f});')
                if p['dot'] and p.get('end'):
                    js.append(f'tl.to("#{p["id"]}-d",{{opacity:0,duration:.28,ease:"power2.in"}},{ur:.3f});')
        html.append('</svg>')
    for it in S.items:
        rel = round(it['at'] - S.t0, 3)
        iid = it['id']
        if it['k'] == 'flash':
            html.append(f'<div class="item clip" id="{iid}" data-start="{rel}" data-duration="0.7" data-track-index="3" style="left:{it["cx"]-it["w"]/2:.0f}px;top:{it["cy"]-it["h"]/2:.0f}px;width:{it["w"]}px;height:{it["h"]}px;z-index:9"><div class="flash" style="border-color:{it["color"]}"></div></div>')
            js.append(f'tl.fromTo("#{iid}",{{opacity:.9,scale:.35}},{{opacity:0,scale:1.7,duration:.6,ease:"expo.out"}},{rel:.3f});')
            continue
        end_abs = it['until'] if it['until'] is not None else S.t1 + OVER
        end_rel = round(min(end_abs - S.t0, dur), 3)
        d = round(max(end_rel - rel, .3), 3)
        MAPX = lambda x: 540 + (x - 540) * 1.1
        MAPY = lambda y: 790 + (y - 700) * 1.2
        if it['k'] == 'img':
            iw, ih = SIZE[it['name']]
            if it['h']: hh = it['h'] * K_IMG; ww = hh * iw / ih
            else: ww = it['w'] * K_IMG; hh = ww * ih / iw
            fade = ' fade' if it['name'].endswith('_head') else ''
            inner = f'<img class="pic{fade}" id="{iid}-p" src="assets/img/{it["name"]}.png" alt="">'
        else:
            bw0, bh0 = it['w'], it['h']
            ww, hh = bw0 * K_BOX, bh0 * K_BOX
            inner = f'<div class="bx" style="width:{bw0}px;height:{bh0}px;transform:scale({K_BOX})">{it["html"]}</div>'
        if hh > ZB - S.zt:
            f_ = (ZB - S.zt) / hh; ww, hh = ww * f_, hh * f_
        cx2, cy2 = MAPX(it['cx']), MAPY(it['cy'])
        cy2 = min(max(cy2, S.zt + hh / 2), ZB - hh / 2)
        left = min(max(cx2 - ww / 2, 62), W - 62 - ww)
        top = cy2 - hh / 2
        it['_cx'], it['_cy'] = left + ww / 2, cy2
        html.append(f'<div class="item clip {it.get("cls","")}" id="{iid}" data-start="{rel}" data-duration="{d}" data-track-index="4" '
                    f'style="left:{left:.0f}px;top:{top:.0f}px;width:{ww:.0f}px;height:{hh:.0f}px;z-index:{it["z"]}">{inner}</div>')
        e, r = it['enter'], it['rot']
        fr = {'pop': 'opacity:0,scale:.55,y:34', 'left': 'opacity:0,x:-340', 'right': 'opacity:0,x:340', 'drop': 'opacity:0,y:-260',
              'up': 'opacity:0,y:280', 'shake': 'opacity:0,scale:.5,y:60', 'none': 'opacity:1'}[e]
        if e == 'none':
            js.append(f'tl.set("#{iid}",{{rotation:{r}}},{rel:.3f});')
        else:
            ease = 'back.out(1.5)' if e in ('pop', 'shake', 'drop') else 'expo.out'
            js.append(f'tl.fromTo("#{iid}",{{{fr},rotation:{r}}},{{opacity:1,scale:1,x:0,y:0,rotation:{r},duration:.5,ease:"{ease}"}},{rel:.3f});')
        if e == 'shake':
            js.append(f'tl.to("#{iid}",{{rotation:{r + 5},duration:.07,yoyo:true,repeat:3,ease:"sine.inOut"}},{rel + .5:.3f});')
        # sortie anticipée : le décor « recule » ; sortie de fin gérée par le décor entier
        if it['until'] is not None:
            js.append(f'tl.to("#{iid}",{{opacity:0,scale:.88,filter:"blur(10px)",duration:.28,ease:"power2.in"}},{end_rel - .3:.3f});')
        if it['k'] == 'img' and it['drift']:
            js.append(f'tl.fromTo("#{iid}-p",{{scale:1}},{{scale:{1 + it["drift"]},duration:{d},ease:"none"}},{rel:.3f});')
        if it['k'] in ('img', 'box') and e != 'none' or it['k'] == 'img':
            # flottement doux et continu (personnages : respiration ; objets : lévitation)
            ch = it['k'] == 'img' and (it['name'].startswith('paolo') or it['name'].startswith('mat'))
            per = 2.4 if ch else 3.0 + (__import__("zlib").crc32(iid.encode()) % 7) * .2
            amp = 10 if ch else 16
            rot = 1.4 if ch else 3.0
            tgt = f'#{iid}-p' if it['k'] == 'img' else f'#{iid}'
            nrep = int(d / per) + 1
            if it['k'] == 'img':
                js.append(f'tl.fromTo("{tgt}",{{y:0,rotation:{-rot / 2}}},{{y:{-amp},rotation:{rot / 2},duration:{per:.2f},ease:"sine.inOut",yoyo:true,repeat:{nrep}}},{rel + .45:.3f});')
        # sons et éclats
        snd = it['snd']
        if snd == 'impact': impact_sfx(it['at'])
        elif snd == 'pop': pop_sfx(it['at'])
        elif isinstance(snd, str): sfx(it['at'], snd, .38 if snd in ('notification', 'ping') else .3)
        elif snd is True and it['k'] == 'img' and e in ('left', 'right') and not (it['name'].startswith('paolo') or it['name'].startswith('mat')): sfx(it['at'], 'whoosh-short', .24)
        if it.get('flash') and e != 'none':
            S.items_flash = getattr(S, 'items_flash', []) + [(it['_cx'], it['_cy'], it['at'] + .12, min((it['w'] or 200) * K_BOX, 320) if it['k'] == 'box' else 290)]
        if it['k'] == 'tiles':
            for i in range(it['count']):
                tt = rel + .05 + i * .11
                js.append(f'tl.fromTo("#{it["tid"]}-{i}",{{opacity:0,scale:.2,y:30}},{{opacity:1,scale:1,y:0,duration:.3,ease:"back.out(2)"}},{tt:.3f});')
                sfx(S.t0 + tt, 'click-soft', .24)
    # éclats (ronds) ajoutés après coup
    for (cx, cy, at, sz) in getattr(S, 'items_flash', []):
        rel = round(at - S.t0, 3); fid = f'{sid}-fl{int(at * 100)}'
        html.append(f'<div class="item clip" id="{fid}" data-start="{rel}" data-duration="0.7" data-track-index="3" style="left:{cx-sz/2:.0f}px;top:{cy-sz/2:.0f}px;width:{sz}px;height:{sz}px;z-index:9"><div class="flash" style="border-color:rgba(255,255,255,.7)"></div></div>')
        js.append(f'tl.fromTo("#{fid}",{{opacity:.8,scale:.4}},{{opacity:0,scale:1.6,duration:.55,ease:"expo.out"}},{rel:.3f});')
    # compteurs / apparition de lignes
    for c in S.counters:
        if 'row' in c:
            rel = round(c['t'] - S.t0, 3)
            js.append(f'tl.fromTo("#{c["row"]}",{{opacity:.0,x:40}},{{opacity:1,x:0,duration:.35,ease:"expo.out"}},{rel:.3f});')
            continue
        rel = round(c['t'] - S.t0, 3)
        fmt = c['fmt'].replace("'", "\\'")
        js.append(f'(function(){{var o={{v:{c["frm"]}}},el=document.getElementById("{c["el"]}");'
                  f'tl.fromTo(o,{{v:{c["frm"]}}},{{v:{c["to"]},duration:{c["dur"]},ease:"power2.out",onUpdate:function(){{'
                  f'var n=Math.round(o.v),s=String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,".");el.textContent=\'{fmt}\'.replace("{{n}}",s);}}}},{rel:.3f});}})();')
        count_sfx(c['t'], c['dur'])
    # le décor entier recule à la fin
    last = ex_end - 0.02
    if sid != STAGES[-1].id:
        js.append(f'tl.to("#{sid}-stage",{{opacity:0,scale:.9,filter:"blur(14px)",duration:{OVER + .02},ease:"power2.in"}},{last - .02:.3f});')
        sfx(S.t1 - .12, 'sweep', .27)
    else:
        js.append(f'tl.to("#{sid}-stage",{{opacity:0,duration:.3,ease:"power1.in"}},{dur - .4:.3f});')
    html.append('</div></div></div>')
    if sid == 's9':
        pass
    comp = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}">
    {chr(10).join('    ' + h for h in html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in js)}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    comp = comp.replace('boil-STAGE', f'boil-{sid}')
    open(os.path.join(OUT, 'compositions', f'{sid}.html'), 'w', encoding='utf-8').write(comp)

for S in STAGES:
    build_stage(S)

# tableau de bord (jauges qualitatives : tendances du récit, pas des données chiffrées) -----------------
hud_t0, hud_t1 = T(2, 'Partiamo', -.1), STAGES[-2].t0
GA = [('sic', 'SICUREZZA', 'linear-gradient(90deg,#3ddc97,#b5f06a)'), ('risc', 'RISCHIO', 'linear-gradient(90deg,#ff6b6b,#ff3d7f)'), ('inc', 'INCERTEZZA', 'linear-gradient(90deg,#b47bff,#ff6bd5)')]
EV = {'sic': [(hud_t0, .85), (T(16, 'ditta'), .40), (T(25, 'giornate'), .18)],
      'risc': [(hud_t0, .10), (T(12, 'elettricista'), .55), (T(13, 'idraulico'), .70)],
      'inc': [(hud_t0, .05), (T(16, 'ditta'), .45), (T(25, 'giornate'), .90)]}
hud_js, hud_html = [], []
for k, (g, lab, grad) in enumerate(GA):
    x = 40 + k * 340
    hud_html.append(f'<div class="hg" style="left:{x}px"><div class="hlab">{lab}</div><div class="htr"><div class="hfill" id="hf-{g}" style="background:{grad}"></div></div></div>')
    first = True
    for (t, v) in EV[g]:
        if first:
            hud_js.append(f'tl.fromTo("#hf-{g}",{{scaleX:0}},{{scaleX:{v},duration:.7,ease:"power3.out"}},{t:.3f});'); first = False
        else:
            hud_js.append(f'tl.to("#hf-{g}",{{scaleX:{v},duration:.6,ease:"power2.inOut"}},{t:.3f});')
hud_js.append(f'tl.fromTo("#hud",{{opacity:0,y:-24}},{{opacity:1,y:0,duration:.4,ease:"expo.out"}},{hud_t0:.3f});')
hud_js.append(f'tl.to("#hud",{{opacity:0,duration:.4,ease:"power2.in"}},{hud_t1 - .1:.3f});')
hud = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="hud" data-width="{W}" data-height="{H}">
    <div id="hud" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="1" style="position:absolute;inset:0;z-index:24">{''.join(hud_html)}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in hud_js)}
    window.__timelines["hud"] = tl;
  </script>
</template>
"""
open(os.path.join(OUT, 'compositions', 'hud.html'), 'w', encoding='utf-8').write(hud)

# sous-titres (composition globale) ----------------------------------------------------------
chtml, cjs = [], []
for bt in BEATS:
    for k, (cs, ce, words) in enumerate(captions(bt)):
        cid = f'cap{bt.n}-{k}'
        spans = []
        for j, (w, em, t0) in enumerate(words):
            if em:
                wid = f'{cid}-w{j}'
                spans.append(f'<b class="k" id="{wid}">{w}</b>')
                cjs.append(f'tl.fromTo("#{wid}",{{color:"#ffffff"}},{{color:"{RED}",duration:.2,ease:"power2.out"}},{max(t0 - .02, cs):.3f});')
            else:
                spans.append(w)
        cd = round(ce - cs, 3)
        chtml.append(f'<div class="cap clip" id="{cid}" data-start="{cs:.3f}" data-duration="{cd}" data-track-index="1" style="top:{CAP_Y - 36}px">{" ".join(spans)}</div>')
        if not (bt.n == 1 and k == 0):
            cjs.append(f'tl.fromTo("#{cid}",{{opacity:0,y:14,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.16,ease:"power3.out"}},{cs:.3f});')
        cjs.append(f'tl.to("#{cid}",{{opacity:0,filter:"blur(5px)",duration:.08,ease:"none"}},{ce - .09:.3f});')
caps = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="caps" data-width="{W}" data-height="{H}">
    {chr(10).join('    ' + h for h in chtml)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in cjs)}
    window.__timelines["caps"] = tl;
  </script>
</template>
"""
open(os.path.join(OUT, 'compositions', 'caps.html'), 'w', encoding='utf-8').write(caps)

# ------------------------------------------------------------------ index
hosts = []
for k, S in enumerate(STAGES):
    dur = round(min(S.t1 - S.t0 + OVER, TOTAL - S.t0), 3)
    hosts.append(f'      <div id="{S.id}" class="clip" data-composition-id="{S.id}" data-composition-src="compositions/{S.id}.html" '
                 f'data-start="{S.t0:.3f}" data-duration="{dur}" data-track-index="{2 + k % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
hosts.append(f'      <div id="hud" class="clip" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{TOTAL}" data-track-index="7" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
hosts.append(f'      <div id="caps" class="clip" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{TOTAL}" data-track-index="6" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>')

SFXLOG.sort()
audio = []
for n, (t, f, v) in enumerate(SFXLOG):
    if t < 0 or t > TOTAL - .2: continue
    t = min(t, TOTAL - SFXDUR[f] - .02)
    src = f'assets/audio/{f}.wav' if (f == 'sweep' or f.startswith('countup-')) else (f'assets/sfx2/{f}.mp3' if f in SFX2 else f'assets/sfx/{f}.mp3')
    audio.append(f'      <audio id="sfx{n}" src="{src}" data-start="{t:.3f}" data-duration="{SFXDUR[f]}" data-track-index="{20 + n % 9}" data-volume="{v}"></audio>')

stars = ''.join(
    f'<i style="left:{(i * 137) % 100}%;top:{(i * 71) % 100}%;width:{2 + i % 3}px;height:{2 + i % 3}px;opacity:{.25 + (i % 5) / 10:.2f}"></i>'
    for i in range(110))
twink = ''.join(f'tl.fromTo("#stars i:nth-child({3 + 7 * j})",{{opacity:.15}},{{opacity:.95,duration:{1.3 + (j % 4) * .45:.2f},yoyo:true,repeat:{int(TOTAL // (1.3 + (j % 4) * .45)) | 1},ease:"sine.inOut"}},{(j * .37) % 2:.2f});\n      '
                for j in range(14))

pdots = ''.join(f'<i style="left:{(i * 83) % 100}%;top:{20 + (i * 47) % 70}%;width:{6 + i % 4 * 3}px;height:{6 + i % 4 * 3}px"></i>' for i in range(26))
parts = ''.join(f'tl.fromTo("#parts i:nth-child({k + 1})",{{y:60,opacity:0}},{{y:-{260 + (k % 5) * 70},opacity:{.35 + (k % 3) * .15:.2f},duration:{5 + (k % 6) * .9:.1f},ease:"sine.inOut",yoyo:true,repeat:{int(TOTAL // (5 + (k % 6) * .9)) + 1}}},{(k * .41) % 3:.2f});\n      ' for k in range(26))
index = f"""<!doctype html>
<html lang="it">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#080826; }}
      #bg {{ position:absolute; inset:0; background:linear-gradient(180deg,#0b0a33 0%,#12104d 50%,#08183f 100%); }}
      .blob {{ position:absolute; border-radius:50%; }}
      #b1 {{ left:-420px; top:-300px; width:1300px; height:1300px; background:radial-gradient(circle,rgba(130,70,210,.5),transparent 66%); }}
      #b2 {{ left:-200px; top:1020px; width:1500px; height:1100px; background:radial-gradient(circle,rgba(20,205,185,.5),transparent 66%); }}
      #b3 {{ left:520px; top:520px; width:1000px; height:1000px; background:radial-gradient(circle,rgba(60,90,230,.4),transparent 66%); }}
      #grid {{ position:absolute; inset:-90px; opacity:.55;
        background-image:linear-gradient(rgba(140,150,255,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(140,150,255,.08) 1px,transparent 1px);
        background-size:90px 90px; -webkit-mask-image:linear-gradient(180deg,transparent 4%,#000 38%,#000 76%,transparent 100%); mask-image:linear-gradient(180deg,transparent 4%,#000 38%,#000 76%,transparent 100%); }}
      #stars {{ position:absolute; inset:0; }}
      #stars i {{ position:absolute; border-radius:50%; background:#fff; }}
      #parts {{ position:absolute; inset:0; }}
      #parts i {{ position:absolute; border-radius:50%; background:radial-gradient(circle,rgba(190,200,255,.95),rgba(120,140,255,0) 70%); }}
      #tint {{ position:absolute; inset:0; background:rgba(50,100,255,0); }}
      #vig {{ position:absolute; inset:0; background:radial-gradient(ellipse 85% 70% at 50% 45%, transparent 55%, rgba(4,4,24,.55) 100%); }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" style="position:absolute;inset:0;font-family:Montserrat,sans-serif">
      <div id="bg"></div>
      <div id="b1" class="blob"></div><div id="b2" class="blob"></div><div id="b3" class="blob"></div>
      <div id="grid"></div>
      <div id="stars">{stars}</div>
      <div id="parts">{pdots}</div>
      <div id="vig"></div>
      <div id="tint"></div>
{chr(10).join(hosts)}
      <audio id="voce" src="assets/voce.wav" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
      <audio id="bed" src="assets/audio/bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="0.55"></audio>
      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1.15"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#b1", {{ x: -120, y: -60, scale: 1 }}, {{ x: 230, y: 190, scale: 1.18, duration: 5.2, ease: "sine.inOut", yoyo: true, repeat: 19 }}, 0);
      tl.fromTo("#b2", {{ x: 140, y: 70, scale: 1 }}, {{ x: -260, y: -150, scale: 1.16, duration: 6.4, ease: "sine.inOut", yoyo: true, repeat: 15 }}, 0);
      tl.fromTo("#b3", {{ x: 160, y: -120 }}, {{ x: -300, y: 230, duration: 7.3, ease: "sine.inOut", yoyo: true, repeat: 13 }}, 0);
      tl.fromTo("#grid", {{ y: 0 }}, {{ y: 90, duration: 4, ease: "none", repeat: 24 }}, 0);
      {parts}
      {twink}
      tl.to("#tint", {{ backgroundColor: "rgba(50,100,255,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(2, 'Partiamo', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(255,60,90,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(11, 'Poi', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(255,170,50,.11)", duration: 1.2, ease: "sine.inOut" }}, {T(16, 'Ora', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(150,90,230,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(22, 'Ma', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(20,200,170,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(29, 'Da', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(120,140,200,.1)", duration: 1.5, ease: "sine.inOut" }}, {STAGES[-2].t0 - .3:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)
open(os.path.join(OUT, 'hyperframes.json'), 'w').write('{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",\n  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},\n  "media": {"autoProxy": true}\n}\n')
open(os.path.join(OUT, 'meta.json'), 'w').write('{"id": "eli-v1", "name": "Elettricista vs idraulico (9:16)"}')
print('ok li:', len(STAGES), 'décors,', len(SFXLOG), 'effets,', len(audio), 'audio')
