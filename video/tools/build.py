"""Génère le projet HyperFrames « La tua vita dopo 15 anni da camionista ».
Usage (depuis video/) :  python3 tools/build.py vertical|landscape
Écrit dans  video/<format>/  : index.html, compositions/*.html, assets/…
"""
import os, re, shutil, sys
from PIL import Image

FORMAT = sys.argv[1] if len(sys.argv) > 1 else 'vertical'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, FORMAT)
CUT = os.path.join(ROOT, 'assets', 'cut')
VOICE = '/root/.claude/uploads/91729ddc-3274-50e3-9f11-8e52419e14ce/280557de-Generated_Audio_October_24_2026_-_5_04PM.wav'
TOTAL = 98.7

if FORMAT == 'vertical':
    W, H, U = 1080, 1920, 1.0          # U : échelle des éléments
    CX, CY = 540, 720                  # centre de la zone visuelle
    CAP_Y, CAP_W, CAP_FS = 1250, 940, 66
    CHIP_Y, XS = 255, 1.0              # XS : écartement horizontal
else:
    W, H, U = 1920, 1080, 0.9
    CX, CY = 960, 430
    CAP_Y, CAP_W, CAP_FS = 930, 1500, 58
    CHIP_Y, XS = 78, 1.55

RED, GOLD, GREEN, INK = '#ff4d6d', '#ffd166', '#3ddc97', '#ffffff'

# ------------------------------------------------------------------ temps
def parse_srt(path):
    t = open(path, encoding='utf-8').read().strip().split('\n\n')
    out = []
    for blk in t:
        l = blk.split('\n')
        a, b = l[1].split(' --> ')
        f = lambda s: (int(s[:2]) * 3600 + int(s[3:5]) * 60 + int(s[6:8]) + int(s[9:]) / 1000)
        out.append((f(a), f(b), ' '.join(l[2:])))
    return out

SC = parse_srt(os.path.join(ROOT, '..', 'scripts', 'camionista-scenes.srt'))
assert len(SC) == 37

# ------------------------------------------------------------------ assets
os.makedirs(os.path.join(OUT, 'assets', 'img'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'compositions'), exist_ok=True)
SIZE = {}
for f in os.listdir(CUT):
    im = Image.open(os.path.join(CUT, f))
    im.thumbnail((1100, 1100))
    im.save(os.path.join(OUT, 'assets', 'img', f), optimize=True)
    SIZE[f[:-4]] = im.size
shutil.copy(VOICE, os.path.join(OUT, 'assets', 'voce.wav'))

# ------------------------------------------------------------------ DSL
class Beat:
    def __init__(self, n, cap, items):
        self.n, self.cap, self.items = n, cap, items
        self.s, self.e, _ = SC[n - 1]

def img(name, dx=0, dy=0, h=None, w=None, enter='pop', delay=0.0, rot=0, z=2, drift=0.05):
    return dict(k='img', name=name, dx=dx, dy=dy, h=h, w=w, enter=enter, delay=delay, rot=rot, z=z, drift=drift)

def box(html, dx=0, dy=0, w=600, h=300, enter='pop', delay=0.0, rot=0, z=3, cls=''):
    return dict(k='box', html=html, dx=dx, dy=dy, w=w, h=h, enter=enter, delay=delay, rot=rot, z=z, cls=cls)

def num(text, sub='', dx=0, dy=0, w=800, h=300, size=190, color=GOLD, **kw):
    size = min(size, int(w / (len(text) * 0.66)))
    s = f'<div class="num" style="font-size:{{S{size}}}px;color:{color}">{text}</div>'
    if sub:
        s += f'<div class="sub" style="font-size:{{S52}}px">{sub}</div>'
    return box(s, dx, dy, w, h, **kw)

def stamp(text, dx=0, dy=0, w=620, h=140, rot=-8, size=62, color=RED, **kw):
    return box(f'<div class="stamp" style="font-size:{{S{size}}}px;color:{color};border-color:{color}">{text}</div>',
               dx, dy, w, h, rot=rot, **kw)

