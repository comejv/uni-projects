from utils import db, fmt
from sqlite3 import Connection, IntegrityError, OperationalError
import requetes


def create_menu(title: str, choices: list[str]) -> int:
    """Affiche un menu à choix à l'utilisateur.

    Args:
        title (str): Titre du menu
        choix (list[str]): Liste de choix

    Returns:
        int : entier représentant le choix choisie par l'utilisateur
    """

    fmt.clear()
    fmt.pbold(title)
    for i, c in enumerate(choices):
        print("%d. %s" % (i+1, c))
    print(end="\n\n\n")

    while True:

        choice = input("\x1b[1F\x1b[KChoix : ")

        try:
            choice = int(choice)
        except ValueError:
            continue

        if 0 < choice <= len(choices):
            return int(choice)


def main_menu(conn: Connection) -> bool:
    """Affiche le menu principal.

    Args:
        conn (Connection): Connexion à la base de données

    Returns:
        bool: `True` si l'utilisateur souhaite continuer, `False` pour quitter le programme
    """

    choice = create_menu(title="Menu principal",
                         choices=["Parcourir les données",
                                  "Insérer ou supprimer des données", "Requêtes avancées",
                                  "Requêtes manuelle", "Quitter"])

    if choice == 1:
        while browse(conn):
            pass
        return True
    elif choice == 2:
        while menu_choice_insert(conn):
            pass
        return True
    elif choice == 3:
        while combined_request(conn):
            pass
        return True
    elif choice == 4:
        while manual_query(conn):
            pass
        return True
    elif choice == 5:
        return False


def browse(conn: Connection) -> bool:
    """Affiche le menu de parcours des données.

    Args:
        conn (Connection): Connexion à la base de données

    Returns:
        bool: `True` si l'utilisateur souhaite continuer, `False` pour
        revenir au menu principal
    """

    tables = ["Clients", "Commandes", "Usines",
              "Transporteurs", "Navires", "Types d'hydrogène",
              "Retour au menu principal"]

    choice = create_menu(title="Parcourir les données",
                         choices=tables)
    if choice == 7:
        return False

    browse_filter(conn, tables[choice-1], prompt_filters=True)


def get_filters(conn: Connection, table: str, desc: str) -> dict[str: str]:
    """Demande à l'utilisateur les filtres qu'il souhaite appliquer à la table `table`.

    Args:
        conn (Connection): Connexion à la base de données
        table (str): Nom de la table

    Returns:
        dict | None: Dictionnaire contenant les filtres {"attribut": "valeur_souhaitée"}
    """

    fmt.clear()
    fmt.pbold(table)
    print("\n" + desc)
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
        else:
            filters[h] = None

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

    filters_description = "Vous pouvez filtrer les données de la table avec les filtres suivants.\n\
        Il est possible de renseigner des valeurs ou des valeurs plancher/plafond avec > et <.\n\
            Par exemple vous pouvez écrire :\n\
                \t(attribut): > 10\n\
            Pour filtrer les données dont l'attribut est supérieur à 10."

    if prompt_filters is True:
        new_filters = get_filters(conn, table, filters_description)
        if new_filters is not None:
            filters.update(new_filters)

    for k, v in filters.copy().items():
        if v is None:
            del filters[k]

    # Construction et exécution de la requête
    if not filters or len(filters) == 0:
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
                try:
                    filters[key] = int(filters[key])
                except ValueError:
                    pass
        args = " AND ".join(args)

        # Attention, cette requête est possiblement un point
        # d'attaque par injection sql (à cause de `table`).
        cursor.execute(
            f"SELECT * FROM {table} WHERE {args}", tuple(filters.values()))

    # Affichage des données
    db.show_results(cursor)

    return True


def insert(conn: Connection, table: str) -> bool:
    """Insère des données dans la table `table`.

    Args:
        conn (Connection): Connexion à la base de données
        table (str): Nom de la table

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
            False sinon.
    """

    input_data = get_filters(conn, table=table)
    # No value must be None
    while None in input_data.values() or input_data is None:
        fmt.pwarn(
            "Veuillez renseigner tous les attributs.",
            hold=True
        )
        input_data = get_filters(conn, table=table)
    insert_error = db.insert_data(
        conn, table=table, data=input_data)
    if insert_error:
        fmt.perror("Erreur d'insertion : ", insert_error, hold=True)
        return True
    fmt.pitalic("Insertion effectuée !", hold=True)
    return False


