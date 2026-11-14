# Analyse détaillée des 2 nouvelles références (Thomas — kebab / valise)

Fichiers : `ssstik.io_1794645300163.mp4` (A, « eau gratuite au kebab », 66,45 s) et `ssstik.io_1794645363652.mp4` (B, « valise cassée », 67,03 s).
Méthode : image par image (30 fps, 1993 et 2011 images), médiane temporelle du fond, mesure des sous-titres image par image, détection des événements audio par fréquence.
**Limite :** je n'ai pas écouté le son, je l'ai mesuré (fréquences, durées, niveaux). Les noms de sons ci-dessous sont des déductions à partir de ces mesures.

## 1. Format technique
- 576×1024 (9:16), 30 fps, H.264 ≈ 0,3 Mb/s. Voix AAC 44,1 kHz stéréo.
- Durée : 66,5 s et 67,0 s. Voix : ~150 mots/min, ton calme, aucune musique de fond détectée.
- Ratio d'échelle pour mes montages 1080×1920 : ×1,875. Pour le 16:9 (1920×1080) : mêmes proportions relatives, mais voir §12.

## 2. Fond (identique sur A et B)
- Dégradé bleu nuit très sombre : coins ≈ RGB (11,22,68), centre ≈ (15,24,74), bas ≈ (14,20,67). Quasi uniforme, **sans taches colorées** (pas d'aurore violette/turquoise).
- **Grille de 1 px** : lignes verticales fixes tous les 51 px (soit 8,85 % de la largeur ⇒ ≈ 96 px à 1080), de x = 47 ; amplitude ≈ +4 à +5 niveaux de luminance (très discrète).
- Lignes horizontales de même pas (51 px), qui **dérivent vers le bas d'environ 0,8 px/s** (à 576 px) et rebouclent.
- **Étoiles** : ≈ 19 points blancs de 2–3 px dans les bandes haute et basse (plus rares au milieu), qui **scintillent** (luminosité qui varie de ±15 à ±100 niveaux d'une image à l'autre) et **dérivent lentement** vers le haut/gauche (≈ −0,34 px/s en y, −0,18 px/s en x). Aucune étoile n'est au même endroit 3 s plus tard.
- Pas de vignette marquée, pas de particules flottantes, pas de changement de teinte entre sections.

## 3. Palette
- Rouge mot-clé : ≈ (248, 72, 88) = `#F84858`.
- Or (nom « THOMAS ») : ≈ (232, 184, 40) = `#E8B828`.
- Cartes d'interface : bleu ardoise ≈ (64–72, 72–80, 112–128) avec léger dégradé et ombre portée ; texte blanc.
- Vert « gratuit / OK » : ≈ (40, 200, 104) = `#28C868`.
- Papier (loi, carte, constat) : crème (248, 248, 240) avec texte sombre, police à empattement (type Cormorant / EB Garamond) pour les documents « officiels ».
- Rouge « refusé / payant » : même rouge que les mots-clés ; or/jaune pour les puces d'alerte (« Attention », « 7 jours max », « Convention de Montréal »).

## 4. Sous-titres (le plus important pour le rythme)
- Police : sans empattement géométrique, très grasse (type Plus Jakarta Sans / Outfit ExtraBold), **majuscules**, blanc pur, ombre douce.
- Position : centrés, **ligne de base à ≈ y 740/1024 (72 %)**, hauteur de texte ≈ 40–46 px à 576 px de large. **Les ≈ 27 % du bas sont vides** (zone d'interface TikTok).
- **Un seul bloc à la fois, 1 à 4 mots par bloc** (« D'EAU À DEUX EUROS », « L'EAU DOIT ÊTRE », « ASSIETTE »). Durée d'un bloc : 0,27 à 1,5 s, médiane ≈ 0,7 s. Les blocs ne se chevauchent pas ; il n'y a pas de « karaoké » mot par mot.
- **Largeur max ≈ 90 %** (x 28–525 sur 576). Quand le texte est trop long, la police **rétrécit automatiquement** (ex. « IL DEMANDE JUSTE UNE CARAFE » ≈ −25 % de taille) au lieu de passer sur deux lignes.
- **Mot-clé en rouge** (`#F84858`) : 1 à 2 mots par bloc (« DEUX EUROS », « PAYANTE », « REFUSER », « AUCUNE AFFICHE »). Le rouge est présent dès l'apparition du bloc (pas de transition de couleur visible).
- Entrée : **fondu + flou ≈ 0,1 s** (le bloc arrive flou et net en 3 images), sortie identique (flou + fondu ≈ 0,1 s). Légère montée de ~4–6 px.

## 5. Composition d'une scène
- Zone de contenu : **de y ≈ 100 à y ≈ 620 sur 1024** (10 % → 60 %), centrée horizontalement. Au-dessus : vide ; sous les sous-titres : vide.
- Un seul « sujet » à la fois : soit un diorama + personnage, soit une carte d'interface, soit les deux (personnage en bas, carte au-dessus). Jamais trois idées simultanées.
- Les personnages mesurent ≈ 200–230 px de haut à 576 px (≈ 20 % de la hauteur) quand ils sont dans un diorama ; ≈ 150 px dans une scène avec carte.
- Ombre portée douce sous chaque objet ; pas de halo derrière les personnages.

## 6. Personnage et dioramas
- Personnage 3D pâte à modeler stylisé, **plusieurs poses distinctes** qui s'alternent (assis qui mange, boit, tient un verre, debout les bras ouverts, marche avec la valise, croise les bras, pointe du doigt). Les poses **changent d'image à image** (pas de simple flottement) : ex. A 0–2 s, il mange puis boit ; B 3–5 s, il marche en tirant la valise (cycle de marche en 2–3 poses).
- Dioramas posés sur le fond (comptoir kebab avec enseigne **néon rose** « Les Cousins » qui s'allume en scintillant ; tapis à bagages ovale avec valises ; comptoir de compagnie ; terrasse de restaurant). Les éléments du diorama sont animés (le patron secoue la tête, la carafe se pose, les frites arrivent).
- Personnages secondaires : patron (noir, tablier), agent d'accueil, ami (gilet gris), tous du même style.

## 7. Cartes d'interface animées (la vraie différence avec mes montages)
Chaque information-clé devient une **mini-interface**, pas un tag :
- **Carte prix** (A 3–5 s) : puce « Bouteille d'eau 2,00 € » + barre « Payer · 2,00 € » ; le prix **descend** 2,00 → 1,25 → 0,00 (compteur), la barre se barre en rouge, puis devient bouton vert « ✓ Gratuite ».
- **Graphique** (A 18–23 s) : carte « La bouteille d'eau », formule « 2 € × 2 × 52 = 208 € » qui se construit terme par terme, **courbe qui se trace** avec points dorés, repère « 52 € », « 148 € », « 208 € ».
- **Document légal** (A 23–31 s) : page crème « Article L541-15-10 », titre en machine à écrire, corps du texte qui apparaît, **surlignage jaune** des mots clés qui se déplace avec la voix, pastille « En vigueur · 2022 », un **livre rouge** qui tombe puis s'ouvre en page.
- **Carte de restaurant** (A 32–36 s) : lignes de menu (prix alignés), ligne « Eau potable gratuite 0,00 € » ajoutée, **affiche inclinée « EAU GRATUITE »** qui se pose.
- **Interrupteurs** (A 47–52 s) : carte « Pour y avoir droit » avec 3 toggles qui **basculent** un à un (vert) ; le dernier (« À emporter ») reste rouge + « ✗ Ne marche pas ».
- **Smartphone** (A 38–45 s, 57–66 s) : mockup qui affiche la loi, puis l'appli « SignalConso » (formulaire rempli, bouton bleu → « ✓ Signalement envoyé » vert), puis page de chaîne « Expliqué par Thomas — S'abonner → ✓ Abonné » avec 3 vignettes vidéo qui apparaissent.
- **Bulles de dialogue** (A 14–17 s) : bulle « LE PATRON — Ici, pas d'eau gratuite. » avec petite queue, qui se transforme en carte avec le prix.
- **Mail** (B 20–37 s) : fenêtre « Nouveau message » (À / Objet remplis), **texte tapé lettre par lettre en synchro avec la voix**, mots clés en jaune, puces de pièces jointes qui s'ajoutent (« Constat.pdf », « Photos (2) », « Facture.pdf », « Liste des affaires »), bouton « Envoyer » → « Envoyé ✓ », pastille « 7 jours max » qui compte 6 → 7.
- **Appareil photo** (B 7–11 s) : viseur avec cadre de mise au point, bouton déclencheur, **flash blanc** puis miniature de la photo.
- **Constat papier** (B 15–19 s) : fiche « Constat d'irrégularité » avec cases à cocher qui se cochent, polaroid de la roue arrachée qui se pose.
- **Tableau des départs** (B 38–42 s) : panneau noir style aéroport, lignes « VL 4521 Rome… », pastilles vertes « ✓ Couvert » qui apparaissent une à une, étiquette dorée « Convention de Montréal ».
- **Comparaison avant/après** (B 46–51 s) : deux cartes « Avant le vol / Après le vol » avec la même valise, un **avion en pointillés** qui passe entre les deux, tampon rouge penché « ✗ Refusé », flash de la photo de départ « ✓ Preuve — intacte avant le vol ».
- **Frise de délai** (B 51–57 s) : barre « Envoyé — 1 mois — 2 mois » avec curseur qui avance, carte « Médiateur Tourisme et Voyage — ✓ Gratuit » avec balance.
- **Suivi de bagage** (B 57–62 s) : « Jour 0 / 21 → 21 / 21 » avec 21 petits carrés qui se remplissent en jaune puis **tout passe au rouge** (« ✗ Perdu »), puis carte « Indemnisation » avec 3 puces cochées.
- **Compteur final** (B 65–66 s) : « Remboursement +0 € → +90 € → +200 € ».
- **Panneau d'arrivées** (B 0–5 s) : bandeau noir « ARRIVÉES Vol 4521 — Tapis 3 — À l'heure » (texte jaune/vert) qui devient « Retard / Remboursement » puis monte 40 → 100 → 170 → 200 €.

## 8. Titre « Expliqué par Thomas » (identique A et B)
- À ≈ 5,2–6,7 s : écran presque vide avec Thomas seul. Le mot « EXPLIQUÉ PAR » apparaît en **petites capitales très espacées** (interlettrage large qui se resserre), puis « **THOMAS** » en **or gras, grande taille**, avec lueur dorée. Dure ≈ 1,5 s, accompagné d'un son multi-tons (voir §10).

## 9. Transitions et mouvement
- **Entrée / sortie des éléments** : glissement (≈ 0,3 s, ease-out) horizontal (poussée de droite à gauche entre deux scènes : ancienne scène sort à gauche **tronquée par le cadre**, nouvelle arrive de la droite) et vertical (objets qui tombent du haut, ex. le livre rouge, ou qui montent du bas). Aucun fondu enchaîné long.
- Les éléments secondaires **arrivent légèrement après** le principal (décalage ≈ 0,1–0,2 s), pas tous en même temps.
- **Rythme visuel** : un changement de scène ou une nouvelle carte toutes les ≈ 2–3 s ; plus de 30 « scènes » en 66 s.
- Les cartes d'interface restent fixes ; leur **contenu** s'anime à l'intérieur (compteurs, curseurs, frappe, cases).
- Pas de zoom caméra global, pas de secousse, pas de flash plein écran sauf le flash de l'appareil photo (B 10 s).
- Dérive très lente du fond (§2) comme seul mouvement ambiant.

## 10. Son (mesuré, pas écouté)
- **Voix seule, aucune musique ni nappe** : plancher de bruit dans les pauses ≈ −60 dB, pauses quasi silencieuses, LRA 2,5 LU, niveau ≈ **−19,5 LUFS** (A −19,5 ; B −19,4), crête ≈ −2 dBFS. (Mon montage actuel est à ≈ −13 LUFS avec nappe + musique : beaucoup plus chargé.)
- **Petits sons d'interface** brefs (50–400 ms), tonals, très aigus, sur les événements visuels : fréquences récurrentes ≈ **6 276 Hz, 9 819 Hz, 2 347 Hz, 3 509 Hz, 2 659 Hz** (pings / clics type notification ou frappe), niveau faible.
- Événements marquants A : ≈ 0,3–1,0 s (4 clics à 6 kHz : le néon qui s'allume) ; 4,96 s (ding fort 2,3 kHz : prix → « Gratuite ») ; 6,4–7,3 s (balayage multi-tons : titre « THOMAS ») ; 21,2 et 21,9 s (dings 2,3 kHz : somme « 208 € ») ; 32,25 s (ding 3,5 kHz long 0,42 s : « Mieux ») ; 44,15–44,9 s (clics 6,3 kHz : carafe/frites) ; 54,7 et 55,6 s (tap 3,5 kHz) ; 58,3 s (ping 2,7 kHz : « signaler »).
- Événements marquants B : ≈ 0,2–0,6 s (clics 6,3 kHz) ; 4,0–5,3 s (frappes 2,3 kHz en rafale : photo) ; 6,3–7,2 s (balayage multi-tons : titre) ; 41,4–42,2 s (rafale clics + 3,1/2,4 kHz : bon d'achat) ; 45,5–46,5 s (clics 9,8 kHz en rafale : tampon/refus) ; 62,3–62,6 s (clic 6,3 kHz) ; 66,7 s (ding 5,7 kHz final : « +200 € »).
- Aucun « impact » grave détecté (peu d'énergie sous 150 Hz hors voix).

## 11. Structure narrative (reproductible)
1. **Phrase-choc + promesse chiffrée** dans les 5 premières secondes (« la compagnie doit te rembourser jusqu'à 200 € »).
2. « Voici comment, expliqué par Thomas » → titre or (§8).
3. **Mise en situation** en dioramas (Thomas + commerçant), conflit, loi/règle présentée en carte « document officiel ».
4. **Étapes pratiques** une idée par carte (mail, photo, délai, médiateur).
5. **Limites honnêtes** (« Attention, si… ») : cartes « Attention » en or.
6. **Appel final** : « envoie ça à ton pote… », puis carte « Expliqué par Thomas — S'abonner ».
- Chaque règle de droit citée avec **sa source visible** (article, convention, site officiel).

## 12. Écarts avec mes montages actuels (à corriger)
| Élément | Références A/B | Mes montages |
|---|---|---|
| Fond | bleu nuit uni, grille 1 px, étoiles qui scintillent | aurore violette/turquoise, blobs, particules, teinte par chapitre |
| Info chiffrée | **mini-interface** (carte, formulaire, graphique, tracker) | pastille / panneau « glass » + compteur |
| Personnage | poses distinctes qui alternent, pas de halo | une pose + flottement, halo violet |
| Sous-titres | 1–4 mots, 72 %, flou 0,1 s, rouge sur 1–2 mots, taille adaptative | une ligne ≤ 24–40 car., mots-clés qui rougissent à l'instant du mot |
| Effets de caméra | aucun | zoom/shake à chaque point fort, dérive de caméra |
| Son | voix seule −19,5 LUFS + pings d'interface | nappe + musique + 80–220 effets, −13 LUFS |
| Transitions | poussée horizontale/verticale 0,3 s, objets tronqués | « le décor recule » (flou + échelle) |
| Éléments chrome | ni règle ni jauges | règle de carrière + jauges HUD |
| Titre | « EXPLIQUÉ PAR THOMAS » espacé + or | aucun |

## 13. Ce que je propose de reproduire à l'identique
1. Fond : dégradé #0B1646→#0F184A, grille 1 px / 96 px (1080), dérive horizontale 1,5 px/s, 19 étoiles scintillantes et dérivantes ; **supprimer** aurore, particules, teintes par chapitre, vignette.
2. Sous-titres : police ExtraBold majuscules, 1–4 mots, flou 0,1 s, rouge `#F84858`, 72 % de la hauteur, taille adaptative à 90 % de la largeur, **supprimer** zoom/shake et dérive de caméra.
3. Bibliothèque de **composants d'interface** réutilisables : carte prix à compteur, graphique avec courbe, document avec surlignage et frappe, carte de menu, toggles, smartphone/appli, bulle de dialogue, mail à frappe, viseur photo + flash, tableau d'affichage, comparaison avant/après avec tampon, frise de délai, tracker de jours (21 carrés), compteur « +200 € », carte « Expliqué par… / S'abonner ».
4. Poses multiples du personnage (≥ 8 par vidéo, dont marche en 2–3 poses) + dioramas.
5. Transitions : poussée horizontale 0,3 s et chutes/montées verticales, éléments tronqués par le cadre.
6. Titre d'intro « EXPLIQUÉ PAR [NOM CHAÎNE] » en capitales espacées + nom en or.
7. Son : voix seule à −19,5 LUFS + banque d'une trentaine de pings tonals (2,3 / 3,1 / 3,5 / 6,3 / 9,8 kHz) calés sur les événements ; **retirer nappe et musique**.
8. **Pour le 16:9** (vidéos longues) : même langage visuel, contenu en bande centrale ≈ 60 % de la hauteur, sous-titres à 82 % de la hauteur, 1920×1080, cartes plus larges (deux cartes côte à côte possibles).

## 14. Points à confirmer avec toi avant de produire
- Le **fond uni** s'applique-t-il aussi au 16:9 ? (Tu avais demandé « le même fond que les shorts » ; ces nouvelles références montrent un fond **différent** des shorts actuels.)
- **Retirer la musique** et la nappe ? Les références n'en ont pas.
- **Retirer la règle de carrière et les jauges** (elles n'existent pas dans les références) ?
- Quel personnage et quelle chaîne pour le titre « EXPLIQUÉ PAR … » ? (« Professione Reale » ?)
