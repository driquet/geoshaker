.. contents:: **Table of contents**

----

What is GeoShaker
#################

Description
-----------
GeoShaker is a web-app created in order to help you find mystery caches.
Most of the time, these caches could be found using a set of coordinates with
severals variables, but sometimes you can't know the value of one or several of
these variables.

That is the case when one or several hints/caches are missing in a geocaching
loop. If one of the cache is gone missing, you cannot find the bonus cache
because you are missing a part of the problem.

In that case, GeoShaker gives you a hand by generating all the combinations,
excluding the ones that are not valid and by displaying them onto a map.


Open-source
-----------
GeoShaker is an open source project. It means you can install it at home or on
you dedicated server. You can get the sources there : `GeoShaker Github link
<https://github.com/driquet/geoshaker>`__.

Coordinates format
------------------
While using GeoShaker, you need to enter coordinates. GeoShaker only understand
coordinates formated as follow :

- N50 40.230 E3 23.102
- N 50 40.230 E 3 23.102

Variables
---------
A variable is an unknown value. You represent it using a symbol (a symbol is a
lowercase letter). This symbol will be replaced by values (from an interval).

For example, using three variables `a`, `b` and `c` : `N50 ab.abc E3 ca.abc`.

Custom markers
--------------
You can add custom markers on the map. It could be useful when searching for a
cache nearby other caches. You place a marker for each of these cache, and
GeoShaker can :

- display a circle around them
- exclude combinations within the circle (because you know that the cache could
  not the there due to the guidelines)

Limitations
-----------

- You can use up to 6 variables
- You cannot generate more than 100.000 combinations (hardware issue)

Arithmetic expressions
######################
Because most of the mystery caches use arithmetic expressions, you can use them
too in GeoShaker. This section explains how to.

Supported operations
--------------------
At the moment, you can use :

- addition/substraction : a + 23, a - b
- multiplication/division : a * 3, a * b, a / 3
- group expressions : a * (b + 3)

Format
------
If you want GeoShaker to understand your arithmetic expressions, you must
respect the arithmetic format. An arithmetic must be surrounded using brackets :
[ and ].

For example: `N50 40 [a + b][a * 2]3 E3 23 12a`.

Examples
--------

- `N50 40 [a * a + 232] E3 23.[a * (3 + b)]`
- `N50 40 abc E3 23.[a * b / 3]`
