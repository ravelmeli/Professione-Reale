"""Découpe les planches Nano Banana en éléments détourés (PNG transparents).
Usage: python3 tools/cutout.py   (depuis le dossier video/)"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import os

SHEETS = {
 'sheet-marco': (3,2,['marco23_full','marco28_full','marco33_full','marco38_full','marco23_head','marco38_head']),
 'sheet-poses': (2,2,['marco23_calc','marco33_chair','marco33_phone','marco38_tired']),
 'sheet-camion':(2,2,['truck_new','truck_worn','truck_broken','cab_interior']),
 'sheet-docs':  (3,2,['patente','cqc','patenteCE','tachigrafo','multa','calendario']),
 'sheet-costi': (3,2,['portafoglio','pompa','assicurazione','rate','bivio','chiavi']),
 'sheet-misc':  (2,2,['figlio','smartphone','soldi','campanella']),
}
OUT='assets/cut'; os.makedirs(OUT,exist_ok=True)

def cutout(cell,band=0.0,name=''):
    a=np.asarray(cell.convert('RGB')).astype(np.int16)
    mn=a.min(axis=2); mx=a.max(axis=2)
    near_white=mn>=240
    lab,_=ndi.label(near_white)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(border))
    fg=~bg
    fg=ndi.binary_opening(fg,iterations=1)
    lab,n=ndi.label(ndi.binary_dilation(fg,iterations=6))
    keep=np.zeros_like(fg)
    for i in range(1,n+1):
        comp=(lab==i)&fg
        area=comp.sum()
        if area<1500: continue
        ys,xs=np.where(comp)
        h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
        sat=(mx-mn)[comp].mean(); lum=a[comp].mean()
        if h/w<0.38 and sat<75 and lum>150: continue   # ombres plates détachées
        keep|=comp
    keep=ndi.binary_fill_holes(keep)
    if band>0:  # ombre de contact : dégradé doux relié au fond ; un bord franc (remorque blanche) bloque la propagation
        lum=ndi.gaussian_filter(a.mean(axis=2),0.7)
        gy,gx=np.gradient(lum)
        G=np.maximum(np.abs(gx),np.abs(gy))
        smooth=keep&(lum>195)&((mx-mn)<60) if band>=2 else keep&(G<=1.6)&(lum>200)&((mx-mn)<48)
        outside=ndi.binary_dilation(~keep,iterations=2)
        lab2,_=ndi.label(smooth)
        seeds=set(np.unique(lab2[smooth&outside]))-{0}
        keep&=~np.isin(lab2,list(seeds))
    lum_all=a.mean(axis=2)
    if name.startswith(('truck','cab_','marco','campanella','soldi','pompa','chiavi')) and not name.endswith('_head'):
        # ligne de sol : tout ce qui se trouve sous le dernier pixel sombre ou coloré est de l'ombre
        solid=keep&((lum_all<110)|((mx-mn)>(125 if name=='cab_interior' else 85)))
        if name=='cab_interior': solid=keep&(a[...,0]>170)&(a[...,1]<80)&(a[...,2]<80)
        rows=np.where(solid.sum(axis=1)>=(25 if name=='cab_interior' else 4))[0]
        if len(rows):
            y_g=rows.max(); keep[y_g+6:,:]=False
            if name.startswith('truck'):   # reste d'ombre sur les côtés des roues
                h_=y_g-rows.min(); pale=keep&(mn>205)&((mx-mn)<30)
                pale[:y_g-int(0.09*h_),:]=False
                keep&=~pale
    if name.startswith('marco') and not name.endswith('_head'):
        # espace blanc entre les jambes : zones quasi blanches dans la moitié basse
        ys=np.where(keep.any(axis=1))[0]; ylow=ys.min()+int(0.55*(ys.max()-ys.min()))
        white=(mn>=236)&((mx-mn)<16)
        white[:ylow,:]=False
        lab3,n3=ndi.label(white&keep|(white&~keep&ndi.binary_dilation(keep,iterations=2)))
        for i in range(1,n3+1):
            m=lab3==i
            if m.sum()>=120: keep&=~m
        keep=ndi.binary_fill_holes(keep) if False else keep
    keep=ndi.binary_erosion(keep,iterations=1)
    alpha=ndi.gaussian_filter(keep.astype(np.float32),0.9)
    alpha=np.clip((alpha-0.15)/0.7,0,1)
    rgba=np.dstack([np.asarray(cell.convert('RGB')),(alpha*255).astype(np.uint8)])
    im=Image.fromarray(rgba,'RGBA')
    bb=im.getchannel('A').point(lambda v:255 if v>8 else 0).getbbox()
    return im.crop(bb) if bb else im

for name,(cols,rows,names) in SHEETS.items():
    im=Image.open(f'assets/raw/{name}.jpg').convert('RGB')
    W,H=im.size; cw,ch=W//cols,H//rows
    for k,n in enumerate(names):
        r,c=divmod(k,cols)
        cell=im.crop((c*cw,r*ch,(c+1)*cw,(r+1)*ch))
        band={'sheet-marco':0.07,'sheet-poses':0.07,'sheet-camion':0.10}.get(name,0.0)
        if n in ('campanella','soldi','cab_interior','tachigrafo','chiavi','portafoglio','bivio'): band=2
        if n=='figlio': band=0
        out=cutout(cell,band,n)
        out.save(f'{OUT}/{n}.png')
        print(n,out.size)
