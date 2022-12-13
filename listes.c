#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <assert.h>
#ifdef NCURSES
#include <ncurses.h>
#endif
#include "listes.h"

/*
 *  Auteur(s) : Emile
 *  Date : MARDI 11 OCTOBRE
 *  Suivi des Modifications :
 *
 */

bool silent_mode;

/* Créer une nouvelle cellule avec Malloc de type cellule_t*/
cellule_t *nouvelleCellule(void)
{
	/* À compléter (utiliser malloc) */
	return (cellule_t *)malloc(sizeof(cellule_t));
}

/* Detruit une cellule avec free()*/
void detruireCellule(cellule_t *cel)
{
	/* À compléter (utiliser free) */
	free(cel);
}

/* Permet de créer des sous séquence dans notre séquence (des branches)*/
void accolade(char *texte, cellule_t *cel, int *i)
{
	while (texte[*i + 1] != '}')
	{
		*i = *i + 1;
		if (texte[*i] != ' ' && texte[*i] != '\n')
		{
			cel->command = texte[*i];
			if (texte[*i] == '{')
			{
				cel->imbr = nouvelleCellule();
				accolade(texte, cel->imbr, i);
			}
			cel->suivant = nouvelleCellule();
			cel = cel->suivant;
		}
	}
	*i = *i + 1;
	cel->command = texte[*i];
	cel->suivant = NULL;
}

/* Converti un tableau de caractère en type séquence (liste chainée)*/
void conversion(char *texte, sequence_t *seq)
{
	cellule_t *cel;
	int i = 0;
	cel = nouvelleCellule();
	seq->tete = cel;
	while (texte[i + 1] != '\0')
	{
		if (texte[i] != ' ' && texte[i] != '\n')
		{
			cel->command = texte[i];
			if (texte[i] == '{')
			{
				cel->imbr = nouvelleCellule();
				accolade(texte, cel->imbr, &i);
			}
			cel->suivant = nouvelleCellule();
			cel = cel->suivant;
		}
		i++;
	}
	cel->command = texte[i];
	cel->suivant = NULL;
}

/* Permet d'afficher la séquence*/
void afficher(sequence_t *seq)
{
	assert(seq); /* Le pointeur doit être valide */
	/* À compléter */
	sequence_t imbr;
	cellule_t *cel;
	cel = seq->tete;
	while (cel->suivant != NULL)
	{
		printf("%c ", cel->command);
		if (cel->command == '{')
		{
			imbr.tete = cel->imbr;
			afficher(&imbr);
		}
		cel = cel->suivant;
	}
	if (cel->command == '}')
	{
		printf("%c ", cel->command);
		return;
	}
	printf("%c", cel->command);
}
