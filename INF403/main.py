from utils import db, fmt
from nav import main_menu


if __name__ == "__main__":
    fmt.clear()
    fmt.pbold("Bienvenu dans HydroGen !")
    print("Hydrogen est un gestionnaire de base de données pour un fournisseur d'hydrogène.")

    conn = db.init_db()

    try:
        while main_menu(conn):
            pass
    except KeyboardInterrupt:
        conn.close()
        fmt.clear()
        print("Au revoir !")

    conn.close()
