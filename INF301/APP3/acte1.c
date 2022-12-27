#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "arbres.h"
#include "arbresphylo.h"
#include "common_tests.h"

int main(int argc, char** argv) {
	if (argc != 2) {
		printf("Usage : %s <nom fichier test>\n", argv[0]);
		return 1;
	}
	FILE* f = fopen(argv[1], "r+");
	if (f == NULL) {
		printf("Erreur, fichier test inexistant\n");
		return 1;
	}

	// LIRE FICHIER TEST (arbre nb_esp nb_carac)
	char* line = NULL;
	char* token;
	char* filename;
	int expected_nb_esp, expected_nb_carac;
	size_t len;
	arbre a ;

	// Recupere arbre
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");

		// Recupère le nom du fichier test
		int l = strlen(token) + 1;
		filename = malloc(l);
		trimwhitespace(filename, l , token);
		FILE* f_arb = fopen(filename, "r+");
		if (f_arb == NULL) {
			printf("Erreur, fichier arbre %s inexistant\n", filename);
			return 1;
		}
		a = lire_arbre(f_arb);
	} else {
		printf("Erreur : pas de nom de fichier");
		return 1;
	}

	// Nombre espece
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		expected_nb_esp = atoi(token);
	}else {
		printf("Erreur : pas de nombre d'espece dans le fichier test\n");
		return 1;
	}

	// Nombre caractéristiques
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		expected_nb_carac = atoi(token);
	}else {
		printf("Erreur : pas de nombre de caractéristiques dans le fichier test\n");
		return 1;
	}

	return test_nb_esp_caracs(a, filename, expected_nb_esp, expected_nb_carac);
}
