#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include "arbres.h"
#include "arbresphylo.h"
#include "listes.h"

/* ACTE I */
void analyse_arbre_rec(arbre racine, int *nb_esp, int *nb_carac)
{
	if (racine == NULL)
	{
		return;
	}

	if (est_feuille(racine))
	{
		(*nb_esp)++;
	}
	else
	{
		(*nb_carac)++;
		analyse_arbre_rec(racine->droit, nb_esp, nb_carac);
		analyse_arbre_rec(racine->gauche, nb_esp, nb_carac);
	}
}

void analyse_arbre(arbre racine, int *nb_esp, int *nb_carac)
{
	*nb_esp = 0;
	*nb_carac = 0;
	analyse_arbre_rec(racine, nb_esp, nb_carac);
}

/* ACTE II */
/* Recherche l'espece dans l'arbre. Modifie la liste passée en paramètre pour y mettre les
 * caractéristiques. Retourne 0 si l'espèce a été retrouvée, 1 sinon.
 */
int rechercher_espece(arbre racine, char *espece, liste_t *seq)
{
	// Arbre vide
	if (racine == NULL)
	{
		return 1;
	}

	// espèce trouvé
	if (strcmp(espece, racine->valeur) == 0)
	{
		return 0;
	}

	// On cherche dans les fils
	if (rechercher_espece(racine->gauche, espece, seq) == 0)
	{
		return 0;
	}

	if (rechercher_espece(racine->droit, espece, seq) == 0)
	{
		ajouter_tete(seq, racine->valeur);
		return 0;
	}

	// On a pas trouvé
	return 1;
}

/* ACTE III*/
/* Doit renvoyer 0 si l'espece a bien ete ajoutee, 1 sinon, et ecrire un
 * message d'erreur.
 */
void ajouter_seq_carac(char *espece, cellule_t *seq, arbre a)
{
	while (seq != NULL)
	{
		a->valeur = seq->val;
		a->droit = nouveau_noeud();
		a = a->droit;
		seq = seq->suivant;
	}
	a->valeur = espece;
}

int ajouter_espece(arbre *a, char *espece, cellule_t *seq)
{
	noeud *noeud;
	if (seq == NULL)
	{
		if (*a == NULL)
		{
			noeud = nouveau_noeud();
			noeud->valeur = espece;
			*a = noeud;
			return 0;
		}
		if (est_feuille(*a))
		{
			printf("Ne peut pas ajouter %s: possède les mêmes caractères que %s.\n", espece, (*a)->valeur);
			return 1;
		}
		return ajouter_espece(&((*a)->gauche), espece, NULL);
	}
	if (*a == NULL)
	{
		noeud = nouveau_noeud();
		*a = noeud;
		ajouter_seq_carac(espece, seq, *a);
		return 0;
	}
	if (est_feuille(*a))
	{
		(*a)->gauche = nouveau_noeud();
		(*a)->gauche->valeur = (*a)->valeur;
		(*a)->valeur = seq->val;
		(*a)->droit = nouveau_noeud();
		ajouter_seq_carac(espece, seq->suivant, ((*a)->droit));
		return 0;
	}
	if (strcmp(seq->val, (*a)->valeur) == 0)
	{
		return ajouter_espece(&(*a)->droit, espece, seq->suivant);
	}
	return ajouter_espece(&(*a)->gauche, espece, seq);
}

// Une autre implémentation impérative plutôt que récursive
/*
int ajouter_espece(arbre *a, char *espece, cellule_t *seq)
{
	// Parcours de l'arbre selon la sequence, ajout des noeuds si besoin
	while (seq != NULL)
	{
		// Si on est dans une feuille, on crée un noeud
		if (*a == NULL || est_feuille(*a))
		{
			// On crée le noeud
			noeud *n = nouveau_noeud();
			n->valeur = seq->val;

			// On crée le fils gauche
			if (*a != NULL)
			{
				noeud *fg = nouveau_noeud();
				fg->valeur = (*a)->valeur;
				n->gauche = fg;
			}

			noeud *n_p = n;

			// On crée en boucle le fils droit jusqu'à la fin de la séquence
			while (seq->suivant != NULL)
			{
				noeud *fd = nouveau_noeud();
				fd->valeur = seq->suivant->val;
				n_p->droit = fd;
				n_p = fd;
				seq = seq->suivant;
			}

			// On crée le noeud de l'espèce
			noeud *fe = nouveau_noeud();
			fe->valeur = espece;
			n_p->droit = fe;

			// On remplace le noeud par le nouveau noeud
			*a = n;

			return 0;
		}
		// Si on est sur un noeud
		// Noeud dans seq
		if (strcmp(seq->val, (*a)->valeur) == 0)
		{
			a = &(*a)->droit;
			seq = seq->suivant;
		}
		// noeud pas dans seq
		else
		{
			a = &(*a)->gauche;
		}
	}

	if (*a == NULL)
	{
		*a = nouveau_noeud();
		(*a)->valeur = espece;
		return 0;
	}

	// Si on a plus de caractéristiques dans la seq, on suit le gauche jusqu'à
	// la fin de l'arbre
	while ((*a)->gauche != NULL)
	{
		a = &(*a)->gauche;
	}
	// Si c'est une feuille, on a déjà une espèce avec cette séquence
	if (est_feuille(*a))
	{
		printf("Ne peut ajouter %s: possède les mêmes caractères que %s.\n", espece, (*a)->valeur);
		return 1;
	}
	// Sinon, on ajoute l'espèce
	else
	{
		(*a)->gauche = nouveau_noeud();
		(*a)->gauche->valeur = espece;
		return 0;
	}

	return 1;
}
*/

