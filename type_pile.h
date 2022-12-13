#ifndef _TYPE_PILE_H_
#define _TYPE_PILE_H_

#define TAILLE_MAX 1000

typedef struct {
  int n;
  int tab[TAILLE_MAX];
} PileEntiers;

/* Constructeurs */

/* Créer une pile vide */
void creer_pile(PileEntiers *p);

/* Opérations d'accès */

/* Retourne vrai ssi p est vide */
int est_vide(PileEntiers *p);

/* Renvoie l'entier en haut de la pile */
/* p doit être non vide */
int sommet(PileEntiers *p);

/* Renvoie le nombre d'éléments dans la pile */
int taille(PileEntiers *p);

/* Afficher les éléments de la pile */
void print(PileEntiers *p);

/* Opérations de modification */

/* Vider la pile p */
void vider(PileEntiers *p);

/* Empiler un entier x */
/* Précondition : taille(p) < TAILLE_MAX */
void empiler(PileEntiers *p, int x);

/* Supprimer et renvoyer l'entier en haut de la pile */
/* Précondition : p non vide */
int depiler(PileEntiers *p);

#endif
