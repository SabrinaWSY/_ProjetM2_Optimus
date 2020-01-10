# _ProjetM2_Optimus
Projet pour cours Documents Structurés TAL INALCO M2

# Problématique
Existe-t-il une corrélation positive entre le nombre de cinéma, le nombre de lieu de tournage et le nombre de monument historique dans les 20 arrondissements de Paris ?

# Visualisation
- Page d'acceuil en xml avec transformation xslt : web/index.xml
- Page de présentation du projet en xml aussi : web/presentation.xml
- Page de résultat en html (pour la varieté de format) : web/html/resultat.html

# Structure du répertoire 
- data : les données csv et json de API
- grammaire : rng et dtd du fichier xml généré
- script : script python pour traiter les fichiers csv, extraire les données pertinentes, et générer les graphes
- web : la visualisation du projet (vient d'être décrit en haut)
- xml : le ficher output xml généré par le script python

# Attention 
- Nous avons remarqué que la nouvelle version de Firefox ne peut pas afficher la page xml correctement, puisqu'il ne prend pas en compte la feuille xslt. If faut donc une version de 6.xxx de Firefox pour le visualisé.
- PS : Si vous n'arrivez pas à visualiser le page xml, il y a une video de visualistation dans cette repo :)
