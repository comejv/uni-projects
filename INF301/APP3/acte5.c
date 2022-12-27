#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "arbres.h"
#include "listes.h"
#include "arbresphylo.h"

#define LINE_SIZE 1000
#define WORD_SIZE 50

struct ec_cell
{
	char *espece;
	cellule_t *caracs;
	struct ec_cell *suivant;
};
typedef struct ec_cell espece_carac_t;

cellule_t *ajouter_cell_fin(cellule_t *ptr)
{
	if (ptr == NULL)
		return malloc(sizeof(cellule_t));
	while (ptr->suivant != NULL)
		ptr = ptr->suivant;
	ptr->suivant = malloc(sizeof(cellule_t));
	return ptr->suivant;
}

/* format fichier table
caract1 caract2 caract3 ... caractN
espece1 espece2 espece3 ... especeN
caract of espece1
caract of espece2
...
caract of especeN
*/
// Lis un tableau de caractéristiques et renvoie la caractéristique
// présente chez le plus d'espèces
void lire_table_carac(arbre **a, FILE *f, espece_carac_t *espece_caracs)
{
	char *ligne = malloc(sizeof(char) * LINE_SIZE);
	char *token = malloc(sizeof(char) * WORD_SIZE);

	liste_t *liste_caracs = malloc(sizeof(liste_t));

	// pointeurs pour le parcours des listes
	cellule_t *ptr_liste_carac = NULL;
	cellule_t *ptr_car_ec = NULL;
	espece_carac_t *ptr_ec = espece_caracs;

	// on fait une liste des caractères
	// pb : retirer newline à la fin de la ligne
	// et dernière cellule vide
	fgets(ligne, LINE_SIZE, f);
	token = strtok(ligne, " ");
	while (token != NULL)
	{
		ptr_liste_carac = ajouter_cell_fin(ptr_liste_carac);
		if (liste_caracs->tete == NULL)
			liste_caracs->tete = ptr_liste_carac;
		ptr_liste_carac->val = malloc(sizeof(char) * WORD_SIZE);
		strcpy(ptr_liste_carac->val, token);
		token = strtok(NULL, " ");
	}

	// on crée les espèces dans espece_caracs
	ptr_ec = espece_caracs;
	fgets(ligne, LINE_SIZE, f);
	token = strtok(ligne, " ");
	while (token != NULL)
	{
		ptr_ec->espece = malloc(sizeof(char) * WORD_SIZE);
		strcpy(ptr_ec->espece, token);
		token = strtok(NULL, " ");
		if (token == NULL)
			break;
		ptr_ec->suivant = malloc(sizeof(espece_carac_t));
		ptr_ec = ptr_ec->suivant;
	}

	// on ajoute les caractéristiques aux espèces
	ptr_ec = espece_caracs;
	while (fgets(ligne, LINE_SIZE, f) != NULL)
	{
		ptr_liste_carac = liste_caracs->tete;
		ptr_car_ec = NULL;
		token = strtok(ligne, " ");
		while (token != NULL)
		{
			if (strcmp(token, "1") == 0)
			{
				ptr_car_ec = ajouter_cell_fin(ptr_car_ec);
				if (ptr_ec->caracs == NULL)
					ptr_ec->caracs = ptr_car_ec;
				ptr_car_ec->val = malloc(sizeof(char) * WORD_SIZE);
				strcpy(ptr_car_ec->val, ptr_liste_carac->val);
				ptr_liste_carac = ptr_liste_carac->suivant;
			}
			token = strtok(NULL, " ");
		}
		ptr_ec = ptr_ec->suivant;
	}

	// On ajoute les espèces tant qu'il y en a
	while (espece_caracs != NULL)
	{
		ajouter_espece(*a, espece_caracs->espece, espece_caracs->caracs);
		espece_caracs = espece_caracs->suivant;
	}
}

int main(int argc, char **argv)
{
	if (argc != 2)
	{
		printf("Usage : %s <nom fichier test>\n", argv[0]);
		return 1;
	}
	char *nom_fichier_test = argv[1];
	FILE *f = fopen(argv[1], "r");
	if (f == NULL)
	{
		printf("Erreur, fichier test %s inexistant\n", nom_fichier_test);
		return 1;
	}

	// ouvrir le fichier source du test
	char *nom_fichier_source = malloc(sizeof(char) * LINE_SIZE);
	fgets(nom_fichier_source, LINE_SIZE, f);
	nom_fichier_source[strlen(nom_fichier_source) - 1] = '\0';
	FILE *source = fopen(nom_fichier_source, "r");
	if (source == NULL)
	{
		printf("Erreur, fichier test %s inexistant\n", nom_fichier_test);
		return 1;
	}

	arbre *a = malloc(sizeof(arbre));
	espece_carac_t *espece_caracs = malloc(sizeof(espece_carac_t));

	// Ici on obtient une liste chainée dont chaque cellule contient
	// une espèce et une liste de caractéristiques
	lire_table_carac(&a, source, espece_caracs);

	// tests
	printf("Test %s : lecture du tableau %s\n", nom_fichier_test, nom_fichier_source);

	char *ligne = malloc(sizeof(char) * LINE_SIZE);
	// Lire nombre caractéristiques attendues
	fgets(ligne, LINE_SIZE, f);
	int nb_carac = atoi(ligne);
	// Lire nombre espèces attendues
	fgets(ligne, LINE_SIZE, f);
	int nb_espece = atoi(ligne);

	// Vérifications nombre caractéristiques et espèces
	int nb_espece_arbre, nb_carac_arbre;
	analyse_arbre(*a, &nb_espece_arbre, &nb_carac_arbre);

	if (nb_espece_arbre != nb_espece)
	{
		printf("\033[0;31mERREUR\033[0m sur %s\n\tNombre d'espèces incorrect : %d attendues mais %d trouvées.\n",
			   nom_fichier_source, nb_espece, nb_espece_arbre);
		return 1;
	}
	else
		printf("Nombre espèces \033[0;32mOK\033[0m\n");

	if (nb_carac_arbre != nb_carac)
	{
		printf("\033[0;31mERREUR\033[0m sur %s\n\tNombre de caractéristiques incorrect : %d attendues mais %d trouvées.\n",
			   nom_fichier_source, nb_carac, nb_carac_arbre);
		return 1;
	}
	else
		printf("Nombre caractéristiques \033[0;32mOK\033[0m\n");

	// Pour vérifier visuellement l'arbre créé décommenter la ligne suivante :
	// affiche_arbre(arbre);
	// et exécuter la commande $ make afficher

	return 0;
}