# ------------------------------------------------------------------ storyboard
B = []
B.append(Beat(1, 'Hai [[ventitré]] anni.', [
    img('marco23_full', dx=170, h=860, enter='none'),
    num('23', 'ANNI', dx=-215, dy=-40, w=500, h=420, size=300, enter='none')]))
B.append(Beat(2, 'Hai speso oltre [[tremila euro]] per patente e CQC.', [
    img('patente', dx=-250, dy=-300, h=290, rot=-8, enter='left'),
    img('cqc', dx=250, dy=-170, h=290, rot=7, enter='right', delay=0.12),
    num('+3.000 €', 'SPESI PER INIZIARE', dx=0, dy=200, w=860, h=330, size=190, color=RED, enter='pop', delay=0.2)]))
B.append(Beat(3, 'Davanti a te, un [[camion]] e la strada.', [
    box('<div class="road"><div class="dash"></div></div>', 0, 260, 1500, 150, enter='none', z=1, cls='roadbox'),
    img('truck_new', dx=0, dy=-10, w=1000, enter='right', drift=0.04)]))
B.append(Beat(4, '[[Quindici anni]] dopo, cosa ti resta davvero?', [
    num('15 ANNI', '', dx=0, dy=-400, w=800, h=200, size=130, color=GOLD, enter='drop'),
    img('marco23_head', dx=-235, dy=20, h=540, enter='left'),
    img('marco38_head', dx=235, dy=20, h=540, enter='right', delay=0.15),
    box('<div class="num" style="font-size:{S150}px;color:#ff4d6d">?</div>', 0, 20, 160, 200, enter='pop', delay=0.35)]))
B.append(Beat(5, 'Anno [[uno]]. Autista neoassunto.', [
    img('marco23_full', h=860, enter='up')]))
B.append(Beat(6, 'Prendi circa [[millecinquecento euro]] lordi al mese.', [
    img('marco23_full', dx=-300, dy=40, h=700, enter='left'),
    num('≈ 1.500 €', 'LORDI AL MESE', dx=190, dy=-110, w=640, h=330, size=130, enter='right'),
    img('soldi', dx=190, dy=260, h=260, enter='pop', delay=0.25)]))
B.append(Beat(7, 'Il resto lo fanno [[trasferte]] e [[straordinari]].', [
    img('truck_new', dx=0, dy=-230, w=760, enter='left'),
    img('calendario', dx=-230, dy=190, h=330, enter='pop', delay=0.15, rot=-5),
    box('<div class="pill" style="font-size:{S54}px">STRAORDINARI</div>', 160, 170, 520, 120, enter='right', delay=0.25),
    box('<div class="pill red" style="font-size:{S54}px">TRASFERTE</div>', 160, 320, 520, 120, enter='right', delay=0.4)]))
B.append(Beat(8, 'La tua casa, adesso, è una [[cabina]].', [
    img('cab_interior', w=840, enter='pop', drift=0.06)]))
B.append(Beat(9, 'Anno [[cinque]]. Patente CE, tratte lunghe.', [
    img('marco28_full', dx=-260, h=820, enter='left'),
    img('patenteCE', dx=250, dy=-190, h=300, rot=7, enter='right'),
    img('truck_new', dx=200, dy=260, w=560, enter='right', delay=0.2)]))
B.append(Beat(10, 'Il minimo contrattuale sale a circa [[duemila euro]] lordi.', [
    img('marco28_full', dx=-330, dy=40, h=720, enter='left'),
    box('<div class="old">1.500 €</div>', 200, -200, 560, 120, enter='drop'),
    num('≈ 2.000 €', 'LORDI AL MESE', dx=200, dy=-30, w=640, h=330, size=130, color=GREEN, enter='pop', delay=0.2),
    box('<div class="arrow">▲</div>', 200, 190, 200, 160, enter='up', delay=0.35)]))
B.append(Beat(11, 'Poi arriva la [[diaria]], fino a [[quarantasei euro]] al giorno.', [
    num('fino a 46 €', 'AL GIORNO · DIARIA', dx=0, dy=-180, w=900, h=360, size=150, enter='pop'),
    img('soldi', dx=0, dy=270, h=400, enter='up', delay=0.2)]))
