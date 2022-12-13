#include "oracle_interprete.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *restos(resultat_inter res)
{
    switch (res)
    {
    case OK_ROBOT:
        return "OK_ROBOT";
    case SORTIE_ROBOT:
        return "SORTIE_ROBOT";
    case ARRET_ROBOT:
        return "ARRET_ROBOT";
    case PLOUF_ROBOT:
        return "PLOUF_ROBOT";
    case CRASH_ROBOT:
        return "CRASH_ROBOT";
    case ERREUR_PILE_VIDE:
        return "ERREUR_PILE_VIDE";
    case ERREUR_ADRESSAGE:
        return "ERREUR_ADRESSAGE";
    case ERREUR_DIVISION_PAR_ZERO:
        return "ERREUR_DIVISION_PAR_ZERO";
    }
}

erreur_lecture_test lire_test(char *f, Environnement *envt, Programme *prog, int *pas_max, etat_final *ef)
{
    FILE *file;
    char f_terrain[100];
    char f_programme[100];
    char e;
    char o;

    file = fopen(f, "r");

    if (file == NULL)
    {
        return ERREUR_FICHIER_TEST;
    }

    fscanf(file, "%s\n", f_terrain);
    fscanf(file, "%s\n", f_programme);
    fscanf(file, "%d\n", pas_max);
    fscanf(file, "%c\n", &e);

    switch (e)
    {
    case 'N':
        ef->res = ARRET_ROBOT;

        // Read x and y position on a line from the file
        fscanf(file, "%d %d\n", &ef->x, &ef->y);

        // Read orientation on a line from the file
        fscanf(file, "%c", &o);

        switch (o)
        {
        case 'N':
            ef->o = Nord;
            break;
        case 'S':
            ef->o = Sud;
            break;
        case 'E':
            ef->o = Est;
            break;
        case 'O':
            ef->o = Ouest;
            break;
        }
        break;
    case 'S':
        ef->res = SORTIE_ROBOT;
        break;
    case 'O':
        ef->res = CRASH_ROBOT;
        break;
    case 'P':
        ef->res = PLOUF_ROBOT;
        break;

    default:
        printf("ERREUR : événement inconnu\n");
        ef->res = ARRET_ROBOT;
        break;
    }

    if (initialise_environnement(envt, f_terrain) != OK_TERRAIN)
    {
        return ERREUR_TERRAIN_TEST;
    }

    if (lire_programme(prog, f_programme).type_err != OK_PROGRAMME)
    {
        return ERREUR_PROGRAMME_TEST;
    }

    return OK;
}

void gerer_erreur_test(erreur_lecture_test e)
{
    switch (e)
    {
    case OK:
        break;
    case ERREUR_FICHIER_TEST:
        printf("Erreur lecture du test : erreur d'ouverture du fichier\n");
        exit(2);
    case ERREUR_TERRAIN_TEST:
        printf("Erreur lecture du test : erreur de lecture du terrain\n");
        exit(2);
    case ERREUR_PROGRAMME_TEST:
        printf("Erreur lecture du test : erreur de lecture du programme\n");
        exit(2);
    }
}

int main(int argc, char **argv)
{
    Environnement envt;
    Programme prog;
    etat_inter etat_inter;
    etat_final etat;
    etat_final etat_attendu;

    int pas_max;
    int pas = 0;

    if (argc != 2)
    {
        printf("Usage: %s <fichier_test>\n", argv[0]);
        return 1;
    }

    gerer_erreur_test(lire_test(argv[1], &envt, &prog, &pas_max, &etat_attendu));

    /* Initialisation de l'état */
    init_etat(&etat_inter);
    do
    {
        etat.res = exec_pas(&prog, &envt, &etat_inter);
    } while (etat.res == OK_ROBOT && pas++ <= pas_max);

    if (etat.res == etat_attendu.res)
    {
        if (etat.res == ARRET_ROBOT)
        {
            position(&envt.r, &etat.x, &etat.y);
            etat.o = orient(&envt.r);
            if (etat.x == etat_attendu.x && etat.y == etat_attendu.y && etat.o == etat_attendu.o)
            {
                printf("%s\033[40G\033[0;32mOK\033[0m\n", argv[1]);
            }
            else
            {
                printf("%s\033[40G\033[0;31mKO\033[0m\n", argv[1]);
                printf("Attendu : %d %d %d (x, y, o)\n", etat_attendu.x, etat_attendu.y, etat_attendu.o);
                printf("Obtenu : %d %d %d (x, y, o)\n", etat.x, etat.y, etat.o);
            }
        }
        else
            printf("%s\033[40G\033[0;32mOK\033[0m\n", argv[1]);
    }
    else
        printf("%s\033[40G\033[0;31mKO\033[0m %s attendu, %s obtenu\n", argv[1], restos(etat_attendu.res), restos(etat.res));
}