#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include <stdlib.h>
#include <ctype.h>
#ifdef NCURSES
#include <ncurses.h>
#endif
#include "listes.h"
#include "curiosity.h"
#include "type_pile.h"


/*
 *  Auteur(s) : EMILE GUILLAUME & 
 *  Date :
 *  Suivi des Modifications :
 *
 */
///////////////////////////////////////////////////////////////////////////
void stop (void)
{
    char enter = '\0';
    printf ("Appuyer sur entrée pour continuer...\n");
    while (enter != '\r' && enter != '\n') { enter = getchar(); }
}
///////////////////////////////////////////////////////////////////////////
void addition(PileEntiers* p,int_cel* ic){
    int a,b;

    a=depiler_int(p);
    b=depiler_int(p);
    ic->b=0;
    ic->i=a+b;
}
///////////////////////////////////////////////////////////////////////////
void soustraction(PileEntiers* p,int_cel* ic){
    int a,b;

    b=depiler_int(p);
    a=depiler_int(p);
    ic->b=0;
    ic->i=a-b;
}
///////////////////////////////////////////////////////////////////////////
void multiplication(PileEntiers* p,int_cel* ic){
    int a,b;

    b=depiler_int(p);
    a=depiler_int(p);
    ic->b=0;
    ic->i=a*b;
}
///////////////////////////////////////////////////////////////////////////
void rotation(PileEntiers* p, int x, int n){
    pile_cel *cel1,*cel2,*precel1;
    int i;

    x=x%n;

    if (x==0)return;

    precel1=p->tete;
    for(i=1; i<n-x; i++){
        precel1=precel1->suivant;
    }
    cel1=precel1->suivant;
    cel2=cel1;
    for(i=1; i<x; i++){
        cel2=cel2->suivant;
    }
    precel1->suivant=cel2->suivant;
    cel2->suivant=p->tete;
    p->tete=cel1;
}
///////////////////////////////////////////////////////////////////////////
void mystere(PileEntiers* p){
    int i;
    pile_cel *cel_pre,*cel_deb,*cel_fin;

    if (p->n>3){
        cel_pre=p->tete;
        for (i=0; i<p->n-4; i++){
            cel_pre=cel_pre->suivant;
        }
        cel_deb=cel_pre->suivant;
        cel_fin=cel_deb->suivant->suivant;
        cel_pre->suivant=NULL;
        cel_fin->suivant=p->tete;
        p->tete=cel_deb;
    }
    echange(p->tete,p->tete->suivant->suivant);
}
///////////////////////////////////////////////////////////////////////////
int interprete (sequence_t* seq, bool debug){    
    ////////////////////////////////
    // Type utile
    cellule_t *cel,*cel1,*cel2;
    PileEntiers pile;
    Pilerec rec;
    sequence_t affichage;
    int ret;       //utilisée pour les valeurs de retour
    int_cel ic;
    int e;
    bool ajout;

    ////////////////////////////////
    // Initialisation
    affichage.tete=seq->tete;
    rec.tete=NULL;
    rec.n=0;
    creer_pile(&pile);
    ajout=false;
    cel= seq->tete;
    debug = true; /* À enlever par la suite et utiliser "-d" sur la ligne de commandes */
    if (!(silent_mode)){
        printf ("Programme:");
        afficher(seq);
        printf ("\n");
        if (debug) stop();
    }

    ////////////////////////////////
    // Programme Interprete
    while ( cel != NULL ) {
        ////////////////////////////
        // Traitement de la commande
        switch (cel->command) {
            case 'A':
                ret = avance();
                if (ret == VICTOIRE) return VICTOIRE; /* on a atteint la cible */
                if (ret == RATE)     return RATE;     /* tombé dans l'eau ou sur un rocher */
                break;
            case 'D':
                droite();
                break; 
            case 'G':
                gauche();
                break; 
            case '+':
                addition(&pile,&ic);
                empiler(&pile,ic);
                break;
            case '-':
                soustraction(&pile,&ic);
                empiler(&pile,ic);
                break; 
            case '*':
                multiplication(&pile,&ic);
                empiler(&pile,ic);
                break; 
            case 'P':
                e=depiler_int(&pile);
                pose(e);
                break;
            case 'M':
                e=depiler_int(&pile);
                ic.b=0;
                ic.i=mesure(e);
                empiler(&pile,ic);
                break;
            case '{':
                ic.b=1;
                ic.s=cel->imbr;
                empiler(&pile,ic);
                break;
            case '?':
                ajout_rec(&rec,cel->suivant);
                ajout=true;
                cel1=depiler_cel(&pile);
                cel2=depiler_cel(&pile);
                e = depiler_int(&pile);
                if ( e != 0){
                    cel1=cel2;
                }
                cel=cel1;
                break;
            case 'X':
                echange(pile.tete,pile.tete->suivant);
                break;
            case '!':
                ajout_rec(&rec,cel->suivant);
                ajout=true;
                cel=depiler_cel(&pile);
                break;
            case 'B':
                e=depiler_int(&pile);
                if (e!=0){
                    ajout_rec(&rec,cel);
                    ajout=true;
                    cel1=sommet_cel(&pile);
                    e--;
                    cel=cel1;
                    ic.b=0;
                    ic.i=e;
                    empiler(&pile,ic);
                }else{
                    supprimer_sommet(&pile);
                }
                break;
            case 'R':
                rotation(&pile,depiler_int(&pile),depiler_int(&pile));
                break;
            case 'C':
                if (type_pile_elem(&pile)){
                    ic.s=sommet_cel(&pile);
                    ic.b=1;
                    empiler(&pile,ic);
                }else{
                    ic.i=sommet_int(&pile);
                    ic.b=0;
                    empiler(&pile,ic);
                }
                break;
            case 'I':
                supprimer_sommet(&pile);
                break;
            case 'Z':
                if (pile.n%2==1){
                    mystere(&pile);
                }
                break;
            default:
                if ( 0 <= (cel->command -'0') && 9 >= (cel->command-'0') ){
                    ic.b=0;
                    ic.i=cel->command-'0';
                    empiler(&pile,ic);
                }
                break;
        }
        ////////////////////////////
        // Prochaine cellule à traiter (usage d'une pile récursive)
        if(!(ajout)){
            if (cel->suivant==NULL){
                cel=recup_rec(&rec);
                while (cel==NULL && rec.n!=0){
                    cel=recup_rec(&rec);
                }
            }else{
                cel=cel->suivant;
            }
        }else{
            if (cel==NULL){
                cel=recup_rec(&rec);
                while (cel==NULL && rec.n != 0){
                    cel=recup_rec(&rec);
                }
            }
            ajout=false;
        }
        ////////////////////////////
        // Affichage pour faciliter le debug 
        affichage.tete=cel; // Permet d'afficher la séquence en cours (la séqence ou une imbrication selon les commandes)
        if (!(silent_mode)){
            afficherCarte();
            printf ("Programme:");
            afficher(&affichage);
            printf ("\n");
            afficherpile(&pile);
            printf ("\n");
            if (debug) stop();
        }
    }
    vider(&pile);

    /* Si on sort de la boucle sans arriver sur la cible,
     * c'est raté :-( */

    return CIBLERATEE;
}