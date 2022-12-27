#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "listes.h"

/* fichier à compléter au besoin */

void init_liste_vide(liste_t *L)
{
    L->tete = NULL;
    return;
}

void liberer_liste(liste_t *L)
{
    cellule_t *cel;

    cel = L->tete;
    while (L->tete != NULL)
    {
        L->tete = L->tete->suivant;
        free(cel);
        cel = L->tete;
    }
}

int ajouter_tete(liste_t *L, string c)
{ /* retourne 0 si OK, 1 sinon  */
    cellule_t *cel;

    if (L == NULL)
    {
        return 1;
    }

    cel = (cellule_t *)malloc(sizeof(cellule_t));
    cel->suivant = L->tete;
    cel->val = c;
    L->tete = cel;
    return 0;
}

void afficher_chainee(liste_t *L)
{
    cellule_t *cel;

    if (L == NULL)
    {
        return;
    }

    cel = L->tete;
    printf("[");
    while (cel->suivant != NULL)
    {
        printf("%s, ", cel->val);
        cel = cel->suivant;
    }
    printf("%s]\n", cel->val);
}


int Nombre_elem_liste(cellule_t *cel){
    int count=0;
    while (cel != NULL)
    {
        count++;
        cel=cel->suivant;
    }
    return count;
}

int recherche_nom(cellule_t *seq, string nom)
{
    cellule_t *cel;
    cel=seq;
    while (cel != NULL)
    {
        if (strcmp(cel->val, nom) == 0)
        {
            return 1;
        }
        cel = cel->suivant;
    }
    return 0;
}