B.append(Beat(12, '[[Non è stipendio.]] Ma ti fa arrivare a fine mese.', [
    img('portafoglio', dx=0, dy=-30, w=800, enter='up'),
    stamp('NON È STIPENDIO', dx=0, dy=210, w=860, h=150, rot=-6, enter='pop', delay=0.3, size=68)]))
B.append(Beat(13, 'Impari il [[tachigrafo]].', [
    img('tachigrafo', w=900, enter='pop', drift=0.06)]))
B.append(Beat(14, '[[Nove ore]] di guida, non una di più.', [
    box('<div class="ring"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" class="ring-bg"/>'
        '<circle id="ringfill" cx="100" cy="100" r="86" class="ring-fg" transform="rotate(-90 100 100)"/></svg>'
        '<div class="ringtxt"><span class="num" style="font-size:{S210}px;color:#ffd166">9</span>'
        '<span class="sub" style="font-size:{S60}px">ORE</span></div></div>', 0, 0, 640, 640, enter='pop')]))
B.append(Beat(15, 'Se sgarri, la [[multa]] arriva.', [
    img('multa', dx=0, dy=-30, h=680, enter='shake', rot=-6),
    stamp('MULTA', dx=140, dy=250, w=520, h=150, rot=-10, enter='pop', delay=0.35, size=80)]))
B.append(Beat(16, 'Anno [[dieci]]. Sei un veterano.', [
    img('marco33_full', h=860, enter='up')]))
B.append(Beat(17, 'Gli scatti di anzianità valgono [[venticinque, trenta euro]] al mese.', [
    img('marco33_full', dx=-330, dy=40, h=720, enter='left'),
    num('+25–30 €', 'AL MESE', dx=200, dy=-60, w=640, h=360, size=122, color=GREEN, enter='right')]))
B.append(Beat(18, 'Ogni [[due anni]].', [
    img('calendario', dy=-10, h=640, enter='pop'),
    box('<div class="pill red" style="font-size:{S70}px">OGNI 2 ANNI</div>', 0, 330, 640, 140, enter='up', delay=0.25)]))
B.append(Beat(19, 'Dopo dieci anni sei [[bravissimo]].', [
    img('marco33_full', h=860, enter='pop'),
    box('<div class="spark">★</div>', -250, -250, 140, 140, enter='pop', delay=0.2),
    box('<div class="spark s2">★</div>', 270, -120, 110, 110, enter='pop', delay=0.35),
    box('<div class="spark">★</div>', 230, 260, 90, 90, enter='pop', delay=0.5)]))
B.append(Beat(20, 'In busta paga, [[quasi non si vede]].', [
    box('<div class="paper"><div class="ph">BUSTA PAGA</div>'
        '<div class="pl"></div><div class="pl s"></div><div class="pl"></div><div class="pl s"></div>'
        '<div class="hl"><span>aumento anzianità</span><b>+ 30 €</b></div><div class="pl"></div></div>',
        0, -20, 760, 700, enter='up')]))
B.append(Beat(21, 'Ogni [[due settimane]], novanta ore di guida al massimo.', [
    num('90 h', 'OGNI 2 SETTIMANE · MASSIMO', dx=0, dy=-120, w=900, h=420, size=230, color=GOLD, enter='pop'),
    box('<div class="bar"><div id="barfill" class="barfill"></div></div>', 0, 210, 860, 70, enter='up', delay=0.2)]))
B.append(Beat(22, 'Il riposo lungo, [[quarantacinque ore]], lo fai fuori dal camion.', [
    img('marco33_chair', dx=120, dy=60, h=760, enter='up'),
    num('45 h', 'DI RIPOSO', dx=-290, dy=-250, w=520, h=360, size=170, color=GREEN, enter='left')]))
B.append(Beat(23, 'Spesso, [[lontano da casa]].', [
    img('marco33_chair', dx=0, dy=90, h=640, enter='none'),
    box('<div class="pill red" style="font-size:{S58}px">LONTANO DA CASA</div>', 0, -330, 820, 130, enter='drop')]))
