#include "environnement.h"
#include <stdio.h>

/* Initialise l'environnement envt :
   - lit le terrain dans le fichier fichier_terrain
   - initialise le robot : coordonnées initiales lues dans le fichier
   terrain, orientation initiale vers l'est
*/
erreur_terrain initialise_environnement(Environnement *envt,
										char *fichier_terrain)
{
	erreur_terrain errt;
	int x, y; // Position initiale du robot
	FILE *f;

	f = fopen(fichier_terrain, "r");

	errt = lire_terrain(f, &(envt->t), &x, &y);

	if (errt != OK_TERRAIN)
	{
		return errt;
	}

	init_robot(&(envt->r), x, y, Est);

	return errt;
}

resultat_deplacement avancer_envt(Environnement *envt)
{
	int x, y; // Position devant le robot

	automate_pas(0, 1, 0);

	// Récupérer la position devant le robot
	position_devant(&(envt->r), &x, &y);

	if ((x < 0) || (x >= largeur(&envt->t)) || (y < 0) ||
		(y >= hauteur(&envt->t)))
	{
		// Le robot est sorti
		return SORTIE;
	}
	else
	{
		// À corriger : il devrait y avoir une fonction pour cela dans le
		// paquetage terrain
		Case case_devant = envt->t.tab[y][x];
		switch (case_devant)
		{
		case LIBRE:
			avancer(&(envt->r));
			return OK_DEPL;
		case EAU:
			return PLOUF;
		case ROCHER:
			return CRASH;
		}
	}
	return OK_DEPL;
}

/* Tourner le robot à gauche */
void gauche_envt(Environnement *envt) { tourner_a_gauche(&(envt->r)); }

/* Tourner le robot à droite */
void droite_envt(Environnement *envt) { tourner_a_droite(&(envt->r)); }

/* Effectuer une mesure
   Paramètre d : la direction de la mesure
	 0 sur place
	 1 devant
	 2 devant droite
	 3 droite
	 4 derrière droite
	 5 derrière
	 6 derrière gauche
	 7 gauche
	 8 devant gauche
   Renvoie le résultat de la mesure :
	 0 rien (case libre ou en-dehors du terrain)
	 1 eau
	 2 rocher
	 3 erreur (valeur du paramètre incorrect)
 */
int mesure_envt(Environnement *envt, int d)
{
	int x, y;	// Position courante du robot
	int dx, dy; // Direction du robot
	int mx, my; // Position de la mesure

	position(&(envt->r), &x, &y);

	switch (orient(&(envt->r)))
	{
	case Nord:
		dx = 0;
		dy = -1;
		break;
	case Est:
		dx = 1;
		dy = 0;
		break;
	case Sud:
		dx = 0;
		dy = 1;
		break;
	case Ouest:
		dx = -1;
		dy = 0;
		break;
	}

	switch (d)
	{
	case 0: // sur place
		mx = x;
		my = y;
		break;
	case 1: // devant
		mx = x + dx;
		my = y + dy;
		automate_pas(1, 0, 0);
		break;
	case 2: // devant droite
		mx = x + dx - dy;
		my = y + dy + dx;
		break;
	case 3: // droite
		mx = x - dy;
		my = y + dx;
		break;
	case 4: // derrière droite
		mx = x - dx - dy;
		my = y - dy + dx;
		break;
	case 5: // derrière
		mx = x - dx;
		my = y - dy;
		break;
	case 6: // derrière gauche
		mx = x - dx + dy;
		my = y - dy - dx;
		break;
	case 7: // gauche
		mx = x + dy;
		my = y - dx;
		break;
	case 8: // devant gauche
		mx = x + dx + dy;
		my = y + dy - dx;
		break;
	default:
		return 3;
	}

	// À corriger : il devrait y avoir une fonction dans le paquetage
	// terrain pour tester le type de case
	switch (envt->t.tab[my][mx])
	{
	case LIBRE:
		return 0;
	case EAU:
		return 1;
	case ROCHER:
		return 2;
	case MARQUE:
		return 3;
	}
	// Ne devrait pas arriver
	return 3;
}

/* Marquer la case sous le robot */
void pose(Environnement *envt, int x)
{
	int x_r, y_r; // Position du robot

	position(&(envt->r), &x_r, &y_r);

	if (x)
		envt->t.tab[y_r][x_r] = LIBRE;
	else
		envt->t.tab[y_r][x_r] = MARQUE;
}

/* Afficher le terrain avec la position et l'orientation du robot */
void afficher_envt(Environnement *envt)
{
	int i, j;
	int h, l;
	char c;

	h = hauteur(&envt->t);
	l = largeur(&envt->t);

	for (i = 0; i < h; i++)
	{
		for (j = 0; j < l; j++)
		{
			if ((j == abscisse(&envt->r)) && (i == ordonnee(&envt->r)))
			{
				// Afficher le robot selon son orientation
				switch (orient(&envt->r))
				{
				case Nord:
					c = '^';
					break;
				case Est:
					c = '>';
					break;
				case Sud:
					c = 'v';
					break;
				case Ouest:
					c = '<';
					break;
				}
			}
			else
			{
				// Afficher la case
				switch (envt->t.tab[i][j])
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
				case MARQUE:
					c = 'M';
					break;
				case ERREUR:
					c = '?';
					break;
				}
			}
			printf("%c", c);
		}
		printf("\n");
	}
	printf("\n");
}
