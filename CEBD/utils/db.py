import sqlite3
from sqlite3 import IntegrityError
import pandas

# Pointeur sur la base de données
data = sqlite3.connect("data/climat_france.db")
data.execute("PRAGMA foreign_keys = 1")


# Fonction permettant d'exécuter toutes les requêtes sql d'un fichier
# Elles doivent être séparées par un point-virgule
def updateDBfile(data: sqlite3.Connection, file):
    # Lecture du fichier et placement des requêtes dans un tableau
    createFile = open(file, "r")
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Exécution de toutes les requêtes du tableau
    cursor = data.cursor()
    for query in sqlQueries:
        cursor.execute(query)


# Action en cas de clic sur le bouton de création de base de données
def createDB():
    try:
        # On exécute les requêtes du fichier de création
        updateDBfile(data, "data/createDB.sql")
    except Exception as e:
        print(
            "L'erreur suivante s'est produite lors de la création de la base : "
            + repr(e)
            + "."
        )
    else:
        data.commit()
        print("Base de données créée avec succès.")


# En cas de clic sur le bouton d'insertion de données
# TODO Q4 Modifier la fonction insertDB pour insérer les données dans les nouvelles tables
def insertDB():
    try:
        # '{}' : paramètre de la requête qui doit être interprété comme une chaine de caractères dans l'insert
        # {}   : paramètre de la requête qui doit être interprété comme un nombre dans l'insert
        # la liste de noms en 3e argument de read_csv_file correspond aux noms des colonnes dans le CSV
        # ATTENTION : les attributs dans la BD sont généralement différents des noms de colonnes dans le CSV
        # Exemple : date_mesure dans la BD et date_obs dans le CSV

        # Insertion des régions
        # On ajoute les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv",
            ";",
            "insert into Regions values (?,?)",
            ["Code Région", "Région"],
        )

        # On ajoute les nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv",
            ";",
            "insert into Regions values (?,?)",
            ["Nouveau Code", "Nom Officiel Région Majuscule"],
        )

        # On ajoute les départements référencés avec les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv",
            ";",
            "insert into Departements (code_departement, nom_departement, code_region) values (?, ?, ?)",
            ["Code Département", "Département", "Code Région"],
        )

        # On renseigne la zone climatique des départements
        read_csv_file(
            "data/csv/ZonesClimatiques.csv",
            ";",
            "update Departements set zone_climatique_departement = ? where code_departement = ?",
            ["zone_climatique", "code_departement"],
        )

        # On modifie les codes région des départements pour les codes des nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv",
            ";",
            "update Departements set code_region = ? where code_region = ?",
            ["Nouveau Code", "Anciens Code"],
        )

        # On supprime les anciennes régions, sauf si l'ancien code et le nouveau sont identiques (pour ne pas perdre les régions qui n'ont pas changé de code)
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv",
            ";",
            "delete from Regions where code_region = ? and ? <> ?",
            ["Anciens Code", "Anciens Code", "Nouveau Code"],
        )
        
        print(
            "Les erreurs UNIQUE constraint sont normales car on insère une seule fois les Regions et les Départemments"
        )
        print("Insertion de mesures en cours...cela peut prendre un peu de temps")
        # On ajoute les mesures
        read_csv_file(
            "data/csv/Mesures.csv",
            ";",
            "insert into Mesures (code_departement, date_mesure, temperature_min_mesure, temperature_max_mesure, temperature_moy_mesure) values (?, ?, ?, ?, ?)",
            ["code_insee_departement", "date_obs", "tmin", "tmax", "tmoy"],
        )

        # Insertion des communes
        read_csv_file(
            "data/csv/Communes.csv",
            ";",
            "insert into Communes (nom_commune, code_departement, arrondissement_commune, canton_commune, population_commune, superficie_commune, altitude_moy_commune) values (?, ?, ?, ?, ?, ?, ?)",
            [
                "Commune",
                "Code Département",
                "Code Arrondissement",
                "Code Canton",
                "Population",
                "Superficie",
                "Altitude Moyenne",
            ],
        )

    except Exception as e:
        print(
            "L'erreur suivante s'est produite lors de l'insertion des données : "
            + repr(e)
            + "."
        )
    else:
        data.commit()
        print("Un jeu de test a été inséré dans la base avec succès.")


# En cas de clic sur le bouton de suppression de la base
def deleteDB():
    try:
        updateDBfile(data, "data/deleteDB.sql")
    except Exception as e:
        print(
            "L'erreur suivante s'est produite lors de la destruction de la base : "
            + repr(e)
            + "."
        )
    else:
        data.commit()
        print("La base de données a été supprimée avec succès.")


def read_csv_file(csvFile, separator, query, columns):
    # Lecture du fichier CSV csvFile avec le séparateur separator
    # pour chaque ligne, exécution de query en la formatant avec les colonnes columns
    df = pandas.read_csv(csvFile, sep=separator)
    df = df.where(pandas.notnull(df), None)
    cursor = data.cursor()
    for ix, row in df.iterrows():
        try:
            tab = []
            for i in range(len(columns)):
                # pour échapper les noms avec des apostrophes, on remplace dans les chaines les ' par ''
                if isinstance(row[columns[i]], str):
                    row[columns[i]] = row[columns[i]].replace("'", "''")
                tab.append(row[columns[i]])
            # Utilisation de tuple pour utiliser la méthode d'insertion VALUE (?, ?, ...,?)
            # print(query, tab)
            cursor.execute(query, tuple(tab))
        except IntegrityError as err:
            print(query, tab)
            print(err)
