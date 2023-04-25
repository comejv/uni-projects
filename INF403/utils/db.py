import sqlite3
from utils import fmt


def create_connexion(db_file):
    """Crée une connexion a la base de données SQLite spécifiée par db_file

    Args:
        db_file (str): Chemin d'accès à la base de données
    """

    try:
        conn = sqlite3.connect(db_file)
        # On active les foreign keys
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except sqlite3.Error as e:
        print(e)


def init_db(use_test_data=None):
    """Initialise la base de données. Si `use_test_data` est `True`, ajoute
    des données de test. Si `use_test_data` est `None`, demande à l'utilisateur.

    Args:
        use_test_data (bool | None, optional): Ajouter des données de test. Par défaut, None.

    Returns:
        sqlite3.Connection: Connexion à la base de données
    """
    # Nom de la BD à créer
    db_file = "data/hydrogen.db"

    # Créer une connexion a la BD
    conn = create_connexion(db_file)

    # Créer les tables et ajouter les types par défaut
    fmt.pitalic("Initialisation de la DB...")
    exec_script(conn, "data/init_tables.sql")
    exec_script(conn, "data/default_types.sql")

    if use_test_data is None:
        use_test_data = fmt.bool_input(
            "Voulez-vous ajouter des données de test ? (O/N) ")

    if use_test_data is True:
        # Ajouter des données de test
        exec_script(conn, "data/default_inserts.sql")

    return conn


def exec_script(conn: sqlite3.Connection, file: str):
    """Exécute sur la base de données toutes les commandes contenues dans le
    fichier fourni en argument.

    Les commandes dans le fichier `file` doivent être séparées par un
    point-virgule.

    Args:
        conn (sqlite3.Connection): Connexion à la base de données
        file (str): Chemin d'accès au fichier contenant les commandes
    """

    # Lecture du fichier et placement des requêtes dans un tableau
    sqlQueries = []

    with open(file, 'r') as f:
        createSql = f.read()
        sqlQueries = createSql.split(";")

    # Exécution de toutes les requêtes du tableau
    cursor = conn.cursor()
    for query in sqlQueries:
        cursor.execute(query)

    # Validation des modifications
    conn.commit()


def exec_query(conn: sqlite3.Connection, query: str, args: tuple = None) -> sqlite3.Cursor:
    """Exécute la requête `query` sur la base de données. Ne commit pas,
    empèche de modifier la base de données.

    Args:
        conn (sqlite3.Connection): Connexion à la base de données
        query (str): Requête à exécuter
        args (tuple, optional): Arguments de la requête. Par défaut, None.
    """

    cursor = conn.cursor()
    if args is None:
        cursor.execute(query)
    else:
        cursor.execute(query, args)

    return cursor


def drop_table(conn: sqlite3.Connection, table: str):
    """Supprime la table `table` de la base de données.

    Args:
        conn (sqlite3.Connection): Connexion à la base de données
        table (str): Nom de la table à supprimer
    """

    cursor = conn.cursor()
    cursor.execute("DROP TABLE ?1", (table,))
    conn.commit()


def drop_all_tables(conn: sqlite3.Connection):
    """Supprime toutes les tables de la base de données.

    Args:
        conn (sqlite3.Connection): Connexion à la base de données
    """

    fmt.pitalic("Suppression des tables...")

    tables = ["CommandesClients", "Navires", "Transporteurs",
              "Clients", "Commandes", "Usines", "Types"]

    cursor = conn.cursor()

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    conn.commit()


def insert_data(conn: sqlite3.Connection, table: str, data: list):
    """Insère les données `data` dans la table `table` dans la base de données.

    Args:
        conn (sqlite3.Connection): Connexion à la base de données
        table (str): Nom de la table à insérer
        data (dict): Données à insérer
    """

    cursor = conn.cursor()
    q_mark_str = ["?"] * len(data)
    q_mark_str = ", ".join(q_mark_str)
    cursor.execute(
        f"INSERT INTO {table} VALUES ({q_mark_str})", tuple(data)
    )

    # Validation des modifications
    print("Insertion réussie de "

    conn.commit()
