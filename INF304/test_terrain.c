#include "terrain.h"
#include <stdio.h>

int main(int argc, char **argv)
{
	FILE *f;
	Terrain t;
	size_t len = 0;
	__ssize_t read;
	char *line = NULL;
	int x, y;

	if (argc < 2)
	{
		printf("Usage : %s <fichier>\n", argv[0]);
		return 1;
	}
	if ((f = fopen(argv[1], "r")) == NULL)
	{
		perror("Impossible d'ouvrir le fichier terrain");
		return 1;
	}

	while (lire_terrain(f, &t, &x, &y) != OK_TERRAIN)
	{
		afficher_terrain(&t);
		fprintf(stderr, "%s", "Erreur dans la lecture du fichier, réessayez :\n");
		read = getline(&line, &len, stdin);
		line[read - 1] = '\0';
		f = fopen(line, "r");
	}

	fclose(f);
	afficher_terrain(&t);
	printf("Position initiale du robot : (%d, %d)\n", x, y);
}
