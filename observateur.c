#include <stdio.h>
#include "observateur.h"

// Automate à trois etats qui vérifie que avancer est toujours précédé d'une mesure
void automate_pas(int mesure_effectuee, int robot_avance, int affichage)
{
    // Déclaration de l'observateur en statique pour qu'il ne soit pas
    // réinitialisé à chaque appel de la fonction
    static Observateur observateur;

    // Si l'obs n'existe pas on le crée
    if (observateur.initialise != 1)
    {
        observateur.automate_etat = 0;
        observateur.initialise = 1;
    }

    switch (observateur.automate_etat)
    {
    // Etat initial
    case 0:
        // Si le robot mesure on passe à l'état 1
        if (mesure_effectuee == 1)
        {
            observateur.automate_etat = 1;
            break;
        }
        // si on avance on passe dans le puit
        else if (robot_avance == 1)
        {
            observateur.automate_etat = 2;
            break;
        }
        // Sinon on boucle sur le 0
        observateur.automate_etat = 0;
        break;

    // Etat transition mesure effectuée
    case 1:
        // On passe à l'état 0 avec tout l'alphabet
        observateur.automate_etat = 0;
        break;

    // Etat puit
    case 2:
        // On boucle sur le puit
        observateur.automate_etat = 2;
        break;
    }

    // Affiche le résultat de l'automate
    if (affichage == 1)
    {
        if (observateur.automate_etat == 2)
        {
            printf("L'automate est dans le puit, une avance n'est pas précédée par une mesure\n");
        }
        else
        {
            printf("L'automate est dans l'état %d, il n'y a pas d'erreur dans le programme\n", observateur.automate_etat);
        }
    }
}
