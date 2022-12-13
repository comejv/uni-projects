#include "environnement.h"
#include "interprete.h"
#include "programme.h"
#include "generation_terrains.h"

void affichage_position_programme(erreur_programme e)
{
    int i;
    printf("Ligne %d, colonne %d :\n", e.num_ligne, e.num_colonne);
    printf("%s\n", e.ligne);
    /* Impression de e.num_colonne-1 espaces */
    for (i = 1; i < e.num_colonne; i++)
    {
        printf(" ");
    }
    /* Impression d'un curseur de position */
    printf("^\n");
}

void gestion_erreur_programme(erreur_programme e)
{
    switch (e.type_err)
    {
    case OK_PROGRAMME:
        break;
    case ERREUR_FICHIER_PROGRAMME:
        printf("Erreur lecture du programme : erreur d'ouverture du fichier\n");
        exit(2);
    case ERREUR_BLOC_NON_FERME:
        printf("Erreur lecture du programme : bloc non fermé\n");
        exit(2);
    case ERREUR_FERMETURE_BLOC_EXCEDENTAIRE:
        printf("Erreur lecture du programme : fermeture de bloc excédentaire\n");
        affichage_position_programme(e);
        exit(2);
    case ERREUR_COMMANDE_INCORRECTE:
        printf("Erreur lecture du programme : commande incorrecte\n");
        affichage_position_programme(e);
        exit(2);
    }
}

typedef struct
{
    int sortie;
    int crash;
    int bloque;
    int pas_total;
    int total;
} stats;


int main(int argc, char *argv[])
{
    erreur_programme errp;
    Programme prog;
    Environnement envt;
    etat_inter etat;
    resultat_inter res;
    int pas = 0;

    stats s;
    // initialisation à 0 des stats
    s.sortie = 0;
    s.crash = 0;
    s.bloque = 0;
    s.pas_total = 0;
    s.total = 0;

    if (argc != 9)
    {
        printf("Usage: %s <fichier_programme> <N> <L> <H> <d> <graine> <nb_step_max> <fichier_res>\n", argv[0]);
        return 1;
    }

    errp = lire_programme(&prog, argv[1]);
    gestion_erreur_programme(errp);

    int N = atoi(argv[2]);
    int L = atoi(argv[3]);
    int H = atoi(argv[4]);
    float d = atof(argv[5]);
    int pas_max = atoi(argv[7]);

    // Res file
    FILE *file_res = fopen(argv[8], "w");
    // Write number of terrains tested
    fprintf(file_res, "%d\n", N);

    // seed
    srand(atoi(argv[6]));

    for (int i = 0; i < N; i++)
    {
        do
        {
            generation_aleatoire(&envt.t, L, H, d);
        } while (existe_chemin_vers_sortie(&envt.t) == 0);
        // init environnement
        init_robot(&envt.r, L / 2, H / 2, Est);

        /* Initialisation de l'état */
        init_etat(&etat);
        do
        {
            // Avec la graine 1239 rajouter cette ligne double le nombre de succès ?!
            // printf("");
            res = exec_pas(&prog, &envt, &etat);
        } while (res == OK_ROBOT && ++pas < pas_max);

        s.total++;

        // Write result : pas if SORTIE_ROBOT, -1 if OK_ROBOT, -2 if PLOUF_ROBOT, -3 if CRASH_ROBOT
        switch (res)
        {
        case SORTIE_ROBOT:
            fprintf(file_res, "%d\n", pas);
            s.pas_total += pas;
            s.sortie++;
            break;
        case OK_ROBOT:
            fprintf(file_res, "-1\n");
            s.bloque++;
            break;
        case PLOUF_ROBOT:
            fprintf(file_res, "-2\n");
            s.crash++;
            break;
        case CRASH_ROBOT:
            fprintf(file_res, "-3\n");
            s.crash++;
            break;
        default:
            fprintf(file_res, "-4 : %d\n", res);
            break;
        }
        pas = 0;
    }

    fclose(file_res);

    // Print stats
    printf("Sortie : %d/%d (%.2f%%)\n", s.sortie, s.total, (float)s.sortie / s.total * 100);
    printf("Bloque : %d/%d (%.2f%%)\n", s.bloque, s.total, (float)s.bloque / s.total * 100);
    printf("Crash : %d/%d (%.2f%%)\n", s.crash, s.total, (float)s.crash / s.total * 100);
    printf("Pas moyen : %.2f\n", (float)s.pas_total / s.sortie);

    return 0;
}