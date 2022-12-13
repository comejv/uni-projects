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

#define eprintf(...) fprintf(stderr, __VA_ARGS__)

#endif

extern bool silent_mode;

struct cellule
{
    char command;            // commande de la séquence actuelle
    struct cellule *suivant; // adresse de la commande suivante
    struct cellule *imbr;    // adresse en cas d'imbrication avec le caractère '{'
};
typedef struct cellule cellule_t;

struct sequence
{
    cellule_t *tete;
};
typedef struct sequence sequence_t;

/* Créer une nouvelle cellule avec Malloc de type cellule_t*/
cellule_t *nouvelleCellule(void);

/* Detruit une cellule avec free()*/
void detruireCellule(cellule_t *);

/* Converti un tableau de caractère en type séquence (liste chainée)*/
void conversion(char *texte, sequence_t *seq);

/* Permet de créer des sous séquence dans notre séquence (des branches)*/
void accolade(char *texte, cellule_t *cel, int *i);

/* Permet d'afficher la séquence*/
void afficher(sequence_t *seq);

#endif
