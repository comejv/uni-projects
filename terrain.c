
#include "terrain.h"
#include "robot.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

erreur_terrain lire_terrain(FILE *f, Terrain *t, int *x, int *y)
{
	char c;
	int robot_pos = 0;

	if (f == NULL)
	{
		fprintf(stderr, "%s", "Impossible de lire le fichier.\n");
		return ERREUR_FICHIER;
	}

	// Lecture de la largeur
	if (fscanf(f, "%d", &t->largeur) != 1)
	{
		fprintf(stderr, "%s", "Erreur lors de la lecture de la largeur.\n");
		return ERREUR_LECTURE_LARGEUR;
	}

	// Lecture de la hauteur
	if (fscanf(f, "%d", &t->hauteur) != 1)
	{
		fprintf(stderr, "%s", "Erreur lors de la lecture de la heuteur.\n");
		return ERREUR_LECTURE_HAUTEUR;
	}

	if (t->hauteur >= DIM_MAX)
	{
		fprintf(stderr, "La hauteur doit être inferieur à %d.\n", DIM_MAX);
		return ERREUR_HAUTEUR_INCORRECTE;
	}
	if (t->largeur >= DIM_MAX)
	{
		fprintf(stderr, "La largeur doit être inferieur à %d.\n", DIM_MAX);
		return ERREUR_LARGEUR_INCORRECTE;
	}

	// Lecture du terrain
	for (int h = 0; h < t->hauteur; h++)
	{
		for (int l = 0; l < t->largeur; l++)
		{
			c = getc(f);
			if (c == EOF)
			{
				fprintf(stderr, "%s", "Les dimensions indiquées ne correspondent pas au terrain donné.");
				return ERREUR_FICHIER;
			}

			switch (c)
			{
			case 'C':
				*x = l;
				*y = h;
				robot_pos++;
			case '.':
				t->tab[h][l] = LIBRE;
				break;
			case '#':
				t->tab[h][l] = ROCHER;
				break;
			case '~':
				t->tab[h][l] = EAU;
				break;

			// Gestion newline
			case '\n':
				// Si ligne trop longue ou trop courte
				if (l != 0)
				{
					fprintf(stderr, "%s", "Le terrain contient une ligne de mauvaise longueur (au niveau du &).\n");
					t->tab[h][t->largeur - 1] = ERREUR;

					return ERREUR_LONGUEUR_LIGNE;
				}
				l--;
				break;

			default:
				fprintf(stderr, "Caractère %c inconnu.\n", c);
				break;
			}
		}
	}

	// Si pas de robot
	if (!robot_pos)
	{
		fprintf(stderr, "%s", "Pas de position de départ pour le robot.\n");
		return ERREUR_POSITION_ROBOT_MANQUANTE;
	}

	// Gestion si trop de lignes
	getc(f);
	c = getc(f);
	if (c != EOF && c != '\n')
	{
		fprintf(stderr, "%s", "Trop de lignes dans le terrain.\n");
		return ERREUR_NOMBRE_LIGNES;
	}

	return OK_TERRAIN;
}

int largeur(Terrain *t)
{
	return t->largeur;
}

int hauteur(Terrain *t)
{
	return t->hauteur;
}

int est_case_libre(Terrain *t, int x, int y)
{
	if ((x >= 0) && (x < t->largeur) && (y >= 0) && (y < t->hauteur))
		return t->tab[y][x] == LIBRE;
	else
		return 0;
}

void afficher_terrain(Terrain *t)
{
	for (int h = 0; h < t->hauteur; h++)
	{
		for (int l = 0; l < t->largeur; l++)
		{
			switch (t->tab[h][l])
			{
			case LIBRE:
				putc('.', stdout);
				break;
			case ROCHER:
				putc('#', stdout);
				break;
			case EAU:
				putc('~', stdout);
				break;

			case ERREUR:
				putc('&', stdout);
			}
		}
		putc('\n', stdout);
	}
}

void ecrire_terrain(FILE *f, Terrain *t, int x, int y)
{
	int i, j;
	char c;

	fprintf(f, "%d\n", t->hauteur);
	fprintf(f, "%d\n", t->largeur);
	for (i = 0; i < t->hauteur; i++)
	{
		for (j = 0; j < t->largeur; j++)
		{
			switch (t->tab[i][j])
			{
			case LIBRE:
				c = '.';
				break;
			case ROCHER:
				c = '#';
				break;
			case EAU:
				c = '~';
				break;
			}
			if (i == x && j == y)
				c = 'C';
			fprintf(f, "%c", c);
		}
		fprintf(f, "\n");
	}
	// fprintf(f, "\n");
}
