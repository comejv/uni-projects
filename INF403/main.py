from utils import db, fmt
from nav import main_menu


if __name__ == "__main__":
    fmt.clear()
    fmt.pbold("Bienvenu dans HydroGen !")
    print("Hydrogen est un gestionnaire de base de données pour un fournisseur d'hydrogène.")

    conn = db.init_db(use_test_data=fmt.binput(
        "Voulez-vous ajouter des données de test ? (O/N) "))

    try:
        while main_menu(conn):
            pass
    except KeyboardInterrupt:
        print("\nAu revoir !")

    conn.close()