def delete(conn: Connection, table: str) -> bool:
    """Supprime des données dans la table `table`.

    Args:
        conn (Connection): Connexion à la base de données
        table (str): Nom de la table

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
            False sinon.
    """

    filters_description = "Veuillez renseigner les attributrs de(s) lignes(s) à supprimer."

    filters = get_filters(conn, table=table, desc=filters_description)
    delete_error = db.delete_data(
        conn, table=table, filters=filters
    )
    if delete_error:
        fmt.perror("Erreur de supression : ", delete_error, hold=True)
        return True
    fmt.pitalic("Suppression effectuée !", hold=True)
    return False


def combined_request(conn: Connection) -> bool:
    """Affiche le menu des requêtes avancées.

    Args:
        conn (Connection): Connexion à la database.

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
            False sinon.
    """

    choice = create_menu(title="Requêtes avancées",
                         choices=["Information client",
                                  "Information nombre de bateau par transporteur",
                                  "Information sur le type d'hydrogène des commandes",
                                  "Information sur le nombre de commandes transportées par transporteur \
                                        selon le type d'hydrogène",
                                  "Retour au menu principale"])

    if choice == 1:
        return requetes.information_client(conn)
    elif choice == 2:
        return requetes.information_navire(conn)
    elif choice == 3:
        return requetes.type_commande(conn)
    elif choice == 4:
        return requetes.information_type_transporteur(conn)
    elif choice == 5:
        return False


def menu_insert_update_delete(conn: Connection, table_name: str) -> bool:
    """Affiche le menu du choix de l'opération de modification de table.

    Args:
        conn (Connection): Connexion à la database.
        table_name (string): Le nom de la table a modifier

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
              False sinon.
    """

    choice = create_menu(f"Que voulez-vous faire dans la table {table_name} ?",
                         ["Insérer des données", "Update des données", "Supprimer des données",
                          "Retour au menu précédent"])
    if table_name == "Commandes":
        table_name = "Commandes_base"
    if choice == 1:
        insert(conn, table_name)
        return False
    elif choice == 2:
        # update(conn, table_name)
        return False
    elif choice == 3:
        delete(conn, table_name)
        return False
    elif choice == 4:
        return False


def menu_choice_insert(conn: Connection) -> bool:
    """Affiche le menu du choix de l'opération de modification de table.

    Args:
        conn (Connection): Connexion à la database.

    Returns:
        bool: True si l'utilisateur souhaite continuer dans le même sous menu,
              False sinon.
    """

    tables = ["Clients", "Commandes", "Usines", "Types", "Navires",
              "Transporteurs", "CommandesClients", "Réinitialiser la base de données",
              "Retourner au menu principale"]

    choice = create_menu("Choisissez la table à modifier :",
                         tables)

    if choice == 8:
        fmt.clear()
        fmt.pbold("Réinitialisation de la base de données.")
        fmt.perror("Cette action est irréversible !")
        if fmt.bool_input("Êtes-vous sûr de vouloir continuer ? (O/N) "):
            db.drop_all_tables(conn)
            db.init_db()
        print("Retour au menu principal.")
        return False
    elif choice == 9:
        return False

    menu_insert_update_delete(conn, table_name=tables[choice - 1])
    return True


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
        # If query is not a select, ignore
        if not res.description:
            fmt.pwarn(
                "Requête invalide ! Seules les requêtes SELECT sont autorisées.")
            return False
        headers = [desc[0] for desc in res.description]
        fmt.print_table(res.fetchall(), headers)
        if res.rowcount == 0:
            fmt.pwarn("Aucune données trouvées !")
    except (OperationalError, IntegrityError) as e:
        fmt.perror(e)
        fmt.pblink("Appuyez sur Entrée pour continuer...")
        input()

    return fmt.bool_input("Voulez-vous faire une autre requête ? (O/N) ")
