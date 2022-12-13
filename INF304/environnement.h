#ifndef _ENVIRONNEMENT_H_
#define _ENVIRONNEMENT_H_

#include "robot.h"
#include "terrain.h"
#include "observateur.h"

/* Environnement : terrain + robot */

typedef struct {
  Robot r;
  Terrain t;
} Environnement;

/* Initialise l'environnement envt :
   - lit le terrain dans le fichier fichier_terrain
   - initialise le robot : coordonnées initiales lues dans le fichier
   terrain, orientation initiale vers l'est
*/
erreur_terrain initialise_environnement(Environnement *envt,
                                        char *fichier_terrain);

/* Résultat d'un déplacement de robot */
typedef enum {
  OK_DEPL, /* Déplacement sur case libre */
  PLOUF,   /* Déplacement dans l'eau */
  CRASH,   /* Déplacement dans un rocher */
  SORTIE,  /* Sortie du terrain */
} resultat_deplacement;

/* Avancer le robot sur le terrain : */
resultat_deplacement avancer_envt(Environnement *envt);

/* Tourner le robot à gauche */
void gauche_envt(Environnement *envt);

/* Tourner le robot à droite */
void droite_envt(Environnement *envt);

/* Effectuer une mesure
   Paramètre d : la direction de la mesure
     0 sur place
     1 devant
     2 devant droite
     3 droite
     4 derrière droite
     5 derrière
     6 derrière gauche
     7 gauche
     8 devant gauche
   Renvoie le résultat de la mesure :
     0 rien (case libre ou en-dehors du terrain)
     1 eau
     2 rocher
 */
int mesure_envt(Environnement *envt, int d);

void pose(Environnement *envt, int d);

/* Afficher le terrain avec la position et l'orientation du robot */
void afficher_envt(Environnement *envt);

#endif
