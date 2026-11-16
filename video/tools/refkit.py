"""refkit — moteur « style Thomas » (références A/B) pour HyperFrames.
Fond bleu nuit + grille + étoiles, sous-titres 1–4 mots, cartes d'interface animées, poussées de scènes,
voix seule + petits sons d'interface.  Usage : voir build_pilota.py
"""
import os, re, json, shutil, difflib, math, zlib, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W, H = 1920, 1080
RED, GOLD, GREEN, SLATE, GREY = '#F84858', '#E8B828', '#28C868', '#6f7bff', '#9aa6e8'
OVER = 0.34
CAP_Y = 915
CFG = {}
BEATS, STAGES, SFXLOG = [], [], []
SIZE = {}
TOTAL = 0.0
norm = lambda t: re.sub(r"[^\w]", "", t.lower().replace("l'", "l").replace("'", ""))

# ------------------------------------------------------------------ temps / mots
class Beat: pass

def init(script, words_json, srt, voice_norm, out, cut_dirs, total, numw=''):
    global BEATS, TOTAL, CFG
    CFG = dict(out=out, voice=voice_norm, cut=cut_dirs)
    for cd in cut_dirs:
        for f in os.listdir(cd):
            if f.endswith('.png') and f[:-4] not in SIZE:
                w, h = Image.open(os.path.join(cd, f)).size; k = min(1.0, 1100 / max(w, h)); SIZE[f[:-4]] = (max(1, round(w * k)), max(1, round(h * k)))
    TOTAL = total
    SC = []
    for blk in open(srt, encoding='utf-8').read().strip().split('\n\n'):
        l = blk.split('\n'); a, b = l[1].split(' --> ')
        f = lambda s: int(s[:2]) * 3600 + int(s[3:5]) * 60 + int(s[6:8]) + int(s[9:]) / 1000
        SC.append((f(a), f(b), ' '.join(l[2:])))
    NUMW = set(numw.split())
    WW = [[d['w'], d['s'], d['e']] for d in json.load(open(words_json))]
    swords = [w for l in open(script, encoding='utf-8') if l.strip() for w in l.split()]
    st = ['NUM' if norm(w) in NUMW else norm(w) for w in swords]
    wt = ['NUM' if re.fullmatch(r'[\d.,]+', w[0]) else norm(w[0]) for w in WW]
    sm = difflib.SequenceMatcher(None, st, wt, autojunk=False)
    TW = [None] * len(swords)
    for b in sm.get_matching_blocks():
        for k in range(b.size): TW[b.a + k] = (WW[b.b + k][1], WW[b.b + k][2])
    known = [i for i, x in enumerate(TW) if x]
    for i in range(len(TW)):
        if TW[i] is None:
            p = max([j for j in known if j < i], default=None); n = min([j for j in known if j > i], default=None)
            if p is None: TW[i] = (0.0, 0.2)
            elif n is None: TW[i] = (TW[p][1], TW[p][1] + .3)
            else:
                fr = (i - p) / (n - p); t = TW[p][1] + (TW[n][0] - TW[p][1]) * fr; TW[i] = (t, t + .25)
    _p = 0.0
    for i in range(len(TW)):
        a, b = TW[i]; a = max(a, _p); b = max(b, a + .12); TW[i] = (a, b); _p = a + .01
    cum = 0
    for k, (s, e, text) in enumerate(SC, 1):
        b = Beat(); b.n, b.text = k, text; nw = len(text.split())
        b.words = [(swords[cum + i], TW[cum + i][0], TW[cum + i][1]) for i in range(nw)]; cum += nw
        BEATS.append(b)
    assert cum == len(swords), (cum, len(swords))
    for i, b in enumerate(BEATS): b.s = 0.0 if i == 0 else b.words[0][1]
    for i, b in enumerate(BEATS): b.e = BEATS[i + 1].s if i + 1 < len(BEATS) else round(b.words[-1][2] + .5, 3)

def T(beat, word=None, off=0.0):
    b = BEATS[beat - 1]
    if word is None: return round(b.s + off, 3)
    k = norm(word)
    for w, t0, t1 in b.words:
        if norm(w).startswith(k): return round(max(b.s, t0) + off, 3)
    for w, t0, t1 in b.words:
        if len(k) >= 4 and k in norm(w): return round(max(b.s, t0) + off, 3)
    for w, t0, t1 in b.words:
        for part in re.split("[']", w):
            if norm(part).startswith(k) and len(k) >= 2: return round(max(b.s, t0) + off, 3)
    raise SystemExit(f'mot introuvable: {word!r} dans le plan {beat}: {b.text}')

PING_K = 0.72      # niveau relatif des pings d'interface
def sfx(t, name, vol=.3):
    SFXLOG.append((round(t, 3), name, vol if name.startswith('R_') else round(vol * PING_K, 3)))
def real(t, name, vol=.22):
    """son réel de la bibliothèque (shorts / vidéo HVAC), en renfort à volume bas"""
    sfx(t, 'R_' + name, vol)
_rot = {'pop': 0}
def pop_sfx(t, vol=.28):
    seq = ['ping_a', 'ping_b', 'ping_c', 'tick']; sfx(t, seq[_rot['pop'] % 4], vol); _rot['pop'] += 1

# ------------------------------------------------------------------ scène
def fmtn(n): return f'{int(round(n)):,}'.replace(',', '.')

