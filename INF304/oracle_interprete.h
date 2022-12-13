#include "environnement.h"
#include "interprete.h"
#include "programme.h"

typedef enum
{
    OK,
    ERREUR_FICHIER_TEST,
    ERREUR_TERRAIN_TEST,
    ERREUR_PROGRAMME_TEST
} erreur_lecture_test;

typedef struct
{
    int x;
    int y;
    Orientation o;
    resultat_inter res;
} etat_final;

// Fonction qui lit un fichier test et initialise l'environnement
erreur_lecture_test lire_test(char *f, Environnement *envt, Programme *prog, int *pas_max, etat_final *ef);

void gerer_erreur_test(erreur_lecture_test e);