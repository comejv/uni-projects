from utils import db, fmt
from sqlite3 import Connection, OperationalError


def main_menu(conn: Connection) -> bool:
    """Affiche le menu principal.

    Args:
        conn (Connection): Connexion à la base de données

    Returns:
        bool: `True` si l'utilisateur souhaite continuer, `False` pour quitter le programme
    """
    fmt.clear()
    fmt.pbold("Menu principal")
    print("1. Parcourir les données")
    print("2. Insérer ou supprimer des données")
    print("3. Requêtes avancées")
    print("4. Requêtes manuelle")
    print("5. Quitter", end="\n\n")

    choice = input("Choix : ")

    while int(choice) < 1 or int(choice) > 5:
        print("\x1b[1F\x1b[K", end="")
        choice = input("Choix : ")

    if choice == "1":
        while browse(conn):
            pass
        return True
    elif choice == "2":
        while insert_delete(conn):
            pass
        return True
    elif choice == "3":
        return True
    elif choice == "4":
        while manual_query(conn):
            pass
        return True
    elif choice == "5":
        return False


def browse(conn: Connection) -> bool:
    """Affiche le menu de parcours des données.

    Args:
        conn (Connection): Connexion à la base de données

    Returns:
        bool: `True` si l'utilisateur souhaite continuer, `False` pour revenir au menu principal
    """
    fmt.clear()
    fmt.pbold("Parcourir les données")
    print("1. Clients")
    print("2. Commandes")
    print("3. Usines")
    print("4. Transporteurs")
    print("5. Navires")
    print("6. Types d'hydrogène")
    print("7. Retour au menu principal", end="\n\n")

    try:
        choice = int(input("Choix : "))
        while int(choice) < 1 or int(choice) > 7:
            print("\x1b[1F\x1b[K", end="")
            choice = input("Choix : ")

    except KeyboardInterrupt:
        return False
    if choice == 1:
        return browse_filter(conn, table="Clients", prompt_filters=True)
    elif choice == 2:
        return browse_filter(conn, table="Commandes", prompt_filters=True)
    elif choice == 3:
        return browse_filter(conn, table="Usines", prompt_filters=True)
    elif choice == 4:
        return browse_filter(conn, table="Transporteurs", prompt_filters=True)
    elif choice == 5:
        return browse_filter(conn, table="Navires", prompt_filters=True)
    elif choice == 6:
        return browse_filter(conn, table="Types", prompt_filters=True)
    elif choice == 7:
        return False


def get_filters(conn: Connection, table: str) -> dict[str: str]:
    """Demande à l'utilisateur les filtres qu'il souhaite appliquer à la table `table`.

    Args:
        conn (Connection): Connexion à la base de données
        table (str): Nom de la table

    Returns:
        dict | None: Dictionnaire contenant les filtres {"attribut": "valeur_souhaitée"}
    """
    fmt.clear()
    fmt.pbold(table)
    filters = {}
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table}")
    except OperationalError:
        fmt.perror("La table n'existe pas !")
        return None

    headers = [desc[0] for desc in cursor.description]
    values = fmt.form_input(headers)

    if values is None:
        return None

    for h, v in zip(headers, values):
        if v != "":
            filters[h] = v

    return filters if len(filters) > 0 else None


def browse_filter(conn: Connection, table: str,
                  filters: dict = None, prompt_filters: bool = False) -> bool:
    """Affiche les données de la table `table` filtrées par `filters`.
    Attention : laisser l'utilisateur choisir le paramètre table rends la fonction
    vulnérable à une injection SQL.

    Args:
        conn (Connection): Connexion à la base de données
        table (str): Nom de la table

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
            False sinon.
    """
    if filters is None:
        filters = {}

    fmt.clear()
    fmt.pbold(table)
    cursor = conn.cursor()

    if prompt_filters is True:
        new_filters = get_filters(conn, table)
        if new_filters is not None:
            filters.update(new_filters)

    # Construction et exécution de la requête
    if not filters:
        cursor.execute(f"SELECT * FROM {table}")
    else:
        args = []
        for i, key in enumerate(filters.keys()):
            if filters[key] is not None:
                first_char = filters[key][0]
                if first_char in ['<', '>']:
                    args.append(f"{key} {first_char} ?{i + 1}")
                    filters[key] = filters[key][1:]
                else:
                    args.append(f"{key} = ?{i + 1}")
        args = " AND ".join(args)

        # Attention, cette requête est possiblement un point
        # d'attaque par injection sql (à cause de `table`).
        cursor.execute(
            f"SELECT * FROM {table} WHERE {args}", tuple(filters.values()))

    # Affichage des données
    headers = [desc[0] for desc in cursor.description]
    fmt.clear()
    fmt.print_table(cursor.fetchall(), headers)

    # Attente de l'utilisateur
    fmt.pblink("Appuyez sur Entrée pour continuer...", end="")
    try:
        input()
    except KeyboardInterrupt:
        return False

    return True


def insert_delete(conn: Connection) -> bool:
    """Affiche le menu d'insertion et de délétions.

    Args:
        conn (Connection): Connexion à la database.

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
            False sinon.
    """
    fmt.clear()
    fmt.pbold("Insertion ou supression des données")
    print("1. Clients")
    print("2. Commandes")
    print("3. Usines")
    print("4. Transporteurs")
    print("5. Types d'hydrogène")
    print("6. Réinitialiser la base de données (irréversible)")
    print("7. Retour au menu principal", end="\n\n")

    choice = int(input("Choix : "))
    while int(choice) < 1 or int(choice) > 7:
        print("\x1b[1F\x1b[K", end="")
        choice = input("Choix : ")

    if choice == 1:
        pass
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        pass
    elif choice == 6:
        fmt.clear()
        fmt.pbold("Réinitialisation de la base de données.")
        fmt.perror("Cette action est irréversible !")
        if fmt.bool_input("Êtes-vous sûr de vouloir continuer ? (O/N) "):
            db.drop_all_tables(conn)
            fmt.pitalic("Réinitialisation de la base de données...")
            db.init_db()
        print("Retour au menu principal.")
        return False
    elif choice == 7:
        return False


def manual_query(conn: Connection) -> bool:
    """Exécute une requête entrée manuellement par l'utilisateur.

    Args:
        conn (Connection): Connexion à la base de données

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
            False sinon.
    """
    fmt.clear()
    fmt.pbold("Requêtes manuelle")
    requete = input("Requête : ")
    try:
        res = db.exec_query(conn, requete)
        headers = [desc[0] for desc in res.description]
        fmt.print_table(res.fetchall(), headers)
    except OperationalError as e:
        fmt.perror(e)
        fmt.pblink("Appuyez sur Entrée pour continuer...")
        input()

    return fmt.bool_input("Voulez-vous faire une autre requête ? (O/N) ")
