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
OUT = os.path.join(ROOT, 'vhvac')
CUT = os.path.join(ROOT, 'assets', 'cut-hvac')
SFXSRC = os.path.join(ROOT, '..', '.claude', 'skills', 'media-use', 'audio', 'assets', 'sfx')
AUDSRC = os.path.join(ROOT, 'assets', 'audio')
VOICE = '/root/.claude/uploads/91729ddc-3274-50e3-9f11-8e52419e14ce/280557de-Generated_Audio_October_24_2026_-_5_04PM.wav'
SCRIPT = os.path.join(ROOT, '..', 'scripts', 'hvac-6min.txt')
SRT = os.path.join(ROOT, '..', 'scripts', 'hvac-scenes.srt')
TOTAL = 355.4
W, H = 1920, 1080
CAP_Y = 960
K_IMG, K_BOX = 1.0, 1.0
ZB = 880
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
NUMW = set('diciannove dieci diciotto venti uno due tre quattro cinque sei milleseicentocinquanta duemilaventisei tredici quattrocentocinquanta seicentosessantacinque millesettecentocinquanta venticinque sessanta trenta ottanta'.split())
norm = lambda t: re.sub(r"[^\w]", "", t.lower().replace("l'", "l"))
WW = [[d['w'], d['s'], d['e']] for d in json.load(open(os.path.join(HERE, 'words-hvac.json')))]
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
open(os.path.join(ROOT, '..', 'scripts', 'hvac-scenes-aligned.srt'), 'w', encoding='utf-8').write(
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
    for w, t0, t1 in b.words:
        if len(k) >= 4 and k in norm(w):
            return round(max(b.s, t0) + off, 3)
    raise SystemExit(f'mot introuvable: {word!r} dans le plan {beat}: {b.text}')

# ------------------------------------------------------------------ assets
for d in ('assets/img', 'assets/sfx', 'assets/sfx2', 'assets/audio', 'compositions'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
SIZE = {}
for f in os.listdir(CUT):
    im = Image.open(os.path.join(CUT, f)); im.thumbnail((1100, 1100))
    im.save(os.path.join(OUT, 'assets', 'img', f), optimize=True); SIZE[f[:-4]] = im.size
shutil.copy(os.path.join(AUDSRC, 'voce_hvac_norm.wav'), os.path.join(OUT, 'assets', 'voce.wav'))
for _f in os.listdir(os.path.join(ROOT, 'assets', 'raw-hvac')):
    if _f.startswith('bg-'):
        Image.open(os.path.join(ROOT, 'assets', 'raw-hvac', _f)).convert('RGB').resize((1920, 1080), Image.LANCZOS).save(os.path.join(OUT, 'assets', 'img', _f), quality=88)
for f in ('bed_long.wav', 'sweep.wav', 'music_long.wav'):
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
        self.zt = 205
        self.n = 0
    def _id(self, p):
        self.n += 1
        return f'{self.id}-{p}{self.n}'
    def bg(self, name):
        self.bgname = name
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
LX, RX, CX = 440, 1290, 960
def tags(s, items, x=RX, y0=300, dy=125, until=None):
    """items = [(texte, couleur, instant)] empilés verticalement"""
    for k, (txt, col, at) in enumerate(items):
        s.tag(txt, x, y0 + k * dy, 80 + 22 * len(txt), col, at=at, until=until)

# ================================ OUVERTURE ================================
s = stage('s1', 1, 3); s.bg('bg-tetto')
s.img('and_19', LX, 520, h=660, enter='left', at=T(1))
s.img('sole', RX, 450, h=360, enter='pop', at=T(1, 'luglio'), until=T(3, 'rame'))
s.tag('luglio · sul tetto', RX, 740, 520, 'gold', at=T(1, 'tetto'), until=T(3, 'rame'))
s.tag('catrame bollente', RX, 850, 420, 'red', at=T(2, 'catrame'), until=T(3, 'rame'))
s.img('rame_isolato', RX, 470, h=300, enter='pop', at=T(3, 'rame'))
s.tag('rame · stagno · caldo', RX, 760, 520, 'gold', at=T(3, 'stagno'))
s.punch(T(1, 'luglio')); s.punch(T(3, 'caldo'))
sfx(.02, 'camera-shutter', .5); sfx(.40, 'whoosh-deep', .4)

s = stage('s2', 4, 7); s.bg('bg-tetto')
s.img('and_19', LX, 520, h=660, enter='none', at=T(4), snd=False)
s.img('unit_out', RX, 480, h=420, enter='right', at=T(4, 'esterna'), until=T(7, 'Non'))
s.tag('il tuo capo', RX, 760, 340, 'blue', at=T(5, 'capo'), until=T(7, 'Non'))
s.tag('«tieni ferma questa»', RX, 870, 520, 'gold', at=T(6, 'ferma'), until=T(7, 'Non'))
s.img('rame_isolato', RX, 470, h=340, enter='pop', at=T(7, 'tubi'))
s.box('<div class="num" style="font-size:230px;color:#ffd166">?</div>', RX + 360, 330, 200, 260, at=T(7, 'sai'))
s.punch(T(5, 'chiave')); s.punch(T(7, 'sai'))

s = stage('s3', 8, 9); s.bg('bg-tetto')
s.img('and_37', LX, 520, h=660, enter='left', at=T(8))
s.img('foglio_timbro', RX, 470, h=420, enter='pop', at=T(8, 'firmare'))
s.tag('tra dieci anni', RX, 780, 440, 'blue', at=T(8, 'dieci'))
s.stamp('SE SBAGLI', RX, 870, 480, rot=-6, size=64, at=T(9, 'sbagli'))
s.punch(T(8, 'firmare')); s.punch(T(9, 'sbagli'), 'shake')

s = stage('s4', 10, 12); s.bg('bg-salotto')
s.img('ventilatore', RX, 470, h=380, enter='pop', at=T(10, 'estate'), until=T(11, 'Ecco'))
s.tag('una casa senza aria', RX, 760, 520, 'red', at=T(10, 'senza'), until=T(11, 'Ecco'))
s.img('unit_split', CX, 360, h=210, enter='drop', at=T(11, 'prima'), until=T(12, 'Un'))
tags(s, [('rumore', 'red', T(12, 'rumore')), ('gocce', 'blue', T(12, 'gocce')), ('poca aria fredda', 'gold', T(12, 'fredda'))], x=CX, y0=360, dy=130)
s.punch(T(10, 'senza')); s.punch(T(12, 'fredda'))

s = stage('s5', 13, 15); s.bg('bg-officina')
s.img('and_27', LX, 520, h=660, enter='left', at=T(13))
s.tag('tecnico HVAC', RX, 300, 440, 'blue', at=T(13, 'HVAC'), until=T(15, 'Iscriviti'))
s.tag('frigorista', RX, 430, 320, 'gold', at=T(14, 'frigorista'), until=T(15, 'Iscriviti'))
s.img('unit_split', RX - 190, 700, h=180, enter='pop', at=T(14, 'installa'), until=T(15, 'Iscriviti'))
s.img('pompa_calore', RX + 190, 690, h=240, enter='pop', at=T(14, 'riscaldamento'), until=T(15, 'Iscriviti'))
s.img('campanella', RX, 640, h=330, enter='pop', at=T(15, 'Iscriviti'))
s.tag('iscriviti', RX, 880, 330, 'red', at=T(15, 'Iscriviti', .2))
s.punch(T(13, 'HVAC')); sfx(T(15, 'Iscriviti'), 'notification', .4)

# ================================ LIVELLO 1 ================================
s = stage('s6', 16, 19); s.bg('bg-officina')
s.img('and_19', LX, 520, h=660, enter='left', at=T(16))
s.tag('livello 1', RX, 280, 340, 'blue', at=T(16, 'uno'))
s.tag('apprendista', RX, 400, 340, 'gold', at=T(16, 'apprendista'))
s.img('rame_isolato', RX - 190, 640, h=240, enter='pop', at=T(17, 'bobine'), until=T(18, 'Il'))
s.img('trapano', RX + 190, 640, h=240, enter='pop', at=T(17, 'trapani'), until=T(18, 'Il'))
s.tag('scale · trapani · tubo', RX, 850, 520, 'gold', at=T(17, 'scale'), until=T(18, 'Il'))
s.panel('stipendio', [dict(label='%', value='del livello', color=GOLD, at=T(18, 'percentuale'))], RX, 640, w=620, at=T(18, 'stipendio'), until=T(19, 'Quindi'))
s.tag('parti basso', RX, 640, 360, 'red', at=T(19, 'basso'))
s.box('<div class="arrow" style="color:#ff4d6d;font-size:120px">▼</div>', RX, 800, 160, 140, at=T(19, 'basso', .2), snd='ping')
s.punch(T(18, 'percentuale')); s.punch(T(19, 'basso'))

s = stage('s7', 20, 21); s.bg('bg-officina')
s.img('and_19', LX, 520, h=660, enter='none', at=T(20), snd=False)
tags(s, [('guardi', 'blue', T(20, 'guardi')), ('impari', 'gold', T(20, 'impari')), ('ti scotti', 'red', T(20, 'scotti'))], x=RX, y0=300, dy=120, until=T(21, 'Impari'))
s.img('unit_out', RX - 280, 520, h=250, enter='pop', at=T(21, 'esterna'))
s.img('unit_split', RX + 120, 520, h=200, enter='pop', at=T(21, 'interna'))
s.tag('unità esterna', RX - 280, 740, 360, 'blue', at=T(21, 'esterna'))
s.tag('unità interna', RX + 100, 740, 360, 'gold', at=T(21, 'interna'))
s.tag('split', RX + 360, 740, 200, 'red', at=T(21, 'split'))
s.punch(T(21, 'nomi'))

s = stage('s8', 22, 24); s.bg('bg-sottotetto')
s.img('pose_attic', CX - 120, 520, h=520, enter='pop', at=T(22, 'tetti'))
s.tag('tetti · balconi · cantine', CX - 120, 820, 620, 'gold', at=T(22, 'balconi'), until=T(23, 'Il'))
s.img('termometro', 1620, 480, h=480, enter='right', at=T(23, 'caldo'))
s.tag('sottotetto ad agosto', CX - 120, 820, 600, 'red', at=T(23, 'sottotetto'), until=T(24, 'Se'))
s.img('rame_isolato', 1540, 560, h=300, enter='pop', at=T(24, 'pieghi'))
s.badge('no', 1700, 420, T(24, 'butti'), size=110)
s.tag('tubo piegato = buttato', CX - 120, 820, 600, 'red', at=T(24, 'butti'))
s.punch(T(23, 'caldo')); s.punch(T(24, 'butti'), 'shake')

s = stage('s9', 25, 27); s.bg('bg-officina')
s.img('and_19', LX, 520, h=660, enter='left', at=T(25))
s.img('bombola', RX, 480, h=400, enter='pop', at=T(25, 'gas'))
s.badge('no', RX + 230, 320, T(25, 'tocchi'), size=120)
s.tag('circuito del gas', RX, 770, 480, 'red', at=T(25, 'gas'), until=T(26, 'Nelle'))
s.tag('strumenti delicati', RX, 770, 520, 'gold', at=T(26, 'strumenti'), until=T(27, 'Quello'))
s.stamp('CONFINE', RX, 870, 480, rot=-6, size=72, at=T(27, 'confine'))
s.punch(T(25, 'tocchi'), 'shake'); s.punch(T(27, 'confine'))

s = stage('s10', 28, 29); s.bg('bg-officina')
s.img('and_19', LX, 520, h=660, enter='none', at=T(28), snd=False)
s.img('bombola', RX, 470, h=400, enter='none', at=T(28), snd=False)
s.tag('fluido refrigerante', RX, 770, 560, 'blue', at=T(28, 'refrigerante'))
s.stamp('VIETATO DISPERDERLO', RX, 870, 700, rot=-5, size=56, at=T(29, 'vietato'))
s.punch(T(29, 'vietato'), 'shake'); sfx(T(29, 'vietato'), 'impact-bass-2', .3)

# ================================ LIVELLO 2 ================================
s = stage('s11', 30, 31); s.bg('bg-officina')
s.img('and_24', LX, 520, h=660, enter='left', at=T(30))
s.tag('livello 2', RX, 300, 340, 'blue', at=T(30, 'due'), until=T(31, 'Dopo'))
s.tag('operaio specializzato', RX, 430, 560, 'gold', at=T(30, 'Operaio'), until=T(31, 'Dopo'))
s.tag('installatore', RX, 560, 360, 'blue', at=T(30, 'installatore'), until=T(31, 'Dopo'))
s.tag('da solo, su impianti veri', RX, 460, 640, 'gold', at=T(31, 'solo'))
s.img('unit_out', RX, 720, h=260, enter='pop', at=T(31, 'impianti'))
s.punch(T(30, 'due')); s.punch(T(31, 'impianti'))

s = stage('s12', 32, 34); s.bg('bg-salotto')
s.img('pose_ladder', LX + 120, 500, h=660, enter='left', at=T(32))
s.tag('unità interna', RX, 300, 360, 'blue', at=T(32, 'interna'), until=T(33, 'Cartelli'))
s.img('evasatore', RX, 480, h=380, enter='right', at=T(33, 'Cartelli'), until=T(34, 'Poi'))
s.tag('cartellatura', RX, 760, 340, 'gold', at=T(33, 'Cartelli'), until=T(34, 'Poi'))
s.img('pompa_vuoto', RX - 130, 470, h=340, enter='pop', at=T(34, 'vuoto'))
s.img('manometri', RX + 190, 480, h=300, enter='pop', at=T(34, 'pompa'))
s.tag('il vuoto', RX, 760, 280, 'blue', at=T(34, 'vuoto'))
s.punch(T(33, 'Cartelli')); s.punch(T(34, 'vuoto'))

s = stage('s13', 35, 35); s.bg('bg-officina')
s.img('and_24', LX, 520, h=660, enter='left', at=T(35))
s.img('clipboard', RX, 470, h=400, enter='pop', at=T(35, 'controlla'))
s.tag('il capo parla poco', RX, 760, 520, 'gold', at=T(35, 'capo'))
s.tag('controlla tutto', RX, 870, 440, 'red', at=T(35, 'controlla'))

s = stage('s14', 36, 39); s.bg('bg-officina')
s.img('and_24', LX, 520, h=660, enter='none', at=T(36), snd=False)
s.panel('minimo contrattuale', [dict(label='LORDO / MESE', fmt='≈ {n} €', to=1650, frm=0, at=T(36, 'milleseicentocinquanta'), dur=1.1, color=GOLD)],
        RX, 400, w=720, at=T(36, 'minimo'), until=T(37, 'Lordi'))
s.img('soldi', RX, 700, h=240, enter='pop', at=T(36, 'euro'), until=T(37, 'Lordi'))
s.stamp('LORDO', RX - 190, 420, 440, rot=-7, size=96, at=T(37, 'Lordi'), until=T(38, 'Scatti'))
s.tag('13 mensilità', RX + 150, 640, 400, 'gold', at=T(37, 'tredici'), until=T(38, 'Scatti'))
s.tag('scatti di anzianità', RX, 340, 520, 'blue', at=T(38, 'Scatti'), until=T(39, 'Ma'))
s.tag('superminimi', RX, 470, 360, 'gold', at=T(38, 'superminimi'), until=T(39, 'Ma'))
s.box('<div class="arrow">▲</div>', RX, 680, 160, 140, at=T(38, 'superminimi', .3), snd='ping', until=T(39, 'Ma'))
s.stamp('SOLO UN MINIMO', RX, 470, 700, rot=-5, size=64, at=T(39, 'minimo'))
s.tag('non è la busta paga', RX, 700, 520, 'red', at=T(39, 'busta'))
s.punch(T(36, 'milleseicentocinquanta')); s.punch(T(37, 'Lordi'), 'shake'); s.punch(T(39, 'minimo'))
sfx(T(36, 'milleseicentocinquanta', 1.0), 'cash-register', .3)

s = stage('s15', 40, 41); s.bg('bg-officina')
s.img('and_24', LX, 520, h=660, enter='none', at=T(40), snd=False)
s.tag('la stessa frase', RX, 360, 460, 'blue', at=T(40, 'frase'), until=T(41, 'Se'))
s.img('bombola', RX - 150, 520, h=360, enter='pop', at=T(41, 'gas'))
s.img('tessera', RX + 180, 560, h=240, enter='pop', at=T(41, 'certificato'))
s.badge('no', RX + 40, 330, T(41, 'toccare'), size=120)
s.tag('senza patentino, niente gas', RX, 840, 700, 'red', at=T(41, 'certificato'))
s.punch(T(41, 'gas'), 'shake')

# ================================ LIVELLO 3 ================================
s = stage('s16', 42, 44); s.bg('bg-officina')
s.img('and_27', LX, 520, h=660, enter='left', at=T(42))
s.tag('livello 3', RX, 280, 340, 'blue', at=T(42, 'tre'))
s.tag('patentino F-gas', RX, 400, 460, 'gold', at=T(42, 'patentino'))
s.img('tessera', RX, 640, h=300, enter='pop', at=T(42, 'FGAS') if False else T(42, 'patentino'), until=T(44, 'Serve'))
s.tag('gas fluorurati', RX, 860, 420, 'blue', at=T(43, 'fluorurati'), until=T(44, 'Serve'))
s.img('unit_out', RX - 190, 640, h=250, enter='pop', at=T(44, 'installare'))
s.img('manometri', RX + 190, 640, h=250, enter='pop', at=T(44, 'riparare'))
s.tag('installare · riparare · smantellare', RX, 860, 780, 'gold', at=T(44, 'smantellare'))
s.punch(T(42, 'patentino')); s.punch(T(44, 'smantellare'))

s = stage('s17', 45, 47); s.bg('bg-officina')
s.img('and_27', LX, 520, h=660, enter='none', at=T(45), snd=False)
s.panel('corso + esame', [dict(label='DA', fmt='{n} €', to=450, frm=0, at=T(45, 'quattrocentocinquanta'), dur=.9, color=GOLD),
                         dict(label='A', fmt='{n} €', to=665, frm=0, at=T(45, 'seicentosessantacinque'), dur=.9, color=GREEN)],
        RX, 420, w=640, at=T(45, 'corso'), until=T(46, 'Poi'))
s.stamp('PIÙ IVA', RX, 740, 380, rot=-7, size=64, at=T(45, 'IVA'), until=T(46, 'Poi'))
s.img('calendario', RX - 130, 470, h=340, enter='pop', at=T(46, 'ogni'), until=T(47, 'Lesame') if False else T(47, 'prove'))
s.tag('quota annuale', RX + 130, 520, 400, 'blue', at=T(46, 'quota'), until=T(47, 'prove'))
tags(s, [('ricerca perdite', 'blue', T(47, 'ricerca')), ('recupero del gas', 'gold', T(47, 'recupero')), ('saldatura', 'red', T(47, 'saldatura'))], x=RX, y0=330, dy=140)
s.punch(T(45, 'seicentosessantacinque')); sfx(T(45, 'seicentosessantacinque', 1.0), 'cash-register', .3)

s = stage('s18', 48, 50); s.bg('bg-officina')
s.img('and_27', LX, 520, h=660, enter='none', at=T(48), snd=False)
s.img('clipboard', RX - 150, 500, h=380, enter='pop', at=T(48, 'registro'), until=T(50, 'Chiunque'))
s.tag('registro telematico', RX, 300, 520, 'blue', at=T(48, 'registro'), until=T(49, 'Da'))
s.tag('banca dati pubblica', RX, 300, 520, 'gold', at=T(49, 'banca'), until=T(50, 'Chiunque'))
s.img('tessera', RX + 220, 540, h=260, enter='pop', at=T(49, 'nome'), until=T(50, 'Chiunque'))
s.badge('ok', RX, 560, T(50, 'regola'), size=140)
s.tag('chiunque può controllare', RX, 820, 620, 'blue', at=T(50, 'controllare'))
s.punch(T(49, 'pubblica')); s.punch(T(50, 'controllare'))

s = stage('s19', 51, 52); s.bg('bg-officina')
s.img('and_27', LX, 520, h=660, enter='none', at=T(51), snd=False)
s.img('rilevatore', RX, 480, h=460, enter='pop', at=T(51, 'tenuta'))
s.tag('prova di tenuta', RX, 800, 460, 'gold', at=T(51, 'tenuta'), until=T(52, 'E'))
s.stamp('SE SBAGLI', RX - 340, 470, 380, rot=-8, size=64, at=T(52, 'sbagli'))
s.tag('lo scopre qualcuno', RX, 800, 520, 'red', at=T(52, 'scopre'))
s.punch(T(51, 'tenuta')); s.punch(T(52, 'sbagli'), 'shake')

# ================================ LIVELLO 4 ================================
s = stage('s20', 53, 55); s.bg('bg-salotto')
s.img('and_32', LX, 520, h=660, enter='left', at=T(53))
s.tag('livello 4', RX, 280, 340, 'blue', at=T(53, 'quattro'), until=T(54, 'Non'))
s.tag('tecnico specializzato', RX, 400, 540, 'gold', at=T(53, 'specializzato'), until=T(54, 'Non'))
s.img('unit_split', RX, 520, h=220, enter='pop', at=T(54, 'split'), until=T(55, 'Destate') if False else T(55, 'pompa'))
s.badge('no', RX + 220, 400, T(54, 'solo'), size=110, until=T(55, 'pompa'))
s.img('pompa_calore', RX, 520, h=380, enter='pop', at=T(55, 'pompa'))
s.img('sole', RX - 350, 360, h=200, enter='pop', at=T(55, 'raffreddi'))
s.img('fiocco', RX + 350, 360, h=200, enter='pop', at=T(55, 'scaldi'))
s.tag('estate: raffreddi', RX - 270, 800, 430, 'gold', at=T(55, 'raffreddi'))
s.tag('inverno: scaldi', RX + 270, 800, 400, 'blue', at=T(55, 'scaldi'))
s.punch(T(55, 'pompa'))

s = stage('s21', 56, 58); s.bg('bg-officina')
s.img('pose_gauges', LX + 60, 520, h=640, enter='left', at=T(56))
s.img('pompa_calore', RX, 460, h=380, enter='right', at=T(56, 'pompe'), until=T(57, 'Cerchi'))
s.tag('impianti più grandi', RX, 760, 520, 'gold', at=T(56, 'grandi'), until=T(57, 'Cerchi'))
s.img('rilevatore', RX - 140, 470, h=400, enter='pop', at=T(57, 'perdita'), until=T(58, 'Ogni'))
s.img('manometri', RX + 190, 480, h=300, enter='pop', at=T(57, 'pressione'), until=T(58, 'Ogni'))
s.tag('perdita invisibile', RX, 760, 480, 'red', at=T(57, 'invisibile'), until=T(58, 'Ogni'))
s.img('clipboard', RX, 470, h=400, enter='pop', at=T(58, 'documentato'))
s.tag('registro dell\'impianto', RX, 760, 520, 'blue', at=T(58, 'registro'))
s.punch(T(56, 'pompe')); s.punch(T(58, 'documentato'))

s = stage('s22', 59, 60); s.bg('bg-officina')
s.img('and_32', LX, 520, h=660, enter='left', at=T(59))
s.panel('minimo contrattuale', [dict(label='LIV. 2', value='1.650 €', color=GREY, strike=True, at=T(59, 'minimo')),
                               dict(label='LIV. 4', fmt='≈ {n} €', to=1750, frm=1650, at=T(59, 'millesettecentocinquanta'), dur=.9, color=GREEN)],
        RX, 400, w=680, at=T(59, 'minimo'))
s.box('<div class="arrow">▲</div>', RX, 680, 160, 140, at=T(59, 'millesettecentocinquanta', .9), snd='ping')
s.tag('autonomia', RX, 840, 340, 'gold', at=T(60, 'autonomia'))
s.punch(T(59, 'millesettecentocinquanta')); sfx(T(59, 'millesettecentocinquanta', .9), 'cash-register', .3)

s = stage('s23', 61, 63); s.bg('bg-tetto')
s.img('pose_van', LX + 70, 520, h=560, enter='left', at=T(61))
s.tag('il telefono suona', RX, 300, 480, 'red', at=T(61, 'telefono'), until=T(62, 'Una'))
s.img('termometro', RX + 160, 520, h=440, enter='pop', at=T(62, 'ferragosto'), until=T(63, 'E'))
s.tag('ferragosto', RX - 130, 520, 340, 'gold', at=T(62, 'ferragosto'), until=T(63, 'E'))
s.img('sole', RX, 480, h=360, enter='pop', at=T(63, 'sole'))
tags(s, [('di sera', 'blue', T(63, 'sera')), ('nei weekend', 'gold', T(63, 'weekend'))], x=RX - 380, y0=720, dy=110)
s.punch(T(61, 'suonare')); s.punch(T(63, 'sole'))

s = stage('s24', 64, 64); s.bg('bg-officina')
s.img('and_32', LX, 520, h=660, enter='left', at=T(64))
s.img('campanella', RX, 480, h=420, enter='pop', at=T(64, 'iscriviti'))
s.tag('iscriviti', RX, 780, 330, 'red', at=T(64, 'iscriviti', .1))
s.tag('mancano 2 livelli', RX, 890, 460, 'gold', at=T(64, 'mancano'))
s.punch(T(64, 'iscriviti')); sfx(T(64, 'iscriviti'), 'notification', .4)

# ================================ LIVELLO 5 ================================
s = stage('s25', 65, 67); s.bg('bg-officina')
s.img('and_37', LX, 520, h=660, enter='left', at=T(65))
s.tag('livello 5', RX, 280, 340, 'blue', at=T(65, 'cinque'), until=T(66, 'Qui'))
s.tag('responsabile tecnico', RX, 400, 520, 'gold', at=T(65, 'Responsabile'), until=T(66, 'Qui'))
s.tag('non basta saper fare', RX, 360, 560, 'red', at=T(66, 'basta'), until=T(67, 'Servono'))
s.img('certificato', RX, 500, h=380, enter='pop', at=T(67, 'diploma'))
s.tag('studi tecnici', RX - 230, 860, 360, 'blue', at=T(67, 'studi'))
s.tag('esperienza', RX + 230, 860, 300, 'gold', at=T(67, 'esperienza'))
s.punch(T(65, 'Responsabile'))

s = stage('s26', 68, 71); s.bg('bg-salotto')
s.img('pose_table', LX + 90, 520, h=560, enter='left', at=T(68))
s.stamp('FIRMA', RX, 300, 360, rot=-7, size=84, at=T(68, 'firmare'), until=T(69, 'La'))
s.img('foglio_timbro', RX, 480, h=420, enter='pop', at=T(69, 'dichiarazione'), until=T(71, 'La'))
s.tag('dichiarazione di conformità', RX, 790, 700, 'blue', at=T(69, 'dichiarazione'), until=T(70, 'Quel'))
s.badge('ok', RX + 300, 340, T(70, 'bene'), size=130, until=T(71, 'La'))
s.tag('impianto fatto bene', RX, 790, 540, 'gold', at=T(70, 'impianto'), until=T(71, 'La'))
s.img('calendario', RX, 470, h=380, enter='pop', at=T(71, 'anni'))
s.tag('la tua firma resta per anni', RX, 790, 700, 'red', at=T(71, 'firma'))
s.punch(T(68, 'firmare')); s.punch(T(69, 'dichiarazione')); s.punch(T(71, 'anni'))

s = stage('s27', 72, 75); s.bg('bg-officina')
s.img('and_37', LX, 520, h=660, enter='left', at=T(72))
s.img('and_19', RX - 150, 560, h=440, enter='pop', at=T(72, 'squadra'), until=T(73, 'Un') if False else T(74, 'E'))
s.img('and_24', RX + 150, 540, h=470, enter='pop', at=T(72, 'squadra'), until=T(74, 'E'))
s.tag('rispondi anche di chi lavora con te', RX, 850, 760, 'gold', at=T(72, 'rispondi'), until=T(73, 'Un'))
s.badge('no', RX, 330, T(73, 'errore'), size=130, until=T(74, 'E'))
s.tag('errore di un collega = tuo', RX, 850, 640, 'red', at=T(73, 'errore'), until=T(74, 'E'))
s.img('clipboard', RX - 190, 520, h=330, enter='pop', at=T(74, 'formazione'), until=T(75, 'Lo'))
s.img('certificato', RX + 190, 520, h=330, enter='pop', at=T(74, 'certificati'), until=T(75, 'Lo'))
s.tag('formazione · certificati · registri', RX, 850, 800, 'blue', at=T(74, 'registri'), until=T(75, 'Lo'))
s.img('foglio_timbro', RX - 190, 500, h=380, enter='pop', at=T(75, 'carta'))
s.img('rame_isolato', RX + 190, 520, h=320, enter='pop', at=T(75, 'rame'))
s.box('<div class="num" style="font-size:150px;color:#fff">=</div>', RX, 500, 160, 160, at=T(75, 'quanto'))
s.tag('la carta pesa quanto il rame', RX, 850, 720, 'gold', at=T(75, 'carta'))
s.punch(T(72, 'squadra')); s.punch(T(73, 'errore'), 'shake'); s.punch(T(75, 'rame'))

# ================================ LIVELLO 6 ================================
s = stage('s28', 76, 78); s.bg('bg-officina')
s.img('and_42', LX + 80, 520, h=620, enter='left', at=T(76))
s.tag('livello 6', RX, 280, 340, 'blue', at=T(76, 'sei'), until=T(77, 'Niente'))
s.tag('apri la tua ditta', RX, 400, 460, 'gold', at=T(76, 'ditta'), until=T(77, 'Niente'))
s.tag('niente più contratto', RX, 330, 520, 'red', at=T(77, 'contratto'), until=T(78, 'Un'))
s.tag('contano i clienti', RX, 460, 460, 'gold', at=T(77, 'clienti'), until=T(78, 'Un'))
s.img('termometro', RX - 170, 520, h=400, enter='pop', at=T(78, 'fresca'))
s.img('fiocco', RX + 170, 520, h=300, enter='pop', at=T(78, 'casa'))
s.tag('quanto è fresca la casa', RX, 850, 640, 'blue', at=T(78, 'fresca'))
s.punch(T(76, 'ditta')); s.punch(T(78, 'fresca'))

s = stage('s29', 79, 81); s.bg('bg-officina')
s.img('and_42', LX + 80, 520, h=620, enter='none', at=T(79), snd=False)
s.panel("tariffa all'ora", [dict(label='DA', fmt='{n} €', to=25, frm=0, at=T(79, 'venticinque'), dur=.8, color=GOLD),
                           dict(label='A', fmt='{n} €', to=60, frm=0, at=T(79, 'sessanta'), dur=.8, color=GREEN)],
        RX, 420, w=600, at=T(79, 'tariffe'), until=T(80, 'Il'))
s.panel('diritto di chiamata', [dict(label='DA', fmt='{n} €', to=30, frm=0, at=T(80, 'trenta'), dur=.8, color=GOLD),
                               dict(label='A', fmt='{n} €', to=80, frm=0, at=T(80, 'ottanta'), dur=.8, color=GREEN)],
        RX, 420, w=600, at=T(80, 'chiamata'), until=T(81, 'Sono'))
s.stamp('STIME', RX, 480, 400, rot=-6, size=96, color=GOLD, at=T(81, 'stime'))
s.tag('non cifre fisse', RX, 700, 440, 'red', at=T(81, 'fisse'))
s.punch(T(79, 'sessanta')); s.punch(T(80, 'ottanta')); s.punch(T(81, 'stime'), 'shake'); sfx(T(80, 'ottanta', .9), 'cash-register', .3)

s = stage('s30', 82, 84); s.bg('bg-officina')
s.img('and_42', LX + 80, 520, h=620, enter='none', at=T(82), snd=False)
s.img('soldi', RX, 480, h=300, enter='pop', at=T(82, 'fatturato'), until=T(83, 'Da'))
s.tag('fatturato ≠ quello che ti resta', RX, 780, 760, 'gold', at=T(82, 'resta'), until=T(83, 'Da'))
s.img('furgone', RX - 440, 440, h=240, enter='pop', at=T(83, 'furgone'), until=T(84, 'Tolgono'))
s.img('cacciaviti', RX - 150, 450, h=240, enter='pop', at=T(83, 'attrezzi'), until=T(84, 'Tolgono'))
s.img('assicurazione', RX + 150, 450, h=240, enter='pop', at=T(83, 'assicurazione'), until=T(84, 'Tolgono'))
s.img('tessera', RX + 450, 460, h=200, enter='pop', at=T(83, 'certificazioni'), until=T(84, 'Tolgono'))
s.tag('furgone', RX - 440, 650, 240, 'red', at=T(83, 'furgone'), until=T(84, 'Tolgono'))
s.tag('attrezzi', RX - 150, 650, 240, 'red', at=T(83, 'attrezzi'), until=T(84, 'Tolgono'))
s.tag('assicurazione', RX + 150, 650, 330, 'red', at=T(83, 'assicurazione'), until=T(84, 'Tolgono'))
s.tag('certificati', RX + 450, 650, 260, 'red', at=T(83, 'certificazioni'), until=T(84, 'Tolgono'))
s.img('manometri', RX - 130, 470, h=300, enter='pop', at=T(84, 'strumenti'))
s.img('calendario', RX + 190, 470, h=300, enter='pop', at=T(84, 'ferie'))
s.badge('no', RX + 190, 330, T(84, 'fai'), size=120)
s.tag('strumenti da rinnovare, ferie che non fai', RX, 850, 880, 'red', at=T(84, 'strumenti'))
s.punch(T(82, 'fatturato')); s.punch(T(84, 'ferie'), 'shake')

s = stage('s31', 85, 87); s.bg('bg-tetto')
s.img('and_42', LX + 80, 520, h=620, enter='left', at=T(85))
s.tag('costo nascosto', RX, 300, 440, 'red', at=T(85, 'costo'))
s.tag('la stagionalità', RX, 430, 440, 'gold', at=T(86, 'stagionalità'))
s.img('sole', RX, 640, h=300, enter='pop', at=T(87, 'estate'))
s.tag('re del condominio', RX, 880, 480, 'gold', at=T(87, 're'))
s.punch(T(85, 'costo')); s.punch(T(87, 'estate'))

s = stage('s32', 88, 88); s.bg('bg-notte')
s.img('pose_sofa', CX - 100, 520, h=500, enter='pop', at=T(88))
s.img('fiocco', 1520, 400, h=300, enter='right', at=T(88, 'inverno') if False else T(88, 'resti'))
s.tag("d'inverno: aspetti", CX - 100, 820, 560, 'blue', at=T(88, 'resti'))
s.punch(T(88, 'resti'))

s = stage('s33', 89, 89); s.bg('bg-tetto')
s.img('and_42', LX + 80, 520, h=620, enter='left', at=T(89))
s.img('sole', RX - 60, 460, h=320, enter='pop', at=T(89, 'caldo'))
s.box('<div class="arrow">▲</div>', RX + 260, 470, 200, 180, at=T(89, 'tanto'), snd='ping')
s.img('soldi', RX - 60, 760, h=200, enter='pop', at=T(89, 'Guadagni'))
s.punch(T(89, 'caldo'))

s = stage('s34', 90, 91); s.bg('bg-notte')
s.img('fiocco', CX - 520, 460, h=360, enter='left', at=T(90, 'freddo'))
s.tag('mesi calmi', CX - 520, 760, 360, 'blue', at=T(90, 'calmi'))
s.img('foglio_timbro', CX + 300, 470, h=420, enter='right', at=T(91, 'firma'))
s.tag('ogni intervento: la tua firma', CX + 300, 790, 700, 'gold', at=T(91, 'intervento'))
s.punch(T(90, 'calmi')); s.punch(T(91, 'firma'))

# ================================ FINAL ================================
s = stage('s35', 92, 96); s.bg('bg-tetto')
s.img('and_19', LX, 520, h=660, enter='left', at=T(92))
s.img('sole', RX, 420, h=320, enter='pop', at=T(92, 'luglio'), until=T(94, 'Non'))
s.tag('il ragazzo non sa ancora', RX, 740, 640, 'blue', at=T(93, 'sa'), until=T(94, 'Non'))
s.stamp('INVISIBILE', RX, 470, 560, rot=-6, size=96, at=T(94, 'invisibile'), until=T(95, 'Se'))
s.badge('ok', RX, 380, T(95, 'bene'), size=140, until=T(96, 'Se'))
s.tag('se fa bene: nessuno ci pensa', RX, 780, 680, 'gold', at=T(95, 'bene'), until=T(96, 'Se'))
s.img('termometro', RX, 480, h=430, enter='pop', at=T(96, 'estate'))
s.tag("un'estate intera ricorderà il suo nome", RX, 800, 860, 'red', at=T(96, 'nome'))
s.punch(T(92, 'tetto')); s.punch(T(94, 'invisibile'), 'shake'); s.punch(T(96, 'nome'))

s = stage('s36', 97, 100); s.bg('bg-officina')
s.img('and_19', LX - 120, 540, h=480, enter='left', at=T(97, 'Dal'))
s.box('<div class="num" style="font-size:150px;color:#ffd166">→</div>', CX - 100, 480, 220, 180, at=T(97, 'passano'))
s.img('and_42', CX + 160, 520, h=560, enter='right', at=T(97, 'ditta'))
s.tag('passano anni', CX - 100, 800, 400, 'gold', at=T(97, 'anni'), until=T(98, 'Ha'))
s.img('unit_split', RX + 190, 360, h=200, enter='pop', at=T(98, 'aria'), until=T(99, 'Un'))
s.img('fiocco', RX + 190, 640, h=260, enter='pop', at=T(98, 'fresca'), until=T(99, 'Un'))
s.tag('un mestiere che vende aria fresca', CX, 880, 780, 'blue', at=T(98, 'mestiere'), until=T(99, 'Un'))
s.tag('nessuno lo nota, finché funziona', CX, 880, 780, 'gold', at=T(99, 'finché'), until=T(100, 'E'))
s.img('sole', RX + 190, 520, h=380, enter='pop', at=T(100, 'caldo'))
s.stamp('PAGA CON IL CALDO', CX, 880, 700, rot=-4, size=56, at=T(100, 'paga'))
s.punch(T(97, 'anni')); s.punch(T(100, 'caldo'), 'shake')

s = stage('s37', 101, 103); s.bg('bg-tetto')
s.img('head_42', LX, 520, h=640, enter='left', at=T(101), drift=0.0)
s.img('campanella', RX + 400, 470, h=320, enter='pop', at=T(101, 'iscriviti'))
s.tag('iscriviti al canale', RX - 150, 320, 520, 'red', at=T(101, 'iscriviti'))
s.tag('a che livello sei?', RX - 150, 470, 520, 'gold', at=T(102, 'livello'))
s.tag('scrivilo nei commenti', RX - 150, 620, 560, 'blue', at=T(102, 'commenti'))
s.tag('quale mestiere vuoi vedere dopo?', RX - 150, 770, 780, 'gold', at=T(103, 'mestiere'))
s.punch(T(101, 'iscriviti'), 'zoom'); sfx(T(101, 'iscriviti'), 'notification', .4)

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
        if cur and cur_len + 1 + len(word) > 40: flush()
        cur.append((word, em, t0))
        if re.search(r'[.,?!]$', word) and len(' '.join(x[0] for x in cur)) >= 9: flush()
    flush()
    merged = []
    for c in chunks:
        if merged and len(c) == 1 and len(c[0][0]) <= 4 and len(' '.join(x[0] for x in merged[-1] + c)) <= 40:
            merged[-1] += c
        else:
            merged.append(c)
    res = []
    for i, c in enumerate(merged):
        ts = c[0][2] if i else bt.s
        te = merged[i + 1][0][2] if i + 1 < len(merged) else bt.e
        res.append((max(ts - 0.04, bt.s) if i else bt.s, te, c))
    return res

KEYS = {norm(x) for x in """tetto luglio caldo rame firmare sbagli HVAC frigorista Iscriviti apprendista stipendio percentuale basso sottotetto gas refrigerante vietato
installatore vuoto minimo milleseicentocinquanta lordi tasse tredici patentino certificazione fluorurati quattrocentocinquanta seicentosessantacinque IVA registro pubblica
perdite specializzato pompe calore millesettecentocinquanta autonomia telefono ferragosto firma dichiarazione conformità squadra ditta clienti fresca venticinque sessanta
trenta ottanta stime fatturato costo nascosto stagionalità estate freddo invisibile commenti livello cartelli confine piegi unità esterna interna""".split()}
CAPMARK = {}
for n, bt in enumerate(BEATS, 1):
    toks = bt.text.split(' ')
    marks, c = [], 0
    for w in toks:
        k = norm(w) in KEYS and c < 2
        if k: c += 1
        marks.append(k)
    CAPMARK[n] = marks
    assert len(marks) == len(bt.words), n

# ------------------------------------------------------------------ CSS
CSS = """
  #root { position:absolute; inset:0; font-family:'Montserrat',sans-serif; color:#fff; }
  .stage { position:absolute; inset:0; transform-origin:50% 45%; }
  .item { position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .item img.pic { width:100%; height:100%; object-fit:contain; display:block; filter:url(#boil-STAGE) drop-shadow(0 16px 24px rgba(0,0,0,.45)); }
  .bx { position:absolute; left:0; top:0; transform-origin:0 0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .bx:has(> .gtag) { flex-direction:row; }
  .item img.pic.fade { -webkit-mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); }
  .bgimg { position:absolute; left:0; top:0; width:1920px; height:1080px; object-fit:cover; filter:brightness(.72) saturate(.95); }
  .bgshade { position:absolute; inset:0; background:linear-gradient(180deg,rgba(8,8,40,.40),rgba(8,8,40,.05) 38%,rgba(8,8,40,.60)); }
  .halo { width:100%; height:100%; border-radius:50%; }
  .num { font-weight:900; line-height:1; letter-spacing:-.02em; text-align:center; white-space:nowrap; text-shadow:0 0 40px rgba(255,255,255,.18); }
  .sub { font-weight:800; letter-spacing:.08em; text-align:center; color:#cdd3ff; margin-top:6px; }
  .stamp { font-family:'Playfair Display',serif; border:7px solid; border-radius:14px; padding:6px 22px; font-weight:900; letter-spacing:.07em; text-align:center; background:rgba(11,11,46,.5); white-space:nowrap; box-shadow:0 0 30px rgba(255,77,109,.25); }
  .gtag { display:inline-flex; align-items:center; gap:12px; padding:13px 30px; border-radius:999px; font-weight:800; font-size:40px; white-space:nowrap;
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
  svg.conn { position:absolute; inset:0; width:1920px; height:1080px; z-index:2; overflow:visible; }
  svg.conn path { fill:none; stroke-width:7; stroke-linecap:round; stroke-dasharray:1; stroke-dashoffset:1; }
  .hg { position:absolute; top:140px; width:520px; }
  .hlab { font-weight:800; font-size:28px; letter-spacing:.08em; color:#b8bdf0; margin-bottom:8px; white-space:nowrap; }
  .htr { height:18px; border-radius:99px; background:rgba(23,26,99,.8); border:2px solid rgba(111,123,255,.55); overflow:hidden; }
  .hfill { width:100%; height:100%; border-radius:99px; transform-origin:left center; }
  .cap { position:absolute; left:0; width:1920px; text-align:center; font-weight:800; font-size:60px; line-height:1.15; text-transform:uppercase; white-space:nowrap; text-shadow:0 5px 16px rgba(0,0,0,.7); z-index:30; }
  .cap b.k { font-weight:900; display:inline-block; }
  .rl-line { position:absolute; left:160px; top:78px; width:1600px; height:6px; border-radius:3px; background:rgba(150,160,255,.35); }
  .rl-fill { position:absolute; left:160px; top:78px; height:6px; border-radius:3px; background:linear-gradient(90deg,#6f7bff,#ff4d6d); width:0; box-shadow:0 0 14px rgba(255,77,109,.6); }
  .rl-tick { position:absolute; top:68px; width:4px; height:26px; border-radius:2px; background:rgba(180,188,255,.55); }
  .rl-num { position:absolute; top:108px; width:80px; margin-left:-40px; text-align:center; font-weight:800; font-size:28px; color:#aab0ee; }
  .rl-dot { position:absolute; top:59px; width:44px; height:44px; margin-left:-22px; border-radius:50%; background:#ff4d6d; border:4px solid #fff; box-shadow:0 0 28px #ff4d6d; }
  .rl-lab { position:absolute; top:8px; width:300px; margin-left:-150px; text-align:center; }
"""

def build_stage(S, prev_end_overlap=True):
    dur = round(min(S.t1 - S.t0 + OVER, TOTAL - S.t0), 3)
    ex_end = round(S.t1 - S.t0, 3)       # fin « logique » du décor, relative
    html, js = [], []
    sid = S.id
    html.append(f'<svg width="0" height="0" style="position:absolute"><filter id="boil-{sid}" x="-3%" y="-3%" width="106%" height="106%"><feTurbulence id="boilt-{sid}" type="fractalNoise" baseFrequency="0.018 0.022" numOctaves="2" seed="1" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.4"/></filter></svg>')
    html.append(f'<div class="stage clip" data-layout-allow-occlusion id="{sid}-stage" data-start="0" data-duration="{dur}" data-track-index="1"><div class="stage" id="{sid}-pun"><div class="stage" id="{sid}-cam">')
    if getattr(S, 'bgname', None): html.append(f'<img class="bgimg" data-layout-allow-occlusion src="assets/img/{S.bgname}.jpg" alt=""><div class="bgshade"></div>')
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
        html.append(f'<svg class="conn clip" id="{sid}-svg" data-start="0" data-duration="{dur}" data-track-index="2" viewBox="0 0 1920 1080">')
        for p in S.paths:
            rel = round(p['at'] - S.t0, 3)
            gl = f'filter:drop-shadow(0 0 7px {p["color"]})'
            X1, Y1, X2, Y2, BD = p['pts']
            X1, X2 = X1, X2
            Y1, Y2 = Y1, Y2
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
        MAPX = lambda x: x
        MAPY = lambda y: y
        if it['k'] == 'img':
            iw, ih = SIZE[it['name']]
            if it['h']: hh = it['h'] * K_IMG; ww = hh * iw / ih
            else: ww = it['w'] * K_IMG; hh = ww * ih / iw
            fade = ' fade' if it['name'].startswith('head_') else ''
            inner = f'<img class="pic{fade}" id="{iid}-p" src="assets/img/{it["name"]}.png" alt="">'
        else:
            bw0, bh0 = it['w'], it['h']
            ww, hh = bw0 * K_BOX, bh0 * K_BOX
            inner = f'<div class="bx" style="width:{bw0}px;height:{bh0}px;transform:scale({K_BOX})">{it["html"]}</div>'
        if hh > ZB - S.zt:
            f_ = (ZB - S.zt) / hh; ww, hh = ww * f_, hh * f_
        cx2, cy2 = MAPX(it['cx']), MAPY(it['cy'])
        cy2 = min(max(cy2, S.zt + hh / 2), ZB - hh / 2)
        left = min(max(cx2 - ww / 2, 70), W - 70 - ww)
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
            ch = it['k'] == 'img' and it['name'].startswith(('and_', 'head_', 'pose_'))
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
        elif snd is True and it['k'] == 'img' and e in ('left', 'right') and not it['name'].startswith(('and_', 'head_', 'pose_')): sfx(it['at'], 'whoosh-short', .24)
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

# règle des 6 niveaux (composition globale) -------------------------------------------------
X0, XS = 160, 320
tk = ''.join(f'<div class="rl-tick" style="left:{X0 + i * XS - 2}px"></div>' for i in range(6))
nums = ''.join(f'<div class="rl-num" style="left:{X0 + i * XS}px">{i + 1}</div>' for i in range(6))
rul_js = []
marks = [(T(16, 'uno', -.1), 0, .1), (T(30, 'due', -.3), 1, .8), (T(42, 'tre', -.3), 2, .8), (T(53, 'quattro', -.3), 3, .8), (T(65, 'cinque', -.3), 4, .8), (T(76, 'sei', -.3), 5, .8)]
rul_js.append(f'var o={{v:0}};function up(){{var v=o.v;var x={X0}+v*{XS};document.getElementById("rl-dot").style.left=x+"px";'
              f'document.getElementById("rl-fill").style.width=(v*{XS})+"px";document.getElementById("rl-lab").style.left=Math.min(Math.max(x,260),1660)+"px";'
              f'document.getElementById("rl-lab").firstChild.lastChild.nodeValue="LIVELLO "+(Math.round(v)+1);}}')
start_t = T(16, 'uno', -.5)
rul_t1 = next(s_ for s_ in STAGES if s_.id == 's35').t0 - .1
rul_js.append(f'tl.fromTo("#rl",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,ease:"expo.out"}},{start_t:.3f});')
for (t, v, d) in marks[1:]:
    rul_js.append(f'tl.to(o,{{v:{v},duration:{d},ease:"power3.inOut",onUpdate:up}},{t:.3f});')
sfx(start_t, 'whoosh', .22)
for (t, v, d) in marks[1:]:
    sfx(t + d, 'ping', .22)
rul_js.append(f'tl.to("#rl",{{opacity:0,duration:.4,ease:"power2.in"}},{rul_t1:.3f});')
ruler = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="rul" data-width="{W}" data-height="{H}">
    <div id="rl" class="clip" data-start="0" data-duration="{round(TOTAL, 3)}" data-track-index="1" style="position:absolute;inset:0;z-index:25">
      <div class="rl-line"></div><div class="rl-fill" id="rl-fill"></div>{tk}{nums}
      <div class="rl-dot" id="rl-dot" style="left:{X0}px"></div>
      <div class="rl-lab" id="rl-lab" style="left:{X0}px"><div class="gtag red"><i class="dot"></i>LIVELLO 1</div></div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in rul_js)}
    window.__timelines["rul"] = tl;
  </script>
