#ifndef TYPE_PILE_H
#define TYPE_PILE_H

#include "listes.h"

//////////////////////////////////////////////////////////
// Type int_cel permettant de stocker les entiers et les adress de cellule_t
typedef struct {
  int b;
  int i;
  cellule_t* s;
} int_cel;

//////////////////////////////////////////////////////////
// Pile de stockage d'int_cel sous forme de liste chaînée
struct cellulep{
  int_cel elem;
  struct cellulep* suivant;
};
typedef struct cellulep pile_cel;

typedef struct {
  int n;
  pile_cel* tete;
} PileEntiers;

//////////////////////////////////////////////////////////
/* Constructeurs */

/* Créer une pile vide */
void creer_pile(PileEntiers *p);

/* Opérations d'accès */

/* Retourne vrai ssi p est vide */
int est_vide(PileEntiers *p);

/* Renvoie le premier élément de la pile du type voulue */
/* p doit être non vide */
int sommet_int(PileEntiers *p);

cellule_t* sommet_cel(PileEntiers *p);

/* Renvoie le nombre d'éléments dans la pile */
int taille(PileEntiers *p);

/* Détecte les imbrication de {}*/
int imbrique(char c,int e);

/* Afficher les éléments de la pile */
void afficherpile(PileEntiers *p);

/* Opérations de modification */

/* Vider la pile p */
void vider(PileEntiers *p);

/* Empiler un entier x */
/* Précondition : taille(p) < TAILLE_MAX */
void empiler(PileEntiers *p, int_cel x);

/* Renvoie si l'élément en tête de la pile est un entier (false) ou une commande (true)*/
/* Précondition : p non vide */
bool type_pile_elem(PileEntiers *p);

/* Supprimer et renvoyer l'entier en haut de la pile */
/* Précondition : p non vide */
int depiler_int(PileEntiers *p);

cellule_t* depiler_cel(PileEntiers *p);

/* Supprime le sommet de la pile*/
/* Précondition : p non vide */
void supprimer_sommet(PileEntiers* p);

/* Echange 2 cellule de type pile cel*/
void echange(pile_cel* cel1, pile_cel* cel2);

#endif