class Stage:
    def __init__(self, sid, b0, b1, push='right'):
        self.id, self.b0, self.b1, self.push = sid, b0, b1, push
        self.t0 = BEATS[b0 - 1].s; self.t1 = BEATS[b1 - 1].e
        self.items, self.js, self.n = [], [], 0
    def _id(self, p): self.n += 1; return f'{self.id}-{p}{self.n}'
    def rel(self, t): return round(t - self.t0, 3)
    def J(self, t, code): self.js.append((self.rel(t), code))
    # ---- primitives
    def item(self, html, cx, cy, w, h, at=None, until=None, enter='pop', z=4, rot=0, snd='pop', cls='', anchor='c', k=1.0):
        iid = self._id('x')
        self.items.append(dict(id=iid, html=html, cx=cx, cy=cy, w=w, h=h, at=self.t0 if at is None else at, until=until,
                               enter=enter, z=z, rot=rot, snd=snd, cls=cls, k=k))
        return iid
    def img(self, name, cx, cy, h=None, w=None, at=None, until=None, enter='pop', z=3, rot=0, snd=None, breathe=False):
        iw, ih = SIZE[name]
        if h: ww, hh = h * iw / ih, h
        else: ww, hh = w, w * ih / iw
        html = f'<img class="pic" src="assets/img/{name}.png" alt="" style="width:100%;height:100%;object-fit:contain">'
        iid = self.item(html, cx, cy, ww, hh, at, until, enter, z, rot, snd, 'ipic')
        if breathe or re.match(r'(rocco|elia|pose|walk)_', name):
            a = self.t0 if at is None else at
            span = (until or self.t1 + OVER) - a
            self.J(a + .45, f'tl.fromTo("#{iid} img",{{scaleY:1,transformOrigin:"50% 100%"}},{{scaleY:1.016,duration:1.5,ease:"sine.inOut",yoyo:true,repeat:{int(span / 1.5) + 1}}},{self.rel(a + .45):.3f});')
        return iid
    def pose(self, seq, cx, cy, h, at=None, until=None, enter='left'):
        """poses successives (coupe franche) : seq = [(nom, instant), ...]"""
        end = until
        for k, (nm, t) in enumerate(seq):
            nxt = seq[k + 1][1] if k + 1 < len(seq) else end
            self.img(nm, cx, cy, h=h, at=t, until=nxt, enter=enter if k == 0 else 'cut')
    def walker(self, frames, x0, x1, cy, h, at, dur, until=None, step=.16):
        """cycle de marche : plusieurs images alternées pendant un déplacement linéaire"""
        iw, ih = SIZE[frames[0]]; ww = h * iw / ih
        inner = ''.join(f'<img src="assets/img/{f}.png" class="wf" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:contain;opacity:{1 if i == 0 else 0}">' for i, f in enumerate(frames))
        iid = self.item(inner, x0, cy, ww, h, at, until or at + dur + .3, 'none', 3, 0, None, 'walker')
        self.J(at, f'tl.fromTo("#{iid}",{{x:0}},{{x:{x1 - x0},duration:{dur},ease:"none"}},{self.rel(at):.3f});')
        k = 0; t = at
        while t < at + dur:
            idx = k % len(frames)
            for j in range(len(frames)):
                self.J(t, f'tl.set("#{iid} .wf:nth-child({j + 1})",{{opacity:{1 if j == idx else 0}}},{self.rel(t):.3f});')
            k += 1; t += step
    def chip(self, text, cx, cy, at=None, until=None, color='slate', size=34, enter='pop', z=6):
        size = int(size * 1.42)
        w = int(len(text) * size * .62 + size * 1.7)
        cols = {'slate': ('rgba(120,135,255,.22)', 'rgba(150,165,255,.55)', '#fff'), 'gold': ('rgba(232,184,40,.20)', GOLD, '#FFE08A'),
                'red': ('rgba(248,72,88,.22)', RED, '#FF9AA6'), 'green': ('rgba(40,200,104,.22)', GREEN, '#9BF0BD')}
        bg, bd, fg = cols[color]
        html = f'<div class="chip" style="font-size:{size}px;background:{bg};border-color:{bd};color:{fg}">{text}</div>'
        return self.item(html, cx, cy, w, int(size * 1.9), at, until, enter, z)
    def stamp(self, text, cx, cy, at=None, until=None, size=64, rot=-7, color=RED, z=8):
        w = int(len(text) * size * .78 + 70)
        html = f'<div class="stamp" style="font-size:{size}px;color:{color};border-color:{color}">{text}</div>'
        iid = self.item(html, cx, cy, w, int(size * 1.9), at, until, 'stamp', z, rot, None, k=1.2)
        a = self.t0 if at is None else at
        sfx(a, 'ding', .3); real(a, 'stamp', .26); return iid
    def badge(self, kind, cx, cy, at, size=96, until=None, z=9):
        sym, col = ('✓', GREEN) if kind == 'ok' else ('✕', RED)
        html = f'<div class="badge" style="background:{col};box-shadow:0 0 26px {col}"><span style="font-size:{int(size * .56)}px;color:{'#08301A' if kind == 'ok' else '#fff'}">{sym}</span></div>'
        sfx(at, 'ping_b' if kind == 'ok' else 'no', .3)
        return self.item(html, cx, cy, size, size, at, until, 'pop', z, 0, None)
    def card(self, cx, cy, w, h, inner, at=None, until=None, enter='pop', z=4, pad=30, cls='', k=1.22):
        html = f'<div class="card {cls}" style="padding:{pad}px">{inner}</div>'
        return self.item(html, cx, cy, w, h, at, until, enter, z, k=k)
    # ---- compteurs
    def counter(self, cx, cy, frm, to, at, fmt='{n}', size=130, color=GOLD, sub='', dur=1.1, until=None, w=700, z=5):
        nid = self._id('n')
        html = (f'<div class="num" id="{nid}-v" style="font-size:{size}px;color:{color}">{fmt.replace("{n}", fmtn(frm))}</div>' +
                (f'<div class="sub" style="font-size:{int(size * .3)}px">{sub}</div>' if sub else ''))
        self.item(html, cx, cy, w, int(size * 1.35 + (int(size * .4) if sub else 0)), at, until, 'pop', z, 0, None, k=1.15)
        self.count_js(f'{nid}-v', frm, to, fmt, at + .08, dur)
        return nid
    def count_js(self, el, frm, to, fmt, t, dur):
        f = fmt.replace("'", "\\'")
        self.J(t, f'(function(){{var o={{v:{frm}}},el=document.getElementById("{el}");tl.fromTo(o,{{v:{frm}}},{{v:{to},duration:{dur},ease:"power2.out",onUpdate:function(){{'
                  f'var n=Math.round(o.v),s=String(n).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,".");el.textContent=\'{f}\'.replace("{{n}}",s);}}}},{self.rel(t):.3f});}})();')
        d = min((0.8, 1.1, 1.4), key=lambda x: abs(x - dur)); sfx(t, f'count_{d}', .22); sfx(t + dur, 'ding', .26)
        if '€' in fmt: real(t + dur - .1, 'cash-register', .2); real(t + .05, 'coins-drop', .12)
    def range_card(self, title, rows, cx, cy, w=640, at=None, until=None, icon=None):
        """rows = [dict(label, frm, to, fmt, color, at, dur)] ; ligne = libellé + valeur qui compte"""
        rh = 116; h = 140 + rh * len(rows)
        pid = self._id('r')
        head = f'<div class="ctitle">{(icon or "")}{title}</div>'
        body = ''
        for j, r in enumerate(rows):
            vid = f'{pid}-v{j}'
            body += (f'<div class="crow" id="{pid}-r{j}"><span class="cl">{r["label"]}</span>'
                     f'<span class="cv" id="{vid}" style="color:{r.get("color", "#fff")}">{r["fmt"].replace("{n}", fmtn(r.get("frm", 0)))}</span></div>')
        self.card(cx, cy, w, h, head + body, at, until)
        for j, r in enumerate(rows):
            t = r.get('at', at if at is not None else self.t0)
            self.count_js(f'{pid}-v{j}', r.get('frm', 0), r['to'], r['fmt'], t + .1, r.get('dur', 1.0))
            if j and r.get('at') and r['at'] > (at or self.t0) + .2:
                self.J(r['at'] - .05, f'tl.fromTo("#{pid}-r{j}",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.3,ease:"expo.out"}},{self.rel(r["at"] - .05):.3f});')
                self.js.insert(0, (0, f'tl.set("#{pid}-r{j}",{{opacity:0}},0);'))
        return pid
    def toggles(self, title, items, cx, cy, w=640, at=None, until=None):
        """items = [(label, instant, 'on'|'off')]"""
        rh = 108; h = 130 + rh * len(items); pid = self._id('t')
        body = f'<div class="ctitle">{title}</div>'
        for j, (lab, t, st) in enumerate(items):
            body += f'<div class="crow"><span class="cl">{lab}</span><span class="tg" id="{pid}-g{j}"><i id="{pid}-k{j}"></i></span></div>'
        self.card(cx, cy, w, h, body, at, until)
        for j, (lab, t, st) in enumerate(items):
            col = GREEN if st == 'on' else RED
            self.J(t, f'tl.to("#{pid}-g{j}",{{backgroundColor:"{col}",duration:.2,ease:"power2.out"}},{self.rel(t):.3f});'
                      f'tl.to("#{pid}-k{j}",{{x:{44 if st == "on" else 0},duration:.2,ease:"back.out(2)"}},{self.rel(t):.3f});')
            sfx(t, 'ping_b' if st == 'on' else 'no', .26)
        return pid
    def tiles(self, n, cols, cx, cy, size, gap, at, times, labels=None, until=None, title=None, color=GREEN, final=None):
        """grille de n cases qui se cochent aux instants `times`"""
        rows = (n + cols - 1) // cols
        gw, gh = cols * size + (cols - 1) * gap, rows * size + (rows - 1) * gap
        pid = self._id('g'); cells = ''
        for i in range(n):
            lab = f'<small>{labels[i]}</small>' if labels else f'<small>{i + 1}</small>'
            cells += f'<div class="tl" id="{pid}-c{i}" style="width:{size}px;height:{size}px">{lab}<b id="{pid}-k{i}" data-layout-allow-overlap>✓</b></div>'
        inner = f'<div class="ctitle">{title}</div>' if title else ''
        inner += f'<div class="tgrid" style="grid-template-columns:repeat({cols},{size}px);gap:{gap}px">{cells}</div>'
        hh = gh + 70 + (70 if title else 0)
        self.card(cx, cy, gw + 70, hh, inner, at, until, pad=30)
        for i, t in enumerate(times[:n]):
            self.J(t, f'tl.fromTo("#{pid}-k{i}",{{opacity:0,scale:.2}},{{opacity:1,scale:1,duration:.28,ease:"back.out(2.4)"}},{self.rel(t):.3f});'
                      f'tl.to("#{pid}-c{i} small",{{opacity:0,duration:.15}},{self.rel(t):.3f});'
                      f'tl.to("#{pid}-c{i}",{{backgroundColor:"{color}",duration:.2}},{self.rel(t):.3f});')
            sfx(t, 'tick' if i % 2 else 'ping_b', .22)
        if final:
            tf, colf = final
            for i in range(n):
                self.J(tf, f'tl.to("#{pid}-c{i}",{{backgroundColor:"{colf}",duration:.25}},{self.rel(tf):.3f});')
            sfx(tf, 'no', .3)
        return pid
    def progress(self, title, cx, cy, w, frm, to, at, dur, left='', right='', color=GOLD, until=None, fmt='{n}', unit='', suffix_marks=None, bigcount=True):
        pid = self._id('p')
        inner = (f'<div class="ctitle">{title}</div><div class="pbar"><div class="pfill" id="{pid}-f" style="background:linear-gradient(90deg,{color},#fff)"></div></div>'
                 f'<div class="plab"><span>{left}</span><span id="{pid}-v" style="color:{color};font-weight:900">{fmt.replace("{n}", fmtn(frm))}{unit}</span><span>{right}</span></div>')
        self.card(cx, cy, w, 250, inner, at, until)
        self.js.insert(0, (0, f'tl.set("#{pid}-f",{{scaleX:{frm / max(to, 1):.3f},transformOrigin:"0 50%"}},0);'))
        self.J(at + .15, f'tl.to("#{pid}-f",{{scaleX:1,duration:{dur},ease:"power2.out"}},{self.rel(at + .15):.3f});')
        self.count_js(f'{pid}-v', frm, to, fmt + unit.replace('{', '{{'), at + .15, dur)
        return pid
    def ecg(self, cx, cy, w, at, until=None, title='Visita di prima classe', status=None):
        pid = self._id('e'); hh = 330
        path = 'M0 120 L70 120 L95 120 L115 60 L135 190 L155 20 L180 150 L205 120 L300 120 L325 120 L345 60 L365 190 L385 20 L410 150 L435 120 L540 120'
        inner = (f'<div class="ctitle">♥ {title}</div><svg viewBox="0 0 540 210" class="ecg" style="width:100%;height:{hh - 160}px">'
                 f'<path id="{pid}-p" d="{path}" pathLength="1" fill="none" stroke="{GREEN}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" '
                 f'style="stroke-dasharray:1;stroke-dashoffset:1;filter:drop-shadow(0 0 8px {GREEN})"/></svg>'
                 f'<div class="chip" id="{pid}-s" style="font-size:30px;background:rgba(232,184,40,.2);border-color:{GOLD};color:#FFE08A;margin:6px auto 0">In corso…</div>')
        self.card(cx, cy, w, hh, inner, at, until)
        a = at + .2; dur = (until or self.t1) - a; real(a, 'heartbeat', .22)
        reps = max(1, int(dur / 1.8))
        self.J(a, f'tl.fromTo("#{pid}-p",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.4,ease:"none",repeat:{reps},repeatDelay:.3}},{self.rel(a):.3f});')
        if status:
            t, txt, col = status
            bgc, fgc = ('rgba(40,200,104,.25)', '#9BF0BD') if col == GREEN else ('rgba(248,72,88,.25)', '#FF9AA6')
            self.J(t, f'(function(){{var e=document.getElementById("{pid}-s");tl.call(function(){{e.textContent="{txt}";e.style.background="{bgc}";e.style.borderColor="{col}";e.style.color="{fgc}";}},null,{self.rel(t):.3f});'
                      f'tl.fromTo(e,{{scale:1}},{{scale:1.2,duration:.12,yoyo:true,repeat:1}},{self.rel(t):.3f});}})();')
            sfx(t, 'no' if col != GREEN else 'ping_b', .3)
        return pid
    def bubble(self, text, cx, cy, at, until=None, size=40, dots=False, who='', tail='down'):
        w = int(max(len(text), 6) * size * .56 + 90)
        inner = (f'<div class="who">{who}</div>' if who else '') + f'<div style="font-size:{size}px;font-weight:800">{text}</div>'
        html = f'<div class="bub {tail}">{inner}</div>'
        return self.item(html, cx, cy, w, int(size * 1.6 + (40 if who else 0) + 40), at, until, 'pop', 6, k=1.2)
    def subcard(self, cx, cy, at, t_click, avatar='head_38', until=None, thumbs=('', '', '')):
        pid = self._id('s'); w, h = 560, 760
        inner = (f'<div class="phone"><div class="pn">12:09</div><div class="av"><img src="assets/img/{avatar}.png"></div>'
                 f'<div class="pt">Spiegato da<br>Professione Reale</div><div class="ps">I tuoi mestieri, in pochi minuti</div>'
                 f'<div class="pbtn" id="{pid}-b">Iscriviti</div><div class="pth">'
                 + ''.join(f'<div class="tn" id="{pid}-t{k}"><i>▶</i></div>' for k in range(3)) + '</div></div>')
        self.item(inner, cx, cy, w, h, at, until, 'up', 6)
        self.js.insert(0, (0, ''.join(f'tl.set("#{pid}-t{k}",{{opacity:0,y:24}},0);' for k in range(3))))
        self.J(t_click, f'tl.fromTo("#{pid}-b",{{scale:1}},{{scale:.92,duration:.1,yoyo:true,repeat:1}},{self.rel(t_click):.3f});'
                        f'tl.to("#{pid}-b",{{backgroundColor:"{GREEN}",color:"#fff",duration:.2}},{self.rel(t_click + .12):.3f});'
                        f'tl.call(function(){{document.getElementById("{pid}-b").textContent="✓ Iscritto";}},null,{self.rel(t_click + .12):.3f});')
        for k in range(3):
            self.J(t_click + .45 + k * .18, f'tl.to("#{pid}-t{k}",{{opacity:1,y:0,duration:.3,ease:"back.out(1.8)"}},{self.rel(t_click + .45 + k * .18):.3f});')
        sfx(t_click, 'subscribe', .32); real(t_click, 'notif', .22)
    def title(self, line1, line2, at, until=None, cy=470):
        iid = self._id('ti')
        html = (f'<div class="ttl"><div class="t1" id="{iid}-a">{line1}</div><div class="t2" id="{iid}-b">{line2}</div></div>')
        self.item(html, W // 2, cy, 1500, 330, at, until, 'none', 8)
        self.J(at, f'tl.fromTo("#{iid}-a",{{opacity:0,scaleX:1.35,filter:"blur(8px)"}},{{opacity:1,scaleX:1,filter:"blur(0px)",duration:.9,ease:"power2.out"}},{self.rel(at):.3f});'
                   f'tl.fromTo("#{iid}-b",{{opacity:0,scale:.82,filter:"blur(12px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.7,ease:"back.out(1.6)"}},{self.rel(at + .45):.3f});')
        sfx(at, 'title_sweep', .3); real(at, 'whoosh-deep', .2)
    def plane(self, name, y0, y1, at, dur, h=260, until=None):
        iw, ih = SIZE[name]; ww = h * iw / ih
        iid = self.item(f'<img src="assets/img/{name}.png" style="width:100%;height:100%;object-fit:contain">', -ww / 2, y0, ww, h, at, until or at + dur + .3, 'none', 2)
        self.J(at, f'tl.fromTo("#{iid}",{{x:0,y:0}},{{x:{W + ww},y:{y1 - y0},duration:{dur},ease:"power1.inOut"}},{self.rel(at):.3f});')
        sfx(at, 'push', .12); real(at, 'whoosh-deep', .12)
    def arrow(self, cx, cy, at, up=True, size=130, until=None):
        col = GREEN if up else RED
        self.item(f'<div class="arrow" style="font-size:{size}px;color:{col};text-shadow:0 0 28px {col}">{"▲" if up else "▼"}</div>', cx, cy, size * 1.3, size * 1.3, at, until, 'pop', 6)
        sfx(at, 'ping_a' if up else 'no', .26)


    # ================= v2 : composants supplémentaires =================
    def wiggle(self, iid, t, amp=6, n=5):
        self.J(t, f'tl.to("#{iid}",{{rotation:{amp},duration:.06,yoyo:true,repeat:{n},ease:"sine.inOut"}},{self.rel(t):.3f});')
    def connect(self, x1, y1, x2, y2, at, until=None, color='rgba(190,200,255,.55)', dur=.4, width=3, dot=True):
        iid = self._id('ln')
        svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0;overflow:visible">'
               f'<path id="{iid}-p" d="M{x1} {y1} L{x2} {y2}" pathLength="1" stroke="{color}" stroke-width="{width}" stroke-linecap="round" fill="none" style="stroke-dasharray:1;stroke-dashoffset:1"/>'
               + (f'<circle id="{iid}-d" cx="{x2}" cy="{y2}" r="7" fill="#fff" opacity="0"/>' if dot else '') + '</svg>')
        self.items.append(dict(id=iid, html=svg, cx=W / 2, cy=H / 2, w=W, h=H, at=self.t0 if at is None else at, until=until, enter='none', z=2, rot=0, snd=None, cls='lines', k=1.0))
        self.J(at, f'tl.fromTo("#{iid}-p",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.out"}},{self.rel(at):.3f});')
        if dot: self.J(at + dur - .05, f'tl.to("#{iid}-d",{{opacity:1,duration:.12}},{self.rel(at + dur - .05):.3f});')
    def radial(self, cx, cy, nodes, at, until=None, color='slate', size=30):
        """nœuds reliés à un centre par un trait fin : nodes = [(libellé, dx, dy, instant, couleur)]"""
        for (lab, dx, dy, t, col) in nodes:
            self.connect(cx, cy, cx + dx, cy + dy, t - .05, until, dur=.35)
            self.chip(lab, cx + dx, cy + dy, t, until, color=col or color, size=size)
    def typed(self, cx, cy, w, h, title, kicker, b0, b1, at, until=None, paper=True, hl=(), size=40, signature=None):
        """document dont le texte se tape mot par mot, calé sur la voix ; hl = mots surlignés en jaune"""
        pid = self._id('d')
        words = [x for b in range(b0, b1 + 1) for x in BEATS[b - 1].words]
        spans = ''
        for j, (wd, t0, t1) in enumerate(words):
            cls = 'dw hl' if norm(wd) in {norm(x) for x in hl} else 'dw'
            spans += f'<span class="{cls}" id="{pid}-w{j}">{wd} </span>'
        cls = 'paper' if paper else 'mail'
        inner = (f'<div class="{cls}"><div class="dk">{kicker}</div><div class="dt">{title}</div>'
                 f'<div class="dbody" style="font-size:{size}px">{spans}</div>' + (f'<div class="dsig">{signature}</div>' if signature else '') + '</div>')
        self.item(inner, cx, cy, w, h, at, until, 'pop', 5, 0, 'R_paper-slide', 'doc')
        self.js.insert(0, (0, f'tl.set("#{pid} .dw",{{opacity:0}},0);'))
        for j, (wd, t0, t1) in enumerate(words):
            self.J(t0, f'tl.set("#{pid}-w{j}",{{opacity:1}},{self.rel(t0):.3f});')
            if j % 3 == 0: sfx(t0, 'tick', .12)
        sfx(at, 'ping_b', .2)
        return pid
    def chart(self, cx, cy, w, h, title, pts, at, until=None, labels=None, fmt='{n} €'):
        """courbe qui se trace ; pts = [(instant, valeur)] ; valeurs normalisées sur le max"""
        pid = self._id('c'); pw, ph = 500, 250
        vmax = max(v for _, v in pts); t0, t1 = pts[0][0], pts[-1][0]
        xs = [(t - t0) / max(t1 - t0, .01) * (pw - 60) + 30 for t, _ in pts]; ys = [ph - 30 - v / vmax * (ph - 70) for _, v in pts]
        d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in zip(xs, ys))
        grid = ''.join(f'<line x1="30" y1="{ph - 30 - k * (ph - 70) / 3:.0f}" x2="{pw - 20}" y2="{ph - 30 - k * (ph - 70) / 3:.0f}" stroke="rgba(150,165,255,.18)" stroke-width="2"/>' for k in range(4))
        dots = ''.join(f'<circle id="{pid}-p{i}" cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{GOLD}" opacity="0"/>' for i, (x, y) in enumerate(zip(xs, ys)))
        svg = (f'<svg viewBox="0 0 {pw} {ph}" style="width:100%;height:{h - 150}px">{grid}<path id="{pid}-l" d="{d}" pathLength="1" fill="none" stroke="url(#g{pid})" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:1;stroke-dashoffset:1;filter:drop-shadow(0 0 8px {GOLD})"/>'
               f'<defs><linearGradient id="g{pid}" x1="0" x2="1"><stop offset="0" stop-color="#ffd166"/><stop offset="1" stop-color="#ff8a5c"/></linearGradient></defs>{dots}</svg>')
        inner = f'<div class="ctitle">{title}</div>{svg}<div class="cv" id="{pid}-v" style="color:{GOLD};text-align:right;font-size:60px">{fmt.replace("{n}", fmtn(pts[0][1]))}</div>'
        self.card(cx, cy, w, h, inner, at, until)
        self.J(t0, f'tl.fromTo("#{pid}-l",{{strokeDashoffset:1}},{{strokeDashoffset:0,duration:{max(t1 - t0, .5)},ease:"none"}},{self.rel(t0):.3f});')
        for i, (t, v) in enumerate(pts):
            self.J(t, f'tl.to("#{pid}-p{i}",{{opacity:1,duration:.2}},{self.rel(t):.3f});')
            self.count_js(f'{pid}-v', pts[i - 1][1] if i else v, v, fmt, t, .5) if i else None
        return pid
    def compare(self, cx, cy, w, left, right, imgl, imgr, at, until=None, stamp_t=None, stamp_txt='✗ Rifiutato'):
        pid = self._id('v'); ph = 270
        panel = lambda lab, im: (f'<div class="cp"><img src="assets/img/{im}.png"><small>{lab}</small></div>')
        inner = f'<div class="cmp">{panel(left, imgl)}{panel(right, imgr)}</div><div class="chip" id="{pid}-s" style="opacity:0;position:absolute;left:50%;top:50%;margin-left:-150px;margin-top:-40px;font-size:40px;background:rgba(248,72,88,.9);border-color:#fff;color:#fff;transform:rotate(-9deg)">{stamp_txt}</div>'
        self.card(cx, cy, w, ph + 130, inner, at, until)
        if stamp_t:
            self.J(stamp_t, f'tl.fromTo("#{pid}-s",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:.2,ease:"power4.in"}},{self.rel(stamp_t):.3f});')
            real(stamp_t, 'stamp', .3)
        return pid
    def viewfinder(self, cx, cy, w, h, img, at, flash_t, until=None):
        pid = self._id('f')
        inner = (f'<div class="vf"><img src="assets/img/{img}.png"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i>'
                 f'<div class="shut"></div><div class="flash" id="{pid}-f"></div></div>')
        self.item(inner, cx, cy, w, h, at, until, 'pop', 5)
        self.J(flash_t, f'tl.fromTo("#{pid}-f",{{opacity:0}},{{opacity:.95,duration:.06,yoyo:true,repeat:1}},{self.rel(flash_t):.3f});')
        real(flash_t, 'camera-shutter', .3)
    def idcard(self, cx, cy, w, name, role, avatar, at, until=None, stripes=0):
        inner = (f'<div class="idc"><div class="ph"><img src="assets/img/{avatar}.png"></div><div class="tx"><b>{name}</b><span>{role}</span>'
                 + ''.join('<i></i>' for _ in range(stripes)) + '</div></div>')
        self.item(inner, cx, cy, w, int(w * .46), at, until, 'pop', 5)

