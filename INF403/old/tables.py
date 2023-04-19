import sqlite3


def init_tables(cur: sqlite3.Cursor):

    # Types (nom_type, prix_type, rejet_max_type)
    cur.execute('''CREATE TABLE IF NOT EXISTS Types
                    (nom_type VARCHAR(10) NOT NULL PRIMARY KEY,
                    prix_type INTEGER NOT NULL,
                    rejet_max_type INTEGER NOT NULL,
                    CONSTRAINT prix_typ_pos CHECK (prix_type > 0),
                    CONSTRAINT rejet_typ_pos CHECK (rejet_max_type >= 0))''')

    # Usines (numero_usine, nom_usine, emplacement_usine, nom_type)
    cur.execute('''CREATE TABLE IF NOT EXISTS Usines
                    (numero_usine INTEGER NOT NULL PRIMARY KEY,
                    nom_usine TEXT NOT NULL,
                    emplacement_usine TEXT NOT NULL,
                    nom_type TEXT NOT NULL,
                    CONSTRAINT num_usi_pos CHECK (numero_usine > 0)
                    FOREIGN KEY (nom_type) REFERENCES Types(nom_type))''')

    # Commandes (numero_commande, quantite_commande, livraison_commande, numero_usine)
    # pas de not null sur livraison_commande car on ne sait pas encore la date de livraison
    # pas de not null sur numero_usine car on ne sait pas encore l'usine
    cur.execute('''CREATE TABLE IF NOT EXISTS Commandes
                    (numero_commande INTEGER NOT NULL PRIMARY KEY,
                    quantite_commande INTEGER NOT NULL,
                    livraison_commande TEXT,
                    numero_usine INTEGER,
                    CONSTRAINT num_cmd_pos CHECK (numero_commande > 0),
                    CONSTRAINT quant_cmd_pos CHECK (quantite_commande > 0),
                    FOREIGN KEY (numero_usine) REFERENCES Usines(numero_usine))''')

    # Clients (numero_client, nom_client, prenom_client, societe_client)
    cur.execute('''CREATE TABLE IF NOT EXISTS Clients
                    (numero_client INTEGER NOT NULL PRIMARY KEY,
                    nom_client TEXT NOT NULL,
                    prenom_client TEXT NOT NULL,
                    societe_client TEXT NOT NULL,
                    CONSTRAINT num_cli_pos CHECK (numero_client > 0))''')

    # Transporteurs (duns_transporteur, nom_transporteur)
    cur.execute('''CREATE TABLE IF NOT EXISTS Transporteurs
                    (duns_transporteur INTEGER NOT NULL PRIMARY KEY,
                    nom_transporteur TEXT NOT NULL,
                    CONSTRAINT duns_transporteur_pos CHECK (duns_transporteur > 0),
                    CONSTRAINT duns_max CHECK (duns_transporteur < 1000000000))''')

    # Navires (imo_navire, capacité_navire, duns_transporteur, numero_commande)
    cur.execute('''CREATE TABLE IF NOT EXISTS Navires
                    (imo_navire INTEGER NOT NULL PRIMARY KEY,
                    capacite_navire INTEGER NOT NULL,
                    duns_transporteur INTEGER NOT NULL,
                    numero_commande INTEGER NOT NULL,
                    CONSTRAINT imo_nav_pos CHECK (imo_navire > 0),
                    CONSTRAINT imo_max CHECK (imo_navire < 10000000),
                    CONSTRAINT cap_nav_pos CHECK (capacite_navire > 0),
                    FOREIGN KEY (duns_transporteur) REFERENCES Transporteurs(duns_transporteur),
                    FOREIGN KEY (numero_commande) REFERENCES Commandes(numero_commande))''')

    # CommandesClients (numero_client, numero_commande, date_commande_client)
    cur.execute('''CREATE TABLE IF NOT EXISTS CommandesClients
                    (numero_client INTEGER NOT NULL,
                    numero_commande INTEGER NOT NULL,
                    date_commande_client TEXT NOT NULL,
                    FOREIGN KEY (numero_client) REFERENCES Clients(numero_client),
                    FOREIGN KEY (numero_commande) REFERENCES Commandes(numero_commande))''')

    # INDEXES
    cur.execute(
        'CREATE INDEX IF NOT EXISTS num_cmd_idx ON Commandes(numero_commande)')
    cur.execute(
        'CREATE INDEX IF NOT EXISTS num_cli_idx ON Clients(numero_client)')
    cur.execute('CREATE INDEX IF NOT EXISTS num_usi_idx ON Usines(numero_usine)')
    cur.execute('CREATE INDEX IF NOT EXISTS imo_nav_idx ON Navires(imo_navire)')
    cur.execute(
        'CREATE INDEX IF NOT EXISTS duns_trans_idx ON Transporteurs(duns_transporteur)')
    cur.execute(
        'CREATE INDEX IF NOT EXISTS num_cmd_cli_idx ON CommandesClients(numero_commande)')

    # TYPES
    types = [('gris', 2, 10), ('bleu', 6, 1), ('vert', 10, 0)]
    cur.executemany('INSERT OR IGNORE INTO Types VALUES (?, ?, ?)', types)

    # Commit
    cur.connection.commit()
