#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include "type_pile.h"

/* Créer une pile vide */
void creer_pile(PileEntiers *p){
    p->n=0;
    p->tete=NULL;
}
/* Opérations d'accès */

/* Retourne vrai ssi p est vide */
int est_vide(PileEntiers *p){
    if (p->n==0){
        return 1;
    }
    return 0;
}

/* Renvoie l'entier en haut de la pile */
/* p doit être non vide */
int sommet_int(PileEntiers *p){
    assert(!est_vide(p));
    pile_cel* cel;

    cel=p->tete;

    return cel->elem.i;
}

cellule_t* sommet_cel(PileEntiers *p){
    assert(!est_vide(p));
    pile_cel* cel;

    cel=p->tete;

    return cel->elem.s;
}

/* Renvoie le nombre d'éléments dans la pile */
int taille(PileEntiers *p){
    return p->n;
}

/* Affiche les éléments de type cellule_t*/
void afficher_cel(cellule_t* cel){
    printf("{");
    if (cel==NULL){
        printf("}");
        return;
    }
    while(cel != NULL){
        if (cel->command == '{'){
            afficher_cel(cel->imbr);
        }else{
        printf("%c",cel->command);
        }
        cel=cel->suivant;
    }
    printf("}");
}
/* Afficher les éléments de la pile */
void afficherpile(PileEntiers *p){
    pile_cel* cel;
    cel=p->tete;

    while( cel != NULL){
        if (cel->elem.b==0){
            printf("%d",cel->elem.i);
        }else{
            afficher_cel(cel->elem.s); 
        }
        printf(" ");
        cel=cel->suivant;
    }
}

/* Opérations de modification */

/* Vider la pile p */
void vider(PileEntiers *p){
    p->n=0;
    pile_cel* cel;
    cel=p->tete;
    while (cel != NULL){
        p->tete=cel->suivant;
        free(cel);
        cel=p->tete;
    }
}

/* Empiler un entier x */
/* Précondition : taille(p) < TAILLE_MAX */
void empiler(PileEntiers *p, int_cel x){
    pile_cel* cel;

    cel=(pile_cel *)malloc(sizeof(pile_cel));
    cel->suivant=p->tete;
    cel->elem=x;
    p->tete=cel;
    p->n++;
}

/* Renvoie si l'élément en tête de la pile est un entier (false) ou une commande (true)*/
/* Précondition : p non vide */
bool type_pile_elem(PileEntiers *p){
    assert(!est_vide(p));
    return (p->tete->elem.b);
}

/* Supprimer et renvoyer l'entier en haut de la pile */
/* Précondition : p non vide */
int depiler_int(PileEntiers *p){
    assert(!est_vide(p));
    assert(p->tete->elem.b==0);
    
    int tmp;
    pile_cel* cel;

    tmp=p->tete->elem.i;
    cel=p->tete->suivant;
    free(p->tete);
    p->tete=cel;
    p->n--;
    return tmp;  
}

cellule_t* depiler_cel(PileEntiers *p){
    assert(!est_vide(p));
    assert(p->tete->elem.b==1);
    
    cellule_t* tmp;
    pile_cel* cel;

    tmp=p->tete->elem.s;
    cel=p->tete->suivant;
    free(p->tete);
    p->tete=cel;
    p->n--;
    return tmp;  
}

/* Supprime le sommet de la pile*/
/* Précondition : p non vide */
void supprimer_sommet(PileEntiers* p){
    assert(!est_vide(p));

    pile_cel* cel;

    cel=p->tete->suivant;
    free(p->tete);
    p->tete=cel;
    p->n--;
}

/* Echange le sommet de la pile avec le suivant*/
/* Précondition : p 2 éléments ou plus */
void echange(pile_cel* cel1,pile_cel*cel2){
    int_cel ic;

    ic=cel1->elem;
    cel1->elem=cel2->elem;
    cel2->elem=ic;
}