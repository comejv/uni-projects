# HydroGen
> Gestionnaire de base de données créé pour un fournisseur fictif d'hydrogène.

## Installation
Pour installer notre projet il suffit de cloner le dépôt, nous ne nous appuyons que sur une bibliothèque de base de python, Sqlite3. Assurez vous de conserver l'architecture des dossiers telle qu'elle est.

# Usage
Pour lancer le gestionnaire il suffit d'exécuter le script `main.py` avec un interpréteur python >=3.9 :
```bash
python3 main.py
```

Au démarrage il vous faudra choisir si vous voulez insérer les valeurs par défaut ou non (clients et commandes fictives, etc). Nous conseillons de les insérer au premier lancement, pour pouvoir tester toutes les fonctionnalités de notre programme.

Une fois arrivé sur le menu principal nous proposons 5 fonctionnalité principales :
1. Parcourir les données : menu qui vous permettra d'avoir accès aux tables en lecture uniquement. Vous pouvez appliquer des filtres à la seléction. Pour voir la table complète laissez les vide (appuyez sur entrée jusqu'à voir la table). Les filtres prennent en compte les valeurs uniques mais comprennent aussi les opérateurs > et < devant un nombre.
2. Insérer ou supprimer des données : ce menu vous donne accès à un sous menu pour chaque table. Vous pouvez ajouter des valeurs (remplir tous les filtres), les mettre à jour (premier menu équivalent pour seléctionner les lignes à mettre à jour, deuxième pour les valeurs à insérer à leur place) ou supprimer des lignes selon les filtres que vous choisissez.
3. Commander : vous demandera de remplir toutes les informations nécessaires à l'ajout d'une nouvelle commande : choix du client, du transporteur, de la quantité, etc.
4. Requêtes avancées : des requêtes préconstruites qui vous permettront de mettre en relation différente tables.
5. Requêtes manuelles : pour exécuter une requête que vous écrivez vous même.

> NB: pour un affichage correct des tables nous conseillons une largeur de terminal d'au minimum 170 colonnes.