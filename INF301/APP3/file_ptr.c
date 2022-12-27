#include <stdlib.h>
#include "file_ptr.h"
#include "arbres.h"

void init_file(file *f)
{
    f->tete = NULL;
    f->queue = NULL;
}

void enfiler(file *f, noeud *n, int niv)
{
    cellule_f *cel;

    cel = (cellule_f *)malloc(sizeof(cellule_f));
    cel->suivant = NULL;
    cel->n = n;
    cel->niveau = niv;

    if (f->tete == NULL)
    {
        f->tete = cel;
        f->queue = cel;
    }
    else
    {
        f->queue->suivant = cel;
        f->queue = cel;
    }
}

cellule_f *defiler(file *f)
{
    cellule_f *cel;

    if (f->tete == NULL)
    {
        return NULL;
    }

    cel = f->tete;
    f->tete = cel->suivant;

    return cel;
}

cellule_f *depiler(file *f)
{
    cellule_f *cel;
    cel = f->tete;
    if (cel == NULL)
    {
        return NULL;
    }

    f->tete = cel->suivant;
    return cel;
}

void empiler(file *f, noeud *n)
{
    cellule_f *cel;

    cel = (cellule_f *)malloc(sizeof(cellule_f));
    cel->suivant = f->tete;
    f->tete = cel;
}

int file_vide(file *f)
{
    return f->tete == NULL;
}