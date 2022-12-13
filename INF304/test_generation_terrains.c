#include "generation_terrains.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int nb_cases_occupees(Terrain *T)
{
	int occupee = 0;
	int x, y;
	for (x = 0; x < largeur(T); x++)
	{
		for (y = 0; y < hauteur(T); y++)
		{
			if (T->tab[x][y] != LIBRE)
				occupee++;
		}
	}
	return occupee;
}

// Test de generation aléatoire de terrains
// Le programme génère n terrains de largeur et hauteur fixes
// avec largeur et hauteur impaires et inférieures a dimension_max de terrain.h
// avec densité d'obstacle dObst
// autre que la case centrale soit occupee
// l'appel du programme se fait avec 5 arguments :
// generation_terrains N largeur hauteur dObstacle fichier_res
// la sortie se fait dans le fichier resultat

int main(int argc, char **argv)
{
	int N, l, h;
	int i = 0, j = 0;
	float dObst, dObst_reel = 0, dObst_moy = 0;
	FILE *resFile;

	if (argc < 6)
	{
		printf(
			"Usage: %s <N> <largeur> <hauteur> <densite_obstacle> <fichier_res> \n",
			argv[0]);
		return 1;
	}

	N = strtol(argv[1], NULL, 10);
	l = strtol(argv[2], NULL, 10);
	h = strtol(argv[3], NULL, 10);
	dObst = strtof(argv[4], NULL);

	// test de l et h
	if (l > DIM_MAX || l % 2 == 0)
	{
		printf("Largeur incorrecte : doit être impaire et <= %d\n", DIM_MAX);
		return 1;
	}
	if (h > DIM_MAX || h % 2 == 0)
	{
		printf("Hauteur incorrecte : doit être impaire et <= %d\n", DIM_MAX);
		return 1;
	}
	if ((dObst > 1) || (dObst < 0))
	{
		printf("Densité incorrecte : doit être comprise entre 0 et 1\n");
		return 1;
	}

	// Ouverture du fichier résultat
	resFile = fopen(argv[5], "w");
	// Écriture du nombre de terrains
	fprintf(resFile, "%d\n", N);

	// Initialisation de la fonction random
	// A compléter
	srand(time(NULL));

	// Génération de N terrains
	while (i < N)
	{
		Terrain *T = malloc(sizeof(Terrain));
		
		// Génération aléatoire du terrain
		// generation_parfait(T, l, h, dObst);
		generation_aleatoire(T, l, h, dObst);
		j++;
		// Écriture du terrain dans le fichier résultat si chemin existe
		if (existe_chemin_vers_sortie(T))
		{
			ecrire_terrain(resFile, T, T->hauteur / 2, T->largeur / 2);
			dObst_reel = (float)nb_cases_occupees(T) / (float)(l * h);
			dObst_moy += dObst_reel;
			fprintf(resFile, "%f\n\n", dObst_reel);
			i++;
		}

		free(T);
	}

	// Écriture/Affichage des statistiques
	dObst_moy /= N;
	fprintf(resFile, "Nombre de terrains générés : %d\n", j);
	fprintf(resFile, "Nombre de terrains avec chemin : %d\n", i);
	fprintf(resFile, "Pourcentage de terrains avec chemin : %f\n", (float)i / (float)j);
	fprintf(resFile, "Densité moyenne d'obstacles : %f\n", dObst_moy);

	printf("Nombre de terrains générés : %d\n", j);
	printf("Nombre de terrains avec chemin : %d\n", i);
	printf("Pourcentage de terrains avec chemin : %f\n", (float)i / (float)j);
	printf("Densité moyenne d'obstacles : %f\n", dObst_moy);

	// fermeture des fichiers
	fclose(resFile);
	return 0;
}
