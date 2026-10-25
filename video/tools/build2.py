"""v2 — « La tua vita dopo 15 anni da camionista », 9:16, style des vidéos de référence.
Usage (depuis video/) :  python3 tools/build2.py     →  video/v2/
Nouveautés : sous-titres en fragments d'une ligne calés mot à mot sur la voix, éléments qui
apparaissent au mot dit, fond aurore + grille, panneaux « verre » avec étiquettes, effets sonores.
"""
import os, re, json, shutil, difflib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'v2')
CUT = os.path.join(ROOT, 'assets', 'cut')
SFXSRC = os.path.join(ROOT, '..', '.claude', 'skills', 'media-use', 'audio', 'assets', 'sfx')
VOICE = '/root/.claude/uploads/91729ddc-3274-50e3-9f11-8e52419e14ce/280557de-Generated_Audio_October_24_2026_-_5_04PM.wav'
SCRIPT = os.path.join(ROOT, '..', 'scripts', 'camionista-short.txt')
SRT = os.path.join(ROOT, '..', 'scripts', 'camionista-scenes.srt')
TOTAL = 98.7

W, H = 1080, 1920
CX, CY = 540, 780
CAP_Y = 1300
RED, GOLD, GREEN, INK, GREY = '#ff4d6d', '#ffd166', '#3ddc97', '#ffffff', '#9aa0d8'

# ------------------------------------------------------------------ temps
def parse_srt(path):
    out = []
    for blk in open(path, encoding='utf-8').read().strip().split('\n\n'):
        l = blk.split('\n')
        a, b = l[1].split(' --> ')
        f = lambda s: int(s[:2]) * 3600 + int(s[3:5]) * 60 + int(s[6:8]) + int(s[9:]) / 1000
        out.append((f(a), f(b), ' '.join(l[2:])))
    return out

SC = parse_srt(SRT)

# alignement mot à mot : texte du script  <->  mots reconnus par Whisper
NUMW = set('ventitré tremila millecinquecento duemila quarantasei venticinque trenta quindici dieci cinque uno due nove novanta quarantacinque millequattrocento trentotto'.split())
norm = lambda t: re.sub(r"[^\w]", "", t.lower().replace("l'", "l"))
WW = json.load(open(os.path.join(HERE, 'words.json')))
swords = [w for l in open(SCRIPT, encoding='utf-8') if l.strip() for w in l.split()]
st = ['NUM' if norm(w) in NUMW else norm(w) for w in swords]
wt = ['NUM' if (re.fullmatch(r'\d+[.,]?', w[0])) else norm(w[0]) for w in WW]
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

