"""Télécharge de vrais effets sonores libres (Openverse, CC0 de préférence) pour la vidéo."""
import json, os, subprocess, urllib.parse, urllib.request, sys
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'sfx2')
QUERIES = {   # nom -> (requête, durée max s)
 'truck-horn': ('truck horn', 4.5), 'diesel-start': ('diesel engine start', 6), 'cash-register': ('cash register', 5),
 'coins-drop': ('coins dropping on table', 3.5), 'stamp': ('stamp', 3), 'paper-slide': ('paper', 3),
 'camera-shutter': ('camera shutter click', 1.5), 'clock-tick': ('clock ticking', 4), 'heartbeat': ('heartbeat', 5),
 'riser': ('riser', 6), 'whoosh-deep': ('whoosh swoosh transition', 2), 'glass-ping': ('sparkle chime magic', 3),
 'door-slam': ('car door slam', 2.5), 'engine-off': ('engine off', 6), 'sigh': ('sigh tired breath', 3),
 'notif': ('phone notification', 2), 'calc-keys': ('calculator', 3), 'swipe': ('ui swipe', 1.5),
}
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=40).read()
credits = []
for name, (q, maxd) in QUERIES.items():
    if os.path.exists(os.path.join(OUT, name + '.mp3')): continue
    api = 'https://api.openverse.org/v1/audio/?' + urllib.parse.urlencode({'q': q, 'license': 'cc0', 'page_size': 20})
    try:
        res = json.loads(get(api))['results']
    except Exception as e:
        print(name, 'recherche échouée', e); continue
    cands = [r for r in res if r.get('duration') and r['duration'] / 1000 <= maxd and r['duration'] / 1000 >= 0.15]
    if not cands:
        print(name, '→ aucun résultat court CC0 pour', q); continue
    r = cands[0]
    try:
        data = get(r['url'])
    except Exception as e:
        print(name, 'téléchargement échoué', e); continue
    tmp = os.path.join(OUT, name + '.src')
    open(tmp, 'wb').write(data)
    # normalise : mono 44,1 kHz, coupe le silence initial, niveau crête ≈ -3 dB
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', 'silenceremove=start_periods=1:start_threshold=-50dB,dynaudnorm=f=150:g=7,volume=-3dB', '-ac', '1', '-ar', '44100', '-b:a', '128k', os.path.join(OUT, name + '.mp3')])
    os.remove(tmp)
    credits.append(f'{name}: "{r.get("title")}" par {r.get("creator")} — {r.get("license")} — {r.get("foreign_landing_url")}')
    print(name, 'ok', round(r['duration'] / 1000, 2), 's |', r.get('title'))
open(os.path.join(OUT, 'CREDITS.md'), 'a').write('\n'.join(credits) + '\n')