/* Doit afficher la liste des caractéristiques niveau par niveau, de gauche
 * à droite, dans le fichier fout.
 * Appeler la fonction avec fout=stdin pour afficher sur la sortie standard.
 */
void afficher_par_niveau(arbre racine, FILE *fout)
{
	if (racine == NULL)
	{
		return;
	}

	file f;
	init_file(&f);
	enfiler(&f, racine, 0);
	int niveau = -1;
	cellule_f *cel;

	while (!file_vide(&f))
	{
		cel = defiler(&f);
		if (est_feuille(cel->n))
			continue;
		if (cel->n->gauche != NULL)
		{
			enfiler(&f, cel->n->gauche, cel->niveau + 1);
		}
		if (cel->n->droit != NULL)
		{
			enfiler(&f, cel->n->droit, cel->niveau + 1);
		}

		if (cel->niveau != niveau)
		{
			niveau = cel->niveau;
			if (niveau != 0)
				fprintf(fout, "\n%s", cel->n->valeur);
			else
				fprintf(fout, "%s", cel->n->valeur);
		}
		else
		{
			fprintf(fout, " %s", cel->n->valeur);
		}
		free(cel);
	}
}

// Acte 4
// parcours de l'arbre en profondeur prefixe
// quand on croise une espece de la seq on vérifie que toutes les autres
// soient dans le sous arbre ou dans la branche opposée

#define NOEUD_VIDE -1
#define ERREUR -2
#define NOEUD_AJOUTE -3

int parcours_prefixe(arbre racine, char *carac, cellule_t *seq, int nb_elem)
{
	//////////////////////////////////////////////////////////////////////////
	// Types utile :
	arbre tmp;
	int droit, gauche;
	//////////////////////////////////////////////////////////////////////////
	// Corps de la fonction :
	if ((racine) == NULL)
	{
		return NOEUD_VIDE;
	}
	if (est_feuille(racine))
	{
		if (recherche_nom(seq, racine->valeur))
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	gauche = parcours_prefixe(racine->gauche, carac, seq, nb_elem);
	if (gauche == nb_elem)
	{
		tmp = nouveau_noeud();
		tmp->valeur = carac;
		tmp->droit = racine->gauche;
		racine->gauche = tmp;
		return NOEUD_AJOUTE;
	}
	if ((gauche == NOEUD_AJOUTE) || (gauche == ERREUR))
	{
		return gauche;
	}
	if (NOEUD_VIDE == gauche)
	{
		return parcours_prefixe(racine->droit, carac, seq, nb_elem);
	}

	droit = parcours_prefixe(racine->droit, carac, seq, nb_elem);

	if (NOEUD_VIDE == droit)
	{
		return gauche;
	}
	if ((NOEUD_AJOUTE == droit) || (ERREUR == droit))
	{
		return droit;
	}
	if ((gauche == 0 || droit == 0) && (gauche != 0 || droit != 0))
	{
		if (droit == nb_elem)
		{
			tmp = nouveau_noeud();
			tmp->valeur = carac;
			tmp->droit = racine->droit;
			racine->droit = tmp;
			return NOEUD_AJOUTE;
		}
		else
		{
			return ERREUR;
		}
	}
	return gauche + droit;
}

int ajouter_carac(arbre *a, char *carac, cellule_t *seq)
{
	//////////////////////////////////////////////////////////////////////////
	// Types utile :
	arbre tmp;
	int nb_elem, ret;
	nb_elem = Nombre_elem_liste(seq);

	ret = parcours_prefixe((*a), carac, seq, nb_elem);

	switch (ret)
	{
	case ERREUR:
		printf("Ne peut pas ajouter %s: ne forme pas un sous-arbre.\n", carac);
		return 0;
	case NOEUD_AJOUTE:
		return 1;
	case NOEUD_VIDE:
		return 0;
	default:
		if (nb_elem == ret)
		{
			tmp = nouveau_noeud();
			tmp->valeur = carac;
			tmp->droit = (*a);
			(*a) = tmp;
			return 1;
		}
		printf("Ne peut pas ajouter %s: ne forme pas un sous-arbre.\n", carac);
		return 0;
	}
}