# ------------------------------------------------------------------ CSS
FONTS = """
  @font-face { font-family:'Plus Jakarta Sans'; font-weight:700; src:url('assets/fonts/PlusJakartaSans-700.ttf') format('truetype'); }
  @font-face { font-family:'Plus Jakarta Sans'; font-weight:800; src:url('assets/fonts/PlusJakartaSans-800.ttf') format('truetype'); }
  @font-face { font-family:'Plus Jakarta Sans'; font-weight:900; src:url('assets/fonts/PlusJakartaSans-800.ttf') format('truetype'); }
  @font-face { font-family:'EB Garamond'; font-weight:500; src:url('assets/fonts/EBGaramond-500.ttf') format('truetype'); }
  @font-face { font-family:'EB Garamond'; font-weight:700; src:url('assets/fonts/EBGaramond-700.ttf') format('truetype'); }
"""
CSS = FONTS + """
  #root { position:absolute; inset:0; font-family:'Plus Jakarta Sans','Montserrat',sans-serif; color:#fff; }
  .stage { position:absolute; inset:0; }
  .item { position:absolute; display:flex; align-items:center; justify-content:center; }
  .item.ipic img { filter:drop-shadow(0 18px 22px rgba(0,0,0,.42)); }
  .item.walker { overflow:visible; } .item.walker img { filter:drop-shadow(0 16px 18px rgba(0,0,0,.4)); }
  .chip { display:inline-block; padding:.22em .8em; border:3px solid; border-radius:999px; font-weight:800; white-space:nowrap; letter-spacing:.01em; box-shadow:0 8px 20px rgba(0,0,0,.28); }
  .stamp { font-family:'EB Garamond','Playfair Display',serif; border:8px solid; border-radius:16px; padding:6px 24px; font-weight:900; letter-spacing:.07em; text-align:center; background:rgba(11,16,60,.55); white-space:nowrap; }
  .badge { width:100%; height:100%; border-radius:50%; display:flex; align-items:center; justify-content:center; border:5px solid rgba(255,255,255,.9); }
  .badge span { font-weight:900; color:#fff; line-height:1; }
  .card { width:100%; height:100%; box-sizing:border-box; border-radius:34px; background:linear-gradient(180deg,rgba(66,76,160,.97),rgba(38,44,118,.97));
          border:3px solid rgba(130,146,255,.38); box-shadow:0 30px 60px rgba(0,0,0,.45), inset 0 0 40px rgba(130,146,255,.10); display:flex; flex-direction:column; }
  .ctitle { font-weight:800; font-size:38px; color:#c9d0ff; letter-spacing:.04em; margin-bottom:16px; display:flex; align-items:center; gap:12px; }
  .crow { display:flex; justify-content:space-between; align-items:center; height:92px; padding:0 26px; margin-top:12px; border-radius:22px; background:rgba(14,18,72,.62); border:2px solid rgba(150,165,255,.16); }
  .cl { font-weight:800; font-size:40px; letter-spacing:.06em; color:#c0c8f6; } .cv { font-weight:900; font-size:66px; white-space:nowrap; }
  .tg { width:104px; height:52px; border-radius:99px; background:#3a3f8f; position:relative; } .tg i { position:absolute; left:6px; top:6px; width:40px; height:40px; border-radius:50%; background:#fff; }
  .tgrid { display:grid; justify-content:center; } .tl { border-radius:16px; background:rgba(14,18,72,.7); border:2px solid rgba(150,165,255,.25); position:relative; display:flex; align-items:center; justify-content:center; }
  .tl small { font-weight:800; font-size:26px; color:#aab4f5; } .tl b { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:42px; color:#fff; opacity:0; }
  .num { font-weight:900; line-height:1; letter-spacing:-.02em; text-align:center; white-space:nowrap; text-shadow:0 0 40px rgba(255,255,255,.18); }
  .sub { font-weight:800; letter-spacing:.1em; text-align:center; color:#cdd3ff; margin-top:8px; }
  .pbar { height:44px; border-radius:99px; background:#171a63; border:3px solid #6f7bff; overflow:hidden; } .pfill { width:100%; height:100%; }
  .plab { display:flex; justify-content:space-between; font-weight:800; font-size:38px; margin-top:16px; color:#c0c8f6; }
  .bub { background:#fff; color:#1b2150; padding:20px 32px; border-radius:30px; text-align:center; box-shadow:0 18px 36px rgba(0,0,0,.4); position:relative; width:100%; height:100%; box-sizing:border-box; display:flex; flex-direction:column; align-items:center; justify-content:center; }
  .bub .who { font-size:22px; letter-spacing:.14em; font-weight:800; color:#3d46a0; margin-bottom:4px; }
  .arrow { font-weight:900; line-height:1; }
  .ecg { display:block; }
  .phone { width:100%; height:100%; box-sizing:border-box; border-radius:56px; background:#fff; color:#1b2150; padding:36px 32px; text-align:center; box-shadow:0 30px 60px rgba(0,0,0,.5); border:10px solid #c9cee8; }
  .phone .pn { font-size:22px; font-weight:800; color:#8a90b8; text-align:left; }
  .phone .av { width:150px; height:150px; border-radius:50%; margin:14px auto 12px; background:#eef0ff; overflow:hidden; display:flex; align-items:flex-end; justify-content:center; }
  .phone .av img { width:150%; margin-bottom:-18%; }
  .phone .pt { font-weight:900; font-size:40px; line-height:1.15; } .phone .ps { font-size:24px; color:#6a73c8; font-weight:700; margin:8px 0 22px; }
  .phone .pbtn { display:inline-block; background:#FFC93C; color:#1b2150; font-weight:900; font-size:34px; padding:14px 46px; border-radius:99px; }
  .phone .pth { display:flex; gap:14px; justify-content:center; margin-top:30px; } .phone .tn { width:140px; height:190px; border-radius:20px; background:linear-gradient(160deg,#ff8a5c,#6f7bff); display:flex; align-items:center; justify-content:center; } .phone .tn i { color:#fff; font-style:normal; font-size:34px; }
  .ttl { width:100%; text-align:center; } .t1 { font-weight:800; font-size:44px; color:#fff; letter-spacing:.62em; padding-left:.62em; } .t2 { font-weight:900; font-size:112px; color:#E8B828; letter-spacing:.02em; margin-top:18px; text-shadow:0 0 50px rgba(232,184,40,.55); white-space:nowrap; }
  .cap { position:absolute; left:0; width:1920px; text-align:center; font-weight:800; font-size:76px; line-height:1.1; text-transform:uppercase; white-space:nowrap; text-shadow:0 6px 18px rgba(0,0,0,.6); z-index:30; letter-spacing:.005em; }
  .cap b.k { font-weight:800; color:#F84858; }
  .paper { width:100%; height:100%; box-sizing:border-box; background:#F8F5EC; color:#2a2418; border-radius:18px; padding:34px 40px; box-shadow:0 26px 54px rgba(0,0,0,.5); font-family:'EB Garamond',serif; }
  .mail { width:100%; height:100%; box-sizing:border-box; background:linear-gradient(180deg,rgba(66,76,160,.97),rgba(38,44,118,.97)); border:3px solid rgba(130,146,255,.38); border-radius:30px; padding:30px 38px; box-shadow:0 26px 54px rgba(0,0,0,.5); }
  .dk { font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:20px; letter-spacing:.16em; color:#9a8a55; text-transform:uppercase; }
  .mail .dk { color:#aab4f5; } .dt { font-weight:700; font-size:50px; margin:6px 0 14px; } .dbody { line-height:1.35; font-weight:500; }
  .mail .dt, .mail .dbody { font-family:'Plus Jakarta Sans',sans-serif; } .mail .dbody { font-weight:700; }
  .dw { transition:none; } .dw.hl { background:linear-gradient(transparent 58%, rgba(255,214,0,.65) 58%); }
  .mail .dw.hl { background:none; color:#FFD54A; } .dsig { margin-top:14px; font-style:italic; opacity:.7; }
  .cmp { display:flex; gap:20px; height:100%; } .cp { flex:1; border-radius:22px; background:rgba(14,18,72,.6); border:2px solid rgba(150,165,255,.2); display:flex; flex-direction:column; align-items:center; justify-content:center; padding:14px; }
  .cp img { max-width:90%; max-height:230px; object-fit:contain; } .cp small { margin-top:10px; font-weight:800; font-size:30px; color:#c0c8f6; }
  .vf { position:relative; width:100%; height:100%; border-radius:30px; background:#0b0e30; border:4px solid #3a3f95; overflow:hidden; display:flex; align-items:center; justify-content:center; box-shadow:0 26px 54px rgba(0,0,0,.5); }
  .vf img { max-height:80%; max-width:80%; object-fit:contain; } .vf i { position:absolute; width:46px; height:46px; border:5px solid #fff; } .vf .c1 { left:36px; top:36px; border-right:0; border-bottom:0; } .vf .c2 { right:36px; top:36px; border-left:0; border-bottom:0; }
  .vf .c3 { left:36px; bottom:36px; border-right:0; border-top:0; } .vf .c4 { right:36px; bottom:36px; border-left:0; border-top:0; } .vf .shut { position:absolute; bottom:18px; left:50%; width:44px; height:44px; margin-left:-22px; border-radius:50%; background:#fff; } .vf .flash { position:absolute; inset:0; background:#fff; opacity:0; }
  .idc { width:100%; height:100%; box-sizing:border-box; background:#fff; color:#1b2150; border-radius:26px; display:flex; gap:22px; align-items:center; padding:22px 28px; box-shadow:0 26px 54px rgba(0,0,0,.5); }
  .idc .ph { width:34%; aspect-ratio:1; border-radius:20px; background:#e8ecff; overflow:hidden; display:flex; align-items:flex-end; justify-content:center; } .idc .ph img { width:140%; margin-bottom:-14%; }
  .idc .tx { display:flex; flex-direction:column; gap:8px; } .idc .tx b { font-size:44px; } .idc .tx span { font-size:28px; color:#6a73c8; font-weight:700; } .idc .tx i { display:inline-block; width:90px; height:12px; background:#E8B828; border-radius:3px; margin-right:6px; }
"""

