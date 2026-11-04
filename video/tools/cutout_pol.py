"""Découpe les planches « poliziotto » par composantes connexes (les planches ne sont pas des grilles régulières).
Usage: python3 tools/cutout_pol.py   (depuis video/)"""
import numpy as np, os
from PIL import Image
from scipy import ndimage as ndi

SHEETS = {
 'sheet-luca':  ['luca_civ_full','luca_uni_full','luca_tired_full','luca_tired_full_b','luca_civ_head','luca_uni_head','luca_head3','luca_head4'],
 'sheet-poses': ['luca_study','luca_pushup','luca_bed','luca_salute'],
 'sheet-places':['scuola','dormitorio','volante','lettera','libri','valigia'],
 'sheet-time':  ['mappa','calendario','soldi','divisa'],
 'sheet-misc':  ['vassoio','casa','cornice','sveglia','bilancia','scudo'],
}
OUT='assets/cut-pol'; os.makedirs(OUT,exist_ok=True)

def cutout(a):
    mn=a.min(axis=2); mx=a.max(axis=2)
    bg=mn>=238
    lab,_=ndi.label(bg)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    fg=~np.isin(lab,list(border))
    fg=ndi.binary_opening(fg,iterations=1)
    return fg,mn,mx

for name,names in SHEETS.items():
    im=Image.open(f'assets/raw-pol/{name}.jpg').convert('RGB'); a=np.asarray(im).astype(np.int16)
    fg,mn,mx=cutout(a)
    lum=a.mean(axis=2)
    # ombres douces : peu saturées, claires, au contact du fond -> retirées
    shadow=fg&((mx-mn)<10)&(lum>188)
    lab_s,_=ndi.label(shadow)
    outside=ndi.binary_dilation(~fg,iterations=2)
    seeds=set(np.unique(lab_s[shadow&outside]))-{0}
    fg2=fg&~np.isin(lab_s,list(seeds))
    # petits trous / bords
    fg2=ndi.binary_opening(fg2,iterations=2)
    lab,n=ndi.label(ndi.binary_dilation(fg2,iterations=(40 if name=='sheet-time' else 9)))
    comps=[]
    for i in range(1,n+1):
        m=(lab==i)&fg2
        if m.sum()<2500: continue
        ys,xs=np.where(m); comps.append((m,ys.mean(),xs.mean()))
    if name=='sheet-time' and len(comps)>4:   # la Sardaigne se détache de la carte : on la rattache à la composante la plus proche
        comps.sort(key=lambda c:c[0].sum()); small=comps.pop(0)
        j=min(range(len(comps)),key=lambda k:(comps[k][1]-small[1])**2+(comps[k][2]-small[2])**2)
        m=comps[j][0]|small[0]; ys,xs=np.where(m); comps[j]=(m,ys.mean(),xs.mean())
    # ordre de lecture : lignes par centre y
    comps.sort(key=lambda c:c[1])
    rows=[];
    for c in comps:
        if rows and abs(rows[-1][0][1]-c[1])<170: rows[-1].append(c)
        else: rows.append([c])
    ordered=[c for r in rows for c in sorted(r,key=lambda c:c[2])]
    print(name,len(ordered),'composantes pour',len(names),'noms')
    for k,(m,_,_) in enumerate(ordered):
        m=ndi.binary_fill_holes(m); m=ndi.binary_erosion(m,iterations=1)
        alpha=np.clip((ndi.gaussian_filter(m.astype(np.float32),0.9)-0.15)/0.7,0,1)
        rgba=np.dstack([np.asarray(im),(alpha*255).astype(np.uint8)])
        o=Image.fromarray(rgba,'RGBA'); bb=o.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox(); o=o.crop(bb)
        n_=names[k] if k<len(names) else f'{name}_{k}'
        o.save(f'{OUT}/{n_}.png'); print(' ',n_,o.size)
