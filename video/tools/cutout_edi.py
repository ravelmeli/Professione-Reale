"""Découpe les planches « poliziotto » par composantes connexes (les planches ne sont pas des grilles régulières).
Usage: python3 tools/cutout_pol.py   (depuis video/)"""
import numpy as np, os
from PIL import Image
from scipy import ndimage as ndi

SHEETS = {
 'sheet-career':  ['rocco_18','rocco_24','rocco_30','rocco_37','rocco_46','head_54'],
 'sheet-heads':   ['head_18','head_24','head_30','head_37','head_46','head_54b'],
 'sheet-labor':   ['pose_sacco','pose_carriola','pose_pala','pose_pioggia'],
 'sheet-walk':    ['walk_1','walk_2','walk_3','pose_point','pose_watch','pose_yawn'],
 'sheet-job':     ['pose_ponteggio','pose_mattoni','pose_ferro','pose_livella'],
 'sheet-life':    ['pose_capo','pose_cabina','pose_pausa','pose_casa'],
 'sheet-dio1':    ['dio_cantiere','dio_ponteggio','dio_scavo','dio_pioggia','dio_cabina','dio_edificio'],
 'sheet-dio2':    ['dio_cucina','dio_magazzino','dio_clinica','dio_pausa','dio_notte','dio_citta'],
 'sheet-tools':   ['cazzuola','livella','martello','mattoni','secchio','metro'],
 'sheet-safety':  ['casco','imbracatura','scarponi','guanti','cono','gilet'],
 'sheet-machines':['carriola','sacchi','ferri','scavatore','betoniera','trabattello'],
 'sheet-papers':  ['progetto','checklist','soldi','calendario','sveglia','patente'],
}
OUT='assets/cut-edi'; os.makedirs(OUT,exist_ok=True)

BGT=238
def cutout(a):
    mn=a.min(axis=2); mx=a.max(axis=2)
    bg=mn>=BGT
    lab,_=ndi.label(bg)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    fg=~np.isin(lab,list(border))
    fg=ndi.binary_opening(fg,iterations=1)
    return fg,mn,mx

for name,names in SHEETS.items():
    im=Image.open(next(p for p in (f'assets/raw-edi/{name}.jpg', f'assets/raw-edi/{name}.png') if os.path.exists(p))).convert('RGB'); a=np.asarray(im).astype(np.int16)
    BGT=238
    fg,mn,mx=cutout(a); lum=a.mean(axis=2)
    fg=ndi.binary_opening(fg,iterations=2)
    lab,n=ndi.label(ndi.binary_dilation(fg,iterations=9))
    comps=[]
    for i in range(1,n+1):
        m=(lab==i)&fg
        if m.sum()<5000: continue
        ys,xs=np.where(m); comps.append([m,ys.min(),ys.max(),xs.min(),xs.max()])
    # petits morceaux détachés (étincelles de la cloche, Sardaigne) : rattachés au voisin le plus proche
    changed=True
    while changed and len(comps)>len(names):
        changed=False; comps.sort(key=lambda c:c[0].sum()); sm=comps[0]
        def gap(c):
            dy=max(0,max(sm[1],c[1])-min(sm[2],c[2])); dx=max(0,max(sm[3],c[3])-min(sm[4],c[4])); return (dx*dx+dy*dy)**.5
        best=min(comps[1:],key=gap)
        if gap(best)<160:
            best[0]=best[0]|sm[0]; ys,xs=np.where(best[0]); best[1:]=[ys.min(),ys.max(),xs.min(),xs.max()]; comps.pop(0); changed=True
    if False:   # deux poses collées (évier + chaudière) : coupe à la ligne la plus vide
        comps.sort(key=lambda c:c[2]-c[1]); big=comps.pop()
        prof=big[0].sum(axis=1); lo=big[1]+int(.35*(big[2]-big[1])); hi=big[1]+int(.65*(big[2]-big[1]))
        cut_y=lo+int(np.argmin(prof[lo:hi]))
        for part in (slice(None,cut_y),slice(cut_y,None)):
            m=np.zeros_like(big[0]); m[part,:]=big[0][part,:]
            ys,xs=np.where(m); comps.append([m,ys.min(),ys.max(),xs.min(),xs.max()])
    if name=='sheet-life' and len(comps)<len(names):   # deux poses empilées dans chaque composante : coupe à la ligne la plus vide
        res=[]
        for c in comps:
            prof=c[0].sum(axis=1); lo=c[1]+int(.30*(c[2]-c[1])); hi=c[1]+int(.70*(c[2]-c[1]))
            cut_y=lo+int(np.argmin(prof[lo:hi]))
            for part in (slice(None,cut_y),slice(cut_y,None)):
                m_=np.zeros_like(c[0]); m_[part,:]=c[0][part,:]
                ys,xs=np.where(m_); res.append([m_,ys.min(),ys.max(),xs.min(),xs.max()])
        comps=res
    comps=[(c[0],(c[1]+c[2])/2,(c[3]+c[4])/2) for c in comps]
    comps.sort(key=lambda c:c[1]); rows=[]
    for c in comps:
        if rows and abs(rows[-1][0][1]-c[1])<240: rows[-1].append(c)
        else: rows.append([c])
    ordered=[c for r in rows for c in sorted(r,key=lambda c:c[2])]
    print(name,len(ordered),'composantes pour',len(names),'noms')
    for k,(m,_,_) in enumerate(ordered):
        ys,xs=np.where(m); y0,y1=ys.min(),ys.max(); h=y1-y0+1
        relax=name in ('sheet-walk','sheet-career','sheet-heads','sheet-labor','sheet-job','sheet-life')
        sh=m&((mx-mn)<(36 if relax else 10))&(lum>(198 if relax else 188)); sh[:y0+int(.78*h),:]=False      # ombre de sol : bas de l'objet seulement
        if False:
            sh2=m&((mx-mn)<30)&(lum>150)&(lum<(241 if k==2 else 227)); sh2[:y0+int(.60*h),:]=False; sh|=sh2
        if name=='sheet-heads': sh[:]=False
        lab_s,_=ndi.label(sh); outside=ndi.binary_dilation(~m,iterations=2)
        seeds=set(np.unique(lab_s[sh&outside]))-{0}
        m=m&~np.isin(lab_s,list(seeds)); m=ndi.binary_opening(m,iterations=2)
        if name in ('sheet-career','sheet-walk','sheet-labor') or (False):    # fond blanc enfermé (pieds de bureau, jambes, rouleau de câble)
            wh=m&(mn>=232)&((mx-mn)<16); lw,nw=ndi.label(wh)
            for q in range(1,nw+1):
                if (lw==q).sum()>=(150 if name in ('sheet-career','sheet-walk') else 600): m=m&~(lw==q)
        m=ndi.binary_fill_holes(m) if (name not in ('sheet-job','sheet-life','sheet-walk','sheet-labor')) else m
        m=ndi.binary_erosion(m,iterations=1)
        alpha=np.clip((ndi.gaussian_filter(m.astype(np.float32),0.9)-0.15)/0.7,0,1)
        rgba=np.dstack([np.asarray(im),(alpha*255).astype(np.uint8)])
        o=Image.fromarray(rgba,'RGBA'); bb=o.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox(); o=o.crop(bb)
        n_=names[k] if k<len(names) else f'{name}_{k}'
        o.save(f'{OUT}/{n_}.png'); print(' ',n_,o.size)
