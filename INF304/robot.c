#include "robot.h"

void init_robot(Robot *r, int x, int y, Orientation o)
{
    r->x = x,
    r->y = y;
    r->o = o;
}

void avancer(Robot *r)
{
    switch (r->o)
    {
    case Nord:
        r->y--;
        break;
    case Sud:
        r->y++;
        break;
    case Est:
        r->x++;
        break;
    case Ouest:
        r->x--;
        break;
    }
}

void tourner_a_gauche(Robot *r)
{
    switch (r->o)
    {
    case Nord:
        r->o = Ouest;
        break;
    case Sud:
        r->o = Est;
        break;
    case Est:
        r->o = Nord;
        break;
    case Ouest:
        r->o = Sud;
        break;
    }
}

void tourner_a_droite(Robot *r)
{
    switch (r->o)
    {
    case Nord:
        r->o = Est;
        break;
    case Sud:
        r->o = Ouest;
        break;
    case Est:
        r->o = Sud;
        break;
    case Ouest:
        r->o = Nord;
        break;
    }
}

void position(Robot *r, int *x, int *y)
{
    *x = r->x;
    *y = r->y;
}

int abscisse(Robot *r)
{
    return r->x;
}

int ordonnee(Robot *r)
{
    return r->y;
}

Orientation orient(Robot *r)
{
    return r->o;
}

void position_devant(Robot *r, int *x, int *y)
{
    switch (r->o)
    {
    case Nord:
        *x = r->x;
        *y = r->y - 1;
        break;
    case Sud:
        *x = r->x;
        *y = r->y + 1;
        break;
    case Est:
        *x = r->x + 1;
        *y = r->y;
        break;
    case Ouest:
        *x = r->x - 1;
        *y = r->y;
        break;
    }
}
