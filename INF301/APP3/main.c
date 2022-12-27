#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "listes.h"
#include "arbres.h"
#include "arbresphylo.h"
#include "file_ptr.h"

int DEBUG = 0;

int main(int argc, char *argv[])
{
    char *fichier = NULL;
    liste_t seq;

    init_liste_vide(&seq);

    if (argc < 2)
    {
        fprintf(stderr, "Usage:  %s [-d] <fichier>\n", argv[0]);
        fprintf(stderr, "\n");
        fprintf(stderr, "Options:\n");
        fprintf(stderr, "\t-d\tmode debug\n");
        exit(1);
    }
    int arg = 1;

    while (arg < argc)
    {
        if (!strncmp(argv[arg], "-d", 2))
        {
            DEBUG = 1;
            arg++;
            continue;
        }
        if (argv[arg][0] == '-')
        {
            fprintf(stderr, "Option inconnue : '%s'\n", argv[arg]);
            exit(1);
        }
        if (fichier == NULL)
        {
            fichier = argv[arg];
            arg++;
            continue;
        }
        else
        {
            fprintf(stderr, "Trop de fichiers sur la ligne de commande : '%s'\n", argv[arg]);
            exit(1);
        }
    }

    debug("Ouverture de %s\n", fichier);
    FILE *f = fopen(fichier, "r");
    if (!f)
    {
        fprintf(stderr, "Erreur à l'ouverture du fichier `%s'\n", fichier);
        perror(fichier);
        exit(1);
    }

    arbre mon_arbre = lire_arbre(f);

    FILE *fout = fopen("ents.arbre", "w");

    afficher_par_niveau(mon_arbre, fout);

    return 0;
}
