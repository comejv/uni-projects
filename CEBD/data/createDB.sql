CREATE TABLE Regions (
    code_region INTEGER,
    nom_region TEXT,
    CONSTRAINT pk_regions PRIMARY KEY (code_region)
);

CREATE TABLE Departements (
    code_insee_departement TEXT,
    nom_departement TEXT,
    code_departement TEXT,
    code_region INTEGER,
    zone_climatique_departement TEXT,
    CONSTRAINT pk_departements PRIMARY KEY (code_insee_departement),
    CONSTRAINT fk_region FOREIGN KEY (code_region) REFERENCES Regions(code_region)
);

CREATE TABLE Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    CONSTRAINT pk_mesures PRIMARY KEY (code_departement, date_mesure),
    CONSTRAINT fk_mesures FOREIGN KEY (code_departement) REFERENCES Departements(code_departement)
);

CREATE TABLE Communes (
    nom_commune TEXT,
    code_departement TEXT,
    arrondissement_commune INTEGER,
    canton_commune INTEGER,
    population_commune INTEGER,
    superficie_commune INTEGER,
    altitude_moy_commune INTEGER,
    CONSTRAINT pk_communes PRIMARY KEY (nom_commune, code_departement),
    CONSTRAINT fk_communes FOREIGN KEY (code_departement) REFERENCES Departements(code_departement)
);

CREATE TABLE Travaux (
    numero_travaux INTEGER,
    code_departement TEXT,
    cout_total_ht_travaux FLOAT,
    cout_induit_ht_travaux FLOAT,
    annee_travaux DATE,
    annee_constr_travaux DATE,
    type_logement_travaux TEXT,
    CONSTRAINT pk_travaux PRIMARY KEY (numero_travaux),
    CONSTRAINT fk_travaux FOREIGN KEY (code_departement) REFERENCES Departements(code_departement)
);

CREATE TABLE Isolations (
    numero_travaux INTEGER,
    poste_isolation TEXT,
    isolant_isolation TEXT,
    epaisseur_isolation INTEGER,
    surface_isolation INTEGER,
    CONSTRAINT pk_isolations PRIMARY KEY (numero_travaux),
    CONSTRAINT fk_isolations FOREIGN KEY (numero_travaux) REFERENCES Travaux(numero_travaux)
);

CREATE TABLE Chauffages (
    numero_travaux INTEGER,
    energie_chauffage_avt_chauffage TEXT,
    energie_chauffage_inst_chauffage TEXT,
    generateur_chauffage TEXT,
    type_chaudiere_chauffage TEXT,
    CONSTRAINT pk_chauffages PRIMARY KEY (numero_travaux),
    CONSTRAINT fk_chauffages FOREIGN KEY (numero_travaux) REFERENCES Travaux(numero_travaux)
);

CREATE TABLE Photovoltaiques (
    numero_travaux INTEGER,
    puissance_installee_photovoltaique INTEGER,
    type_panneau_photovoltaique TEXT,
    CONSTRAINT pk_photovoltaiques PRIMARY KEY (numero_travaux),
    CONSTRAINT fk_photovoltaiques FOREIGN KEY (numero_travaux) REFERENCES Travaux(numero_travaux)
);