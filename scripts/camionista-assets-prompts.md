# Prompts d'images — « La tua vita dopo 15 anni da camionista »

Style : 3D pâte à modeler (comme les références). Le personnage s'appelle **Marco** (nom de travail, à changer si tu veux).
Chaque image est générée **isolée sur fond uni**, pour que je la détoure et que je l'anime en HTML.
Tout le texte (chiffres, fiches de paie, graphiques, compteurs, cartes d'interface) est fait en HTML : **aucune image ne doit contenir de texte**.

---

## 0. Mode d'emploi

1. **Génère d'abord C-01** (Marco à 23 ans). Valide le visage et le style avant de continuer.
2. **Utilise C-01 comme image de référence** pour tous les autres Marco (C-02 à C-12) :
   - Midjourney : `--cref <url C-01> --cw 100` (ou `--oref` en v7)
   - Autres outils (Flux Kontext, Nano Banana, GPT-image, etc.) : joins C-01 en image de référence et ajoute « same character as the reference image ».
3. **Utilise toujours le BLOC STYLE et le BLOC FOND** ci-dessous, collés à la fin de chaque prompt.
4. Format : personnages et objets en **1:1**, scènes d'ambiance (E-xx) en **1:1** avec le sujet centré (je recadre en 9:16 et en 16:9).
5. Résolution minimum **2048 px** de côté. Nomme chaque fichier avec son identifiant (ex. `C-01.png`).
6. Si le fond n'est pas bien uni, génère à nouveau : un fond propre se détoure beaucoup mieux.

### BLOC STYLE (à coller dans chaque prompt)
```
soft 3D claymation style, handmade plasticine clay look, matte clay material with subtle fingerprint texture, soft rounded edges, chunky simplified proportions, big expressive eyes with white highlights, stop-motion animated film feel, warm soft studio lighting with a gentle colored rim light, shallow depth of field, premium 3D animated feature quality, highly detailed
```

### BLOC FOND (à coller dans chaque prompt d'objet ou de personnage)
```
isolated on a plain flat solid light gray background, subject centered with generous margin, full subject visible, soft contact shadow only, no other objects
```

### BLOC NÉGATIF (si ton outil a un champ « negative prompt », sinon ajoute « no … » en fin de prompt)
```
text, letters, numbers, logos, watermark, brand names, license plate text, 2D illustration, flat vector, anime, photorealistic, live action, extra fingers, extra limbs, deformed face, blurry, cropped, busy background
```

---

## 1. MARCO — fiche personnage (identité à garder identique)

**À verrouiller dans chaque image de Marco :**
- Visage rond et sympathique, **grands yeux sombres** avec reflets blancs, **gros sourcils bruns épais**, nez rond, peau olive.
- **Cheveux** bruns foncés, courts et ondulés.
- **Vêtements fixes** : veste de travail **vert bleuté foncé** avec **deux bandes réfléchissantes orange** sur les manches, t-shirt gris, jean bleu, **bottes marron**.
- Il **vieillit** de 23 à 38 ans : voir les étapes ci-dessous. Ne change jamais les vêtements ni les couleurs.

**Description commune (à répéter dans chaque prompt de Marco) :**
```
Marco, a friendly Italian truck driver character, round face, big dark eyes with white highlights, thick dark-brown eyebrows, round nose, olive skin, short wavy dark-brown hair, dark teal work jacket with two orange reflective stripes on the sleeves, grey t-shirt, blue jeans, brown work boots
```

### C-01 — Marco à 23 ans, référence principale (utilisé aux scènes 1, 5, 34)
```
[Description commune de Marco], age 23, slim, clean-shaven, fresh and hopeful expression with a small confident smile, full body standing front view, relaxed pose, arms slightly away from the body, facing camera. [BLOC STYLE] [BLOC FOND]
```

### C-02 — Marco à 23 ans, vue de trois quarts (turnaround)
```
[Description commune de Marco], age 23, slim, clean-shaven, hopeful smile, full body three-quarter view turned to his right, walking forward with confidence. [BLOC STYLE] [BLOC FOND]
```

### C-03 — Marco à 23 ans, regard inquiet / calcul (scène 2, 6)
```
[Description commune de Marco], age 23, slim, clean-shaven, holding a small calculator in one hand and looking at it with a worried expression, one eyebrow raised, full body front view. [BLOC STYLE] [BLOC FOND]
```

### C-04 — Marco à 28 ans, « Anno cinque » (scènes 9 à 15)
```
[Description commune de Marco], age 28, slightly broader shoulders, light stubble, confident but a little tired eyes, full body standing front view, one hand resting on a steering wheel-like hip pose, facing camera. [BLOC STYLE] [BLOC FOND]
```

### C-05 — Marco à 28 ans, concentré au volant (scènes 13, 14)
```
[Description commune de Marco], age 28, light stubble, seated, hands on a large truck steering wheel, eyes focused straight ahead, upper body view from the front, only the steering wheel and his torso visible. [BLOC STYLE] [BLOC FOND]
```

### C-06 — Marco à 33 ans, « Anno dieci » (scènes 16 à 24)
```
[Description commune de Marco], age 33, short trimmed dark beard, a small round belly, visible tiredness under the eyes, proud but weary expression, full body standing front view, arms crossed, facing camera. [BLOC STYLE] [BLOC FOND]
```

### C-07 — Marco à 33 ans, assis, fatigué (scènes 22, 23)
```
[Description commune de Marco], age 33, short trimmed dark beard, small belly, sitting alone on a folding camping chair, head slightly down, tired and lonely expression, full body three-quarter view. [BLOC STYLE] [BLOC FOND]
```

### C-08 — Marco à 33 ans, au téléphone (scène 24)
```
[Description commune de Marco], age 33, short trimmed dark beard, holding a smartphone in front of him with both hands, looking at the screen with a soft emotional smile, tender expression, upper body view, the phone screen is a plain glowing blank rectangle. [BLOC STYLE] [BLOC FOND]
```

### C-09 — Marco à 38 ans, « Anno quindici », référence de fin (scènes 25, 35, 36)
```
[Description commune de Marco], age 38, short beard with grey-white salt-and-pepper patches, grey hair at the temples, dark eye bags, a larger round belly, slightly hunched shoulders, jacket slightly faded and worn, tired but dignified expression, full body standing front view, arms hanging down, facing camera. [BLOC STYLE] [BLOC FOND]
```

### C-10 — Marco à 38 ans, hésitant au bivio (scènes 25, 26)
```
[Description commune de Marco], age 38, grey-white salt-and-pepper beard, grey temples, eye bags, round belly, standing with one hand scratching the back of his head, thoughtful hesitating expression, looking sideways, full body three-quarter view. [BLOC STYLE] [BLOC FOND]
```

### C-11 — Marco à 38 ans, fatigué dans la cabine (scènes 32, 33)
```
[Description commune de Marco], age 38, grey-white salt-and-pepper beard, grey temples, heavy eye bags, round belly, sitting tired with one hand on his forehead, shoulders slumped, sad and thoughtful expression, upper body three-quarter view. [BLOC STYLE] [BLOC FOND]
```

### C-12 — Marco à 38 ans, gros plan visage (scène 36)
```
[Description commune de Marco], age 38, grey-white salt-and-pepper beard, grey temples, heavy eye bags, a bittersweet half-smile, head and shoulders close-up portrait, facing the camera, warm side lighting. [BLOC STYLE] [BLOC FOND]
```

---

## 2. PERSONNAGE SECONDAIRE

### P-01 — Le fils de Marco, 7 ans (scène 24, sur l'écran du téléphone)
```
a cute 7-year-old Italian boy, round face, big dark eyes, short wavy dark-brown hair like his father, blue t-shirt, waving happily to the camera, upper body view. [BLOC STYLE] [BLOC FOND]
```

---

## 3. CAMION (même modèle partout)

**Verrouillage :** camion italien de type **cabine avancée (cab-over)**, cabine **rouge**, remorque **blanche**, pare-chocs gris, deux phares ronds, **aucun logo, aucun texte, aucune plaque lisible**. Il vieillit un peu à partir de l'« Anno quindici » (rayures légères).

### T-01 — Camion tracteur + remorque, trois quarts avant (scènes 3, 9, 34, 37)
```
a red cab-over European semi truck with a white trailer, three-quarter front view, round headlights, grey bumper, clean and polished, no logos, no text, no readable license plate. [BLOC STYLE] [BLOC FOND]
```

### T-02 — Camion de profil (pour le faire rouler à l'écran, scènes 3, 9)
```
the same red cab-over European semi truck with a white trailer, perfect side view, wheels clearly visible, all four wheels on the same ground line, no logos, no text, no readable license plate. [BLOC STYLE] [BLOC FOND]
```

### T-03 — Camion usé, trois quarts avant (scènes 25, 26, 35)
```
the same red cab-over European semi truck with a white trailer, three-quarter front view, slightly worn, small scratches and mud on the lower body, dusty windshield, no logos, no text, no readable license plate. [BLOC STYLE] [BLOC FOND]
```

### T-04 — Camion en panne (scène 31)
```
the same red cab-over European semi truck, front hood cab tilted open showing the engine, a thin trail of smoke coming out, a red warning triangle on the ground in front of it, three-quarter front view, no logos, no text. [BLOC STYLE] [BLOC FOND]
```

### T-05 — Intérieur de la cabine avec couchette (scène 8)
```
the inside of a European truck cab seen from behind the seats, a small bunk bed with a rumpled blanket and a pillow behind the seats, a hanging air freshener, a thermos on the dashboard, warm yellow cabin light, cozy but cramped, no text. [BLOC STYLE] [BLOC FOND]
```

---

## 4. OBJETS (un par image)

| ID | Scène | Objet |
|---|---|---|
| O-01 | 2 | Permis de conduire italien (carte rose, sans texte) |
| O-02 | 2 | Carte CQC (carte rigide, camion en pictogramme) |
| O-03 | 2, 6, 12 | Pile de pièces et de billets de banque |
| O-04 | 9 | Permis catégorie CE (même carte que O-01, avec un pictogramme camion + remorque) |
| O-05 | 13, 14 | Tachygraphe numérique |
| O-06 | 15 | Contravention (papier avec bande rouge) |
| O-07 | 17, 18 | Calendrier mural (pages qui se tournent) |
| O-08 | 12 | Portefeuille ouvert, presque vide |
| O-09 | 30 | Pompe à essence |
| O-10 | 30 | Document d'assurance avec tampon |
| O-11 | 30 | Plaquette de facilité de paiement (rates) |
| O-12 | 26 | Poteau de signalisation en fourche (deux flèches) |
| O-13 | 26 | Clés du camion avec porte-clés |
| O-14 | 24 | Smartphone (cadre seul, écran lumineux uni) |
| O-15 | 22 | Chaise de camping et petite lampe |
| O-16 | 37 | Cloche de notification + bouton d'abonnement stylisé (sans texte) |

### O-01 — Permis de conduire
```
a rounded pink Italian driver's license card, a small plain photo area and plain blank lines, a tiny steering wheel icon, no text, no numbers, floating at a slight angle. [BLOC STYLE] [BLOC FOND]
```

### O-02 — Carte CQC
```
a rigid yellow-and-blue professional driver qualification card, a small plain photo area, a pictogram of a truck, no text, no numbers, floating at a slight angle. [BLOC STYLE] [BLOC FOND]
```

### O-03 — Pièces et billets
```
a small stack of gold coins next to a few folded euro-style green banknotes with plain symbols only, no readable numbers, no text, front view. [BLOC STYLE] [BLOC FOND]
```

### O-04 — Permis CE
```
a rounded pink driver's license card with a bold pictogram of a truck pulling a trailer in the corner, plain blank lines, no text, no numbers, floating at a slight angle. [BLOC STYLE] [BLOC FOND]
```

### O-05 — Tachygraphe
```
a digital truck tachograph device, grey rectangular body with a small round clock-like display, a few buttons and a card slot, no text, no numbers on the display, front view. [BLOC STYLE] [BLOC FOND]
```

### O-06 — Contravention
```
a paper traffic fine ticket with a red stripe at the top, plain blank lines, a small stamp mark, slightly curved paper, no text, no numbers. [BLOC STYLE] [BLOC FOND]
```

### O-07 — Calendrier
```
a wall calendar with a spiral binding on top, the top page half turned, a grid of plain small squares, no text, no numbers. [BLOC STYLE] [BLOC FOND]
```

### O-08 — Portefeuille presque vide
```
an open brown leather wallet with just one small coin inside, a faint dusty look, front view, no text. [BLOC STYLE] [BLOC FOND]
```

### O-09 — Pompe à essence
```
a gas station diesel pump, green and white body, round gauge on the front, a black nozzle hanging on the side, no text, no logos, three-quarter view. [BLOC STYLE] [BLOC FOND]
```

### O-10 — Assurance
```
an insurance document with a blue shield symbol on the top, plain blank lines and a round red stamp, slightly curved paper, no text, no numbers. [BLOC STYLE] [BLOC FOND]
```

### O-11 — Rates (échéancier)
```
a small payment booklet with a grid of plain squares, a few squares marked with check ticks, a paper clip on the corner, no text, no numbers. [BLOC STYLE] [BLOC FOND]
```

### O-12 — Poteau en fourche
```
a wooden signpost with two arrows pointing in two different directions, left and right, no text, no symbols on the arrows, a little grass at the base. [BLOC STYLE] [BLOC FOND]
```

### O-13 — Clés du camion
```
a set of truck keys on a ring with a small red toy-truck keychain, front view, no text. [BLOC STYLE] [BLOC FOND]
```

### O-14 — Smartphone
```
a modern smartphone, front view, the screen is a plain softly glowing blue rectangle, no icons, no text. [BLOC STYLE] [BLOC FOND]
```

### O-15 — Chaise de camping et lampe
```
a small folding camping chair next to a little camping lantern with a warm glowing light, three-quarter view, no text. [BLOC STYLE] [BLOC FOND]
```

### O-16 — Cloche d'abonnement
```
a golden notification bell with a small red dot badge and a rounded rectangular button next to it, both plain with no text and no logos, front view. [BLOC STYLE] [BLOC FOND]
```

---

## 5. DÉCORS (pas détourés, sujet centré)

| ID | Scène | Décor |
|---|---|---|
| E-01 | 3, 4 | Route droite au crépuscule, vers l'horizon |
| E-02 | 22, 23 | Parking de poids lourds, de nuit, lumière froide |
| E-03 | 37 | Route au coucher de soleil (fin) |

### E-01 — Route
```
a long straight highway going to the horizon at dusk, soft purple and teal sky, a few tiny stars, simple rounded clay-style hills and trees on each side, the road center is empty, wide cinematic composition with the road centered, no vehicles, no text. [BLOC STYLE]
```

### E-02 — Parking de nuit
```
a quiet truck parking lot at night, a few parked trailers in the distance, a single tall lamp post with a soft cold light, a dark navy sky with stars, empty foreground space in the center, no text, no logos. [BLOC STYLE]
```

### E-03 — Route au coucher de soleil
```
a long road going into a warm orange and pink sunset, simple rounded clay-style hills, a calm bittersweet mood, empty center of the road, no vehicles, no text. [BLOC STYLE]
```

---

## 6. Récapitulatif (36 images)

| Famille | Images | Nombre |
|---|---|---|
| Marco | C-01 à C-12 | 12 |
| Fils | P-01 | 1 |
| Camion | T-01 à T-05 | 5 |
| Objets | O-01 à O-16 | 16 |
| Décors | E-01 à E-03 | 3 |

Les éléments faits en **HTML** (rien à générer) : fiches de paie, chiffres animés (1 500 €, 2 000 €, 46 €, 25-30 €, 1 400-3 000 €), graphiques (fatturato/utile), compteurs (9 h, 90 h, 45 h), cartes d'interface, tampons rouges, fond dégradé nuit, sous-titres et mots clés en rouge.

## 7. Contrôle qualité avant de m'envoyer les images

- Marco a bien **le même visage** (yeux, sourcils, nez, cheveux) dans C-01 à C-12.
- Il **vieillit** de manière lisible : 23 (imberbe) → 28 (barbe légère) → 33 (barbe, petit ventre) → 38 (barbe poivre et sel, tempes grises, cernes, ventre).
- Les **vêtements** sont identiques partout (veste vert bleuté, bandes orange, t-shirt gris, jean, bottes marron).
- Le **camion** est le même modèle sur T-01 à T-04.
- **Aucun texte** ni logo n'apparaît dans une image.
- Les **fonds sont uniformes** (sauf les décors E-xx).
