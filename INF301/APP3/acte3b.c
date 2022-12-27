#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "arbres.h"
#include "arbresphylo.h"
#include "common_tests.h"

#define BUF_SZ 100000
char buf1[BUF_SZ], buf2[BUF_SZ];

int main(int argc, char** argv) {
	if (argc != 2) {
		printf("Usage : %s <nom fichier test>\n", argv[0]);
		return 1;
	}
	char* fichier_test = argv[1];
	FILE* f = fopen(argv[1], "r+");
	if (f == NULL) {
		printf("Erreur, fichier test %s inexistant\n", fichier_test);
		return 1;
	}

	char* line = NULL;
	char* token;
	char* nom_fichier;
	size_t len;

	arbre a;
	// Recupere arbre
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");

		// Recupère le nom du fichier test
		int l = strlen(token) + 1;
		nom_fichier = malloc(l);
		trimwhitespace(nom_fichier, l , token);
		FILE* f_arb = fopen(nom_fichier, "r+");
		if (f_arb == NULL) {
			fprintf(stderr, "Erreur, fichier arbre %s inexistant\n", nom_fichier);
			return 1;
		}
		a = lire_arbre(f_arb);
	} else {
		fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}

	FILE* ftest = fopen("_tmp", "w");
	afficher_par_niveau(a, ftest);
	fclose(ftest);
	ftest = fopen("_tmp", "r");

	int prof = 1;
	while(fgets(buf1, BUF_SZ, f)) {
		fgets(buf2, BUF_SZ, ftest);
		char* end = buf2 + strlen(buf2) - 1;
		while(end > buf2 && isspace(*end))
			end--;
		end[1] = '\0';
		buf1[strlen(buf1)-1] = '\0';
		if(strcmp(buf1, buf2) != 0) {
			fprintf(stderr, "\033[0;31mERREUR\033[0m sur %s, ligne: %d \nAttendu : %s \nTrouvé :  %s \n", 
					fichier_test, prof, buf1, buf2);
			return 1;
		}
		prof++;
	}
	printf("%s \033[0;32mOK\033[0m\n", fichier_test);
	// remove("_tmp");

	return 0;
}
