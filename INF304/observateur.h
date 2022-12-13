#ifndef OBSERVATEUR_H
#define OBSERVATEUR_H

// Observateur est une struct capable de controller si une mesure a été effectuée
// et si le robot a avancé
typedef struct obs
{
    int automate_etat;
    int initialise;
} Observateur;

// Fonction automate qui vérifie que avancer est toujours précédé d'une mesure
void automate_pas(int mesure_effectuee, int robot_avance, int affichage);

#endif