# ------------------------------------------------------------------ rendu d'une scène
def _unused(): pass

def build_stage(S):
    out = CFG['out']; sid = S.id
    dur = round(min(S.t1 - S.t0 + OVER, TOTAL - S.t0), 3)
    html, js = [], []
    html.append(f'<div class="stage clip" data-layout-allow-occlusion id="{sid}-stage" data-start="0" data-duration="{dur}" data-track-index="1">')
    # poussée : entrée (début) + sortie (fin) selon la direction
    d = S.push
    fromv = {'right': 'x:%d' % W, 'left': 'x:%d' % -W, 'up': 'y:%d' % H, 'down': 'y:%d' % -H, 'none': 'x:0'}[d]
    outv = {'right': 'x:%d' % -W, 'left': 'x:%d' % W, 'up': 'y:%d' % -H, 'down': 'y:%d' % H, 'none': 'x:0'}[d]
    if d != 'none':
        js.append(f'tl.fromTo("#{sid}-stage",{{{fromv}}},{{x:0,y:0,duration:.34,ease:"power3.out"}},0);')
    if sid != STAGES[-1].id:
        ex = round(S.t1 - S.t0, 3)
        js.append(f'tl.to("#{sid}-stage",{{{outv},duration:.34,ease:"power2.in"}},{ex:.3f});')
    for it in S.items:
        rel = round(it['at'] - S.t0, 3)
        end_abs = it['until'] if it['until'] is not None else S.t1 + OVER
        end_rel = round(min(end_abs - S.t0, dur), 3)
        d_ = round(max(end_rel - rel, .3), 3)
        cx, cy, w, h = it['cx'], it['cy'], it['w'], it['h']
        left, top = cx - w / 2, cy - h / 2
        html.append(f'<div class="item clip {it["cls"]}" id="{it["id"]}" data-start="{rel}" data-duration="{d_}" data-track-index="4" '
                    f'style="left:{left:.0f}px;top:{top:.0f}px;width:{w:.0f}px;height:{h:.0f}px;z-index:{it["z"]}">'
                    + (f'<div style="width:100%;height:100%;transform:scale({it["k"]});transform-origin:50% 50%;display:flex;align-items:center;justify-content:center">{it["html"]}</div>' if it['k'] != 1.0 else it['html']) + '</div>')
        e, r = it['enter'], it['rot']
        fr = {'pop': 'opacity:0,scale:.6,y:30', 'left': 'opacity:0,x:-260', 'right': 'opacity:0,x:260', 'drop': 'opacity:0,y:-300', 'up': 'opacity:0,y:300',
              'stamp': 'opacity:0,scale:1.9', 'bounce': 'opacity:0,y:-520', 'cut': 'opacity:1', 'none': 'opacity:1'}[e]
        if e in ('cut', 'none'):
            js.append(f'tl.set("#{it["id"]}",{{rotation:{r}}},{rel:.3f});')
        else:
            ease = 'back.out(1.6)' if e in ('pop', 'drop') else ('power4.in' if e == 'stamp' else ('bounce.out' if e == 'bounce' else 'expo.out'))
            dd = .18 if e == 'stamp' else (.8 if e == 'bounce' else .42)
            js.append(f'tl.fromTo("#{it["id"]}",{{{fr},rotation:{r}}},{{opacity:1,scale:1,x:0,y:0,rotation:{r},duration:{dd},ease:"{ease}"}},{rel:.3f});')
        if it['snd'] == 'pop': pop_sfx(it['at'])
        elif isinstance(it['snd'], str): sfx(it['at'], it['snd'], .2 if it['snd'].startswith('R_') else .28)
    # js des composants (triés)
    for t, code in sorted(S.js, key=lambda x: x[0]): js.append(code)
    html.append('</div>')
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
    open(os.path.join(out, 'compositions', f'{sid}.html'), 'w', encoding='utf-8').write(comp)

