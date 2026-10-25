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
OUT = os.path.join(ROOT, 'v3')
CUT = os.path.join(ROOT, 'assets', 'cut')
SFXSRC = os.path.join(ROOT, '..', '.claude', 'skills', 'media-use', 'audio', 'assets', 'sfx')
AUDSRC = os.path.join(ROOT, 'assets', 'audio')
VOICE = '/root/.claude/uploads/91729ddc-3274-50e3-9f11-8e52419e14ce/280557de-Generated_Audio_October_24_2026_-_5_04PM.wav'
SCRIPT = os.path.join(ROOT, '..', 'scripts', 'camionista-short.txt')
SRT = os.path.join(ROOT, '..', 'scripts', 'camionista-scenes.srt')
TOTAL = 98.7
W, H = 1080, 1920
CAP_Y = 1300
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
NUMW = set('ventitré tremila millecinquecento duemila quarantasei venticinque trenta quindici dieci cinque uno due nove novanta quarantacinque millequattrocento trentotto'.split())
norm = lambda t: re.sub(r"[^\w]", "", t.lower().replace("l'", "l"))
WW = json.load(open(os.path.join(HERE, 'words.json')))
swords = [w for l in open(SCRIPT, encoding='utf-8') if l.strip() for w in l.split()]
st = ['NUM' if norm(w) in NUMW else norm(w) for w in swords]
wt = ['NUM' if re.fullmatch(r'\d+[.,]?', w[0]) else norm(w[0]) for w in WW]
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
for d in ('assets/img', 'assets/sfx', 'assets/audio', 'compositions'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
SIZE = {}
for f in os.listdir(CUT):
    im = Image.open(os.path.join(CUT, f)); im.thumbnail((1100, 1100))
    im.save(os.path.join(OUT, 'assets', 'img', f), optimize=True); SIZE[f[:-4]] = im.size
shutil.copy(VOICE, os.path.join(OUT, 'assets', 'voce.wav'))
for f in ('bed.wav', 'sweep.wav'):
    shutil.copy(os.path.join(AUDSRC, f), os.path.join(OUT, 'assets', 'audio', f))
SFXDUR = {k: v['duration'] for k, v in json.load(open(os.path.join(SFXSRC, 'manifest.json'))).items()}
SFXDUR['sweep'] = 0.9
for f in os.listdir(SFXSRC):
    if f.endswith('.mp3') or f == 'CREDITS.md':
        shutil.copy(os.path.join(SFXSRC, f), os.path.join(OUT, 'assets', 'sfx', f))

# ------------------------------------------------------------------ DSL
SFXLOG = []     # (t_abs, name, volume)
_rot = {'pop': 0, 'impact': 0}
def sfx(t, name, vol=.33):
    SFXLOG.append((round(t, 3), name, vol))

def pop_sfx(t, vol=.3):
    seq = ['pop', 'ping', 'click-soft', 'pop']
    sfx(t, seq[_rot['pop'] % 4], vol); _rot['pop'] += 1

def impact_sfx(t):
    sfx(t, 'impact-bass-1' if _rot['impact'] % 2 == 0 else 'impact-bass-2', .45); _rot['impact'] += 1

class Stage:
    def __init__(self, sid, b0, b1, ruler=None):
        self.id, self.b0, self.b1 = sid, b0, b1
        self.t0 = BEATS[b0 - 1].s
        self.t1 = BEATS[b1 - 1].e
        self.items, self.paths, self.counters = [], [], []
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
        dx, dy = x2 - x1, y2 - y1
        c1 = (x1 + dx * .5, y1 + bend); c2 = (x1 + dx * .5, y2 - bend)
        self.paths.append(dict(id=pid, d=f'M{x1} {y1} C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {x2} {y2}', color=color, at=at, dur=dur, end=(x2, y2), dot=dot, until=until))
    def flash_at(self, cx, cy, at, size=260, color='rgba(255,255,255,.75)'):
        self.items.append(dict(k='flash', id=self._id('f'), cx=cx, cy=cy, w=size, h=size, at=at, color=color))

def fmtn(n):
    s = f'{int(round(n)):,}'.replace(',', '.')
    return s

# ------------------------------------------------------------------ STORYBOARD
STAGES = []
def stage(sid, b0, b1):
    s = Stage(sid, b0, b1); STAGES.append(s); return s

LX, RX = 205, 730            # colonne du personnage / colonne de droite
# ---- S1 : accroche (0 – 5,28) -----------------------------------------------------
s = stage('s1', 1, 2)
s.box('<div class="halo" style="background:radial-gradient(circle,rgba(120,90,255,.5) 0%,transparent 68%)"></div>', LX, 700, 620, 620, enter='none', z=1, snd=None)
s.img('marco23_full', LX, 700, h=560, enter='none', snd=False)
s.box('<div class="num" style="font-size:250px;color:#ffd166">23</div><div class="sub" style="font-size:46px">ANNI</div>', RX - 20, 560, 520, 340, enter='none', snd=None)
s.panel('costi iniziali', [dict(label='PATENTE C', value='≈ 1.200 €', color=INK, at=T(2, 'patente')),
                         dict(label='CQC · 140 ORE', value='≈ 2.400 €', color=INK, at=T(2, 'CQC')),
                         dict(label='TOTALE', fmt='> {n} €', to=3000, frm=0, at=T(2, 'tremila'), dur=1.0, color=RED)],
        RX, 960, w=620, at=T(2, 'speso'))
s.img('patente', 600, 290, h=170, rot=-8, enter='left', at=T(2, 'patente'), z=5)
s.img('cqc', 880, 300, h=170, rot=7, enter='right', at=T(2, 'CQC'), z=5)

# ---- S2 : camion + quindici anni (5,28 – 10,54) --------------------------------------
s = stage('s2', 3, 4)
s.box('<div class="road"><div class="dash" id="s2-dash"></div></div>', 540, 700, 1500, 150, enter='none', z=1, snd=None, until=T(4, 'Quindici', -0.1), cls='roadbox')
s.img('truck_new', 540, 600, w=900, enter='right', at=T(3), until=T(4, 'Quindici', -0.1), drift=0.04)
s.img('marco23_head', 300, 700, h=420, enter='left', at=T(4, 'Quindici'), dim=None)
s.img('marco38_head', 780, 700, h=420, enter='right', at=T(4, 'cosa'))
s.box('<div class="num" style="font-size:170px;color:#ff4d6d">?</div>', 540, 690, 160, 200, at=T(4, 'resta'), snd='pop')
s.tag('15 anni dopo', 540, 470, 520, 'red', at=T(4, 'Quindici', .25))

# ---- S3 : anno 1 (10,54 – 19,38) ---------------------------------------------------
s = stage('s3', 5, 7)
s.box('<div class="halo" style="background:radial-gradient(circle,rgba(120,90,255,.45) 0%,transparent 68%)"></div>', LX, 700, 600, 600, enter='none', z=1, snd=None)
s.img('marco23_full', LX, 700, h=540, enter='left', at=T(5), snd=True)
s.tag('autista neoassunto', RX, 400, 540, 'blue', at=T(5, 'Autista'), until=T(7, 'resto'))
s.panel('stipendio', [dict(label='LORDO · MESE', fmt='≈ {n} €', to=1500, frm=0, at=T(6, 'millecinquecento'), dur=1.1, color=GOLD)],
        RX, 590, w=540, at=T(6, 'circa'), until=T(7, 'resto'))
s.conn(330, 640, 455, 590, T(6, 'circa', .3), GOLD, bend=0, until=T(7, 'resto'))
s.img('soldi', RX + 40, 840, h=200, enter='pop', at=T(6, 'euro'), until=T(7, 'resto'))
s.img('truck_new', RX, 560, w=400, enter='right', at=T(7, 'resto'))
s.tag('trasferte', RX, 760, 420, 'red', at=T(7, 'trasferte'))
s.tiles('LMMGVSD', 652, 930, at=T(7, 'straordinari'), size=84)
s.tag('+ straordinari', 652, 1040, 500, 'gold', at=T(7, 'straordinari', .5))

# ---- S4 : cabina (19,38 – 22,06) -----------------------------------------------------
s = stage('s4', 8, 8)
s.img('cab_interior', 540, 650, w=780, enter='pop', at=T(8), drift=0.05)
s.tag('la tua casa', 540, 1010, 500, 'red', at=T(8, 'casa'))

# ---- S5 : anno 5 (22,06 – 28,68) -----------------------------------------------------
s = stage('s5', 9, 10)
s.img('marco28_full', LX, 700, h=540, enter='left', at=T(9))
s.img('patenteCE', RX, 400, h=200, rot=6, enter='right', at=T(9, 'CE'), until=T(10, 'minimo'))
s.conn(340, 620, 600, 440, T(9, 'CE', .2), GREEN, bend=40, until=T(10, 'minimo'))
s.img('truck_new', RX, 700, w=420, enter='right', at=T(9, 'tratte'), until=T(10, 'minimo'))
s.panel('stipendio lordo', [dict(label='ANNO 1', value='1.500 €', color=GREY, strike=True, at=T(10, 'minimo')),
                            dict(label='ANNO 5', fmt='≈ {n} €', to=2000, frm=1500, at=T(10, 'duemila'), dur=.9, color=GREEN)],
        RX, 620, w=560, at=T(10, 'minimo'))
s.box(f'<div class="arrow">▲</div>', RX, 870, 120, 100, at=T(10, 'duemila', .9), snd='ping')
s.badge('ok', RX + 255, 520, T(10, 'duemila', .9))

# ---- S6 : diaria / non è stipendio (28,68 – 35,70) -----------------------------------
s = stage('s6', 11, 12)
s.img('marco28_full', 170, 740, h=480, enter='none', snd=False, until=None)
s.tag('la diaria', RX, 360, 440, 'gold', at=T(11), until=T(12, 'Non'))
s.panel('diaria', [dict(label='FINO A', fmt='{n} € / giorno', to=46, frm=0, at=T(11, 'quarantasei'), dur=.8, color=GOLD)],
        RX, 560, w=560, at=T(11, 'Poi', .2), until=T(12, 'Non'))
s.img('soldi', RX, 830, h=240, enter='up', at=T(11, 'fino'), until=T(12, 'Non'))
s.img('portafoglio', RX, 640, w=520, enter='up', at=T(12, 'Non'))
s.stamp('NON È STIPENDIO', RX, 880, 600, rot=-6, size=52, at=T(12, 'stipendio'))
s.badge('no', RX + 235, 520, T(12, 'stipendio', .3))

# ---- S7 : tachigrafo / 9 ore / multa (35,70 – 41,40) ---------------------------------
s = stage('s7', 13, 15)
s.img('tachigrafo', 540, 620, w=640, enter='pop', at=T(13), until=T(14, 'Nove'), drift=0.05)
s.tag('il tachigrafo', 540, 330, 480, 'blue', at=T(13, 'tachigrafo'), until=T(14, 'Nove'))
s.tag('limite di guida', 540, 330, 520, 'red', at=T(14, 'Nove'), until=T(15, 'multa'))
s.box('<div class="ring"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="ring-bg"/>'
      '<circle id="s7-ringfill" cx="100" cy="100" r="86" class="ring-fg" transform="rotate(-90 100 100)"/></svg>'
      '<div class="ringtxt"><span class="num" id="s7-ringnum" style="font-size:160px;color:#ffd166">0</span>'
      '<span class="sub" style="font-size:40px">ORE / GIORNO</span></div></div>', 540, 640, 480, 480, at=T(14, 'Nove'), until=T(15, 'multa'))
s.counters.append(dict(el='s7-ringnum', frm=0, to=9, fmt='{n}', t=T(14, 'Nove', .1), dur=1.4))
s.img('multa', 540, 640, h=520, enter='shake', rot=-6, at=T(15, 'multa'))
s.stamp('MULTA', 700, 900, 460, rot=-10, size=74, at=T(15, 'arriva'))

# ---- S8 : anno 10 (41,40 – 49,36) ---------------------------------------------------
s = stage('s8', 16, 18)
s.box('<div class="halo" style="background:radial-gradient(circle,rgba(120,90,255,.45) 0%,transparent 68%)"></div>', LX, 700, 600, 600, enter='none', z=1, snd=None)
s.img('marco33_full', LX, 700, h=540, enter='left', at=T(16))
s.panel('scatti di anzianità', [dict(label='AL MESE', fmt='+{n} €', to=30, frm=0, at=T(17, 'venticinque'), dur=1.3, color=GREEN)],
        RX, 520, w=540, at=T(17, 'scatti'), until=T(18, 'Ogni'))
s.conn(330, 640, 455, 540, T(17, 'scatti', .3), GREEN, bend=0, until=T(18, 'Ogni'))
s.img('calendario', RX, 700, h=380, enter='pop', at=T(18, 'Ogni'))
s.tag('ogni 2 anni', RX, 950, 440, 'red', at=T(18, 'due'))

# ---- S9 : bravissimo / busta paga (49,36 – 53,94) ------------------------------------
s = stage('s9', 19, 20)
s.box('<div class="halo" style="background:radial-gradient(circle,rgba(255,209,102,.38) 0%,transparent 68%)"></div>', 540, 700, 740, 740, enter='none', z=1, snd=None, until=T(20, 'busta'))
s.img('marco33_full', 540, 700, h=560, enter='pop', at=T(19), until=T(20, 'busta'))
for k, (x, y, sz) in enumerate([(300, 480, 120), (800, 560, 96), (760, 900, 84), (330, 880, 76)]):
    s.box(f'<div class="spark" style="font-size:{sz}px">★</div>', x, y, sz + 20, sz + 20, at=T(19, 'bravissimo', k * .12), until=T(20, 'busta'), snd='pop' if k == 0 else None)
s.box('<div class="paper"><div class="ph">BUSTA PAGA</div><div class="pl"></div><div class="pl s"></div><div class="pl"></div>'
      '<div class="hl" id="s9-hl"><span>aumento anzianità</span><b>+30 €</b></div><div class="pl s"></div></div>',
      540, 650, 620, 520, enter='up', at=T(20, 'busta'))
sfx(T(20, 'quasi'), 'whoosh-short', .2)

# ---- S10 : 90 h / 45 h / lontano (53,94 – 62,56) -------------------------------------
s = stage('s10', 21, 23)
s.tag('limite massimo', 540, 360, 520, 'red', at=T(21), until=T(22, 'riposo'))
s.bignum('{n} h', 90, 540, 560, at=T(21, 'novanta'), dur=1.4, size=210, color=GOLD, sub='OGNI 2 SETTIMANE', w=700, until=T(22, 'riposo'))
s.box('<div class="bar"><div id="s10-barfill" class="barfill"></div></div>', 540, 790, 760, 62, enter='up', at=T(21, 'novanta', .3), until=T(22, 'riposo'), snd=None)
s.img('marco33_chair', 640, 730, h=500, enter='up', at=T(22, 'riposo'))
s.bignum('{n} h', 45, 270, 480, at=T(22, 'quarantacinque'), dur=1.1, size=150, color=GREEN, sub='DI RIPOSO', w=420, enter='left')
s.img('truck_new', 270, 780, w=330, enter='pop', at=T(22, 'camion'))
s.badge('no', 270, 780, T(22, 'camion', .2), size=110)
s.tag('lontano da casa', 540, 360, 640, 'red', at=T(23, 'lontano'))

# ---- S11 : videochiamata (62,56 – 65,06) ----------------------------------------------
s = stage('s11', 24, 24)
s.img('marco33_phone', 270, 700, h=500, enter='left', at=T(24))
s.box('<div class="phone"><img class="kid" src="assets/img/figlio.png"></div>', 790, 660, 300, 540, enter='right', at=T(24, 'figlio'), snd='notification')
s.tag('videochiamata', 790, 330, 460, 'blue', at=T(24, 'videochiamate'))

# ---- S12 : anno 15 / bivio / opzioni (65,06 – 71,38) ------------------------------------
s = stage('s12', 25, 26)
s.img('marco38_full', LX - 20, 710, h=540, enter='left', at=T(25))
s.img('bivio', RX, 650, h=420, enter='right', at=T(25, 'bivio'), until=T(26, 'Continuare'))
s.box('<div class="opt"><div class="otitle">DIPENDENTE</div><img src="assets/img/truck_worn.png"></div>', RX + 20, 450, 540, 210, at=T(26, 'dipendente'))
s.conn(330, 620, 460, 470, T(26, 'dipendente', -.2), GREEN, bend=30)
s.badge('ok', RX + 270, 360, T(26, 'dipendente', .5))
s.box('<div class="or">OPPURE</div>', RX + 20, 640, 300, 70, at=T(26, 'comprare'))
s.box('<div class="opt gold"><div class="otitle">PADRONCINO</div><img class="keys" src="assets/img/chiavi.png"></div>', RX + 20, 840, 540, 210, at=T(26, 'padroncino'))
s.conn(330, 760, 460, 850, T(26, 'padroncino', -.2), GOLD, bend=30)

# ---- S13 : fatturato / utile / stima (71,38 – 79,48) -----------------------------------
s = stage('s13', 27, 29)
s.box('<div class="chart"><div class="col"><div id="s13-b1" class="b gr"></div><div class="lbl">FATTURATO</div></div>'
      '<div class="col"><div id="s13-b2" class="b rd"></div><div class="lbl">UTILE</div></div></div>', 540, 640, 720, 560, enter='up', at=T(27), until=T(28, 'stime'))
s.panel('padroncino · stima', [dict(label='NETTO AL MESE', value='<span id="s13-ra">0</span> – <span id="s13-rb">0</span> €', color=GOLD)], 540, 520, w=860, at=T(28, 'stime'), until=None)
s.counters.append(dict(el='s13-ra', frm=0, to=1400, fmt='{n}', t=T(28, 'millequattrocento'), dur=1.0))
s.counters.append(dict(el='s13-rb', frm=0, to=3000, fmt='{n}', t=T(28, 'tremila'), dur=1.0))
s.stamp('NETTI', 340, 860, 420, rot=-8, size=92, at=T(29, 'Netti'))
s.stamp('AL MESE', 740, 940, 520, rot=6, size=76, color=GREEN, at=T(29, 'mese'))

# ---- S14 : coûts / panne (79,48 – 84,66) ------------------------------------------------
s = stage('s14', 30, 31)
s.box('<div class="meter"><div class="mlab">UTILE AL MESE</div><div class="mtrack"><div id="s14-fill" class="mfill"></div></div></div>', 540, 400, 820, 150, enter='down' if False else 'drop', at=T(30))
s.img('pompa', 190, 760, h=270, enter='left', at=T(30, 'Gasolio'), until=T(31, 'camion', -.05))
s.tag('gasolio', 190, 950, 300, 'red', at=T(30, 'Gasolio', .1), until=T(31, 'camion', -.05))
s.img('assicurazione', 540, 760, h=270, enter='drop', at=T(30, 'assicurazione'), until=T(31, 'camion', -.05), rot=4)
s.tag('assicurazione', 540, 950, 420, 'red', at=T(30, 'assicurazione', .1), until=T(31, 'camion', -.05))
s.img('rate', 890, 760, h=240, enter='right', at=T(30, 'rate'), until=T(31, 'camion', -.05), rot=-4)
s.tag('rate', 890, 950, 220, 'red', at=T(30, 'rate', .1), until=T(31, 'camion', -.05))
s.conn(190, 640, 330, 480, T(30, 'Gasolio', .15), RED, bend=30, until=T(31, 'camion', -.05))
s.conn(540, 640, 540, 480, T(30, 'assicurazione', .15), RED, bend=0, until=T(31, 'camion', -.05))
s.conn(890, 640, 740, 480, T(30, 'rate', .15), RED, bend=30, until=T(31, 'camion', -.05))
s.img('truck_broken', 540, 780, w=700, enter='pop', at=T(31, 'camion'), drift=0.04)
s.stamp('FERMO', 540, 1040, 400, rot=-6, size=70, at=T(31, 'ferma'))

# ---- S15 : finale (84,66 – 89,10), puis 89,10 – 94,68, puis fin ---------------------------
s = stage('s15', 32, 33)
s.img('marco38_full', 250, 710, h=540, enter='left', at=T(32), until=T(33, 'cambio'))
s.img('truck_worn', 740, 790, w=480, enter='right', at=T(32, 'lavoro'), until=T(33, 'cambio'))
s.img('marco38_tired', 540, 700, h=600, enter='up', at=T(33, 'cambio'))
s.img('calendario', 220, 460, h=300, enter='drop', at=T(33, 'anni'), rot=-8)
s = stage('s16', 34, 35)
s.img('marco23_full', 250, 710, h=540, enter='left', at=T(34), until=T(35, 'A', -.05))
s.img('truck_new', 740, 790, w=480, enter='right', at=T(34, 'camion'), until=T(35, 'A', -.05))
s.img('marco38_full', 250, 710, h=540, enter='pop', at=T(35, 'A'))
s.img('truck_worn', 740, 790, w=480, enter='pop', at=T(35, 'A'))
s.tag('trentotto', 540, 380, 380, 'red', at=T(35, 'trentotto'))
s = stage('s17', 36, 37)
s.img('marco38_head', 540, 640, h=700, enter='pop', at=T(36), until=T(37, 'Iscriviti', -.1), drift=0.08)
s.img('campanella', 540, 640, w=860, enter='pop', at=T(37, 'Iscriviti'), drift=0.0, snd=False)
s.box('<div class="cta">ISCRIVITI</div>', 712, 628, 380, 100, at=T(37, 'Iscriviti', .2), z=9, snd=None)
sfx(T(37, 'Iscriviti'), 'notification', .4)

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

CAPTXT = {1: 'Hai [[ventitré]] anni.', 2: 'Hai speso oltre [[tremila euro]] per patente e CQC.', 3: 'Davanti a te, un [[camion]] e la strada.',
 4: '[[Quindici anni]] dopo, cosa ti resta davvero?', 5: 'Anno [[uno]]. Autista neoassunto.', 6: 'Prendi circa [[millecinquecento euro]] lordi al mese.',
 7: 'Il resto lo fanno [[trasferte]] e [[straordinari]].', 8: 'La tua casa, adesso, è una [[cabina]].', 9: 'Anno [[cinque]]. Patente CE, tratte lunghe.',
 10: 'Il minimo contrattuale sale a circa [[duemila euro]] lordi.', 11: 'Poi arriva la [[diaria]], fino a [[quarantasei euro]] al giorno.',
 12: '[[Non è stipendio.]] Ma ti fa arrivare a fine mese.', 13: 'Impari il [[tachigrafo]].', 14: '[[Nove ore]] di guida, non una di più.',
 15: 'Se sgarri, la [[multa]] arriva.', 16: 'Anno [[dieci]]. Sei un veterano.', 17: 'Gli scatti di anzianità valgono [[venticinque, trenta euro]] al mese.',
 18: 'Ogni [[due anni]].', 19: 'Dopo dieci anni sei [[bravissimo]].', 20: 'In busta paga, [[quasi non si vede]].',
 21: 'Ogni [[due settimane]], novanta ore di guida al massimo.', 22: 'Il riposo lungo, [[quarantacinque ore]], lo fai fuori dal camion.',
 23: 'Spesso, [[lontano da casa]].', 24: 'Tuo figlio cresce nelle [[videochiamate]].', 25: 'Anno [[quindici]]. Il bivio.',
 26: 'Continuare da [[dipendente]], o comprare il camion e diventare [[padroncino]].', 27: "Il [[fatturato]] sale. L'[[utile]], molto meno.",
 28: 'Le stime vanno da [[millequattrocento]] a [[tremila euro]].', 29: '[[Netti]], al mese.', 30: '[[Gasolio]], [[assicurazione]] e [[rate]] le paghi tu.',
 31: 'E se il camion si ferma, [[ti fermi tu]].', 32: 'La strada ti ha dato un [[lavoro sicuro]].', 33: 'E in cambio, ti ha preso [[gli anni]].',
 34: 'Hai [[ventitré]] anni. Un camion. Una strada.', 35: 'A [[trentotto]], la strada è ancora lì.', 36: "Tu, un po' [[meno]].",
 37: '[[Iscriviti]], se vuoi sapere cosa serve davvero.'}
CAPMARK = {}
for n, c in CAPTXT.items():
    emph, marks = False, []
    for tk in c.split(' '):
        if '[[' in tk: emph = True
        marks.append(emph)
        if ']]' in tk: emph = False
    CAPMARK[n] = marks
    assert len(marks) == len(BEATS[n - 1].words), n

# ------------------------------------------------------------------ CSS
CSS = """
  #root { position:absolute; inset:0; font-family:'Montserrat',sans-serif; color:#fff; }
  .stage { position:absolute; inset:0; transform-origin:50% 45%; }
  .item { position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .item img.pic { width:100%; height:100%; object-fit:contain; display:block; filter:drop-shadow(0 16px 24px rgba(0,0,0,.45)); }
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
  .item:has(> .gtag) { flex-direction:row; }
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
    html.append(f'<div class="stage clip" id="{sid}-stage" data-start="0" data-duration="{dur}" data-track-index="1"><div class="stage" id="{sid}-cam">')
    js.append(f'tl.fromTo("#{sid}-cam",{{scale:1,y:0}},{{scale:1.09,y:-34,duration:{dur},ease:"none"}},0);')
    # connecteurs
    if S.paths:
        html.append(f'<svg class="conn clip" id="{sid}-svg" data-start="0" data-duration="{dur}" data-track-index="2" viewBox="0 0 1080 1920">')
        for p in S.paths:
            rel = round(p['at'] - S.t0, 3)
            gl = f'filter:drop-shadow(0 0 7px {p["color"]})'
            html.append(f'<path id="{p["id"]}" d="{p["d"]}" pathLength="1" stroke="{p["color"]}" style="{gl}"/>')
            if p['dot'] and p.get('end'):
                html.append(f'<circle id="{p["id"]}-d" cx="{p["end"][0]}" cy="{p["end"][1]}" r="11" fill="{p["color"]}" opacity="0" style="{gl}"/>')
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
        if it['k'] == 'img':
            iw, ih = SIZE[it['name']]
            if it['h']: hh = it['h']; ww = hh * iw / ih
            else: ww = it['w']; hh = ww * ih / iw
            fade = ' fade' if it['name'].endswith('_head') else ''
            inner = f'<img class="pic{fade}" id="{iid}-p" src="assets/img/{it["name"]}.png" alt="">'
        else:
            ww, hh = it['w'], it['h']
            inner = it['html']
        left, top = it['cx'] - ww / 2, it['cy'] - hh / 2
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
            ch = it['k'] == 'img' and it['name'].startswith('marco')
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
        elif snd is True and it['k'] == 'img' and e in ('left', 'right') and not it['name'].startswith('marco'): sfx(it['at'], 'whoosh-short', .24)
        if it.get('flash') and e != 'none':
            S.items_flash = getattr(S, 'items_flash', []) + [(it['cx'], it['cy'], it['at'] + .12, min(it['w'] or 200, 300) if it['k'] == 'box' else 260)]
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
        pop_sfx(c['t'] + .5, .2) if False else None
    # animations propres
    if sid == 's2':
        js.append(f'tl.fromTo("#s2-dash",{{x:0}},{{x:-280,duration:{T(4,"Quindici") - S.t0:.2f},ease:"none"}},0);')
    if sid == 's7':
        js.append(f'tl.fromTo("#s7-ringfill",{{strokeDashoffset:540.4}},{{strokeDashoffset:0,duration:1.4,ease:"power2.out"}},{T(14,"Nove",.1) - S.t0:.2f});')
        # flash rouge de la multa
        js.append(f'tl.fromTo("#s7-redflash",{{opacity:0}},{{opacity:.55,duration:.08,yoyo:true,repeat:1,ease:"none"}},{T(15,"multa",.05) - S.t0:.2f});')
    if sid == 's9':
        js.append(f'tl.fromTo("#s9-hl",{{borderColor:"rgba(255,77,109,0)",scale:1}},{{borderColor:"#ff4d6d",scale:1.07,duration:.35,ease:"back.out(2)"}},{T(20,"quasi") - S.t0:.2f});')
    if sid == 's10':
        js.append(f'tl.fromTo("#s10-barfill",{{scaleX:0}},{{scaleX:1,duration:1.5,ease:"power2.out"}},{T(21,"novanta",.3) - S.t0:.2f});')
    if sid == 's13':
        js.append(f'tl.fromTo("#s13-b1",{{scaleY:0}},{{scaleY:1,duration:.7,ease:"power3.out"}},{T(27,"fatturato",.1) - S.t0:.2f});')
        js.append(f'tl.fromTo("#s13-b2",{{scaleY:0}},{{scaleY:1,duration:.7,ease:"power3.out"}},{T(27,"utile",.05) - S.t0:.2f});')
    if sid == 's14':
        t = lambda b, w: T(b, w, .25) - S.t0
        js.append(f'tl.fromTo("#s14-fill",{{scaleX:1}},{{scaleX:.72,duration:.5,ease:"power2.out"}},{t(30,"Gasolio"):.2f});')
        js.append(f'tl.to("#s14-fill",{{scaleX:.46,duration:.5,ease:"power2.out"}},{t(30,"assicurazione"):.2f});')
        js.append(f'tl.to("#s14-fill",{{scaleX:.24,duration:.5,ease:"power2.out"}},{t(30,"rate"):.2f});')
        js.append(f'tl.to("#s14-fill",{{scaleX:.02,backgroundColor:"#ff4d6d",duration:.5,ease:"power2.in"}},{T(31,"ferma",.1) - S.t0:.2f});')
    # le décor entier recule à la fin
    last = ex_end - 0.02
    if sid != STAGES[-1].id:
        js.append(f'tl.to("#{sid}-stage",{{opacity:0,scale:.9,filter:"blur(14px)",duration:{OVER + .02},ease:"power2.in"}},{last - .02:.3f});')
        sfx(S.t1 - .12, 'sweep', .27)
    else:
        js.append(f'tl.to("#{sid}-stage",{{opacity:0,duration:.3,ease:"power1.in"}},{dur - .4:.3f});')
    if sid == 's7':
        html.insert(1, f'<div class="clip" id="s7-redflash" data-start="0" data-duration="{dur}" data-track-index="5" style="position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 40%,rgba(255,40,70,.8) 100%);opacity:0;z-index:20"></div>')
    html.append('</div></div>')
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
    open(os.path.join(OUT, 'compositions', f'{sid}.html'), 'w', encoding='utf-8').write(comp)

for S in STAGES:
    build_stage(S)

# règle de carrière (composition globale) -------------------------------------------------
X0, XS = 90, 60
ticks = ''.join(f'<div class="rl-tick" style="left:{X0 + i * XS - 2}px"></div>' for i in range(16))
nums = ''.join(f'<div class="rl-num" style="left:{X0 + i * XS}px">{i}</div>' for i in (0, 5, 10, 15))
rul_js = []
marks = [(T(4, 'Quindici'), 15, .95), (T(5, 'uno', -.35), 1, .55), (T(9, 'cinque', -.2), 5, .6), (T(16, 'dieci', -.2), 10, .6), (T(25, 'quindici', -.2), 15, .7)]
rul_js.append(f'var o={{v:0}};function up(){{var v=o.v;var x={X0}+v*{XS};document.getElementById("rl-dot").style.left=x+"px";'
              f'document.getElementById("rl-fill").style.width=(v*{XS})+"px";document.getElementById("rl-lab").style.left=Math.min(x,880)+"px";'
              f'document.getElementById("rl-lab").firstChild.lastChild.nodeValue="ANNO "+Math.round(v);}}')
start_t = T(4, 'Quindici', -.25)
rul_js.append(f'tl.fromTo("#rl",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,ease:"expo.out"}},{start_t:.3f});')
for (t, v, d) in marks:
    rul_js.append(f'tl.to(o,{{v:{v},duration:{d},ease:"power3.inOut",onUpdate:up}},{t:.3f});')
sfx(T(4, 'Quindici'), 'whoosh', .22)
for (t, v, d) in marks[1:]:
    sfx(t + d, 'ping', .22)
rul_js.append(f'tl.to("#rl",{{opacity:0,duration:.4,ease:"power2.in"}},{STAGES[-3].t0 - .1:.3f});')
ruler = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="rul" data-width="{W}" data-height="{H}">
    <div id="rl" class="clip" data-start="{start_t:.3f}" data-duration="{round(STAGES[-3].t0 + .5 - start_t, 3)}" data-track-index="1" style="position:absolute;inset:0;z-index:25">
      <div class="rl-line"></div><div class="rl-fill" id="rl-fill"></div>{ticks}{nums}
      <div class="rl-dot" id="rl-dot" style="left:{X0}px"></div>
      <div class="rl-lab" id="rl-lab" style="left:{X0}px"><div class="gtag red"><i class="dot"></i>ANNO 0</div></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in rul_js)}
    window.__timelines["rul"] = tl;
  </script>
</template>
"""
# (le « #rl » démarre à start_t : les temps de la composition sont locaux à son hôte → hôte = 0 s)
ruler = ruler.replace(f'data-start="{start_t:.3f}" data-duration="{round(STAGES[-3].t0 + .5 - start_t, 3)}"', f'data-start="0" data-duration="{round(TOTAL, 3)}"')
# on garde les temps absolus dans la timeline : l'hôte « rul » démarre à 0
open(os.path.join(OUT, 'compositions', 'rul.html'), 'w', encoding='utf-8').write(ruler)

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
hosts.append(f'      <div id="rul" class="clip" data-composition-id="rul" data-composition-src="compositions/rul.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
hosts.append(f'      <div id="caps" class="clip" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{TOTAL}" data-track-index="6" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>')

SFXLOG.sort()
audio = []
for n, (t, f, v) in enumerate(SFXLOG):
    if t < 0 or t > TOTAL - .2: continue
    t = min(t, TOTAL - SFXDUR[f] - .02)
    src = f'assets/audio/{f}.wav' if f == 'sweep' else f'assets/sfx/{f}.mp3'
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
{chr(10).join(hosts)}
      <audio id="voce" src="assets/voce.wav" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
      <audio id="bed" src="assets/audio/bed.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="1"></audio>
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
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)
open(os.path.join(OUT, 'hyperframes.json'), 'w').write('{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",\n  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},\n  "media": {"autoProxy": true}\n}\n')
open(os.path.join(OUT, 'meta.json'), 'w').write('{"id": "camionista-v3", "name": "La tua vita dopo 15 anni da camionista (9:16 v3)"}')
print('ok v3:', len(STAGES), 'décors,', len(SFXLOG), 'effets,', len(audio), 'audio')
