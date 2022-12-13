---- Makefile -----
Fonctions :
- clean : effacer les fichiers objets intermédiaires
- clear : clean et effacer fichiers exécutables
- all : tout compiler et clean
- tests : cf Oracle

----- Oracle (curiosity-test) -----
Pour exécuter tous les tests à la suite utiliser la fonction tests du makefile :
$ make all tests
Ou un par un :
$ ./oracle_interprete tests/clone.test
Tous les tests doivent passer (OK) sauf le test pose_marque (KO) car la fonction n'est pas implémentée.

----- Génération terrains -----
$ ./test_generation_terrains 3 25 25 .7 terrains

----- Robots -----
$ ./curiosity_perfs tests/programmes/labyrinthe.prg 50 25 25 .7 1234 5000 /dev/null

----- Observateur -----
L'observateur est intégré au fichier curiosity. Pour l'exécuter on fera donc :
$ ./curiosity tests/terrains/terrain_1.txt tests/programmes/observateur_KO_mais_OK.prg

NB : les tests fournis sont à réaliser avec le terrain_1.txt et leur résultat attendu est dans leur nom.
