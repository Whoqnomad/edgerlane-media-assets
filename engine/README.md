# Moteur de visuels EDGERLANE MEDIA

- `lib.py` : gabarit commun (header `EDGERLANE [MEDIA]` + date, barre de progression, tag catégorie, pied de page sources + EDGERLANE.COM), moteur 3D isométrique (`Iso` : `box`, `cyl`, `label`, `platform`, `svg` auto-cadré) et `line_chart`.
- `example_posts_2026-10-10.py` : 6 posts de référence (simples, carrousels, 3D, graphique, agenda). **S'en inspirer pour chaque nouveau post.**
- `render.py <module.py> <sortie>` : rend chaque entrée de `POSTS` en PNG 1080×1350.

Date du header : dans le module du jour, `import lib; lib.DATE_TAG = "LUN. 12.10.2026"` avant de construire les pages.

## Règles de DA
- Catégories : `eco` jaune #F5B80B (macro, taux, banques centrales, matières premières), `fr` bleu #3B6BFF (politique française), `us` rouge #E5303A (politique américaine). Le vert #22C55E uniquement pour une variation positive.
- Fond noir, titres Inter Display Black en capitales, un chiffre clé en grand, sources datées en pied de page.
- Placer la scène 3D dans une zone bornée (`iso.svg(1000, hauteur)`), sans chevauchement avec le texte ; pour des barres comparatives, aligner sur l'axe écran (x = i*k, y = -i*k) et mettre les valeurs dans une rangée HTML sous la scène.
- Dernière slide d'un carrousel : « Contenu informatif, pas un conseil en investissement. » + CTA « Journalise tes trades sur edgerlane.com ».
- Vérifier chaque PNG visuellement avant publication (aucun texte qui se chevauche ou qui déborde).
