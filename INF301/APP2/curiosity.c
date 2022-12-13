#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>
#include "listes.h"
#include "curiosity.h"

/*
 *  Auteur(s) :
 *  Date :
 *  Suivi des Modifications :
 *
 */

struct carte mars;

unsigned int cX=9999,cY=9999; // Position de curiosity (cX,cY)
int dX=1,dY=0;  // Direction de curiosity (dX,dY)=(1,0)|(-1,0)|(0,1)|(0,-1)


void initCarte (int carte_num)
{
    mars.carte_num = carte_num;
    mars.hauteur = 0;
    mars.largeur = 0;
    for(int j=0;j<tailleCarte;j++) {
        for(int i=0;i<tailleCarte;i++) {
            mars.map[j][i]='\0';
            mars.marques[j][i]=false;
        }
    }
    cX = 9999; cY = 9999;
    dX = 1; dY = 0;
}

void ajoutLigneCarte (char *ligne)
{
    assert (mars.hauteur < tailleCarte);

    if (mars.hauteur == 0) { /* première ligne */
        mars.largeur = strlen (ligne) - 1; /* sans le retour à la ligne */
    }
    else {
        assert (mars.largeur == strlen (ligne)-1);
    }

    for (unsigned int i=0; i<mars.largeur; i++) {
        if (ligne[i] == 'C') {
            mars.map[mars.hauteur][i] = PLAIN;
            if (cX != 9999 || cY != 9999) {
                eprintf ("Curiosity déjà placée sur la carte!\n");
                exit (1);
            }
            cX = i;
            cY = mars.hauteur;
        }
        else if (ligne[i] == 'M') {
            mars.map[mars.hauteur][i] = PLAIN;
            mars.marques[mars.hauteur][i] = true;
        }
        else if (ligne[i] == 'P') { /* marque finale avec Curiosity dessus */
            mars.map[mars.hauteur][i] = PLAIN;
            mars.marques[mars.hauteur][i] = true;
            cX = i;
            cY = mars.hauteur;
        }
        else {
            mars.map[mars.hauteur][i] = ligne[i];
        }
    }
    mars.hauteur++;
}


int char_to_color (char c);

void afficherCarte ()
{
    unsigned int i,j;
    char c;

    printf("\n\n\n\n\n\nCarte de mars.\n");
    printf("--------------\n\n\n\n");

    for(j=0;j<mars.hauteur;j++) {

        for(i=0;i<mars.largeur;i++) {	
            c = mars.map[j][i]; 
            if (c=='\0') {	  //hors carte, étrange...
                if (i==0) {
                    j = tailleCarte;
                    break;
                }
                break;
            }
            if ((i==cX)&&(j==cY)) { //position curiosity
                if (dX==1)      { putchar('>');}
                else if (dX==-1){ putchar('<');}
                else if (dY==1) { putchar('V');}
                else            { putchar('^');}
            }
            else {
                putchar(c);
            }
        }
        printf("\n");
    }
    printf("\n\n\n\n--------------\n\n");
    return;
}

/* Vérifie que toutes les marques sur la carte de test ont bien été 
 * posées par Curiosity, et que Curiosity n'a pas posé plus de marques
 * que demandé. */
bool verifieMarques (void)
{
    unsigned int i,j;
    bool erreur = false;

    for(j=0;j<mars.hauteur;j++) {
        for(i=0;i<mars.largeur;i++) {
            if (! (  (mars.map[j][i] == MARK)
                        == (mars.marques[j][i]))) {
                if (!erreur) {
                    eprintf ("******************************************\n");
                    eprintf ("*        ERREUR                          *\n");
                    eprintf ("* marque(s) manquante(s) ou en trop!     *\n");
                    erreur = true;
                }
                eprintf ("- erreur de marque position: %dx%d\n",i,j);
            }
        }
    }
    return !erreur;
}


int avance(void)
{
    int tmpX = cX + dX;
    int tmpY = cY + dY;

    if (tmpX < 0 || tmpX >= (int)mars.largeur ||
        tmpY < 0 || tmpY >= (int)mars.hauteur ) {
        eprintf("Sortie de carte !!!\n");
        return RATE;
    }

    char c=mars.map[tmpY][tmpX];

    if (c== WATER) {
        eprintf("Plouf !?!\n");
        return RATE;
    }
    if (c== ROCK) {
        eprintf("Ouch!!!\n");
        return RATE;
    }
    cX=tmpX;
    cY=tmpY;
    if (c==TARGET) {

        if (! silent_mode) {
            printf("**************************\n");
            printf("*                        *\n");
            printf("*     Victoire !!!       *\n");
            printf("*                        *\n");
            printf("**************************\n\n\n");
        }
        return VICTOIRE;
    }
    if ((c!='.')&&(c!='M')&&(c!='m')) {
        printf("Oups ! Curiosity est sur '%c'\n\n",c);
        return RATE;
    }
    return REUSSI;
}


void droite() {
    if (dX==1) {
        dX=0;
        dY=1;
    } else if (dX==-1) {
        dX=0;
        dY=-1;
    } else if (dY==1) {
        dX=-1;
        dY=0;
    } else {
        dX=1;
        dY=0;
    }
}


void gauche() {
    if (dX==1) {
        dX=0;
        dY=-1;
    } else if (dX==-1) {
        dX=0;
        dY=1;
    } else if (dY==1) {
        dX=1;
        dY=0;
    } else {
        dX=-1;
        dY=0;
    }
}


char charMesure(int dir) {
    switch (dir) {
        case 0: return mars.map[cY][cX];
        case 1: return mars.map[cY+dY][cX+dX];
        case 2: return mars.map[cY+dY+dX][cX+dX-dY];
        case 3: return mars.map[cY+dX][cX-dY];
        case 4: return mars.map[cY-dY+dX][cX-dX-dY];
        case 5: return mars.map[cY-dY][cX-dX];
        case 6: return mars.map[cY-dY-dX][cX-dX+dY];
        case 7: return mars.map[cY-dX][cX+dY];
        case 8: return mars.map[cY+dY-dX][cX+dX+dY];
        default: 
                eprintf("Direction inconnue: %d\n", dir);
                assert (false);
    }
}

int char_to_color (char c) {
    switch (c) {
        case TARGET:return CTARGET;
        case PLAIN: return CPLAIN;
        case MARK:  return CMARK;
        case WATER: return CWATER;
        case ROCK:  return CROCK;
        default: 
                eprintf("Terrain inconnu: %c\n", c);
                assert (false);
    }
}

int char_to_mesure (char c) {
    switch (c) {
        case TARGET:
        case PLAIN: return 0;
        case MARK:  return 1;
        case WATER: return 2;
        case ROCK:  return 3;
        default:
                eprintf("Terrain inconnu: %c\n", c);
                assert (false);
    }
}

int mesure(int dir) {
    return char_to_mesure (charMesure(dir));
}

void pose (int arg) {
    if (arg == 0) {
        mars.map[cY][cX]= PLAIN;
    } else {
        mars.map[cY][cX]= MARK;
    }
}