B.append(Beat(24, 'Tuo figlio cresce nelle [[videochiamate]].', [
    img('marco33_phone', dx=-240, dy=60, h=640, enter='left'),
    box('<div class="phone"><img class="kid" src="assets/img/figlio.png"></div>', 270, -20, 330, 600, enter='right', delay=0.15)]))
B.append(Beat(25, 'Anno [[quindici]]. Il bivio.', [
    img('marco38_full', dx=-250, h=780, enter='left'),
    img('bivio', dx=225, dy=40, h=590, enter='right', delay=0.1)]))
B.append(Beat(26, 'Continuare da [[dipendente]], o comprare il camion e diventare [[padroncino]].', [
    box('<div class="opt"><div class="otitle">DIPENDENTE</div><img src="assets/img/truck_worn.png"></div>', 0, -195, 760, 320, enter='left'),
    box('<div class="or">OPPURE</div>', 0, 5, 340, 90, enter='pop', delay=0.3),
    box('<div class="opt gold"><div class="otitle">PADRONCINO</div><img class="keys" src="assets/img/chiavi.png"></div>', 0, 215, 760, 320, enter='right', delay=0.4)]))
B.append(Beat(27, 'Il [[fatturato]] sale. L\'[[utile]], molto meno.', [
    box('<div class="chart"><div class="col"><div id="bar1" class="b gr"></div><div class="lbl">FATTURATO</div></div>'
        '<div class="col"><div id="bar2" class="b rd"></div><div class="lbl">UTILE</div></div></div>', 0, -10, 860, 700, enter='up')]))
B.append(Beat(28, 'Le stime vanno da [[millequattrocento]] a [[tremila euro]].', [
    num('1.400 – 3.000 €', 'STIMA · PADRONCINO', dx=0, dy=-20, w=1000, h=420, size=112, color=GOLD, enter='pop'),
    img('soldi', dx=0, dy=270, h=250, enter='up', delay=0.2)]))
B.append(Beat(29, '[[Netti]], al mese.', [
    num('1.400 – 3.000 €', '', dx=0, dy=-120, w=1000, h=260, size=112, color=GOLD, enter='none'),
    stamp('NETTI', dx=-150, dy=150, w=520, h=170, rot=-8, size=100, enter='pop'),
    stamp('AL MESE', dx=160, dy=300, w=620, h=170, rot=6, size=84, color=GREEN, enter='pop', delay=0.2)]))
B.append(Beat(30, '[[Gasolio]], [[assicurazione]] e [[rate]] le paghi tu.', [
    img('pompa', dx=-250, dy=-170, h=380, enter='left'),
    img('assicurazione', dx=250, dy=-150, h=340, enter='right', delay=0.3, rot=5),
    img('rate', dx=0, dy=240, h=290, enter='up', delay=0.7, rot=-4)]))
B.append(Beat(31, 'E se il camion si ferma, [[ti fermi tu]].', [
    img('truck_broken', w=1000, enter='pop', drift=0.05)]))
B.append(Beat(32, 'La strada ti ha dato un [[lavoro sicuro]].', [
    img('marco38_full', dx=-270, h=780, enter='left'),
    img('truck_worn', dx=205, dy=110, w=560, enter='right', delay=0.1)]))
B.append(Beat(33, 'E in cambio, ti ha preso [[gli anni]].', [
    img('marco38_tired', dx=40, dy=60, h=820, enter='up'),
    img('calendario', dx=-300, dy=-300, h=330, enter='drop', delay=0.2, rot=-8)]))
B.append(Beat(34, 'Hai [[ventitré]] anni. Un camion. Una strada.', [
    img('marco23_full', dx=-250, h=800, enter='left'),
    img('truck_new', dx=215, dy=210, w=560, enter='right', delay=0.1)]))
B.append(Beat(35, 'A [[trentotto]], la strada è ancora lì.', [
    img('marco38_full', dx=-250, h=800, enter='pop'),
    img('truck_worn', dx=215, dy=210, w=560, enter='none')]))
B.append(Beat(36, 'Tu, un po\' [[meno]].', [
    img('marco38_head', h=900, dy=-40, enter='pop', drift=0.1)]))
