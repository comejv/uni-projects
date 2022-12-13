#ifndef _PROGRAMME_H_
#define _PROGRAMME_H_

/* Taille maximum d'un programme */
#define PROG_TAILLE_MAX 10000

/* Programmes pour le robot Curiosity */

/* Types de commandes */
typedef enum {
  Avancer,   /* A */
  Gauche,    /* G */
  Droite,    /* D */
  Mesure,    /* M */
  Marque,    /* P */
  DebutBloc, /* { */
  FinBloc,   /* } */
  EmpilerNb, /* -?[0-9]+ */
  ExecBloc,  /* ! */
  CondExec,  /* ? */
  Echange,   /* X */
  Mult,      /* * */
  Add,       /* + */
  Div,       /* / */
  Sub,       /* - */
  Rotation,  /* R */
  Clone,     /* C */
  Boucle,    /* B */
  Ignore,    /* I */
} Type_Commande;

/* Commande */
typedef struct {
  Type_Commande cmd;
  int aux; /* Valeur auxiliaire */
} Commande;

/* Programme : séquence de commandes */
typedef struct {
  Commande tab[PROG_TAILLE_MAX];
  int lg;
} Programme;

/* Erreurs de lecture d'un programme */
typedef enum {
  OK_PROGRAMME,
  ERREUR_FICHIER_PROGRAMME,
  ERREUR_BLOC_NON_FERME,
  ERREUR_FERMETURE_BLOC_EXCEDENTAIRE,
  ERREUR_COMMANDE_INCORRECTE
} type_erreur_programme;

typedef struct {
  type_erreur_programme type_err;
  char *ligne;                /* Ligne du programme contenant l'erreur */
  int num_ligne, num_colonne; /* Position de l'erreur dans le fichier */
} erreur_programme;

/* Lecture d'un programme prog dans le fichier nom_fichier */
erreur_programme lire_programme(Programme *prog, char *nom_fichier);

#endif
