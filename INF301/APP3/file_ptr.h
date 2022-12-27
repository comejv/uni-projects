#ifndef __FILE_PTR_H__
#define __FILE_PTR_H__

#include <stdio.h>
#include "arbres.h"
typedef struct cellule_file 
{
    noeud *n;
    int niveau;
    struct cellule_file *suivant;
} cellule_f;

typedef struct 
{
    cellule_f *tete;
    cellule_f *queue;
} file;

void init_file(file *f);
void enfiler(file *f, noeud *n, int niv);
cellule_f *defiler(file *f);
cellule_f *depiler(file *f);
void empiler(file *f, noeud *n);
int file_vide(file *f);

#endif