B.append(Beat(37, '[[Iscriviti]], se vuoi sapere cosa serve davvero.', [
    img('campanella', w=900, enter='pop', drift=0.0),
    box('<div class="cta" style="font-size:{S58}px">ISCRIVITI</div>', 190, -30, 400, 110, enter='pop', delay=0.2, z=5)]))

CHAPTERS = [
    ('c1', 1, 4, None), ('c2', 5, 8, 'ANNO 1'), ('c3', 9, 15, 'ANNO 5'),
    ('c4', 16, 24, 'ANNO 10'), ('c5', 25, 31, 'ANNO 15'), ('c6', 32, 37, None)]

# ------------------------------------------------------------------ rendu
def sc(v): return int(round(v * U))

def fill(html):
    return re.sub(r'\{S(\d+)\}', lambda m: str(sc(int(m.group(1)))), html)

def cap_html(t):
    return re.sub(r'\[\[(.+?)\]\]', r'<b class="k">\1</b>', t)

CSS = f"""
  #root {{ position:absolute; inset:0; font-family:'Montserrat',sans-serif; color:{INK}; }}
  .abs {{ position:absolute; }}
  .item {{ position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
  .item img.pic {{ width:100%; height:100%; object-fit:contain; display:block; filter:drop-shadow(0 {sc(18)}px {sc(26)}px rgba(0,0,0,.45)); }}
  .item img.pic.fade {{ -webkit-mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); mask-image:linear-gradient(to bottom,#000 78%,transparent 100%); }}
  .num {{ font-weight:900; line-height:1; letter-spacing:-.02em; text-align:center; white-space:nowrap; text-shadow:0 0 {sc(40)}px rgba(255,255,255,.18); }}
  .sub {{ font-weight:800; letter-spacing:.08em; text-align:center; color:#cdd3ff; margin-top:{sc(8)}px; }}
  .col1 {{ display:flex; flex-direction:column; align-items:center; justify-content:center; }}
  .stamp {{ border:{sc(10)}px solid; border-radius:{sc(18)}px; padding:{sc(10)}px {sc(30)}px; font-weight:900; letter-spacing:.04em; text-align:center; background:rgba(11,11,46,.55); white-space:nowrap; }}
  .pill {{ background:#2a2f7a; border:{sc(5)}px solid #6f7bff; border-radius:999px; padding:{sc(14)}px {sc(40)}px; font-weight:900; letter-spacing:.06em; white-space:nowrap; color:#fff; box-shadow:0 0 {sc(40)}px rgba(111,123,255,.45); }}
  .pill.red {{ background:#5a1530; border-color:{RED}; box-shadow:0 0 {sc(40)}px rgba(255,77,109,.45); }}
  .old {{ font-weight:900; font-size:{sc(78)}px; color:#8d92c9; text-decoration:line-through; text-decoration-thickness:{sc(7)}px; }}
  .arrow {{ font-weight:900; font-size:{sc(120)}px; color:{GREEN}; text-shadow:0 0 {sc(36)}px rgba(61,220,151,.6); }}
  .chip {{ font-weight:900; font-size:{sc(54)}px; letter-spacing:.14em; padding:{sc(12)}px {sc(44)}px; border-radius:999px; background:{RED}; color:#fff; box-shadow:0 0 {sc(46)}px rgba(255,77,109,.55); white-space:nowrap; }}
  .ring {{ position:relative; width:100%; height:100%; }}
  .ring svg {{ width:100%; height:100%; }}
  .ring-bg {{ fill:none; stroke:#2a2f7a; stroke-width:16; }}
  .ring-fg {{ fill:none; stroke:{GOLD}; stroke-width:16; stroke-linecap:round; stroke-dasharray:540.4; stroke-dashoffset:540.4; }}
  .ringtxt {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
  .spark {{ font-size:{sc(130)}px; color:{GOLD}; text-shadow:0 0 {sc(40)}px rgba(255,209,102,.8); line-height:1; }}
  .spark.s2 {{ font-size:{sc(96)}px; }}
  .paper {{ width:100%; height:100%; background:#f4ecd8; border-radius:{sc(22)}px; padding:{sc(44)}px {sc(52)}px; box-shadow:0 {sc(24)}px {sc(50)}px rgba(0,0,0,.5); color:#3b3328; transform-origin:center; }}
  .paper .ph {{ font-weight:900; font-size:{sc(52)}px; letter-spacing:.12em; margin-bottom:{sc(34)}px; color:#5a4a33; }}
  .paper .pl {{ height:{sc(22)}px; border-radius:99px; background:#d8cdb2; margin:{sc(26)}px 0; width:100%; }}
  .paper .pl.s {{ width:68%; }}
  .paper .hl {{ display:flex; justify-content:space-between; align-items:center; margin:{sc(34)}px 0; padding:{sc(20)}px {sc(26)}px; border:{sc(7)}px solid {RED}; border-radius:{sc(20)}px; font-weight:800; font-size:{sc(40)}px; }}
  .paper .hl b {{ font-size:{sc(66)}px; color:{RED}; }}
  .bar {{ width:100%; height:100%; background:#2a2f7a; border-radius:99px; overflow:hidden; border:{sc(5)}px solid #6f7bff; }}
  .barfill {{ width:100%; height:100%; background:linear-gradient(90deg,#ffd166,#ff8a4d); transform-origin:left center; }}
  .phone {{ width:100%; height:100%; background:#1b1d4a; border:{sc(14)}px solid #9aa0c8; border-radius:{sc(56)}px; overflow:hidden; display:flex; align-items:flex-end; justify-content:center; box-shadow:0 0 {sc(60)}px rgba(100,160,255,.45); }}
  .phone .kid {{ width:132%; max-width:none; margin-bottom:-4%; }}
  .opt {{ width:100%; height:100%; border-radius:{sc(34)}px; background:rgba(42,47,122,.78); border:{sc(6)}px solid #6f7bff; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:{sc(10)}px; }}
  .opt.gold {{ background:rgba(90,64,12,.7); border-color:{GOLD}; }}
  .opt .otitle {{ font-weight:900; font-size:{sc(62)}px; letter-spacing:.08em; }}
  .opt img {{ height:{sc(210)}px; }}
  .opt img.keys {{ height:{sc(220)}px; }}
  .or {{ font-weight:900; font-size:{sc(54)}px; letter-spacing:.2em; color:#cdd3ff; text-align:center; }}
  .chart {{ width:100%; height:100%; display:flex; align-items:flex-end; justify-content:space-around; gap:{sc(60)}px; padding-bottom:{sc(10)}px; }}
  .chart .col {{ flex:1; height:100%; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; }}
  .chart .b {{ width:80%; border-radius:{sc(26)}px {sc(26)}px 0 0; transform-origin:bottom center; }}
  .chart .gr {{ height:100%; background:linear-gradient(180deg,#5af0b0,#1fa974); }}
  .chart .rd {{ height:22%; background:linear-gradient(180deg,#ff7a93,#d62d52); }}
  .chart .lbl {{ margin-top:{sc(22)}px; font-weight:900; font-size:{sc(48)}px; letter-spacing:.08em; }}
  .roadbox {{ overflow:hidden; }}
  .road {{ position:absolute; left:0; right:0; top:{sc(30)}px; bottom:{sc(30)}px; background:#14163f; border-top:{sc(6)}px solid #3a3f95; border-bottom:{sc(6)}px solid #3a3f95; }}
  .dash {{ position:absolute; left:-30%; right:-30%; top:50%; height:{sc(10)}px; background:repeating-linear-gradient(90deg,{GOLD} 0 {sc(70)}px,transparent {sc(70)}px {sc(140)}px); }}
  .cta {{ font-weight:900; letter-spacing:.06em; color:#fff; text-shadow:0 {sc(4)}px {sc(10)}px rgba(120,40,0,.6); text-align:center; white-space:nowrap; }}
  .cap {{ position:absolute; left:{(W-CAP_W)//2}px; width:{CAP_W}px; text-align:center; font-weight:900; font-size:{CAP_FS}px; line-height:1.18; text-transform:uppercase; letter-spacing:.01em; text-shadow:0 {sc(6)}px {sc(18)}px rgba(0,0,0,.65); }}
  .cap .k {{ color:{RED}; }}
"""

