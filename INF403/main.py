from utils import db, fmt


def init_db(use_placeholder=False):
    # Nom de la BD à créer
    db_file = "data/hydrogen.db"

    # Créer une connexion a la BD
    conn = db.creer_connexion(db_file)

    # Créer les tables et ajouter les types par défaut
    fmt.pitalic("Initialisation de la DB...")
    db.exec_script(conn, "data/init_tables.sql")
    db.exec_script(conn, "data/default_types.sql")

    if use_placeholder:
        # Ajouter des données de test
        fmt.pitalic("Ajout des données de test...")
        db.exec_script(conn, "data/default_inserts.sql")


def menu():
    fmt.pbold("Menu principal")
    print("1. Parcourir les données")
    print("2. Insérer ou supprimer des données")
    print("3. Requêtes avancées")
    print("4. Quitter", end="\n\n")

    choice = input("Choix: ")

    while choice not in ["1", "2", "3", "4"]:
        print("\x1b[1F\x1b[K", end="")
        choice = input("Choix: ")

    if choice == "1":
        pass
    if choice == "2":
        insert_delete()
    if choice == "3":
        pass
    if choice == "4":
        exit()


def insert_delete():
    print("1. Gestion des clients")
    print("2. Gestion des commandes")
    print("3. Gestion des usines")
    print("4. Gestion des transporteurs")
    print("5. Gestion des types d'hydrogène")


if __name__ == "__main__":
    fmt.pbold("Bienvenu dans Hydrogen !")
    print("Hydrogen est un gestionnaire de base de données pour un fournisseur d'hydrogène.")

    init_db(use_placeholder=fmt.binput(
        "Voulez-vous ajouter des données de test ? (O/N) "))
