#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#ifdef NCURSES
#include <ncurses.h>
#endif
#include "listes.h"


/*
 *  Auteur(s) : Emile 
 *  Date : MARDI 11 OCTOBRE
 *  Suivi des Modifications :
 *
 */

bool silent_mode = false;

/* Créer une nouvelle cellule avec Malloc de type cellule_t*/
cellule_t* nouvelleCellule (void){
  return (cellule_t*)malloc(sizeof(cellule_t));
}

/* Detruit une cellule avec free()*/
void detruireCellule (cellule_t* cel){
  free(cel);
}

/* Ajoute à la Pile recursive */
void ajout_rec(Pilerec *r, cellule_t* cel){
  ///////////////
  // Type utile
  rec_cel *new_cel;
  ///////////////
  // Processus
  new_cel=(rec_cel*)malloc(sizeof(rec_cel));
  new_cel->suivant=r->tete;
  new_cel->cel=cel;
  r->tete=new_cel;
  r->n++;
}

/* Enleve a la pile recursive */
cellule_t* recup_rec(Pilerec *r){
  ///////////////
  // Type utile
  cellule_t* cel;
  rec_cel* temp;
  ///////////////
  // Processus
  if (r->n==0){
      return NULL;
  }
  cel=r->tete->cel;
  temp=r->tete;
  r->tete=r->tete->suivant;
  free(temp);
  r->n--;
  return cel;
}

/* Avance l'indice de lecture du texte pour ingorer les espaces et newline */
void prochain_char(char *texte, int *i){
    while (texte[*i]==' ' || texte[*i]=='\n'){
     *i=*i+1;
    }
}

/* Converti un tableau de caractère en type séquence (liste chainée)*/
void conversion (char *texte, sequence_t *seq)
{
  ///////////////
  //Type utile pour la fonction conversion
  cellule_t *cel;
  Pilerec rec;
  int i=0;
  char c;
  ///////////////
  // Initialisation
  rec.n=0;
  prochain_char(texte,&i);
  if (texte[i]=='\0'){
    seq->tete=NULL;
    return;
  }
  cel = nouvelleCellule();
  seq -> tete = cel;
  ///////////////
  // Processus
  while(texte[i]!='\0'){
    c=texte[i];
    i++;
    prochain_char(texte,&i);
    if (c != '}'){
      cel->command=c;
    }
    switch (c){
    case '{':
      if (texte[i]=='}'){
        i++;
        cel->imbr=NULL;
        cel->suivant=nouvelleCellule();
        cel=cel->suivant;
        break;
      }
      ajout_rec(&rec,cel);
      cel->imbr=nouvelleCellule();
      cel = cel->imbr;
      break;

    case '}':
      cel->suivant=NULL;
      cel=recup_rec(&rec); //Pas de break pour faire le default
    default:
    if (texte[i] != '}' && texte[i] != '\0'){
      cel->suivant=nouvelleCellule();
      cel=cel->suivant;
    }
    break;
    }
  }
  cel->suivant=NULL;
}

/* Permet d'afficher la séquence*/
void afficher (sequence_t* seq){
  ///////////////
  // Assertion
  assert (seq); /* Le pointeur doit être valide */
  ///////////////
  // Type utile et Initialiation
  sequence_t imbr;
  cellule_t* cel;
  cel=seq->tete;
  ///////////////
  // Processus
  while(cel != NULL ){
    printf("%c",cel->command);
    if (cel->command=='{'){
      imbr.tete=cel->imbr;
      afficher(&imbr);
      printf("}");
    }
    if (cel->suivant!=NULL){
      printf(" ");  
    }
    cel=cel->suivant;
  }
}
