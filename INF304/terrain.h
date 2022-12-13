#ifndef _TERRAIN_H_
#define _TERRAIN_H_
#include <stdio.h>

typedef enum
{
   LIBRE,
   EAU,
   ROCHER,
   MARQUE,
   ERREUR
} Case;

#define DIM_MAX 256

// indexation utilisée :
//  1er  indice : abscisse = colonne (colonne de gauche : abscisse = 0)
//  2ème indice : ordonnée = ligne   (ligne du haut     : ordonnée = 0)

typedef struct
{
   int largeur, hauteur;
   Case tab[DIM_MAX][DIM_MAX];
} Terrain;

typedef enum
{
   OK_TERRAIN,
   ERREUR_FICHIER,
   ERREUR_LECTURE_LARGEUR,
   ERREUR_LECTURE_HAUTEUR,
   ERREUR_LARGEUR_INCORRECTE,
   ERREUR_HAUTEUR_INCORRECTE,
   ERREUR_CARACTERE_INCORRECT,
   ERREUR_LONGUEUR_LIGNE,
   ERREUR_NOMBRE_LIGNES,
   ERREUR_POSITION_ROBOT_MANQUANTE
} erreur_terrain;

/* Lecture d'un terrain dans un fichier f, ouvert en lecture
   Résultats :
   t le terrain lu
   x, y position initiale du robot lue dans le fichier terrain
   Renvoie :
   OK si la lecture s'est déroulée correctement
   ERREUR_FICHIER si le fichier n'a pas pu être ouvert
   ... (à compléter)
 */
erreur_terrain lire_terrain(FILE *f, Terrain *t, int *x, int *y);

/* Largeur d'un terrain */
int largeur(Terrain *t);

/* Hauteur d'un terrain */
int hauteur(Terrain *t);

/* Indique si la case de coordonnées (x,y) est libre
   Renvoie vrai ssi les 3 conditions suivantes sont vraies :
    - 0 <= x < largeur
    - 0 <= y < hauteur
    - t.tab[x][y] = LIBRE
 */
int est_case_libre(Terrain *t, int x, int y);

/* Affichage d'un terrain t sur la sortie standard */
void afficher_terrain(Terrain *t);

/* Écriture d'un terrain t dans un fichier f ouvert en écriture.
   x et y contiennent les coordonnées du robot
   Le terrain est écrit au format lisible par lire_terrain */
void ecrire_terrain(FILE *f, Terrain *t, int x, int y);

#endif