"""Storyboard « La tua vita a ogni livello come pilota di linea » — style références A/B, 16:9."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import refkit as R
from refkit import T, sfx, GOLD, GREEN, RED, GREY

HERE = R.HERE; ROOT = R.ROOT
R.init(script=os.path.join(ROOT, '..', 'scripts', 'pilota-5min.txt'), words_json=os.path.join(HERE, 'words-pilota.json'),
       srt=os.path.join(ROOT, '..', 'scripts', 'pilota-scenes.srt'), voice_norm=os.path.join(ROOT, 'assets', 'audio', 'voce_pilota_norm.wav'),
       out=os.path.join(ROOT, 'vpil'), cut_dirs=[os.path.join(ROOT, 'assets', 'cut-pil'), os.path.join(ROOT, 'assets', 'cut-hvac')],
       total=309.0, numw='diciannove quindici quattordici millecinquecento novantamila centosessantamila trentamila settantacinquemila ottantamila centodiecimila duecentoventimila uno due tre quattro cinque')
STAGES = R.STAGES
def stage(sid, b0, b1, push='right'):
    s = R.Stage(sid, b0, b1, push); STAGES.append(s); return s
LX, RX = 470, 1360          # colonne personnage / cartes
EL = 680                     # hauteur d'un personnage debout

def level(s, n, name, at):
    s.chip(f'LIVELLO {n}  ·  {name}', 960, 78, at, color='gold', size=24)

# ===== OUVERTURE =====================================================================
s = stage('s01', 1, 3)
s.img('dio_medico', 1290, 430, h=520, at=T(1), enter='right', until=T(2, 'elettrocardiogramma'))
s.img('pose_visita', LX + 40, 500, h=560, at=T(1), enter='left')
s.chip('centro aeromedico', 1290, 740, T(1, 'aeromedico'), color='slate', size=30, until=T(2, 'elettrocardiogramma'))
s.ecg(1290, 430, 640, T(2, 'elettrocardiogramma'), until=None, title='Elettrocardiogramma')
s.bubble('…', 1290, 150, T(3, 'medico'), until=None, size=52, who='IL MEDICO')
s.chip('non dice niente', 1290, 740, T(3, 'niente'), color='red', size=30)

s = stage('s02', 4, 6)
s.img('pose_visita', LX + 40, 500, h=560, at=T(4), enter='cut')
s.ecg(1290, 430, 680, T(4), title='Visita di prima classe', status=(T(5, 'valore'), 'Non idoneo', RED))
s.chip('da qui dipende tutto', 1290, 740, T(4, 'dipende'), color='gold', size=30, until=T(5, 'Se'))
s.badge('no', 1650, 270, T(5, 'finisce'), size=110)
s.chip('il sogno finisce qui', 1290, 740, T(5, 'sogno'), color='red', size=30, until=T(6, 'Succede'))
s.chip('succede spesso', 1290, 740, T(6, 'spesso'), color='red', size=30)

s = stage('s03', 7, 8)
s.img('pose_capt', 640, 470, h=560, at=T(7))
s.plane('aereo_volo', 250, 190, T(7, 'centinaia'), 3.6, h=240)
s.chip('tra 15 anni', 1450, 330, T(7, 'quindici'), color='gold', size=34, until=T(8, 'E'))
s.chip('centinaia di persone a bordo', 1450, 470, T(7, 'centinaia'), color='slate', size=28, until=T(8, 'E'))
s.chip('si fidano di te', 1450, 330, T(8, 'fideranno'), color='slate', size=34)
s.badge('ok', 1450, 520, T(8, 'passato'), size=130)
s.chip('oggi sei passato', 1450, 690, T(8, 'passato'), color='green', size=32)

s = stage('s04', 9, 9)
s.title('SPIEGATO DA', 'PROFESSIONE REALE', T(9), cy=300)
s.img('elia_26', 960, 610, h=400, at=T(9, 'vita'), enter='up')
s.chip('pilota di linea', 560, 600, T(9, 'pilota'), color='slate', size=32)
s.chip('a ogni livello', 1360, 600, T(9, 'livello'), color='gold', size=32)

s = stage('s05', 10, 10)
s.img('elia_26', LX, 470, h=EL, at=T(10), enter='left')
s.subcard(RX, 450, T(10), T(10, 'Iscriviti', .5), avatar='head_26')
s.chip('quanto guadagna davvero?', RX, 880, T(10, 'guadagna'), color='gold', size=34) if False else None

# ===== LIVELLO 1 ====================================================================
s = stage('s06', 11, 14, 'up')
level(s, 1, 'ALLIEVO PILOTA', T(11, 'uno'))
s.img('elia_19', LX, 520, h=EL - 40, at=T(11), enter='left')
s.toggles('Certificato medico · 1ª classe', [('Vista', T(13, 'Vista'), 'on'), ('Udito', T(13, 'udito'), 'on'), ('Cuore', T(13, 'cuore'), 'on'), ('Testa', T(13, 'testa'), 'on')], RX, 500, 680, T(12, 'certificato'), until=T(14, 'Ogni'))
s.chip('↻ ogni anno', RX, 480, T(14, 'Ogni'), color='gold', size=44)

s = stage('s07', 15, 18)
s.img('pose_studio', LX + 20, 520, w=640, at=T(15), enter='left')
ttimes = [T(15, 'quattordici', .6 + k * .12) for k in range(14)]
ttimes = [T(16) + k * ((T(18, 'esame') - T(16)) / 14) for k in range(14)]
s.tiles(14, 7, RX, 380, 78, 14, T(15, 'quattordici'), ttimes, title='14 esami ATPL')
for nm, wd, (x, y) in (('Aerodinamica', 'Aerodinamica', (1130, 630)), ('Meteorologia', 'meteorologia', (1560, 630)), ('Navigazione', 'navigazione', (1130, 730)), ('Regolamenti', 'regolamenti', (1560, 730))):
    s.chip(nm, x, y, T(16, wd), color='slate', size=30, until=T(17, 'In'))
s.chip('centinaia di ore di teoria', RX, 680, T(17, 'centinaia'), color='gold', size=32)

s = stage('s08', 19, 20)
s.img('pose_studio', LX + 20, 520, w=640, at=T(19), enter='cut')
s.chip('di sera', RX - 200, 250, T(19, 'sera'), color='slate', size=34)
s.chip('nei weekend', RX + 200, 250, T(19, 'weekend'), color='slate', size=34)
s.chip('gli amici escono', RX, 360, T(19, 'amici'), color='red', size=34)
s.counter(RX, 620, 0, 0, T(20, 'costo'), fmt='?', size=170, color=GOLD, sub='il costo', dur=.1, w=520)

s = stage('s09', 21, 22)
s.img('elia_19', LX, 520, h=EL - 40, at=T(21), enter='left')
s.range_card('Formazione completa · stima', [dict(label='DA', frm=0, to=90000, fmt='{n} €', color=GOLD, at=T(21, 'novantamila')),
                                              dict(label='A', frm=0, to=160000, fmt='{n} €', color=RED, at=T(21, 'centosessantamila'))], RX, 400, 700, T(21, 'stima'))
s.img('contratto', RX - 200, 710, h=190, at=T(22, 'debito'), until=None, enter='drop')
s.stamp('DEBITO', RX + 130, 710, T(22, 'debito'), size=68, rot=-6)

s = stage('s10', 23, 25)
s.img('elia_19', LX, 520, h=EL - 40, at=T(23), enter='cut')
s.chip('la famiglia ipoteca la casa', RX, 330, T(23, 'ipotecano'), color='red', size=30, until=T(24, 'E'))
s.chip('19 anni', RX, 270, T(24, 'diciannove'), color='slate', size=36)
s.chip('0 € di stipendio', RX, 370, T(24, 'nessuno'), color='red', size=36)
s.img('soldi', RX, 580, h=220, at=T(24, 'stipendio'), enter='pop')
s.badge('no', RX + 200, 520, T(24, 'stipendio', .2), size=110)
s.stamp('STIME', RX, 740, T(25, 'Sono'), size=64, rot=-6, color=GOLD)
s.chip('dipendono dalla scuola', RX, 640, T(25, 'dipendono'), color='gold', size=36) if False else None

# ===== LIVELLO 2 =====================================================================
s = stage('s11', 26, 27, 'up')
level(s, 2, 'LICENZA, MA NESSUN CONTRATTO', T(26, 'due'))
s.img('pose_esame', 560, 540, w=760, at=T(26), enter='left')
s.chip('prova pratica', RX, 400, T(27, 'pratica'), color='gold', size=38)
s.chip("con l'esaminatore", RX, 520, T(27, 'esaminatore'), color='slate', size=34)

s = stage('s12', 28, 29)
s.img('pose_istruttore', 560, 520, w=760, at=T(28), enter='left')
s.chip('un\'ora di volo', RX, 230, T(28, 'ora'), color='gold', size=38)
s.img('checklist', RX, 600, h=330, at=T(29, 'errore'), enter='right')
s.stamp('ERRORE', RX + 160, 540, T(29, 'errore'), size=64, rot=-9)
s.chip('scritto su un foglio', RX, 790, T(29, 'foglio'), color='slate', size=30)

s = stage('s13', 30, 32)
s.img('elia_22', LX, 520, h=EL - 40, at=T(30), enter='left')
s.img('cappello', 1010, 300, h=170, at=T(30, 'commerciale'), enter='drop')
s.chip('CPL · licenza commerciale', 1520, 300, T(30, 'CPL'), color='gold', size=30)
s.progress('ORE DI VOLO', RX, 600, 700, 0, 1500, T(32, 'ATPL'), 1.4, left='ore minime', right='ATPL', color=GOLD, fmt='{n}', unit=' ore')
s.chip('non quelle che cercano le compagnie', RX, 790, T(31, 'compagnie'), color='red', size=26)

s = stage('s14', 33, 34)
s.img('logbook', RX - 100, 520, h=440, at=T(33), enter='right')
s.img('elia_22', LX, 520, h=EL - 40, at=T(33), enter='cut')
s.chip('si accumulano lavorando', RX - 100, 180, T(33, 'accumulano'), color='gold', size=34, until=T(34, 'Ogni'))
s.chip('scritta a mano', RX - 100, 180, T(34, 'mano'), color='slate', size=34)

s = stage('s15', 35, 37)
s.img('clessidra', LX + 20, 500, h=520, at=T(35), enter='left')
s.img('contratto', RX - 130, 390, h=300, at=T(35, 'debito'), enter='drop', until=T(36, 'Fai'))
s.chip('il debito aspetta', RX - 130, 650, T(35, 'debito'), color='red', size=40, until=T(36, 'Fai'))
s.img('dio_scuola_volo', RX - 100, 450, h=380, at=T(36, 'istruttore'), enter='right', until=T(37, 'E'))
s.chip("istruttore · turisti in volo", RX - 100, 700, T(36, 'istruttore'), color='gold', size=36, until=T(37, 'E'))
s.chip('fermi per mesi', RX - 100, 450, T(37, 'mesi'), color='red', size=42)
s.arrow(RX + 400, 450, T(37, 'fermi'), up=False, size=110)

# ===== LIVELLO 3 =====================================================================
s = stage('s16', 38, 41, 'up')
level(s, 3, 'PRIMO UFFICIALE JUNIOR', T(38, 'tre'))
s.img('elia_26', LX, 520, h=EL - 40, at=T(38), enter='left')
s.img('dio_simulatore', RX - 40, 430, h=360, at=T(39, 'abilitazione'), enter='right', until=T(41, 'Si'))
s.chip('type rating', RX - 40, 700, T(39, 'abilitazione'), color='gold', size=38, until=T(40, 'Il'))
s.chip('lo paghi tu', RX - 40, 700, T(40, 'paghi'), color='red', size=38, until=T(41, 'Si'))
s.range_card('Simulatore · durata', [dict(label='DA', frm=0, to=1, fmt='{n} mese', color=GOLD, at=T(41, 'uno')), dict(label='A', frm=0, to=3, fmt='{n} mesi', color=GREEN, at=T(41, 'tre'))], RX - 40, 460, 620, T(41, 'type'))

s = stage('s17', 42, 45)
s.img('dio_aula', 1050, 440, h=400, at=T(42, 'contratto'), enter='right')
s.img('elia_26', LX, 520, h=EL - 40, at=T(42), enter='left')
s.chip('sala briefing', 1610, 330, T(43, 'briefing'), color='slate', size=30, until=T(44, 'Gli'))
s.chip('divisa nuova', 1610, 440, T(43, 'divisa'), color='gold', size=30, until=T(44, 'Gli'))
s.chip('il tuo nome sul badge', 1610, 550, T(43, 'badge'), color='slate', size=28, until=T(44, 'Gli'))
s.chip('più stipendio', RX - 170, 330, T(44, 'stipendi'), color='green', size=40) if False else None
s.chip('stipendi variano', 1610, 330, T(44, 'variano'), color='gold', size=32, until=T(45, 'Alcune'))
s.chip('+ stipendio', 1610, 330, T(45, 'pagano'), color='green', size=32)
s.chip('+ ore di volo', 1610, 440, T(45, 'volare'), color='red', size=32)

s = stage('s18', 46, 47)
s.img('elia_26', LX, 520, h=EL - 40, at=T(46), enter='cut')
s.range_card("Primo ufficiale junior · lordo/anno", [dict(label='DA', frm=0, to=30000, fmt='{n} €', color=GOLD, at=T(46, 'trentamila')),
                                                       dict(label='A', frm=0, to=75000, fmt='{n} €', color=GREEN, at=T(46, 'settantacinquemila'))], RX, 400, 740, T(46, 'stime'))
s.stamp('LORDO', RX - 250, 700, T(47, 'Lordi'), size=76, rot=-7)
s.chip('prima delle tasse', RX + 260, 700, T(47, 'prima'), color='red', size=30)

s = stage('s19', 48, 51)
s.img('pose_fo', 560, 520, w=760, at=T(48), enter='left')
s.chip('sedile destro', RX, 300, T(48, 'destra'), color='gold', size=38, until=T(49, 'Il'))
s.bubble('…', RX, 300, T(49, 'comandante'), size=60, who='IL COMANDANTE', until=T(50, 'Fai'))
s.toggles('Procedure', [('Annunci', T(50, 'annunci'), 'on'), ('Controlli', T(50, 'controlli'), 'on'), ('Procedure', T(50, 'procedure'), 'on')], RX, 470, 640, T(50, 'Fai'), until=T(51, 'Sbagliare'))
s.img('checklist', RX, 480, h=360, at=T(51, 'checklist'), enter='drop')
s.stamp("NON È UN'OPZIONE", RX, 760, T(51, 'opzione'), size=44, rot=-5)

s = stage('s20', 52, 54)
s.img('elia_26', LX, 520, h=EL - 40, at=T(52), enter='cut')
s.tiles(6, 6, RX, 380, 84, 14, T(52, 'sei'), [T(52, 'sei') + .2 * k for k in range(6)], labels=['1', '2', '3', '4', '5', '6'], title='Ogni 6 mesi · simulatore')
s.badge('no', RX + 330, 560, T(53, 'fallisci'), size=100)
s.chip('se lo fallisci: torni a studiare', RX, 700, T(53, 'fallisci'), color='red', size=30, until=T(54, 'Per'))
s.img('clessidra', RX, 650, h=250, at=T(54, 'anni'), enter='drop')
s.chip('la carriera dipende da queste prove', RX, 800, T(54, 'dipende'), color='gold', size=26)

# ===== LIVELLO 4 =====================================================================
s = stage('s21', 55, 58, 'up')
level(s, 4, 'PRIMO UFFICIALE SENIOR', T(55, 'quattro'))
s.img('elia_31', LX, 520, h=EL - 40, at=T(55), enter='left')
s.img('carta', RX - 180, 480, h=330, at=T(57, 'rotte'), enter='right')
s.chip('rotte', RX - 180, 680, T(57, 'rotte'), color='slate', size=40, until=T(58, 'Sai'))
s.chip('aeroporti difficili', RX - 180, 775, T(57, 'aeroporti'), color='gold', size=36, until=T(58, 'Sai'))
s.img('temporale', RX + 200, 460, h=300, at=T(58, 'tempesta'), enter='pop')
s.chip('meteo', RX + 200, 680, T(57, 'meteo'), color='slate', size=40)
s.chip('solo rumore?', RX + 200, 775, T(58, 'rumore'), color='gold', size=34)

s = stage('s22', 59, 61)
s.img('elia_31', LX, 520, h=EL - 40, at=T(59), enter='cut')
s.range_card('Primo ufficiale senior · lordo/anno', [dict(label='DA', frm=0, to=80000, fmt='{n} €', color=GOLD, at=T(59, 'ottantamila')),
                                                       dict(label='A', frm=0, to=110000, fmt='{n} €', color=GREEN, at=T(59, 'centodiecimila'))], RX, 400, 760, T(59, 'stime'))
s.chip('i turni non cambiano', RX, 700, T(60, 'turni'), color='red', size=44, until=T(61, 'Ma'))
s.chip('solo il penultimo gradino', RX, 700, T(61, 'penultimo'), color='gold', size=44)

s = stage('s23', 62, 62)
s.img('elia_31', LX, 520, h=EL - 40, at=T(62), enter='left')
s.subcard(RX, 450, T(62), T(62, 'iscriviti', .4), avatar='head_31')
s.chip("manca l'ultimo livello", RX, 880, T(62, 'manca'), color='gold', size=34) if False else None

s = stage('s24', 63, 65)
s.img('dio_hotel', 560, 480, h=500, at=T(63), enter='left')
s.img('pose_hotel', 560, 480, w=640, at=T(64), enter='cut') if False else None
s.chip('sveglie alle 3', RX, 270, T(63, 'Sveglie'), color='red', size=44, until=T(65, 'Il'))
s.chip('notti in hotel', RX, 400, T(63, 'hotel'), color='slate', size=44, until=T(65, 'Il'))
s.chip('fusi orari', RX, 530, T(63, 'fusi'), color='gold', size=44, until=T(65, 'Il'))
s.img('orologi', RX, 610, h=170, at=T(65, 'orologio'), enter='drop')
s.chip('orologio ≠ corpo', RX, 800, T(65, 'corpo'), color='red', size=32)
s.chip('città diverse', 560, 790, T(64, 'diverse'), color='slate', size=34)

s = stage('s25', 66, 68)
s.img('pose_visita', LX + 40, 500, h=560, at=T(66), enter='left')
s.ecg(RX, 420, 700, T(66, 'medico'), title='Visita medica · ogni anno', status=(T(67, 'valore'), 'Non idoneo', RED))
s.chip('un\'influenza', RX, 760, T(67, 'influenza'), color='gold', size=40, until=T(67, 'valore'))
s.chip('un valore sbagliato', RX, 760, T(67, 'valore'), color='red', size=40, until=T(67, 'resti'))
s.chip('resti a terra', RX, 800, T(67, 'terra'), color='red', size=40)
s.stamp('IDONEITÀ PERSA = LAVORO PERSO', RX, 680, T(68, 'persa'), size=36, rot=-4)

# ===== LIVELLO 5 =====================================================================
s = stage('s26', 69, 72, 'up')
level(s, 5, 'COMANDANTE', T(69, 'cinque'))
s.img('pose_capt', 560, 520, w=760, at=T(69), enter='left')
for k, (txt, wd) in enumerate((('partire', 'partire'), ('ritardare', 'ritardare'), ('tornare indietro', 'tornare'))):
    s.chip(txt, RX, 280 + 135 * k, T(70, wd), color=['green', 'gold', 'red'][k], size=44, until=T(71, 'Sei'))
s.chip('responsabile di ogni persona', RX, 400, T(71, 'responsabile'), color='gold', size=34, until=T(72, 'Il'))
s.img('carburante', 1110, 480, h=270, at=T(72, 'carburante'), enter='pop')
s.img('temporale', 1400, 480, h=250, at=T(72, 'meteo'), enter='pop')
s.img('valigia', 1690, 490, h=270, at=T(72, 'peso'), enter='pop')
s.chip('carburante', 1110, 700, T(72, 'carburante'), color='slate', size=30)
s.chip('meteo', 1400, 700, T(72, 'meteo'), color='slate', size=30)
s.chip('peso', 1690, 700, T(72, 'peso'), color='slate', size=30)

s = stage('s27', 73, 74)
s.img('elia_38', LX, 520, h=EL - 40, at=T(73), enter='left')
s.range_card('Comandante · lordo/anno', [dict(label='DA', frm=0, to=110000, fmt='{n} €', color=GOLD, at=T(73, 'centodieci')),
                                          dict(label='A', frm=0, to=220000, fmt='{n} €', color=GREEN, at=T(73, 'duecentoventimila'))], RX, 350, 760, T(73, 'stime'))
s.stamp('NON GARANTITE', RX, 690, T(74, 'garantite'), size=64, rot=-6, color=GOLD)
s.chip('dipendono da compagnia e contratto', RX, 800, T(74, 'dipendono'), color='slate', size=28)

s = stage('s28', 75, 77)
s.img('pose_capt', 560, 520, w=760, at=T(75), enter='cut')
s.chip('non ti pagano per volare', RX, 330, T(75, 'volare'), color='red', size=44, until=T(76, 'Ti'))
s.chip('ti pagano per decidere', RX, 330, T(76, 'decisioni'), color='gold', size=48)
s.chip('quelle che nessuno vede', RX, 470, T(77, 'nessuno'), color='slate', size=44)
s.badge('ok', RX, 600, T(77, 'salvano'), size=130)
s.chip('e che salvano tutti', RX, 760, T(77, 'salvano'), color='green', size=44)

s = stage('s29', 78, 81)
s.img('pose_casa', 600, 520, w=820, at=T(78), enter='left')
s.chip('il costo nascosto', RX, 250, T(78, 'costo'), color='red', size=40)
for k, (txt, wd) in enumerate((('compleanni', 'compleanni'), ('cene', 'cene'), ('feste', 'feste'))):
    s.chip(txt, (1220, 1530, 1760)[k], 360, T(79, wd), color='gold', size=34, until=T(80, 'Metà'))
s.progress("TEMPO LONTANO DA CASA", RX, 520, 700, 0, 50, T(80, 'Metà'), 1.0, left='', right="all'anno", color=GOLD, fmt='{n}', unit=' %')
s.chip('i figli crescono lontano', RX, 780, T(81, 'figli'), color='slate', size=30)

s = stage('s30', 82, 82)
s.img('clessidra', 700, 500, h=520, at=T(82, 'limite'), enter='drop')
s.chip("limite d'età", RX, 400, T(82, 'limite'), color='red', size=52)
s.chip('arriva il giorno', RX, 560, T(82, 'giorno'), color='slate', size=36)

# ===== CHIUSURA ======================================================================
s = stage('s31', 83, 85)
s.img('dio_medico', 1290, 420, h=450, at=T(83), enter='right')
s.img('elia_19', LX, 520, h=EL - 40, at=T(83, 'diciannove'), enter='left')
s.chip('di nuovo a 19 anni', 1290, 730, T(83, 'diciannove'), color='slate', size=32, until=T(84, 'Il'))
s.chip('non sa quanto gli costerà', 1290, 730, T(84, 'costerà'), color='red', size=30, until=T(85, 'Non'))
s.stamp('INVISIBILE', 1290, 730, T(85, 'invisibile'), size=62, rot=-6, color=GOLD)

s = stage('s32', 86, 87)
s.img('aereo_terra', 700, 470, h=340, at=T(86), enter='left')
s.badge('ok', 700, 700, T(86, 'bene'), size=110)
s.chip('nessuno ringrazia', 700, 800, T(86, 'ringrazia'), color='gold', size=32)
s.img('temporale', 1400, 470, h=320, at=T(87, 'male'), enter='right')
s.badge('no', 1400, 700, T(87, 'male'), size=110)
s.chip('ricordano il tuo nome', 1400, 800, T(87, 'ricordano'), color='red', size=32)

s = stage('s33', 88, 89)
s.img('head_19', 600, 480, h=470, at=T(88), enter='left')
s.img('head_46', 1320, 480, h=470, at=T(88, 'mestiere'), enter='right')
s.chip('porta le persone a casa', 960, 140, T(88, 'porta'), color='green', size=44, until=T(89, 'E'))
s.chip('metà della vita lontano dalla sua', 960, 140, T(89, 'metà'), color='red', size=44)

s = stage('s34', 90, 90)
s.img('elia_38', LX, 520, h=EL - 40, at=T(90), enter='left')
s.subcard(RX, 450, T(90), T(90, 'iscriviti', .3), avatar='head_38')

s = stage('s35', 91, 92)
s.img('head_46', LX + 40, 480, h=520, at=T(91), enter='left')
s.bubble('Pilota, o sogni di diventarlo?', RX, 330, T(91, 'pilota'), size=46, who='SCRIVILO NEI COMMENTI')
s.chip('lavori nel settore?', RX, 480, T(91, 'pilota'), color='slate', size=38)
s.bubble('Quale mestiere dopo?', RX, 690, T(92, 'mestiere'), size=44, who='LA PROSSIMA PUNTATA')

KEYS = {R.norm(x) for x in """novantamila centosessantamila trentamila settantacinquemila ottantamila centodiecimila duecentoventimila millecinquecento quattordici quindici diciannove
lordi debito stima stime idoneità comandante ATPL CPL type rating medico classe invisibile famiglie nascosto decisioni figli iscriviti commenti sogno
prima uno due tre quattro cinque""".split()}
R.render(KEYS)
R.audit()
