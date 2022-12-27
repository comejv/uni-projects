#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
	FILE* f = fopen(argv[1], "r+");
	if (f == NULL) {
		printf("Erreur, fichier test %s inexistant\n", fichier_test);
		return 1;
	}

	// LIRE FICHIER TEST (arbre nb_esp nb_carac)
	char* line = NULL;
	char* token;
	char* nom_fichier;
	char* nom_carac;
	int nb_especes_avec_carac;
	char**especes;
	size_t len;
	bool possible;
	int nb_especes;
	int nb_carac;
	int nb_especes_a_tester;

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

	// Nom carac
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		int l = strlen(token) + 1;
		nom_carac = malloc(l);
		trimwhitespace(nom_carac, l , token);
	}else {
		fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}

	// Nombre carac a ajouter
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		nb_especes_avec_carac = atoi(token);
	}else {
		fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}

	// especes  à chercher
	especes = (char**) malloc(nb_especes_avec_carac * sizeof(char*)); 
	// On ne lit pas cette ligne si il n'y a pas de caracteristiques a inserer
	if (nb_especes_avec_carac > 0) {
		if (getline(&line, &len, f) != -1) {
			for (int i = 0; i < nb_especes_avec_carac; i++){
				if (i == 0)
					token = strtok(line, " ");
				else 
					token = strtok(NULL, " ");
				if (token == NULL) {
					fprintf(stderr, "Reçu %d caracteristiques mais %d était demandé\n",
							i, nb_especes_avec_carac);
					return 1;
				}
				int l = strlen(token) + 1;
				char* espece= malloc(l);
				trimwhitespace(espece, l , token);
				especes[i] = espece;
			}
		} else {
			fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
			return 1;
		}
	}

	// Insertion possible ou impossible
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		int l = strlen(token) + 1;
		char*possible_ou_non = malloc(l);
		trimwhitespace(possible_ou_non, l , token);
		if (strcmp(possible_ou_non, "possible") == 0) {
			possible = true;
		} else if (strcmp(possible_ou_non, "impossible") == 0) {
			possible = false;
		} else {
			fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
			return 1;
		}
	}else {
		fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}

	// Propriétés sur l'arbre à vérifier après l'appel à insérer

	// Nombre espèces
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		nb_especes = atoi(token);
	}else {
		fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}
	
	// Nombre noeuds
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		nb_carac = atoi(token);
	}else {
		fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}

	// Tests sur les caractéristiques d'espèces
	// Nombre especes à tester
	if (getline(&line, &len, f) != -1) {
		token = strtok(line, " ");
		nb_especes_a_tester = atoi(token);
	}else {
		fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
		return 1;
	}

	// Boucles especes à tester
	//

	espece_caracs_t* especes_caracs =
		(espece_caracs_t*) malloc(nb_especes_a_tester * sizeof(espece_caracs_t)); 
	for (int i = 0; i < nb_especes_a_tester; i++) {
		// Premiere ligne, nom de l'animal
		if (getline(&line, &len, f) == -1) {
			fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
			return 1;
		}
		token = strtok(line, " ");
		int l = strlen(token);
		char* espece = malloc(l);
		trimwhitespace(espece, l , token);
		especes_caracs[i].espece = espece;

		// Deuxieme ligne nombre de caracteristiques
		if (getline(&line, &len, f) == -1) {
			fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
			return 1;
		}
		token = strtok(line, " ");
		int nb_caracs = atoi(token);
		especes_caracs[i].nb_caracs = nb_caracs;

		// Troisième ligne caractéristiques
		char** caracs = (char**)malloc(nb_caracs * sizeof(char*));
		if (nb_caracs > 0 && getline(&line, &len, f) == -1) {
			fprintf(stderr, "Erreur : %s mauvais format de fichier test\n", fichier_test);
			return 1;
		}
		for (int i = 0; i < nb_caracs; i++){
			if (i == 0)
				token = strtok(line, " ");
			else 
				token = strtok(NULL, " ");
			if (token == NULL) {
				fprintf(stderr, "Reçu %d caracteristiques mais %d était demandé\n",
						i, nb_carac);
				return 1;
			}
			int l = strlen(token) + 1;
			char* carac = malloc(l);
			trimwhitespace(carac, l , token);
			caracs[i] = carac;
		}
		especes_caracs[i].caracs = caracs;
	}


	// Test
	liste_t seq ;
	init_liste_vide(&seq);
	for (int i = nb_especes_avec_carac - 1; i >= 0; i--) {
		ajouter_tete(&seq, especes[i]);
	}

	printf("Test %s : Ajoute %s dans l'arbre %s\n", fichier_test, nom_carac, nom_fichier);
	if (!ajouter_carac(&a, nom_carac, seq.tete)) {
		if (!possible) {
			printf("Impossible d'insérer %s dans %s comme prévu : \033[0;32mOK\033[0m\n",
					nom_carac, nom_fichier);
		} else {
			fprintf(stderr, "\033[0;31mERREUR\033[0m %s n'a pas été insérée dans l'arbre %s\
					(ajouter_carac a renvoyé 0) mais elle aurait pourtant du être ajoutée\n",
					nom_carac, nom_fichier);
			return -1;
		}
	}
	liberer_liste(&seq);

	// Verifier l'arbre
	return verifier_arbre(a, nom_fichier, nb_especes, nb_carac, nb_especes_a_tester, especes_caracs);
}
