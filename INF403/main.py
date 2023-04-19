from utils import db, fmt


def main():
    # Nom de la BD à créer
    db_file = "data/hydrogen.db"

    # Créer une connexion a la BD
    conn = db.creer_connexion(db_file)

    # Créer les tables et ajouter les types par défaut
    fmt.pitalic("Initialisation de la DB avec les types par défaut.")
    db.mise_a_jour_bd(conn, "data/init_tables.sql")
    db.mise_a_jour_bd(conn, "data/default_types.sql")


if __name__ == "__main__":
    main()