# ------------------------------------------------------------------ assets
for d in ('assets/img', 'assets/sfx', 'compositions'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
SIZE = {}
for f in os.listdir(CUT):
    im = Image.open(os.path.join(CUT, f)); im.thumbnail((1100, 1100))
    im.save(os.path.join(OUT, 'assets', 'img', f), optimize=True); SIZE[f[:-4]] = im.size
shutil.copy(VOICE, os.path.join(OUT, 'assets', 'voce.wav'))
SFXDUR = {k: v['duration'] for k, v in json.load(open(os.path.join(SFXSRC, 'manifest.json'))).items()}
for f in os.listdir(SFXSRC):
    if f.endswith('.mp3') or f == 'CREDITS.md':
        shutil.copy(os.path.join(SFXSRC, f), os.path.join(OUT, 'assets', 'sfx', f))

# ------------------------------------------------------------------ DSL
class Beat:
    def __init__(self, n, cap, items):
        self.n, self.cap, self.items = n, cap, items
        self.s, self.e, text = SC[n - 1]
        self.text = text

def img(name, dx=0, dy=0, h=None, w=None, enter='pop', at=None, delay=0.0, rot=0, z=2, drift=0.03, sfx=None):
    return dict(k='img', name=name, dx=dx, dy=dy, h=h, w=w, enter=enter, at=at, delay=delay, rot=rot, z=z, drift=drift, sfx=sfx)

def box(html, dx=0, dy=0, w=600, h=300, enter='pop', at=None, delay=0.0, rot=0, z=3, cls='', sfx=None):
    return dict(k='box', html=html, dx=dx, dy=dy, w=w, h=h, enter=enter, at=at, delay=delay, rot=rot, z=z, cls=cls, sfx=sfx)

def num(text, sub='', dx=0, dy=0, w=800, h=300, size=190, color=GOLD, **kw):
    size = min(size, int(w / (len(text) * 0.66)))
    s = f'<div class="num" style="font-size:{size}px;color:{color}">{text}</div>'
    if sub:
        s += f'<div class="sub" style="font-size:44px">{sub}</div>'
    kw.setdefault('sfx', 'pop')
    return box(s, dx, dy, w, h, **kw)

def stamp(text, dx=0, dy=0, w=620, h=140, rot=-8, size=62, color=RED, **kw):
    kw.setdefault('sfx', 'impact-bass-1')
    return box(f'<div class="stamp" style="font-size:{size}px;color:{color};border-color:{color}">{text}</div>', dx, dy, w, h, rot=rot, **kw)

def tag(text, dx=0, dy=0, w=520, color='blue', **kw):
    kw.setdefault('sfx', 'pop')
    return box(f'<div class="gtag {color}"><i class="dot"></i>{text}</div>', dx, dy, w, 96, **kw)

def panel(title, rows, dx=0, dy=0, w=760, **kw):
    rh = 124
    h = 118 + rh * len(rows) + 36
    r = ''.join(
        f'<div class="row"><span class="rl">{l}</span><span class="rv{" strike" if s else ""}" style="color:{c}">{v}</span></div>'
        for (l, v, c, s) in [(*x, False) if len(x) == 3 else x for x in rows])
    kw.setdefault('sfx', 'pop')
    return box(f'<div class="glass"><div class="gtag blue small"><i class="dot"></i>{title}</div>{r}</div>', dx, dy, w, h, **kw)

def tiles(letters, dx=0, dy=0, w=900, **kw):
    t = ''.join(f'<div class="tile" style="animation-delay:{i}"><b>{c}</b></div>' for i, c in enumerate(letters))
    kw.setdefault('sfx', 'click-soft')
    return box(f'<div class="tiles">{t}</div>', dx, dy, w, 130, **kw)

def halo(dx=0, dy=0, size=700, color='rgba(120,90,255,.45)'):
    return box(f'<div class="halo" style="background:radial-gradient(circle,{color} 0%,transparent 68%)"></div>', dx, dy, size, size, enter='none', z=1, sfx=None)

# ------------------------------------------------------------------ storyboard
B = []
A = B.append
A(Beat(1, 'Hai [[ventitré]] anni.', [
    halo(170, 40, 760),
    img('marco23_full', dx=170, h=800, enter='none'),
    num('23', 'ANNI', dx=-215, dy=-40, w=500, h=420, size=300, enter='none', sfx=None)]))
A(Beat(2, 'Hai speso oltre [[tremila euro]] per patente e CQC.', [
    img('patente', dx=-260, dy=-330, h=230, rot=-8, enter='left', sfx='whoosh-short'),
    img('cqc', dx=260, dy=-300, h=230, rot=7, enter='right', at='CQC', sfx='whoosh-short'),
    panel('costi iniziali', [('PATENTE C', '≈ 1.200 €', INK), ('CQC · 140 ORE', '≈ 2.400 €', INK), ('TOTALE', '> 3.000 €', RED)],
          dx=0, dy=170, w=800, at='speso')]))
A(Beat(3, 'Davanti a te, un [[camion]] e la strada.', [
    box('<div class="road"><div class="dash"></div></div>', 0, 250, 1500, 150, enter='none', z=1, cls='roadbox', sfx=None),
    img('truck_new', dx=0, dy=-20, w=1000, enter='right', sfx='whoosh', drift=0.04)]))
A(Beat(4, '[[Quindici anni]] dopo, cosa ti resta davvero?', [
    tag('15 anni dopo', dx=0, dy=-420, w=560, color='red'),
    img('marco23_head', dx=-235, dy=10, h=520, enter='left', sfx='whoosh-short'),
    img('marco38_head', dx=235, dy=10, h=520, enter='right', at='cosa', sfx='whoosh-short'),
    box('<div class="num" style="font-size:150px;color:#ff4d6d">?</div>', 0, 10, 160, 200, enter='pop', at='resta', sfx='pop')]))
A(Beat(5, 'Anno [[uno]]. Autista neoassunto.', [
    halo(0, 60, 760),
    img('marco23_full', h=780, enter='up', sfx='whoosh-short')]))
A(Beat(6, 'Prendi circa [[millecinquecento euro]] lordi al mese.', [
    img('marco23_full', dx=-300, dy=40, h=660, enter='left'),
    panel('stipendio', [('LORDO AL MESE', '≈ 1.500 €', GOLD)], dx=200, dy=-150, w=560, at='circa'),
    img('soldi', dx=200, dy=190, h=240, enter='pop', at='euro', sfx='pop')]))
A(Beat(7, 'Il resto lo fanno [[trasferte]] e [[straordinari]].', [
    img('truck_new', dx=0, dy=-280, w=720, enter='left', sfx='whoosh-short'),
    tag('trasferte', dx=0, dy=-30, w=520, color='red', at='trasferte'),
    tiles('LMMGVSD', dx=0, dy=140, w=900, at='straordinari'),
    tag('+ straordinari', dx=0, dy=290, w=560, color='gold', at='straordinari', delay=0.4)]))
A(Beat(8, 'La tua casa, adesso, è una [[cabina]].', [
    img('cab_interior', w=820, dy=-30, enter='pop', drift=0.05),
    tag('la tua casa', dx=0, dy=400, w=520, color='red', at='casa')]))
A(Beat(9, 'Anno [[cinque]]. Patente CE, tratte lunghe.', [
    img('marco28_full', dx=-260, h=780, enter='left', sfx='whoosh-short'),
    img('patenteCE', dx=250, dy=-210, h=280, rot=7, enter='right', at='CE', sfx='whoosh-short'),
    img('truck_new', dx=210, dy=260, w=540, enter='right', at='tratte', sfx='whoosh')]))
A(Beat(10, 'Il minimo contrattuale sale a circa [[duemila euro]] lordi.', [
    img('marco28_full', dx=-320, dy=40, h=700, enter='left'),
    panel('stipendio lordo', [('ANNO 1', '1.500 €', GREY, True), ('ANNO 5', '≈ 2.000 €', GREEN)],
          dx=190, dy=-60, w=620, at='contrattuale')]))
A(Beat(11, 'Poi arriva la [[diaria]], fino a [[quarantasei euro]] al giorno.', [
    tag('la diaria', dx=0, dy=-390, w=480, color='gold'),
    panel('diaria', [('FINO A', '46 € / giorno', GOLD)], dx=0, dy=-130, w=800, at='arriva'),
    img('soldi', dx=0, dy=250, h=380, enter='up', at='fino', sfx='pop')]))
A(Beat(12, '[[Non è stipendio.]] Ma ti fa arrivare a fine mese.', [
    img('portafoglio', dx=0, dy=-40, w=780, enter='up'),
    stamp('NON È STIPENDIO', dx=0, dy=200, w=860, h=150, rot=-6, at='stipendio', size=66)]))
A(Beat(13, 'Impari il [[tachigrafo]].', [
    img('tachigrafo', w=880, dy=-20, enter='pop', drift=0.05),
    tag('il tachigrafo', dx=0, dy=330, w=520, color='blue', at='tachigrafo')]))
A(Beat(14, '[[Nove ore]] di guida, non una di più.', [
    box('<div class="ring"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="ring-bg"/>'
        '<circle id="ringfill" cx="100" cy="100" r="86" class="ring-fg" transform="rotate(-90 100 100)"/></svg>'
        '<div class="ringtxt"><span class="num" style="font-size:210px;color:#ffd166">9</span>'
        '<span class="sub" style="font-size:60px">ORE AL GIORNO</span></div></div>', 0, -20, 640, 640, enter='pop', sfx='pop'),
    tag('limite di guida', dx=0, dy=-430, w=540, color='red', at='Nove')]))
A(Beat(15, 'Se sgarri, la [[multa]] arriva.', [
    img('multa', dx=0, dy=-50, h=640, enter='shake', rot=-6, sfx='error'),
    stamp('MULTA', dx=150, dy=230, w=520, h=150, rot=-10, at='arriva', size=80)]))
A(Beat(16, 'Anno [[dieci]]. Sei un veterano.', [
    halo(0, 60, 760),
    img('marco33_full', h=780, enter='up', sfx='whoosh-short')]))
A(Beat(17, 'Gli scatti di anzianità valgono [[venticinque, trenta euro]] al mese.', [
    img('marco33_full', dx=-320, dy=40, h=700, enter='left'),
    panel('scatti di anzianità', [('AL MESE', '+25–30 €', GREEN)], dx=190, dy=-80, w=620, at='scatti')]))
A(Beat(18, 'Ogni [[due anni]].', [
    img('calendario', dy=-30, h=640, enter='pop', sfx='pop'),
    tag('ogni 2 anni', dx=0, dy=340, w=520, color='red', at='due')]))
A(Beat(19, 'Dopo dieci anni sei [[bravissimo]].', [
    halo(0, 60, 760, 'rgba(255,209,102,.35)'),
    img('marco33_full', h=780, enter='pop', sfx='pop'),
    box('<div class="spark">★</div>', -250, -250, 140, 140, enter='pop', at='bravissimo', sfx='sparkle'),
    box('<div class="spark s2">★</div>', 270, -120, 110, 110, enter='pop', at='bravissimo', delay=.15),
    box('<div class="spark">★</div>', 230, 260, 90, 90, enter='pop', at='bravissimo', delay=.3)]))
A(Beat(20, 'In busta paga, [[quasi non si vede]].', [
    box('<div class="paper"><div class="ph">BUSTA PAGA</div>'
        '<div class="pl"></div><div class="pl s"></div><div class="pl"></div><div class="pl s"></div>'
        '<div class="hl"><span>aumento anzianità</span><b>+ 30 €</b></div><div class="pl"></div></div>',
        0, -30, 760, 700, enter='up', sfx='whoosh-short')]))
A(Beat(21, 'Ogni [[due settimane]], novanta ore di guida al massimo.', [
    tag('limite massimo', dx=0, dy=-330, w=540, color='red'),
    num('90 h', 'OGNI 2 SETTIMANE', dx=0, dy=-110, w=900, h=420, size=230, color=GOLD, at='novanta'),
    box('<div class="bar"><div id="barfill" class="barfill"></div></div>', 0, 190, 860, 70, enter='up', at='novanta', delay=.2, sfx=None)]))
A(Beat(22, 'Il riposo lungo, [[quarantacinque ore]], lo fai fuori dal camion.', [
    img('marco33_chair', dx=140, dy=70, h=700, enter='up'),
    num('45 h', 'DI RIPOSO', dx=-290, dy=-250, w=520, h=360, size=170, color=GREEN, enter='left', at='quarantacinque'),
    img('truck_new', dx=-250, dy=190, w=380, enter='pop', at='camion', sfx='pop'),
    box('<div class="cross">✕</div>', -250, 190, 150, 150, enter='pop', at='camion', delay=.15, z=6, sfx=None)]))
A(Beat(23, 'Spesso, [[lontano da casa]].', [
    img('marco33_chair', dx=0, dy=90, h=640, enter='none'),
    tag('lontano da casa', dx=0, dy=-330, w=700, color='red', at='lontano')]))
A(Beat(24, 'Tuo figlio cresce nelle [[videochiamate]].', [
    img('marco33_phone', dx=-240, dy=60, h=620, enter='left', sfx='whoosh-short'),
    box('<div class="phone"><img class="kid" src="assets/img/figlio.png"></div>', 270, -30, 330, 600, enter='right', at='figlio', sfx='notification'),
    tag('videochiamata', dx=270, dy=-400, w=520, color='blue', at='videochiamate')]))
A(Beat(25, 'Anno [[quindici]]. Il bivio.', [
    img('marco38_full', dx=-250, h=760, enter='left', sfx='whoosh-short'),
    img('bivio', dx=225, dy=40, h=580, enter='right', at='bivio', sfx='pop')]))
A(Beat(26, 'Continuare da [[dipendente]], o comprare il camion e diventare [[padroncino]].', [
    box('<div class="opt"><div class="otitle">DIPENDENTE</div><img src="assets/img/truck_worn.png"></div>', 0, -195, 760, 320, enter='left', sfx='whoosh-short'),
    box('<div class="or">OPPURE</div>', 0, 5, 340, 90, enter='pop', at='comprare', sfx='pop'),
    box('<div class="opt gold"><div class="otitle">PADRONCINO</div><img class="keys" src="assets/img/chiavi.png"></div>', 0, 215, 760, 320, enter='right', at='padroncino', sfx='whoosh-short')]))
A(Beat(27, 'Il [[fatturato]] sale. L\'[[utile]], molto meno.', [
    box('<div class="chart"><div class="col"><div id="bar1" class="b gr"></div><div class="lbl">FATTURATO</div></div>'
        '<div class="col"><div id="bar2" class="b rd"></div><div class="lbl">UTILE</div></div></div>', 0, -10, 860, 700, enter='up', sfx='whoosh-short')]))
A(Beat(28, 'Le stime vanno da [[millequattrocento]] a [[tremila euro]].', [
    panel('padroncino · stima', [('NETTO AL MESE', '1.400 – 3.000 €', GOLD)], dx=0, dy=-90, w=900, at='stime'),
    img('soldi', dx=0, dy=250, h=280, enter='up', at='tremila', sfx='pop')]))
A(Beat(29, '[[Netti]], al mese.', [
    num('1.400 – 3.000 €', '', dx=0, dy=-140, w=1000, h=260, size=112, color=GOLD, enter='none', sfx=None),
    stamp('NETTI', dx=-150, dy=130, w=520, h=170, rot=-8, size=100, at='Netti'),
    stamp('AL MESE', dx=160, dy=290, w=620, h=170, rot=6, size=84, color=GREEN, at='mese')]))
A(Beat(30, '[[Gasolio]], [[assicurazione]] e [[rate]] le paghi tu.', [
    img('pompa', dx=-250, dy=-170, h=380, enter='left', at='Gasolio', sfx='pop'),
    tag('gasolio', dx=-250, dy=60, w=380, color='red', at='Gasolio', delay=.1, sfx=None),
    img('assicurazione', dx=250, dy=-150, h=340, enter='right', at='assicurazione', rot=5, sfx='pop'),
    tag('assicurazione', dx=250, dy=60, w=440, color='red', at='assicurazione', delay=.1, sfx=None),
    img('rate', dx=0, dy=250, h=270, enter='up', at='rate', rot=-4, sfx='pop'),
    tag('rate', dx=0, dy=420, w=260, color='red', at='rate', delay=.1, sfx=None)]))
A(Beat(31, 'E se il camion si ferma, [[ti fermi tu]].', [
    img('truck_broken', w=960, dy=-40, enter='pop', drift=0.04, sfx='impact-bass-1'),
    tag('camion fermo', dx=0, dy=400, w=560, color='red', at='ferma')]))
A(Beat(32, 'La strada ti ha dato un [[lavoro sicuro]].', [
    img('marco38_full', dx=-270, h=760, enter='left', sfx='whoosh-short'),
    img('truck_worn', dx=205, dy=110, w=560, enter='right', at='lavoro', sfx='whoosh-short')]))
A(Beat(33, 'E in cambio, ti ha preso [[gli anni]].', [
    img('marco38_tired', dx=40, dy=60, h=800, enter='up'),
    img('calendario', dx=-300, dy=-300, h=330, enter='drop', at='anni', rot=-8, sfx='pop')]))
A(Beat(34, 'Hai [[ventitré]] anni. Un camion. Una strada.', [
    img('marco23_full', dx=-250, h=780, enter='left', sfx='whoosh-short'),
    img('truck_new', dx=215, dy=210, w=560, enter='right', at='camion', sfx='whoosh-short')]))
A(Beat(35, 'A [[trentotto]], la strada è ancora lì.', [
    img('marco38_full', dx=-250, h=780, enter='pop', sfx='pop'),
    img('truck_worn', dx=215, dy=210, w=560, enter='none')]))
A(Beat(36, 'Tu, un po\' [[meno]].', [
    img('marco38_head', h=900, dy=-40, enter='pop', drift=0.08, sfx='impact-bass-1')]))
A(Beat(37, '[[Iscriviti]], se vuoi sapere cosa serve davvero.', [
    img('campanella', w=900, enter='pop', drift=0.0, sfx='notification'),
    box('<div class="cta">ISCRIVITI</div>', 190, -30, 400, 110, enter='pop', delay=0.2, z=5, sfx=None)]))

CHAPTERS = [('c1', 1, 4, None), ('c2', 5, 8, 'anno 1'), ('c3', 9, 15, 'anno 5'),
            ('c4', 16, 24, 'anno 10'), ('c5', 25, 31, 'anno 15'), ('c6', 32, 37, None)]

# ------------------------------------------------------------------ mots / sous-titres
cum = 0
for bt in B:
    nw = len(bt.text.split())
    bt.words = [(swords[cum + i], TW[cum + i][0], TW[cum + i][1]) for i in range(nw)]
    cum += nw
assert cum == len(swords), (cum, len(swords))

def anchor(bt, word):
    k = norm(word)
    for w, t0, t1 in bt.words:
        if norm(w).startswith(k) or norm(w).startswith('l' + k):
            return max(0.0, t0 - bt.s)
    raise SystemExit(f'ancre introuvable: {word!r} dans le plan {bt.n}: {bt.text}')

def captions(bt):
    toks = bt.cap.split(' ')
    assert len(toks) == len(bt.words), (bt.n, toks, bt.text)
    items = []
    for tk, (w, t0, t1) in zip(toks, bt.words):
        items.append((tk.replace('[[', '').replace(']]', ''), '[[' in tk or ']]' in tk or (items and items[-1][2] and not tk.startswith('[[') and False), t0))
    # propagation de l'emphase entre [[ et ]]
    emph, out = False, []
    for tk, (w, t0, t1) in zip(toks, bt.words):
        if '[[' in tk: emph = True
        out.append((tk.replace('[[', '').replace(']]', ''), emph, t0))
        if ']]' in tk: emph = False
    chunks, cur = [], []
    def flush():
        if cur: chunks.append(list(cur)); cur.clear()
    for word, em, t0 in out:
        cur_len = len(' '.join(x[0] for x in cur))
        if cur and cur_len + 1 + len(word) > 24:
            flush()
        cur.append((word, em, t0))
        if re.search(r'[.,?!]$', word) and len(' '.join(x[0] for x in cur)) >= 9:
            flush()
    flush()
    # évite un fragment d'un seul mot court isolé
    merged = []
    for c in chunks:
        if merged and len(c) == 1 and len(c[0][0]) <= 4 and len(' '.join(x[0] for x in merged[-1] + c)) <= 24:
            merged[-1] += c
        else:
            merged.append(c)
    res = []
    for i, c in enumerate(merged):
        t_start = c[0][2] if i else bt.s
        t_end = merged[i + 1][0][2] if i + 1 < len(merged) else bt.e
        html = ' '.join(f'<b class="k">{w}</b>' if e else w for w, e, _ in c)
        res.append((max(t_start - 0.04, bt.s) if i else bt.s, t_end, html))
    return res

# ------------------------------------------------------------------ rendu
CSS = """
  #root { position:absolute; inset:0; font-family:'Montserrat',sans-serif; color:#fff; }
  .abs { position:absolute; }
  .item { position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .item img.pic { width:100%; height:100%; object-fit:contain; display:block; filter:drop-shadow(0 18px 26px rgba(0,0,0,.45)); }
  .item img.pic.fade { -webkit-mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); }
  .halo { width:100%; height:100%; border-radius:50%; }
  .num { font-weight:900; line-height:1; letter-spacing:-.02em; text-align:center; white-space:nowrap; text-shadow:0 0 40px rgba(255,255,255,.18); }
  .sub { font-weight:800; letter-spacing:.08em; text-align:center; color:#cdd3ff; margin-top:8px; }
  .stamp { border:10px solid; border-radius:18px; padding:10px 30px; font-weight:900; letter-spacing:.04em; text-align:center; background:rgba(11,11,46,.55); white-space:nowrap; }
  .gtag { display:inline-flex; align-items:center; gap:14px; padding:16px 34px; border-radius:999px; font-weight:800; font-size:40px; letter-spacing:.01em; white-space:nowrap;
          background:rgba(40,44,120,.62); border:3px solid rgba(150,160,255,.55); box-shadow:0 0 40px rgba(111,123,255,.35); color:#fff; }
  .gtag.red { background:rgba(90,22,52,.66); border-color:rgba(255,77,109,.7); box-shadow:0 0 40px rgba(255,77,109,.35); }
  .gtag.gold { background:rgba(84,60,10,.66); border-color:rgba(255,209,102,.75); box-shadow:0 0 40px rgba(255,209,102,.3); }
  .gtag.small { font-size:30px; padding:10px 26px; align-self:flex-start; margin-bottom:6px; }
  .gtag .dot { width:16px; height:16px; border-radius:50%; background:#ff4d6d; box-shadow:0 0 14px #ff4d6d; flex:none; }
  .item:has(> .gtag) { flex-direction:row; }
  .glass { width:100%; height:100%; border-radius:40px; padding:28px 34px; background:linear-gradient(180deg,rgba(60,64,160,.52),rgba(24,26,92,.62));
           border:3px solid rgba(150,160,255,.45); box-shadow:0 30px 60px rgba(0,0,0,.45), inset 0 0 50px rgba(120,130,255,.14); display:flex; flex-direction:column; }
  .glass .row { display:flex; justify-content:space-between; align-items:center; padding:14px 22px; margin-top:10px; border-radius:22px; background:rgba(14,16,70,.55); border:2px solid rgba(150,160,255,.18); height:104px; }
  .glass .rl { font-weight:800; font-size:28px; letter-spacing:.1em; color:#b8bdf0; }
  .glass .rv { font-weight:900; font-size:56px; white-space:nowrap; }
  .glass .rv.strike { text-decoration:line-through; text-decoration-thickness:6px; }
  .tiles { display:flex; gap:14px; justify-content:center; width:100%; }
  .tile { width:104px; height:116px; border-radius:24px; background:linear-gradient(180deg,#ffe28a,#f2b83c); display:flex; align-items:center; justify-content:center; box-shadow:0 10px 24px rgba(0,0,0,.4); }
  .tile b { font-weight:900; font-size:56px; color:#2a2308; }
  .cross { font-weight:900; font-size:150px; color:#ff4d6d; text-shadow:0 0 40px rgba(255,77,109,.7); line-height:1; }
  .ring { position:relative; width:100%; height:100%; }
  .ring svg { width:100%; height:100%; }
  .ring-bg { fill:none; stroke:#2a2f7a; stroke-width:16; }
  .ring-fg { fill:none; stroke:#ffd166; stroke-width:16; stroke-linecap:round; stroke-dasharray:540.4; stroke-dashoffset:540.4; }
  .ringtxt { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .spark { font-size:130px; color:#ffd166; text-shadow:0 0 40px rgba(255,209,102,.8); line-height:1; }
  .spark.s2 { font-size:96px; }
  .paper { width:100%; height:100%; background:#f4ecd8; border-radius:22px; padding:44px 52px; box-shadow:0 24px 50px rgba(0,0,0,.5); color:#3b3328; }
  .paper .ph { font-weight:900; font-size:52px; letter-spacing:.12em; margin-bottom:34px; color:#5a4a33; }
  .paper .pl { height:22px; border-radius:99px; background:#d8cdb2; margin:26px 0; width:100%; }
  .paper .pl.s { width:68%; }
  .paper .hl { display:flex; justify-content:space-between; align-items:center; margin:34px 0; padding:20px 26px; border:7px solid #ff4d6d; border-radius:20px; font-weight:800; font-size:36px; }
  .paper .hl b { font-size:56px; color:#ff4d6d; white-space:nowrap; }
  .bar { width:100%; height:100%; background:#2a2f7a; border-radius:99px; overflow:hidden; border:5px solid #6f7bff; }
  .barfill { width:100%; height:100%; background:linear-gradient(90deg,#ffd166,#ff8a4d); transform-origin:left center; }
  .phone { width:100%; height:100%; background:#1b1d4a; border:14px solid #9aa0c8; border-radius:56px; overflow:hidden; display:flex; align-items:flex-end; justify-content:center; box-shadow:0 0 60px rgba(100,160,255,.45); }
  .phone .kid { width:132%; max-width:none; margin-bottom:-4%; }
  .opt { width:100%; height:100%; border-radius:34px; background:rgba(42,47,122,.78); border:6px solid #6f7bff; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; }
  .opt.gold { background:rgba(90,64,12,.7); border-color:#ffd166; }
  .opt .otitle { font-weight:900; font-size:62px; letter-spacing:.08em; }
  .opt img { height:190px; }
  .opt img.keys { height:200px; }
  .or { font-weight:900; font-size:54px; letter-spacing:.2em; color:#cdd3ff; text-align:center; }
  .chart { width:100%; height:100%; display:flex; align-items:flex-end; justify-content:space-around; gap:60px; padding-bottom:10px; }
  .chart .col { flex:1; height:100%; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; }
  .chart .b { width:80%; border-radius:26px 26px 0 0; transform-origin:bottom center; }
  .chart .gr { height:100%; background:linear-gradient(180deg,#5af0b0,#1fa974); }
  .chart .rd { height:22%; background:linear-gradient(180deg,#ff7a93,#d62d52); }
  .chart .lbl { margin-top:22px; font-weight:900; font-size:48px; letter-spacing:.08em; }
  .roadbox { overflow:hidden; }
  .road { position:absolute; left:0; right:0; top:30px; bottom:30px; background:#14163f; border-top:6px solid #3a3f95; border-bottom:6px solid #3a3f95; }
  .dash { position:absolute; left:-30%; right:-30%; top:50%; height:10px; background:repeating-linear-gradient(90deg,#ffd166 0 70px,transparent 70px 140px); }
  .cta { font-weight:900; font-size:58px; letter-spacing:.06em; color:#fff; text-shadow:0 4px 10px rgba(120,40,0,.6); text-align:center; white-space:nowrap; }
  .chip { position:absolute; left:0; width:1080px; top:150px; display:flex; justify-content:center; z-index:20; }
  .cap { position:absolute; left:0; width:1080px; text-align:center; font-weight:800; font-size:58px; line-height:1.15; text-transform:uppercase; letter-spacing:.01em; white-space:nowrap; text-shadow:0 5px 16px rgba(0,0,0,.7); z-index:30; }
  .cap .k { color:#ff4d6d; font-weight:900; }
"""

class Out:
    sfx = []   # (t_abs, file, vol)

def build_chapter(cid, a, b, chip):
    beats = B[a - 1:b]
    t0 = beats[0].s
    dur = round(beats[-1].e - t0, 3)
    html, js = [], []
    if chip:
        html.append(f'<div class="chip clip" id="{cid}-chip" data-start="0" data-duration="{dur}" data-track-index="9">'
                    f'<div class="gtag red"><i class="dot"></i>{chip}</div></div>')
        js.append(f'tl.fromTo("#{cid}-chip",{{opacity:0,y:-40,scale:.9}},{{opacity:1,y:0,scale:1,duration:.4,ease:"expo.out"}},0);')
        js.append(f'tl.to("#{cid}-chip",{{opacity:0,duration:.2,ease:"power2.in"}},{dur - 0.22});')
        Out.sfx.append((t0 + .02, 'pop', .35))
    zt = (330 if chip else 215)
    zb = 1215
    for bt in beats:
        ls, d = round(bt.s - t0, 3), round(bt.e - bt.s, 3)
        le = round(ls + d, 3)
        for i, it in enumerate(bt.items):
            eid = f'{cid}-b{bt.n}-i{i}'
            if it['k'] == 'img':
                iw, ih = SIZE[it['name']]
                if it['h']: hh = it['h']; ww = hh * iw / ih
                else: ww = it['w']; hh = ww * ih / iw
                fade = ' fade' if it['name'].endswith('_head') else ''
                inner = f'<img class="pic{fade}" id="{eid}-p" src="assets/img/{it["name"]}.png" alt="">'
                bw, bh = ww, hh
                if bh > zb - zt:
                    f = (zb - zt) / bh; bw, bh = bw * f, bh * f
            else:
                bw, bh = it['w'], it['h']
                inner = it['html']
            cy_i = min(max(CY + it['dy'], zt + bh / 2), zb - bh / 2)
            left, top = CX + it['dx'] - bw / 2, cy_i - bh / 2
            html.append(f'<div class="item clip {it.get("cls","")}" id="{eid}" data-start="{ls}" data-duration="{d}" '
                        f'data-track-index="{1 + i}" style="left:{left:.0f}px;top:{top:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;z-index:{it["z"]}">{inner}</div>')
            st = round(ls + (anchor(bt, it['at']) if it['at'] else 0) + it['delay'], 3)
            st = min(st, le - 0.8)
            edur = round(min(.5, max(.2, le - 0.22 - st)), 3)
            r, e = it['rot'], it['enter']
            fr = {'pop': 'opacity:0,scale:.6,y:36', 'left': 'opacity:0,x:-380', 'right': 'opacity:0,x:380',
                  'drop': 'opacity:0,y:-280', 'up': 'opacity:0,y:300', 'shake': 'opacity:0,scale:.5,y:60', 'none': 'opacity:1'}[e]
            if e == 'none':
                js.append(f'tl.set("#{eid}",{{rotation:{r}}},{st});')
            else:
                # l'élément reste invisible jusqu'à son mot
                js.append(f'tl.fromTo("#{eid}",{{opacity:0}},{{opacity:0,duration:.01}},{ls});')
                ease = 'back.out(1.5)' if e in ('pop', 'shake', 'drop') else 'expo.out'
                js.append(f'tl.fromTo("#{eid}",{{{fr},rotation:{r}}},{{opacity:1,scale:1,x:0,y:0,rotation:{r},duration:{edur},ease:"{ease}"}},{st});')
            if e == 'shake':
                js.append(f'tl.to("#{eid}",{{rotation:{r + 5},duration:.07,yoyo:true,repeat:3,ease:"sine.inOut"}},{st + 0.5:.3f});')
            js.append(f'tl.to("#{eid}",{{opacity:0,scale:.95,filter:"blur(8px)",duration:.17,ease:"power2.in"}},{le - 0.19:.3f});')
            if it['k'] == 'img' and it['drift']:
                js.append(f'tl.fromTo("#{eid}-p",{{scale:1}},{{scale:{1 + it["drift"]},duration:{d},ease:"none"}},{ls});')
            if it['sfx']:
                vol = 0.5 if it['sfx'].startswith('impact') else (0.4 if it['sfx'] in ('notification', 'error') else 0.33)
                Out.sfx.append((t0 + st - 0.02, it['sfx'], vol))
        # sous-titres
        for k, (cs, ce, chtml) in enumerate(captions(bt)):
            cl, cd = round(cs - t0, 3), round(ce - cs, 3)
            cid_cap = f'{cid}-cap{bt.n}-{k}'
            html.append(f'<div class="cap clip" id="{cid_cap}" data-start="{cl}" data-duration="{cd}" data-track-index="10" style="top:{CAP_Y - 36}px">{chtml}</div>')
            if not (bt.n == 1 and k == 0):
                js.append(f'tl.fromTo("#{cid_cap}",{{opacity:0,y:16,scale:.97}},{{opacity:1,y:0,scale:1,duration:.14,ease:"power3.out"}},{cl});')
            js.append(f'tl.to("#{cid_cap}",{{opacity:0,duration:.07,ease:"none"}},{round(cl + cd - 0.08, 3)});')
        ls0 = ls
        if bt.n == 3:
            js.append(f'tl.fromTo("#{cid}-b3-i0 .dash",{{x:0}},{{x:-280,duration:{d},ease:"none"}},{ls0});')
        if bt.n == 14:
            js.append(f'tl.to("#ringfill",{{strokeDashoffset:0,duration:{min(2.0, d - .5):.2f},ease:"power2.out"}},{ls0 + .3:.2f});')
        if bt.n == 21:
            at_ = ls0 + anchor(bt, 'novanta')
            js.append(f'tl.fromTo("#barfill",{{scaleX:0}},{{scaleX:1,duration:{min(2.4, d - at_ + ls0 - .6):.2f},ease:"power2.out"}},{at_ + .2:.2f});')
        if bt.n == 27:
            js.append(f'tl.fromTo("#bar1",{{scaleY:0}},{{scaleY:1,duration:.6,ease:"power3.out"}},{ls0 + anchor(bt, "fatturato") + .1:.2f});')
            js.append(f'tl.fromTo("#bar2",{{scaleY:0}},{{scaleY:1,duration:.6,ease:"power3.out"}},{ls0 + anchor(bt, "utile") + .1:.2f});')
        if bt.n == 37:
            js.append(f'tl.fromTo("#{cid}-b37-i0-p",{{rotation:0}},{{rotation:7,duration:.09,yoyo:true,repeat:7,ease:"sine.inOut"}},{ls0 + .5:.2f});')
    comp = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
    {chr(10).join('    ' + h for h in html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in js)}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""
    open(os.path.join(OUT, 'compositions', f'{cid}.html'), 'w', encoding='utf-8').write(comp)
    return t0, dur

hosts = []
for k, (cid, a, b, chip) in enumerate(CHAPTERS):
    t0, dur = build_chapter(cid, a, b, chip)
    hosts.append(f'    <div id="{cid}" class="clip" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
                 f'data-start="{t0:.3f}" data-duration="{dur}" data-track-index="{2 + k % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')

# effets sonores (ordre chronologique, sans chevauchement excessif d'un même fichier)
Out.sfx.sort()
audio = []
for n, (t, f, v) in enumerate(Out.sfx):
    d = SFXDUR[f]
    audio.append(f'      <audio id="sfx{n}" src="assets/sfx/{f}.mp3" data-start="{max(t, 0):.3f}" data-duration="{d}" data-track-index="{20 + n % 4}" data-volume="{v}"></audio>')

stars = ''.join(
    f'<i style="left:{(i * 137) % 100}%;top:{(i * 71) % 100}%;width:{2 + i % 3}px;height:{2 + i % 3}px;opacity:{.25 + (i % 5) / 10:.2f}"></i>'
    for i in range(90))
twink = ''.join(f'tl.fromTo("#stars i:nth-child({3 + 7 * j})",{{opacity:.15}},{{opacity:.95,duration:{1.3 + (j % 4) * .45:.2f},yoyo:true,repeat:{int(TOTAL // (1.3 + (j % 4) * .45)) | 1},ease:"sine.inOut"}},{(j * .37) % 2:.2f});\n      '
                for j in range(12))

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
      #b1 {{ left:-420px; top:-300px; width:1300px; height:1300px; background:radial-gradient(circle,rgba(130,70,210,.48),transparent 66%); }}
      #b2 {{ left:-200px; top:1020px; width:1500px; height:1100px; background:radial-gradient(circle,rgba(20,205,185,.48),transparent 66%); }}
      #b3 {{ left:520px; top:520px; width:1000px; height:1000px; background:radial-gradient(circle,rgba(60,90,230,.38),transparent 66%); }}
      #grid {{ position:absolute; inset:0; opacity:.5;
        background-image:linear-gradient(rgba(140,150,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(140,150,255,.07) 1px,transparent 1px);
        background-size:90px 90px; -webkit-mask-image:linear-gradient(180deg,transparent 5%,#000 40%,#000 75%,transparent 100%); mask-image:linear-gradient(180deg,transparent 5%,#000 40%,#000 75%,transparent 100%); }}
      #stars {{ position:absolute; inset:0; }}
      #stars i {{ position:absolute; border-radius:50%; background:#fff; }}
      #vig {{ position:absolute; inset:0; background:radial-gradient(ellipse 85% 70% at 50% 45%, transparent 55%, rgba(4,4,24,.55) 100%); }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" style="position:absolute;inset:0;font-family:Montserrat,sans-serif">
      <div id="bg"></div>
      <div id="b1" class="blob"></div><div id="b2" class="blob"></div><div id="b3" class="blob"></div>
      <div id="grid"></div>
      <div id="stars">{stars}</div>
      <div id="vig"></div>
{chr(10).join(hosts)}
      <audio id="voce" src="assets/voce.wav" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#b1", {{ x: 0, y: 0 }}, {{ x: 150, y: 110, duration: {TOTAL}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#b2", {{ x: 0, y: 0 }}, {{ x: -130, y: -70, duration: {TOTAL}, ease: "sine.inOut" }}, 0);
      tl.fromTo("#b3", {{ x: 0, y: 0 }}, {{ x: -170, y: 120, duration: {TOTAL}, ease: "sine.inOut" }}, 0);
      {twink}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)
open(os.path.join(OUT, 'hyperframes.json'), 'w').write('{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",\n  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},\n  "media": {"autoProxy": true}\n}\n')
open(os.path.join(OUT, 'meta.json'), 'w').write('{"id": "camionista-v2", "name": "La tua vita dopo 15 anni da camionista (9:16 v2)"}')
print('ok v2', len(Out.sfx), 'sfx')
for bt in B[:6]:
    print(bt.n, [(round(a, 2), round(b, 2), re.sub('<[^>]+>', '', h)) for a, b, h in captions(bt)])