</template>
"""
open(os.path.join(OUT, 'compositions', 'rul.html'), 'w', encoding='utf-8').write(ruler)

# tableau de bord (jauges qualitatives : tendances du récit, pas des données chiffrées) -----------------
hud_t0, hud_t1 = start_t + .2, rul_t1
GA = [('stip', 'STIPENDIO', 'linear-gradient(90deg,#ffd166,#ff9e4d)'), ('resp', 'RESPONSAB.', 'linear-gradient(90deg,#3ddc97,#b5f06a)'), ('stress', 'STRESS', 'linear-gradient(90deg,#ff6b6b,#ff3d7f)')]
EV = {'stip': [(hud_t0, .15), (T(36, 'milleseicentocinquanta'), .30), (T(59, 'millesettecentocinquanta'), .45), (T(79, 'sessanta'), .70)],
      'resp': [(hud_t0, .05), (T(30, 'due'), .20), (T(42, 'tre'), .40), (T(53, 'quattro'), .55), (T(65, 'Responsabile'), .80), (T(76, 'ditta'), 1.0)],
      'stress': [(hud_t0, .10), (T(25, 'tocchi'), .20), (T(52, 'sbagli'), .40), (T(61, 'telefono'), .60), (T(73, 'errore'), .80), (T(85, 'costo'), .95)]}
hud_js, hud_html = [], []
for k, (g, lab, grad) in enumerate(GA):
    x = 160 + k * 600
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
hosts.append(f'      <div id="rul" class="clip" data-composition-id="rul" data-composition-src="compositions/rul.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
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
      <audio id="bed" src="assets/audio/bed_long.wav" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-volume="0.55"></audio>
      <audio id="music" src="assets/audio/music_long.wav" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-volume="1.15"></audio>
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
      tl.to("#tint", {{ backgroundColor: "rgba(50,100,255,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(16, 'uno', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(20,200,170,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(30, 'due', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(255,170,50,.11)", duration: 1.2, ease: "sine.inOut" }}, {T(42, 'tre', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(255,60,90,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(53, 'quattro', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(150,90,230,.13)", duration: 1.2, ease: "sine.inOut" }}, {T(65, 'cinque', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(255,200,80,.11)", duration: 1.2, ease: "sine.inOut" }}, {T(76, 'sei', -.2):.2f});
      tl.to("#tint", {{ backgroundColor: "rgba(120,140,200,.1)", duration: 1.5, ease: "sine.inOut" }}, {T(92, 'tetto', -.5):.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)
open(os.path.join(OUT, 'hyperframes.json'), 'w').write('{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",\n  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},\n  "media": {"autoProxy": true}\n}\n')
open(os.path.join(OUT, 'meta.json'), 'w').write('{"id": "cyber-v1", "name": "Il tuo primo anno come analista di cybersecurity (9:16)"}')
print('ok cyb:', len(STAGES), 'décors,', len(SFXLOG), 'effets,', len(audio), 'audio')