def build_chapter(cid, a, b, chip):
    beats = B[a - 1:b]
    t0 = beats[0].s
    dur = round(beats[-1].e - t0, 3)
    html, js = [], []
    z = 0
    if chip:
        html.append(f'<div class="abs clip" id="{cid}-chip" data-start="0" data-duration="{dur}" data-track-index="9" '
                    f'style="left:0;width:{W}px;top:{CHIP_Y - sc(40)}px;height:{sc(90)}px;display:flex;justify-content:center;z-index:20">'
                    f'<div class="chip">{chip}</div></div>')
        js.append(f'tl.fromTo("#{cid}-chip",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:.4,ease:"back.out(1.6)"}},0);')
        js.append(f'tl.to("#{cid}-chip",{{opacity:0,duration:.2,ease:"power2.in"}},{dur - 0.22});')
    for bt in beats:
        ls, d = round(bt.s - t0, 3), round(bt.e - bt.s, 3)
        le = round(ls + d, 3)
        for i, it in enumerate(bt.items):
            eid = f'{cid}-b{bt.n}-i{i}'
            if it['k'] == 'img':
                iw, ih = SIZE[it['name']]
                if it['h']: hh = sc(it['h']); ww = hh * iw / ih
                else: ww = sc(it['w']); hh = ww * ih / iw
                fade = ' fade' if it['name'].endswith('_head') else ''
                inner = f'<img class="pic{fade}" id="{eid}-p" src="assets/img/{it["name"]}.png" alt="">'
                bw, bh = ww, hh
            else:
                bw, bh = sc(it['w']), sc(it['h'])
                inner = fill(it['html'])
            zt = (CHIP_Y + sc(95)) if chip else sc(215 if FORMAT == 'vertical' else 40)
            zb = CAP_Y - sc(125) if FORMAT == 'vertical' else 835
            if it['k'] == 'img' and bh > zb - zt:       # image trop haute pour la zone libre : on la réduit
                f = (zb - zt) / bh; bw, bh = bw * f, bh * f
            cy_i = min(max(CY + it['dy'] * U, zt + bh / 2), zb - bh / 2)
            left = CX + it['dx'] * U * XS - bw / 2
            top = cy_i - bh / 2
            html.append(f'<div class="item clip {it.get("cls","")}" id="{eid}" data-start="{ls}" data-duration="{d}" '
                        f'data-track-index="{1 + i}" style="left:{left:.0f}px;top:{top:.0f}px;width:{bw:.0f}px;height:{bh:.0f}px;z-index:{it["z"]}">{inner}</div>')
            st = round(ls + it['delay'], 3)
            r = it['rot']
            e = it['enter']
            fr = {'pop': 'opacity:0,scale:.55,y:40', 'left': 'opacity:0,x:-420', 'right': 'opacity:0,x:420',
                  'drop': 'opacity:0,y:-300', 'up': 'opacity:0,y:320', 'shake': 'opacity:0,scale:.5,y:60',
                  'none': 'opacity:1'}[e]
            if e == 'none':
                js.append(f'tl.set("#{eid}",{{rotation:{r}}},{st});')
            else:
                ease = 'back.out(1.6)' if e in ('pop', 'shake', 'drop') else 'power3.out'
                js.append(f'tl.fromTo("#{eid}",{{{fr},rotation:{r}}},{{opacity:1,scale:1,x:0,y:0,rotation:{r},duration:.42,ease:"{ease}"}},{st});')
            if e == 'shake':
                js.append(f'tl.to("#{eid}",{{rotation:{r + 5},duration:.07,yoyo:true,repeat:3,ease:"sine.inOut"}},{st + 0.45:.3f});')
            js.append(f'tl.to("#{eid}",{{opacity:0,scale:.94,duration:.16,ease:"power2.in"}},{le - 0.18:.3f});')
            if it['k'] == 'img' and it['drift']:
                js.append(f'tl.fromTo("#{eid}-p",{{scale:1}},{{scale:{1 + it["drift"]},duration:{d},ease:"none"}},{ls});')
        cid_cap = f'{cid}-cap{bt.n}'
        html.append(f'<div class="cap clip" id="{cid_cap}" data-start="{ls}" data-duration="{d}" data-track-index="10" '
                    f'style="top:{CAP_Y - sc(95)}px;z-index:30{";font-size:%dpx" % int(CAP_FS*0.82) if len(re.sub(chr(91)+chr(91)+"|"+chr(93)+chr(93),"",bt.cap))>58 else ""}">{cap_html(bt.cap)}</div>')
        if bt.n != 1:
            js.append(f'tl.fromTo("#{cid_cap}",{{opacity:0,y:34}},{{opacity:1,y:0,duration:.22,ease:"power3.out"}},{ls});')
        js.append(f'tl.to("#{cid_cap}",{{opacity:0,duration:.12,ease:"power2.in"}},{le - 0.14:.3f});')
        # animations propres à un beat
        if bt.n == 3:
            js.append(f'tl.fromTo("#{cid}-b3-i0 .dash",{{x:0}},{{x:{-sc(280)},duration:{d},ease:"none"}},{ls});')
        if bt.n == 14:
            js.append(f'tl.to("#ringfill",{{strokeDashoffset:0,duration:{min(2.0, d - .5):.2f},ease:"power2.out"}},{ls + .3:.2f});')
        if bt.n == 21:
            js.append(f'tl.fromTo("#barfill",{{scaleX:0}},{{scaleX:1,duration:{min(2.4, d - .8):.2f},ease:"power2.out"}},{ls + .3:.2f});')
        if bt.n == 27:
            js.append(f'tl.fromTo("#bar1",{{scaleY:0}},{{scaleY:1,duration:.6,ease:"power3.out"}},{ls + .25:.2f});')
            js.append(f'tl.fromTo("#bar2",{{scaleY:0}},{{scaleY:1,duration:.6,ease:"power3.out"}},{ls + 1.0:.2f});')
        if bt.n == 37:
            js.append(f'tl.fromTo("#{cid}-b37-i0-p",{{rotation:0}},{{rotation:7,duration:.09,yoyo:true,repeat:7,ease:"sine.inOut"}},{ls + .5:.2f});')
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

