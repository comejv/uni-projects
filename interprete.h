#ifndef _INTERPRETE_H_
#define _INTERPRETE_H_

#include "environnement.h"
#include "programme.h"
#include "type_pile.h"

/* Interprétation d'un programme dans un environnement */

/* Résultat de l'interprétation */
typedef enum
{
  OK_ROBOT,                 /* Le robot est sur une case libre et le programme n'est pas terminé*/
  SORTIE_ROBOT,             /* Le robot est sorti du terrain */
  ARRET_ROBOT,              /* Le programme est terminé */
  PLOUF_ROBOT,              /* Le robot est tombé dans l'eau */
  CRASH_ROBOT,              /* Le robot est rentré dans un rocher */
  ERREUR_PILE_VIDE,         /* Erreur : pile vide */
  ERREUR_ADRESSAGE,         /* Erreur d'adressage : indice de commande incorrect */
  ERREUR_DIVISION_PAR_ZERO /* Erreur : tentative de division par 0 */
} resultat_inter;

/* Etat de l'interprète */
typedef struct
{
  /* Program counter : adresse de la prochaine commande à exécuter */
  int pc;
  /* Pile de données */
  PileEntiers stack;
  /* Pile d'adresses de retour */
  PileEntiers sp;
} etat_inter;

/* Initialisation de l'état */
void init_etat(etat_inter *etat);

/* Pas d'exécution de l'interprète : exécute une commande, modifie
   l'environnement et l'état, renvoie l'état du robot */
resultat_inter exec_pas(Programme *prog, Environnement *envt, etat_inter *etat);

#endif
