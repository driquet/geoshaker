.. contents:: **Table of contents**

----

Qu'est ce que GeoShaker
#######################

Description
-----------
GeoShaker est une application web créée dans le but de vous aider à trouver des
caches mystères. La plupart du temps, ces caches sont basées sur des coordonnées
contenant des variables. Parfois, vous ne pouvez pas trouver une de ces
variables.

C'est le cas lorsque un et/ou plusieurs indices ou caches sont manquants dans un
circuit. Si l'un de ces éléments est manquant, vous ne pouvez pas trouver la
cache bonus, car il vous manque une partie de la réponse.

Dans ce cas, GeoShaker peut vous aider en générant toutes les combinaisons
possibles, en excluant celles qui ne sont pas valides et en les affichant sur
une carte.


Open-source
-----------
GeoShaker est un projet open source. Cela signifie que vous pouvez l'installer
chez vous ou sur un serveur dédié. Les sources sont accessibles ici :
`Github <https://github.com/driquet/geoshaker>`__.

Format des coordonnées
----------------------
Lorsque vous utilisez GeoShaker, il vous faut entrer des coordonnées. Voici le
format de coordonnées à utiliser :

- N50 40.230 E3 23.102
- N 50 40.230 E 3 23.102

Variables
---------
Une variable est une valeur inconnue. Elle est représentée par un symbole (un
symbole étant une lettre minuscule). Ce symbole sera remplacé par des valeurs
comprises dans un intervalle.

Par exemple, voici trois variables `a`, `b` et `c` : `N50 ab.abc E3 ca.abc`.

Marqueurs personnalisés
-----------------------
Vous pouvez ajouter des marqueurs personnalisés sur la carte. Cela peut être
utile lorsque vous cherchez une cache qui est proche d'autres caches. Placez un
marqueur pour chacune de ces caches et GeoShaker peut :

- afficher un cercle autour de ces caches
- exclure les combinaisons pour lesquelles le résultat se trouve dans ce cercle
  (parce que vous savez que la distance minimale est de 161m, selon les
  guidelines)

Limites
-------

- Vous pouvez utiliser jusqu'à 6 variables
- Vous ne pouvez pas générer plus de 100000 combinaisons (pour des raisons
  matérielles)

Expressions arithmétiques
#########################
Puisque la plupart des caches mystères utilisent des expressions arithmétiques,
vous pouvez les utiliser dans GeoShaker. Cette partie explique comment.


Opérations supportées
---------------------
Pour le moment, vous pouvez utiliser :

- addition/substraction : a + 23, a - b
- multiplication/division : a * 3, a * b, a / 3
- groupement d'expressions : a * (b + 3)

Format
------
Pour que GeoShaker sache qu'il s'agisse d'une expression arithmétique, vous devez
l'entourer par des croches : [ et ].

Par exemple : `N50 40 [a + b][a * 2]3 E3 23 12a`.

Exemples
--------

- `N50 40 [a * a + 232] E3 23.[a * (3 + b)]`
- `N50 40 abc E3 23.[a * b / 3]`