stars = ''.join(
    f'<i style="left:{(i * 137) % 100}%;top:{(i * 71) % 100}%;width:{2 + i % 3}px;height:{2 + i % 3}px;opacity:{.25 + (i % 5) / 10:.2f}"></i>'
    for i in range(70))

index = f"""<!doctype html>
<html lang="it">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0b0b2e; }}
      #bg {{ position:absolute; inset:0; background:
        radial-gradient(ellipse 90% 45% at 50% 100%, rgba(20,200,180,.42), transparent 70%),
        radial-gradient(ellipse 80% 50% at 15% 0%, rgba(120,70,200,.35), transparent 70%),
        linear-gradient(180deg,#0e0d38 0%,#15125a 55%,#0a1f4a 100%); }}
      #stars {{ position:absolute; inset:0; }}
      #stars i {{ position:absolute; border-radius:50%; background:#fff; }}
      #glow {{ position:absolute; left:0; right:0; bottom:0; height:35%; background:radial-gradient(ellipse 70% 100% at 50% 100%, rgba(30,220,190,.30), transparent 70%); }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" style="position:absolute;inset:0;font-family:Montserrat,sans-serif">
      <div id="bg"></div>
      <div id="stars">{stars}</div>
      <div id="glow"></div>
{chr(10).join(hosts)}
      <audio id="voce" src="assets/voce.wav" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#glow", {{ opacity: .55 }}, {{ opacity: 1, duration: {TOTAL}, ease: "none" }}, 0);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)
for f in ('hyperframes.json',):
    open(os.path.join(OUT, f), 'w').write('{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",\n  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},\n  "media": {"autoProxy": true}\n}\n')
open(os.path.join(OUT, 'meta.json'), 'w').write('{"id": "camionista-%s", "name": "La tua vita dopo 15 anni da camionista (%s)"}' % (FORMAT, FORMAT))
print('ok', FORMAT, W, H)
