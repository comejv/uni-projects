#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <assert.h>
#ifdef NCURSES
#include <ncurses.h>
#endif
#include "curiosity.h"
#include "listes.h"
#include "interprete.h"

/*
 *  Auteur(s) :
 *  Date :
 *  Suivi des Modifications :
 *
 */


#define LINESIZE 256
#define PROGSIZE 400000096
#define EXIT_TRICHEURS 2

char program[PROGSIZE];
sequence_t prog_seq;
int numero_carte = -1; /* ne lancer que le test de cette carte */


/* void help(char *progname __attribute__((unused))) */
void help(char *progname)
{
    eprintf ("Usage: %s [-d] [-carte <n>] <fichier>\n\n", progname);
    eprintf ("Options:\n");
    eprintf ("\t-d\t\tmode debug\n");
    eprintf ("\t-carte <n>\tUtiliser la carte <n> du fichier de test\n");
    eprintf ("\t-silent\tSupprimer tous les output (pour les tests de performance)\n");
    exit(EXIT_FAILURE);
}


/*
 * Lance l'interprétation du programme <prog> sur la carte <carte>.
 */
void launch (bool debug, int carte_num)
{
    if (program[0] != '\0' && carte_num != -1 &&
            (numero_carte == -1 || numero_carte == carte_num)) {

        if (! silent_mode) {
            printf ("Lancement du test...\n");
            printf ("\tProgramme: %s\n", program);
            afficherCarte ();
        }

        /* curiosity_reset (cur); */

        conversion(program,&prog_seq);

        switch (interprete (&prog_seq, debug)) { //interprete le programme lu jusqu'a la fin de son execution 

            if (! silent_mode) {
                afficherCarte();
            }
            case VICTOIRE:
                if (mars.map[cY][cX] != TARGET) {
                    printf ("*********************************************\n");
                    printf ("Curiosity n'est pas sur la cible !\n");
                    printf ("Pourquoi l'interprète crie-t-il victoire ?!?\n");
                    printf ("...\n");
                    printf ("... (tricheurs)...\n");
                    exit (EXIT_TRICHEURS);
                } else {
                    if (verifieMarques ()) {
                        if (! silent_mode) {
                            printf ("***************************\n");
                            printf ("Carte %d passée avec succès\n", mars.carte_num);
                        }
                    } else {
                        if (! silent_mode) {
                            printf ("*********************************************\n");
                            printf ("Échec sur la carte %d\n", mars.carte_num);
                        }
                        exit (EXIT_FAILURE);
                    }
                }
                break;
            case CIBLERATEE:
                printf ("*********************************************\n");
                printf ("Curiosity n'est pas sur la cible !\n");
            case RATE:
                printf ("*********************************************\n");
                printf ("Échec sur la carte %d\n", mars.carte_num);
                exit (EXIT_FAILURE);
            default:
                printf ("Valeur de retour de l'interpréte inconnue\n");
                exit (EXIT_FAILURE);
        }
    }
}

void read_test_file (char* fichier, bool debug)
{
    FILE *f = fopen (fichier,"r");
    char *line = NULL;
    size_t maxlinesize = 0;

    bool in_prog = true;
    int carte_num = -1;

    if (f==NULL) {
        eprintf ("Impossible d'ouvrir %s en lecture.\n", fichier);
        exit(EXIT_FAILURE);
    }



    program[0] = '\0'; /* nouveau programme */

    while (! feof(f)) {

        ssize_t linesize = getline (&line, &maxlinesize, f);

        if (linesize == -1) { /* end of file */
            /* perror ("Error reading file:"); */
            break;
        }

        char *p = line;

        while (*p == ' ') p++;
        if (*p == '#') continue; /* commentaire */
        if (*p == '\n') continue; /* ligne vide */

        if (!strncmp(p, "Pile", 4)) {
            /* Pas de gestion de la directive "Pile" */
            continue;
        }

        if (!strncmp(p, "Programme", 9)) {
            launch (debug, carte_num);

            program[0] = '\0'; /* nouveau programme */
            carte_num = -1;
            in_prog = true;
            continue;
        }

        if (!strncmp(p, "Map", 3)) {
            launch (debug, carte_num);

            carte_num = atoi (p+4);

            initCarte (carte_num);


            if (! silent_mode) {
                printf ("Lecture de la map n°%d\n", carte_num);
            }
            in_prog = false;
            continue;
        }

        if (in_prog) {
            /* ajout ligne au programme */
            assert (strlen(program) + linesize < PROGSIZE);
            strcat (program, line);
        }
        else {
            /* ajout ligne à la carte */
            ajoutLigneCarte (line);
        }
    }
    fclose(f);

    free (line);
    launch (debug, carte_num);

}


int main(int argc, char *argv[]) {
    int arg;
    bool debug = false;
    char *fichier = NULL;

    if (argc<2) {
        help (argv[0]);
    }

    arg = 1;
    while (arg < argc) {
        if (! strncmp(argv[arg], "-h", 2)) {
            help (argv[0]);
        }
        else if (! strncmp(argv[arg], "-d", 2)) {

#ifndef SILENT
            /* Ignore in silent mode */
            debug = true;
#endif
            arg++;
            continue;
        }

        else if (! strncmp(argv[arg], "-carte", 6)) {
            numero_carte = atoi(argv[arg+1]);
            arg += 2;
            continue;
        }

        else if (! strncmp(argv[arg], "-silent", 7)) {
            silent_mode = true;
            arg++;

            printf("Attention ! Si vous lisez ce message, c'est que\n"
                    "vous n'avez pas desactive les fonctions d'affichage !\n"
                    "Pour le faire, changez les flags de compilation (voir Makefile)\n"
                    "et forcez la recompilation complete du projet avec 'make -B'.\n");
            continue;
        }


        else if (fichier) {
            fprintf (stderr, "Un seul fichier de test autorisé!\n");
            exit (EXIT_FAILURE);
        }

        fichier = argv[arg];

        if (! silent_mode) {
            printf ("Fichier de test: %s\n", fichier);
        }

        arg++;
    }


    read_test_file (fichier, debug);

    exit (EXIT_SUCCESS);
}

