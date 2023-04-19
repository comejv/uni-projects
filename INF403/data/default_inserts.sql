-- Usines
INSERT OR IGNORE INTO Usines VALUES (1, "Butagaz", "Saint-Étienne", "gris");
INSERT OR IGNORE INTO Usines VALUES (2, "Blue and me", "Lyon", "bleu");
INSERT OR IGNORE INTO Usines VALUES (3, "You're a good guy", "Paris", "vert");
INSERT OR IGNORE INTO Usines VALUES (4, "Petroleum gaz", "Marseille", "gris");
INSERT OR IGNORE INTO Usines VALUES (5, "Airgaz", "Toulouse", "bleu");
INSERT OR IGNORE INTO Usines VALUES (6, "O2 Industries", "Bordeaux", "vert");
INSERT OR IGNORE INTO Usines VALUES (7, "Bienvenue chez les gris", "Lille", "gris");
INSERT OR IGNORE INTO Usines VALUES (8, "Kill all humans", "Lille", "gris");
INSERT OR IGNORE INTO Usines VALUES (9, "Kill our Planet", "Dubai", "gris");
INSERT OR IGNORE INTO Usines VALUES (10, "Money eq Power", "Petrograd", "gris");
INSERT OR IGNORE INTO Usines VALUES (11, "Vegaz", "Sofia", "gris");
INSERT OR IGNORE INTO Usines VALUES (12, "Beauvais", "Beauvais", "bleu");
INSERT OR IGNORE INTO Usines VALUES (13, "Beautifull like you", "Alta", "vert");
INSERT OR IGNORE INTO Usines VALUES (14, "Happiness", "Helsinki", "vert");
INSERT OR IGNORE INTO Usines VALUES (15, "Mom's proud", "Budapest", "vert");
INSERT OR IGNORE INTO Usines VALUES (16, "Meeeh industries", "Lisbon", "bleu");
INSERT OR IGNORE INTO Usines VALUES (17, "I'm blue", "Bucarest", "bleu");
INSERT OR IGNORE INTO Usines VALUES (18, "I'm green", "Bucarest", "vert");
INSERT OR IGNORE INTO Usines VALUES (19, "The way of hydrogen", "Pandora", "bleu");
INSERT OR IGNORE INTO Usines VALUES (20, "You're a blue, Harry", "Hogwarts", "bleu");

-- Clients
INSERT OR IGNORE INTO Clients VALUES (1, "Antoine", "Baniel", "Geoguessr Inc.");
INSERT OR IGNORE INTO Clients VALUES (2, "Donald", "Tromp", "Gray House");
INSERT OR IGNORE INTO Clients VALUES (3, "Nicolas", "Hublot", "Sauvez les ours");
INSERT OR IGNORE INTO Clients VALUES (4, "Jean", "Dupont", "Société anonyme");
INSERT OR IGNORE INTO Clients VALUES (5, "Jeanne", "Dupont", "Société anonyme");
INSERT OR IGNORE INTO Clients VALUES (6, "Fry", "Poutine", "Plats polis");
INSERT OR IGNORE INTO Clients VALUES (7, "Jonnhy", "Rock", "Nashville Gaz");
INSERT OR IGNORE INTO Clients VALUES (8, "Jonnhy", "Claude", "Mourtocolliboeuf Industries");
INSERT OR IGNORE INTO Clients VALUES (9, "Jonnhy", "Michel", "V 2.0");
INSERT OR IGNORE INTO Clients VALUES (10, "Rastato", "Poulos", "Sydney Corp.");
INSERT OR IGNORE INTO Clients VALUES (11, "Legrand", "Schtroumpf", "Champindustries");
INSERT OR IGNORE INTO Clients VALUES (12, "Jean", "Dujardin", "Organisation Sociétale Saine 117");
INSERT OR IGNORE INTO Clients VALUES (13, "Jeanne", "Oskour", "Gentandévoi");
INSERT OR IGNORE INTO Clients VALUES (14, "Unesco", "Spa", "Probablement pas");
INSERT OR IGNORE INTO Clients VALUES (15, "Giuseppe", "Verdi", "Lanterne Inc.");

-- Commandes
INSERT OR IGNORE INTO Commandes VALUES (1, 800, "2023-05-06", 1);
INSERT OR IGNORE INTO Commandes VALUES (2, 350, "2023-05-17", 3);
INSERT OR IGNORE INTO Commandes VALUES (3, 1000, "2023-06-18", 15);
INSERT OR IGNORE INTO Commandes VALUES (4, 500, "2023-06-27", 8);
INSERT OR IGNORE INTO Commandes VALUES (5, 200, "2023-07-01", 17);
INSERT OR IGNORE INTO Commandes VALUES (6, 1500, "2023-07-01", 10);


-- Transporteurs
INSERT OR IGNORE INTO Transporteurs VALUES (182722456, "US AIR FORCE");
INSERT OR IGNORE INTO Transporteurs VALUES (172732552, "ICEBERG boat");
INSERT OR IGNORE INTO Transporteurs VALUES (156735638, "Port de plaisance de Palavas-les-flots");
INSERT OR IGNORE INTO Transporteurs VALUES (271947638, "Marine belge");

-- Navires
INSERT OR IGNORE INTO Navires VALUES (8376158, 1000, 172732552, 1);
INSERT OR IGNORE INTO Navires VALUES (8472902, 500, 271947638, 2);
INSERT OR IGNORE INTO Navires VALUES (2672795, 1500, 182722456, 3);
INSERT OR IGNORE INTO Navires VALUES (4792047, 550, 156735638, 4);
INSERT OR IGNORE INTO Navires VALUES (9284636, 200, 156735638, 5);
INSERT OR IGNORE INTO Navires VALUES (2678316, 1500, 182722456, 6);

-- Commandes clients
INSERT OR IGNORE INTO CommandesClients VALUES (2, 6, "2023-03-15");
INSERT OR IGNORE INTO CommandesClients VALUES (7, 6, "2023-03-15");
INSERT OR IGNORE INTO CommandesClients VALUES (7, 4, "2023-04-15");
INSERT OR IGNORE INTO CommandesClients VALUES (1, 5, "2023-02-27");
INSERT OR IGNORE INTO CommandesClients VALUES (6, 1, "2023-04-02");
INSERT OR IGNORE INTO CommandesClients VALUES (12, 2, "2023-02-27");
INSERT OR IGNORE INTO CommandesClients VALUES (11, 3, "2023-02-27");
