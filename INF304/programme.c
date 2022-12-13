#include "programme.h"
#include "type_pile.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LGMAX 1000

// Renvoie vrai si c est un chiffre
int est_chiffre(char c) { return (c >= '0') && (c <= '9'); }

/* Lecture d'un programme prog dans le fichier nom_fichier */
erreur_programme lire_programme(Programme *prog, char *nom_fichier) {
  FILE *fprog;
  char ligne[LGMAX];
  int numligne;
  erreur_programme res; // Résultat de la fonction
  PileEntiers pile;     // Pile pour lier les ouvertures/fermetures de bloc

  // Ouverture du fichier en lecture
  fprog = fopen(nom_fichier, "r");
  if (fprog == NULL) {
    res.type_err = ERREUR_FICHIER_PROGRAMME;
    return res;
  }

  // Initialisation du programme
  prog->lg = 0;

  // Initialisation de la pile
  creer_pile(&pile);

  numligne = 0;
  while ((!feof(fprog)) && (fgets(ligne, LGMAX, fprog) != NULL)) {
    int i;
    int nb;
    int lgligne;

    numligne++;
    i = 0;
    while ((i < LGMAX) && (ligne[i] != '\0') && (ligne[i] != '#')) {
      switch (ligne[i]) {
      case ' ':
      case '\t':
      case '\n':
        // Ignorer les espaces
        i++;
        break;
      case 'A':
        prog->tab[prog->lg].cmd = Avancer;
        prog->lg++;
        i++;
        break;
      case 'G':
        prog->tab[prog->lg].cmd = Gauche;
        prog->lg++;
        i++;
        break;
      case 'D':
        prog->tab[prog->lg].cmd = Droite;
        prog->lg++;
        i++;
        break;
      case 'M':
        prog->tab[prog->lg].cmd = Mesure;
        prog->lg++;
        i++;
        break;
      case 'P':
        prog->tab[prog->lg].cmd = Marque;
        prog->lg++;
        i++;
        break;
      case '{':
        prog->tab[prog->lg].cmd = DebutBloc;
        // Empiler la position du début de bloc
        empiler(&pile, prog->lg);
        prog->lg++;
        i++;
        break;
      case '}':
        // Dépiler la position du début de bloc correspondant
        if (est_vide(&pile)) {
          // Erreur : fermeture de bloc exccédentaire
          res.type_err = ERREUR_FERMETURE_BLOC_EXCEDENTAIRE;
          lgligne = strlen(ligne);
          res.ligne = malloc((lgligne + 1) * sizeof(char));
          strcpy(res.ligne, ligne);
          res.num_ligne = numligne;
          res.num_colonne = i + 1;
          return res;
        } else {
          int debut = depiler(&pile);
          // Lier le début du bloc avec la fin
          prog->tab[debut].aux = prog->lg;
          prog->tab[prog->lg].cmd = FinBloc;
          prog->lg++;
        }
        i++;
        break;
      case '!':
        prog->tab[prog->lg].cmd = ExecBloc;
        prog->lg++;
        i++;
        break;
      case '?':
        prog->tab[prog->lg].cmd = CondExec;
        prog->lg++;
        i++;
        break;
      case 'X':
        prog->tab[prog->lg].cmd = Echange;
        prog->lg++;
        i++;
        break;
      case '*':
        prog->tab[prog->lg].cmd = Mult;
        prog->lg++;
        i++;
        break;
      case '+':
        prog->tab[prog->lg].cmd = Add;
        prog->lg++;
        i++;
        break;
      case '/':
        prog->tab[prog->lg].cmd = Div;
        prog->lg++;
        i++;
        break;
      case '-':
        i++;
        if ((i < LGMAX) && est_chiffre(ligne[i])) {
          // lire un nombre à partir de la position i
          nb = 0;
          while ((i < LGMAX) && est_chiffre(ligne[i])) {
            nb = 10 * nb + (ligne[i] - '0');
            i++;
          }
          prog->tab[prog->lg].cmd = EmpilerNb;
          prog->tab[prog->lg].aux = nb;
          prog->lg++;
        } else {
          prog->tab[prog->lg].cmd = Sub;
          prog->lg++;
        }
        break;
      case 'R':
        prog->tab[prog->lg].cmd = Rotation;
        prog->lg++;
        i++;
        break;
      case 'C':
        prog->tab[prog->lg].cmd = Clone;
        prog->lg++;
        i++;
        break;
      case 'B':
        prog->tab[prog->lg].cmd = Boucle;
        prog->lg++;
        i++;
        break;
      case 'I':
        prog->tab[prog->lg].cmd = Ignore;
        prog->lg++;
        i++;
        break;
      default:
        if (est_chiffre(ligne[i])) {
          // lire un nombre à partir de la position i
          nb = 0;
          while ((i < LGMAX) && est_chiffre(ligne[i])) {
            nb = 10 * nb + (ligne[i] - '0');
            i++;
          }
          prog->tab[prog->lg].cmd = EmpilerNb;
          prog->tab[prog->lg].aux = nb;
          prog->lg++;
        } else {
          // Erreur : caractère incorrect à la position courante
          res.type_err = ERREUR_COMMANDE_INCORRECTE;
          lgligne = strlen(ligne);
          res.ligne = malloc((lgligne + 1) * sizeof(char));
          strcpy(res.ligne, ligne);
          res.num_ligne = numligne;
          res.num_colonne = i + 1;
          return res;
        }
      }
    }
  }

  // Fin du fichier : la pile doit être vide
  if (est_vide(&pile)) {
    res.type_err = OK_PROGRAMME;
  } else {
    res.type_err = ERREUR_BLOC_NON_FERME;
  }

  return res;
}
