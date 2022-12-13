#ifndef LISTES_H
#define LISTES_H

#include <stdbool.h>

/*
 * Pour réaliser des tests de performance, désactiver tous les 
 * affichages.
 * Pour cela, le plus simple est de redefinir les fonctions principales 
 * en decommentant les 3 lignes suivantes et en commentant l'ancienne 
 * definition de 'eprintf' juste dessous.
 */

#ifdef SILENT

#define printf(fmt, ...) (0)
#define eprintf(fmt, ...) (0)
#define putchar(c) (0)

#else

#define eprintf(...) fprintf (stderr, __VA_ARGS__)

#endif

extern bool silent_mode;

//////////////////////////////////////////////////////////
// Séquence
struct cellule {
    char   command;//commande de la séquence actuelle
    struct cellule *suivant;//adresse de la commande suivante
    struct cellule *imbr;//debut d'une imbrication
};
typedef struct cellule cellule_t;

struct sequence {
    cellule_t *tete;
};
typedef struct sequence sequence_t;
//////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////
// Pile récursive
struct rec_cel {
  cellule_t* cel;
  struct rec_cel *suivant;
};
typedef struct rec_cel rec_cel;

typedef struct{
  int n;
  rec_cel* tete;
}Pilerec;
//////////////////////////////////////////////////////////

/* Créer une nouvelle cellule avec Malloc de type cellule_t*/
cellule_t* nouvelleCellule (void);

/* Detruit une cellule avec free()*/
void detruireCellule (cellule_t*);

/* Ajoute à la Pile recursive */
void ajout_rec(Pilerec *r, cellule_t* cel);

/* Enleve a la pile recursive */
cellule_t* recup_rec(Pilerec *r);

/* Avance l'indice de lecture du texte pour ingorer les espaces et newline */
void prochain_char(chartexte, int *i);

/* Converti un tableau de caractère en type séquence (liste chainée)*/
void conversion (char *texte, sequence_t *seq);

/* Permet d'afficher la séquence*/
void afficher (sequence_t* seq);


#endif
