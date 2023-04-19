CREATE TABLE IF NOT EXISTS Types (
    nom_type VARCHAR(10) NOT NULL,
    prix_type INTEGER NOT NULL,
    rejet_max_type INTEGER NOT NULL,
    CONSTRAINT pk_types PRIMARY KEY (nom_type),
    CONSTRAINT prix_typ_pos CHECK (prix_type > 0),
    CONSTRAINT rejet_typ_pos CHECK (rejet_max_type >= 0)
);

CREATE TABLE IF NOT EXISTS Usines (
    numero_usine INTEGER NOT NULL,
    nom_usine TEXT NOT NULL,
    emplacement_usine TEXT NOT NULL,
    nom_type TEXT NOT NULL,
    CONSTRAINT pk_usines PRIMARY KEY (numero_usine),
    CONSTRAINT num_usi_pos CHECK (numero_usine > 0) FOREIGN KEY (nom_type) REFERENCES TYPES(nom_type)
);

CREATE TABLE IF NOT EXISTS Commandes (
    numero_commande INTEGER NOT NULL,
    quantite_commande INTEGER NOT NULL,
    livraison_commande TEXT,
    numero_usine INTEGER,
    CONSTRAINT pk_commandes PRIMARY KEY (numero_commande),
    CONSTRAINT num_cmd_pos CHECK (numero_commande > 0),
    CONSTRAINT quant_cmd_pos CHECK (quantite_commande > 0),
    CONSTRAINT fk_num_usine FOREIGN KEY (numero_usine) REFERENCES Usines(numero_usine)
);

CREATE TABLE IF NOT EXISTS Clients (
    numero_client INTEGER NOT NULL,
    nom_client TEXT NOT NULL,
    prenom_client TEXT NOT NULL,
    societe_client TEXT NOT NULL,
    CONSTRAINT pk_clients PRIMARY KEY (numero_client),
    CONSTRAINT num_cli_pos CHECK (numero_client > 0)
);

CREATE TABLE IF NOT EXISTS Transporteurs (
    duns_transporteur INTEGER NOT NULL,
    nom_transporteur TEXT NOT NULL,
    CONSTRAINT pk_transporteurs PRIMARY KEY (duns_transporteur),
    CONSTRAINT duns_transporteur_pos CHECK (duns_transporteur > 0),
    CONSTRAINT duns_max CHECK (duns_transporteur < 1000000000)
);

CREATE TABLE IF NOT EXISTS Navires (
    imo_navire INTEGER NOT NULL,
    capacite_navire INTEGER NOT NULL,
    duns_transporteur INTEGER NOT NULL,
    numero_commande INTEGER NOT NULL,
    CONSTRAINT pk_navires PRIMARY KEY (imo_navire),
    CONSTRAINT imo_nav_pos CHECK (imo_navire > 0),
    CONSTRAINT imo_max CHECK (imo_navire < 10000000),
    CONSTRAINT cap_nav_pos CHECK (capacite_navire > 0),
    CONSTRAINT fk_duns FOREIGN KEY (duns_transporteur) REFERENCES Transporteurs(duns_transporteur),
    CONSTRAINT fk_num_cmd FOREIGN KEY (numero_commande) REFERENCES Commandes(numero_commande),
    CONSTRAINT num_cmd UNIQUE (numero_commande)
);

CREATE TABLE IF NOT EXISTS CommandesClients (
    numero_client INTEGER NOT NULL,
    numero_commande INTEGER NOT NULL,
    date_commande_client TEXT NOT NULL,
    CONSTRAINT pk_commandes_clients PRIMARY KEY (numero_client, numero_commande),
    CONSTRAINT fk_num_cli FOREIGN KEY (numero_client) REFERENCES Clients(numero_client),
    CONSTRAINT fk_num_cmd FOREIGN KEY (numero_commande) REFERENCES Commandes(numero_commande)
);
