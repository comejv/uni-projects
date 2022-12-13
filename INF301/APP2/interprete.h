#ifndef INTERPRETE_H
#define INTERPRETE_H

#include "listes.h"
#include "curiosity.h"
#include "type_pile.h"

/* Permet de faire une pose dans l'exécution du programme (pour facilité le débug)*/
void stop (void);

/* additionnne 2 entier dans un int_cel*/
void addition(PileEntiers* p,int_cel* ic);

/* soustrait 2 entier dans un int_cel*/
void soustraction(PileEntiers* p,int_cel* ic);

/* multiplie 2 entier dans un int_cel*/
void multiplication(PileEntiers* p,int_cel* ic);

/* Effectue x rotation des n éléments de la pile vers la gauche*/
void rotation(PileEntiers* p, int x, int n);

/* Echange le dernier élément de la pile avec l'avant avant dernier
et place les 3 dernier au début de la pile*/
void mystere(PileEntiers* p);

/* Fonction principale*/
int interprete (sequence_t* seq, bool debug);

#endif
