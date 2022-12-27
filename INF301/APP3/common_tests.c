#include "listes.h"
#include <stdio.h>
#include <stdlib.h>
#include "common_tests.h"


// Honteusement pompé sur
// https://stackoverflow.com/questions/122616/how-do-i-trim-leading-trailing-whitespace-in-a-standard-way
// Stores the trimmed input string into the given output buffer, which must be
// large enough to store the result.  If it is too small, the output is
// truncated.
size_t trimwhitespace(char *out, size_t len, const char *str)
{
  if(len == 0)
    return 0;

  const char *end;
  size_t out_size;

  // Trim leading space
  while(isspace((unsigned char)*str)) str++;

  if(*str == 0)  // All spaces?
  {
    *out = 0;
    return 1;
  }

  // Trim trailing space
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) end--;
  end++;

  // Set output size to minimum of trimmed string length and buffer size minus 1
  out_size = (size_t)(end - str) < len-1 ? (end - str) : len-1;

  // Copy trimmed string and add null terminator
  memcpy(out, str, out_size);
  out[out_size] = 0;

  return out_size;
}

int test_nb_esp_caracs(arbre a, char* filename, int expected_nb_esp, int expected_nb_carac) {
	int nb_esp, nb_carac;
	analyse_arbre(a, &nb_esp, &nb_carac);
	if (nb_esp == expected_nb_esp && nb_carac == expected_nb_carac){
		printf("Nombre espèces et caractéristiques pour %s\033[0;32m OK\033[0m\n", filename);
		return 0;
	}
	if (nb_esp != expected_nb_esp) {
		fprintf(stderr, "\033[0;31mERREUR\033[0m pour le fichier %s, nombre d'espèces obtenu = %d mais on attendait %d\n", filename, nb_esp, expected_nb_esp);
	}
	if (nb_carac != expected_nb_carac){
		fprintf(stderr, "\033[0;31mERREUR\033[0m pour le fichier %s, nombre de caractéristiques obtenu = %d mais on attendait %d\n", filename, nb_carac, expected_nb_carac);
	}
	return 1;
}


int test_list_carac(int nb_attendues, char** attendues, liste_t trouvees) {

	cellule_t* cel = trouvees.tete;
	for (int i = 0; i < nb_attendues; i++) {
		char* expected = attendues[i];
		if (cel == NULL) {
			fprintf(stderr, "\033[0;31mERREUR\033[0m - les caractéristiques suivantes sont manquantes :\n");
			for (int j = i; j < nb_attendues; j++) {
				fprintf(stderr, "%s ", attendues[j]);
			}
			fprintf(stderr, "\n");
			// TOOO
			return 1;
		}
		char* val = cel->val;
		if (strcmp(val, expected) != 0) {
			fprintf(stderr, "\033[0;31mERREUR\033[0m: on attendait %s mais on a trouvé %s\n",
					attendues[i], val);
			return 1;
		} else {
			printf("%s \033[0;32mOK\033[0m\n", expected);
		}
		cel = cel->suivant;
	}
	if (cel != NULL) {
		fprintf(stderr, "\033[0;31mERREUR\033[0m - les caractéristiques suivantes sont en trop dans la liste :\n");
		while (cel != NULL) {
			fprintf(stderr, "%s ", cel->val);
			cel = cel->suivant;
		}
		fprintf(stderr, "\n");
		return 1;
	}
	return 0;
}

int verifier_arbre(arbre a, char* nom_arbre,
		int nb_especes_attendues, int nb_caracs_attendues,
		int nb_especes_tests,
		espece_caracs_t * especes_caracs // consommé - ne pas réutiliser
		) {
	if (test_nb_esp_caracs(a, nom_arbre, nb_especes_attendues, nb_caracs_attendues) != 0)
		return 1;
	for (int i = 0; i < nb_especes_tests; i++){
		liste_t seq;
		init_liste_vide(&seq);
		espece_caracs_t esp_car = especes_caracs[i];
		printf("Testing %s\n", esp_car.espece);
		int present = rechercher_espece(a, esp_car.espece, &seq);
		if (present != 0) {
			fprintf(stderr, "\033[0;31mERREUR\033[0m %s n'est pas présent dans l'arbre %s après insertion\n",
					esp_car.espece, nom_arbre);
			return 1;
		}
		if (test_list_carac(esp_car.nb_caracs, esp_car.caracs, seq) != 0) {
			return 1;
		}
		free( esp_car.caracs);
		liberer_liste(&seq);
	}
	return 0;
}
