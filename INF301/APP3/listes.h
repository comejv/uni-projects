#ifndef _LISTES_H
#define _LISTES_H

typedef char* string;

struct cellule {
	string val;
	struct cellule* suivant;
};

typedef struct cellule cellule_t;

struct liste {
	cellule_t *tete;
};

typedef struct liste liste_t;

/* cree une nouvelle liste, initialement vide */
void init_liste_vide(liste_t* L);

/* libère toutes les cellules de la liste */
void liberer_liste(liste_t *L);

/* Ajouter une nouvelle cellule contenant c
 * en tête de la liste L.
 * Si l'ajout est réussi, le résultat est 0,
 * et 1 sinon (échec de l'ajout)
 */
int ajouter_tete(liste_t *L, string c);

/* Affiche une liste chaînée*/
void afficher_chainee(liste_t *L);

int Nombre_elem_liste(cellule_t *cel);

// Recherche string dans la liste chaînée
int recherche_nom(cellule_t *seq, string nom);

#endif /* _LISTES_H */