# ------------------------------------------------------------------ sous-titres
def chunks(bt, keys):
    """découpe un plan en blocs de 1 à 4 mots (≤ 26 caractères)"""
    toks = [(w, t0, t1) for (w, t0, t1) in bt.words]
    blocks, cur = [], []
    def flush():
        if cur: blocks.append(list(cur)); cur.clear()
    for i, (w, t0, t1) in enumerate(toks):
        txt = ' '.join(x[0] for x in cur + [(w, t0, t1)])
        if cur and (len(txt) > 26 or len(cur) >= 3 or (cur[-1][0][-1] in '.,;:?!' and len(' '.join(x[0] for x in cur)) >= 7)):
            flush()
        cur.append((w, t0, t1))
        if w[-1] in '.?!': flush()
    flush()
    # fusionne les blocs d'un seul mot très court avec le voisin
    merged = []
    for b in blocks:
        if merged and len(b) == 1 and len(b[0][0]) <= 4 and len(' '.join(x[0] for x in merged[-1] + b)) <= 26 and len(merged[-1]) < 3:
            merged[-1] += b
        else: merged.append(b)
    return merged

def build_captions(keys):
    chtml, cjs = [], []
    for bt in BEATS:
        ms = chunks(bt, keys)
        for k, c in enumerate(ms):
            cs = c[0][1] if (k or bt.n > 1) else 0.0
            nxt = ms[k + 1][0][1] if k + 1 < len(ms) else None
            ce = nxt if nxt is not None else bt.e
            if nxt is None: ce = min(ce, c[-1][2] + .35) if BEATS[bt.n - 1].e - c[-1][2] > .5 else ce
            if ce - cs < .25: ce = cs + .25
            cid = f'cap{bt.n}-{k}'
            spans = []
            for (w, t0, t1) in c:
                spans.append(f'<b class="k">{w}</b>' if (norm(w) in keys) else w)
            txt = ' '.join(spans)
            fs = 76
            L = sum(len(x[0]) for x in c) + len(c) - 1
            if L > 24: fs = int(76 * 24 / L)
            chtml.append(f'<div class="cap clip" id="{cid}" data-start="{cs:.3f}" data-duration="{round(ce - cs, 3)}" data-track-index="1" style="top:{CAP_Y - 48}px;font-size:{fs}px">{txt}</div>')
            if not (bt.n == 1 and k == 0):
                cjs.append(f'tl.fromTo("#{cid}",{{opacity:0,y:8,filter:"blur(9px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.1,ease:"power2.out"}},{cs:.3f});')
            cjs.append(f'tl.to("#{cid}",{{opacity:0,filter:"blur(6px)",duration:.08,ease:"none"}},{ce - .09:.3f});')
    open(os.path.join(CFG['out'], 'compositions', 'caps.html'), 'w', encoding='utf-8').write(f"""<template>
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
""")

