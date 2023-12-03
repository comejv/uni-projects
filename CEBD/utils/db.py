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
            "data/csv/MesuresSmall.csv",
            ";",
            "insert into Mesures (code_departement, date_mesure, temperature_min_mesure, temperature_max_mesure, temperature_moy_mesure) values (?, ?, ?, ?, ?)",
            ["code_insee_departement", "date_obs", "tmin", "tmax", "tmoy"],
        )

        # Insertion des communes
        print("Insertion des communes...")
        read_csv_file(
            "data/csv/Communes.csv",
            ";",
            "insert into Communes (code_commune, nom_commune, code_departement, arrondissement_commune, canton_commune, population_commune, superficie_commune, altitude_moy_commune) values (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                "Code Commune",
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
        print("Insertion de Région, Département, Mesure et Commune réussie.")

    # Insertion des travaux isolation
    print("Insertion des Isolations")
    df = pandas.read_csv("data/csv/Isolation.csv", sep=";")
    query_travaux = "INSERT INTO Travaux (numero_travaux, code_departement, cout_total_ht_travaux, cout_induit_ht_travaux, annee_travaux, annee_constr_travaux, type_logement_travaux) VALUES (?, ?, ?, ?, ?, ?, ?)"
    query_isolation = "INSERT INTO Isolations (numero_travaux, poste_isolation, isolant_isolation, epaisseur_isolation, surface_isolation) VALUES (?, ?, ?, ?, ?)"
    idx = 0
    for _, row in df.iterrows():
        att_travaux = [
            row["code_departement"],
            row["cout_total_ht"],
            row["cout_induit_ht"],
            row["annee_travaux"],
            row["annee_construction"],
            row["type_logement"],
        ]
        att_isolation = [
            row["poste_isolation"],
            row["isolant"],
            row["epaisseur"],
            row["surface"],
        ]
        try:
            cursor = data.cursor()
            cursor.execute(query_travaux, tuple([idx] + att_travaux))
            cursor.execute(query_isolation, tuple([idx] + att_isolation))
        except IntegrityError as err:
            data.rollback()
            print("Insertion fail with values ", att_travaux + att_isolation, " : ", err)
        else:
            idx += 1
            data.commit()
    print("Insertion des Isolations réussie.")

    # Insertion des travaux chauffage
    print("Insertion des Chauffages...")
    df = pandas.read_csv("data/csv/Chauffage.csv", sep=";")
    query_chauffage = "INSERT INTO Chauffages (numero_travaux, energie_chauffage_avt_chauffage, energie_chauffage_inst_chauffage, generateur_chauffage, type_chaudiere_chauffage) VALUES (?, ?, ?, ?, ?)"
    for _, row in df.iterrows():
        att_travaux = [
            row["code_departement"],
            row["cout_total_ht"],
            row["cout_induit_ht"],
            row["annee_travaux"],
            row["annee_construction"],
            row["type_logement"],
        ]
        att_chauffage = [
            row["energie_chauffage_avt_travaux"],
            row["energie_chauffage_installee"],
            row["generateur"],
            row["type_chaudiere"],
        ]
        try:
            cursor = data.cursor()
            cursor.execute(query_travaux, tuple([idx] + att_travaux))
            cursor.execute(query_chauffage, tuple([idx] + att_chauffage))
        except IntegrityError as err:
            data.rollback()
            print("Insertion fail with values ", att_travaux + att_chauffage, " : ", err)
        else:
            idx += 1
            data.commit()
    print("Insertion des Chauffages réussie.")

    # Insertion des travaux photovolataïque
    print("Insertion des Photovoltaique...")
    df = pandas.read_csv("data/csv/Photovoltaique.csv", sep=";")
    query_photovoltaique = "INSERT INTO Photovoltaiques (numero_travaux, puissance_installee_photovoltaique, type_panneau_photovoltaique) VALUES (?, ?, ?)"
    for _, row in df.iterrows():
        att_travaux = [
            row["code_departement"],
            row["cout_total_ht"],
            row["cout_induit_ht"],
            row["annee_travaux"],
            row["annee_construction"],
            row["type_logement"],
        ]
        att_photovoltaique = [
            row["puissance_installee"],
            row["type_panneaux"],
        ]
        try:
            cursor = data.cursor()
            cursor.execute(query_travaux, tuple([idx] + att_travaux))
            cursor.execute(query_photovoltaique, tuple([idx] + att_photovoltaique))
        except IntegrityError as err:
            data.rollback()
            print(err)
        else:
            idx += 1
            data.commit()
    print("Insertion fail with values ", att_travaux + att_photovoltaique, " : ", err)

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
            # print(err)
            pass
