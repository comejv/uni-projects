#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#include "arbres.h"
#include "arbresphylo.h"
#include "common_tests.h"

int main(int argc, char** argv) {
	if (argc != 2) {
		printf("Usage : %s <nom fichier test>\n", argv[0]);
		return 1;
	}
	char* fichier_test = argv[1];
	FILE* f = fopen(fichier_test, "r+");
	if (f == NULL) {
		printf("Erreur, fichier test %s inexistant\n", fichier_test);
		return 1;
	}

	// LIRE FICHIER TEST (arbre nb_esp nb_carac)
	char* line = NULL;
	char* token;
	char* nom_fichier;
	char* nom_espece;
	int expected_nb_carac;
	char**expected_caracs;
	size_t len;
	bool present= true;

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

	// Nom espece
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		int l = strlen(token) + 1;
		nom_espece = malloc(l);
		trimwhitespace(nom_espece, l , token);
	}else {
		fprintf(stderr, "Erreur :  %s mauvais format de fichier test \n", fichier_test);
		return 1;
	}

	// Absent ou present
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		int l = strlen(token) + 1;
		char* absent_ou_present = malloc(l);
		trimwhitespace(absent_ou_present, l , token);
		if (strcmp(absent_ou_present, "absent") == 0)
			present = false;
		else if (strcmp(absent_ou_present, "present") == 0)
			present = true;
		else {
			fprintf(stderr, "Erreur : %s mauvais format de fichier test", fichier_test);
		}
	}else {
		fprintf(stderr, "Erreur :  %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}

	if (!present) {
		liste_t seq;
		init_liste_vide(&seq);
		printf("Cherche %s dans l'arbre %s\n", nom_espece, nom_fichier);
		if (rechercher_espece(a, nom_espece, &seq) == 0) 
			fprintf(stderr, "\033[0;31mERREUR\033[0m sur %s\n\t %s est absent de l'arbre %s mais rechercher_espece a renvoyé présent\n", fichier_test, nom_espece, nom_fichier);
		return 0;
		liberer_liste(&seq);
	}
	else {
		// Nombre carac
		if (getline(&line, &len, f) != -1) {
			token = strtok(line, " ");
			expected_nb_carac = atoi(token);
		}else {
			fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
			return 1;
		}

		expected_caracs = (char**) malloc(expected_nb_carac * sizeof(char*)); 
		if (getline(&line, &len, f) != -1) {
			for (int i = 0; i < expected_nb_carac; i++){
				if (i == 0)
					token = strtok(line, " ");
				else 
					token = strtok(NULL, " ");
				if (token == NULL) {
					fprintf(stderr, "Reçu %d caracteristiques mais %d était demandé\n", i, expected_nb_carac);
					return 1;
				}
				int l = strlen(token) + 1;
				char* carac= malloc(l);
				trimwhitespace(carac, l , token);
				expected_caracs[i] = carac;
			}
		} else {
			fprintf(stderr, "Erreur : pas de nombre d'espece dans le fichier test\n");
			return 1;
		}

		liste_t seq;
		init_liste_vide(&seq);
		printf("Cherche %s dans l'arbre %s\n", nom_espece, nom_fichier);
		int present = rechercher_espece(a, nom_espece, &seq);
		if (present != 0) {
				fprintf(stderr, "\033[0;31mERREUR\033[0m sur %s\n\tL'espece %s n'a pas été trouvée dans l'arbre %s \n",
						fichier_test, nom_espece, nom_fichier);
				return 1;
		}
		int result = test_list_carac(expected_nb_carac, expected_caracs, seq);
		liberer_liste(&seq);
		return result;
	}
	return 0;
}
