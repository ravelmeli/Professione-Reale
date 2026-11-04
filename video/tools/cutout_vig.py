"""Découpe les planches « poliziotto » par composantes connexes (les planches ne sont pas des grilles régulières).
Usage: python3 tools/cutout_pol.py   (depuis video/)"""
import numpy as np, os
from PIL import Image
from scipy import ndimage as ndi

SHEETS = {
 'sheet-davide': ['davide_civ_full','davide_uni_full','davide_int_full','davide_esp_full','davide_capo_full','davide_head10'],
 'sheet-poses':  ['davide_study','davide_run','davide_bed','davide_lead'],
 'sheet-props3': ['camion','caserma','casco','manichetta','allarme','estintore'],
 'sheet-props4': ['mappa_roma','orologio','scala','radio','fiamma','caffe'],
}
OUT='assets/cut-vig'; os.makedirs(OUT,exist_ok=True)

def cutout(a):
    mn=a.min(axis=2); mx=a.max(axis=2)
    bg=mn>=238
    lab,_=ndi.label(bg)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    fg=~np.isin(lab,list(border))
    fg=ndi.binary_opening(fg,iterations=1)
    return fg,mn,mx

for name,names in SHEETS.items():
    im=Image.open(f'assets/raw-vig/{name}.jpg').convert('RGB'); a=np.asarray(im).astype(np.int16)
    fg,mn,mx=cutout(a); lum=a.mean(axis=2)
    fg=ndi.binary_opening(fg,iterations=2)
    lab,n=ndi.label(ndi.binary_dilation(fg,iterations=9))
    comps=[]
    for i in range(1,n+1):
        m=(lab==i)&fg
        if m.sum()<2500: continue
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
    comps=[(c[0],(c[1]+c[2])/2,(c[3]+c[4])/2) for c in comps]
    comps.sort(key=lambda c:c[1]); rows=[]
    for c in comps:
        if rows and abs(rows[-1][0][1]-c[1])<170: rows[-1].append(c)
        else: rows.append([c])
    ordered=[c for r in rows for c in sorted(r,key=lambda c:c[2])]
    print(name,len(ordered),'composantes pour',len(names),'noms')
    for k,(m,_,_) in enumerate(ordered):
        ys,xs=np.where(m); y0,y1=ys.min(),ys.max(); h=y1-y0+1
        relax=name!='sheet-props4'
        sh=m&((mx-mn)<(36 if relax else 10))&(lum>(198 if relax else 188)); sh[:y0+int(.78*h),:]=False      # ombre de sol : bas de l'objet seulement
        lab_s,_=ndi.label(sh); outside=ndi.binary_dilation(~m,iterations=2)
        seeds=set(np.unique(lab_s[sh&outside]))-{0}
        m=m&~np.isin(lab_s,list(seeds)); m=ndi.binary_opening(m,iterations=2)
        m=ndi.binary_fill_holes(m); m=ndi.binary_erosion(m,iterations=1)
        alpha=np.clip((ndi.gaussian_filter(m.astype(np.float32),0.9)-0.15)/0.7,0,1)
        rgba=np.dstack([np.asarray(im),(alpha*255).astype(np.uint8)])
        o=Image.fromarray(rgba,'RGBA'); bb=o.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox(); o=o.crop(bb)
        n_=names[k] if k<len(names) else f'{name}_{k}'
        o.save(f'{OUT}/{n_}.png'); print(' ',n_,o.size)
