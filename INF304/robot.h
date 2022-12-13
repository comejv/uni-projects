#ifndef _ROBOT_H_
#define _ROBOT_H_

typedef enum
{
  Nord,
  Est,
  Sud,
  Ouest
} Orientation;

typedef struct
{
  int x, y;
  Orientation o;
} Robot;

/* initialiser le robot r en position (x,y) et orientation o */
void init_robot(Robot *r, int x, int y, Orientation o);

/* faire avancer le robot d'une case */
void avancer(Robot *r);

/* faire tourner le robot à gauche */
void tourner_a_gauche(Robot *r);

/* faire tourner le robot à droite */
void tourner_a_droite(Robot *r);

/* recupere la position de la case du robot */
void position(Robot *r, int *x, int *y);

/* recupere la position en abscisse de la case du robot */
int abscisse(Robot *r);

/* recupere la position en ordonnee de la case du robot */
int ordonnee(Robot *r);

/* recupere l'orientation du robot */
Orientation orient(Robot *r);

/* recupere la position de la case devant le robot */
void position_devant(Robot *r, int *x, int *y);

#endif