# ------------------------------------------------------------------ projet
RDUR = {}
def render(keys):
    out = CFG['out']
    for d in ('assets/img', 'assets/sfx3', 'assets/audio', 'compositions'): os.makedirs(os.path.join(out, d), exist_ok=True)
    DONE = set()
    for cd in CFG['cut']:
        for f in os.listdir(cd):
            if f.endswith('.png'):
                n = f[:-4]
                if os.path.exists(os.path.join(out, 'assets', 'img', f)) and n in DONE: continue
                im = Image.open(os.path.join(cd, f)); im.thumbnail((1100, 1100)); im.save(os.path.join(out, 'assets', 'img', f), optimize=True); DONE.add(n)
    shutil.copy(CFG['voice'], os.path.join(out, 'assets', 'voce.wav'))
    os.makedirs(os.path.join(out, 'assets', 'fonts'), exist_ok=True); os.makedirs(os.path.join(out, 'assets', 'sfx2'), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, 'assets', 'fonts')): shutil.copy(os.path.join(ROOT, 'assets', 'fonts', f), os.path.join(out, 'assets', 'fonts', f))
    s2 = os.path.join(ROOT, 'assets', 'sfx2')
    for f in os.listdir(s2):
        if f.endswith('.mp3'):
            shutil.copy(os.path.join(s2, f), os.path.join(out, 'assets', 'sfx2', f))
            RDUR['R_' + f[:-4]] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(s2, f)], capture_output=True, text=True).stdout.strip())
    sfxd = os.path.join(ROOT, 'assets', 'sfx3'); DUR = {}
    for f in os.listdir(sfxd):
        shutil.copy(os.path.join(sfxd, f), os.path.join(out, 'assets', 'sfx3', f))
        DUR[f[:-4]] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(sfxd, f)], capture_output=True, text=True).stdout.strip())
    DUR.update(RDUR)
    for S in STAGES: build_stage(S)
    build_captions(keys)
    # push sfx
    for S in STAGES[1:]: sfx(S.t0 - .02, 'push', .1)
    hosts = []
    for k, S in enumerate(STAGES):
        dur = round(min(S.t1 - S.t0 + OVER, TOTAL - S.t0), 3)
        hosts.append(f'      <div id="{S.id}" class="clip" data-composition-id="{S.id}" data-composition-src="compositions/{S.id}.html" data-start="{S.t0:.3f}" data-duration="{dur}" data-track-index="{2 + k % 2}" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>')
    hosts.append(f'      <div id="caps" class="clip" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{TOTAL}" data-track-index="6" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>')
    SFXLOG.sort(); audio = []
    for n, (t, f, v) in enumerate(SFXLOG):
        if t < 0 or t > TOTAL - .3 or f not in DUR: continue
        t = min(t, TOTAL - DUR[f] - .02)
        src = f'assets/sfx2/{f[2:]}.mp3' if f.startswith('R_') else f'assets/sfx3/{f}.wav'
        audio.append(f'      <audio id="sfx{n}" src="{src}" data-start="{t:.3f}" data-duration="{DUR[f]:.3f}" data-track-index="{20 + n % 9}" data-volume="{v}"></audio>')
    stars = ''.join(f'<i style="left:{(i * 137 + 31) % 100}%;top:{(i * 71 + 17) % 100}%;width:{3 + i % 2}px;height:{3 + i % 2}px"></i>' for i in range(36))
    twink = ''.join(f'tl.fromTo("#stars i:nth-child({k + 1})",{{opacity:.15}},{{opacity:1,duration:{.6 + (k % 5) * .35:.2f},yoyo:true,repeat:{int(TOTAL // (.6 + (k % 5) * .35)) | 1},ease:"sine.inOut"}},{(k * .23) % 2:.2f});\n      ' for k in range(36))
    drift = f'tl.fromTo("#stars",{{x:0,y:0}},{{x:-{int(.3 * TOTAL) + 10},y:-{int(.6 * TOTAL) + 10},duration:{TOTAL},ease:"none"}},0);'
    index = f"""<!doctype html>
<html lang="it">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      {FONTS}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0E1650; }}
      #bg {{ position:absolute; inset:0; background:radial-gradient(ellipse 90% 80% at 50% 45%, #0F184A 0%, #0D1660 55%, #0B1646 100%); }}
      #gv {{ position:absolute; inset:0; background-image:linear-gradient(90deg, rgba(150,165,255,.075) 1px, transparent 1px); background-size:96px 96px; background-position:47px 0; }}
      #gh {{ position:absolute; left:0; right:0; top:-96px; bottom:-96px; background-image:linear-gradient(180deg, rgba(150,165,255,.075) 1px, transparent 1px); background-size:96px 96px; }}
      #stars {{ position:absolute; left:0; top:0; width:{W + int(.3 * TOTAL) + 40}px; height:{H + int(.6 * TOTAL) + 40}px; }}
      #stars i {{ position:absolute; border-radius:50%; background:#fff; box-shadow:0 0 8px rgba(255,255,255,.7); }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" style="position:absolute;inset:0;font-family:'Plus Jakarta Sans',Montserrat,sans-serif">
      <div id="bg"></div><div id="gv"></div><div id="gh"></div>
      <div id="stars">{stars}</div>
{chr(10).join(hosts)}
      <audio id="voce" src="assets/voce.wav" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-volume="1"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#gh", {{ y: 0 }}, {{ y: 96, duration: 64, ease: "none", repeat: {int(TOTAL // 64) + 1} }}, 0);
      {drift}
      {twink}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(index)
    open(os.path.join(out, 'hyperframes.json'), 'w').write('{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",\n  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},\n  "media": {"autoProxy": true}\n}\n')
    open(os.path.join(out, 'meta.json'), 'w').write(json.dumps({'id': os.path.basename(out), 'name': os.path.basename(out)}))
    print('ok ref:', len(STAGES), 'scènes,', len(SFXLOG), 'sons,', len(audio), 'audio')


def audit(min_frac=.10, min_overlap=.5):
    """signale les éléments visibles en même temps qui se chevauchent (hors fonds / halos)"""
    for S in STAGES:
        its = [it for it in S.items if it['z'] >= 2 and it['enter'] != 'none' or it['cls'] == 'walker']
        for i in range(len(its)):
            for j in range(i + 1, len(its)):
                a, b = its[i], its[j]
                a0, a1 = a['at'], (a['until'] if a['until'] is not None else S.t1)
                b0, b1 = b['at'], (b['until'] if b['until'] is not None else S.t1)
                ov = min(a1, b1) - max(a0, b0)
                if ov < min_overlap: continue
                aw, ah = a['w'] * a['k'], a['h'] * a['k']; ax0, ax1, ay0, ay1 = a['cx'] - aw / 2, a['cx'] + aw / 2, a['cy'] - ah / 2, a['cy'] + ah / 2
                bw, bh = b['w'] * b['k'], b['h'] * b['k']; bx0, bx1, by0, by1 = b['cx'] - bw / 2, b['cx'] + bw / 2, b['cy'] - bh / 2, b['cy'] + bh / 2
                ix, iy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
                if ix <= 0 or iy <= 0: continue
                fr = ix * iy / min(aw * ah, bw * bh)
                if fr >= min_frac:
                    ta = re.sub('<[^>]+>', '', a['html'])[:28] or re.findall(r'img/(\w+)', a['html'])[:1]
                    tb = re.sub('<[^>]+>', '', b['html'])[:28] or re.findall(r'img/(\w+)', b['html'])[:1]
                    print(f"  [{S.id}] {fr:.0%} {ov:.1f}s : {ta} × {tb}")
        for it in S.items:
            iw_, ih_ = it['w'] * it['k'], it['h'] * it['k']; x0, x1, y0, y1 = it['cx'] - iw_ / 2, it['cx'] + iw_ / 2, it['cy'] - ih_ / 2, it['cy'] + ih_ / 2
            if it['enter'] not in ('none',) and it['cls'] != 'walker' and (x0 < 20 or x1 > W - 20 or y0 < 20 or y1 > CAP_Y - 70):
                t = re.sub('<[^>]+>', '', it['html'])[:28] or re.findall(r'img/(\w+)', it['html'])[:1]
                print(f"  [{S.id}] hors zone x={x0:.0f}-{x1:.0f} y={y0:.0f}-{y1:.0f} : {t}")


def estimate_mix(vol_voice=1.0):
    """mixe voix + sons (mêmes gains que les <audio data-volume>) et mesure le niveau intégré"""
    import numpy as np, wave, tempfile
    sr = 48000
    def load(path):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True).stdout
        return np.frombuffer(raw, dtype=np.float32)
    mix = np.zeros(int(sr * TOTAL), dtype=np.float32)
    v = load(CFG['voice']); mix[:min(len(v), len(mix))] += vol_voice * v[:len(mix)]
    cache = {}
    for t, f, vol in SFXLOG:
        if t < 0 or t > TOTAL - .3: continue
        p = os.path.join(ROOT, 'assets', 'sfx2', f[2:] + '.mp3') if f.startswith('R_') else os.path.join(ROOT, 'assets', 'sfx3', f + '.wav')
        if p not in cache: cache[p] = load(p)
        y = cache[p] * vol; i = int(t * sr); mix[i:i + len(y)] += y[:len(mix) - i]
    out = os.path.join(tempfile.gettempdir(), 'mix_est.wav')
    with wave.open(out, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.findall(r'I:\s+(-?[\d.]+) LUFS', r); p = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)
    print('mix estimé:', m[-1] if m else '?', 'LUFS ; crête', p[-1] if p else '?', 'dBFS')
