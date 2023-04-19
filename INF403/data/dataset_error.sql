-- INSERT PRODUISANT DES ERREURS
-- Veuillez exécuter le fichier "default_inserts.sql" pour obtenir les erreurs
--------------------------------------
--Types:
INSERT INTO Types VALUES ("jaune",7,2); -- Pas d'hydrogène jaune sur le marché (restreint a vert, bleu et gris)
INSERT INTO Types VALUES ("vert",-7,2); -- prix négatif
INSERT INTO Types VALUES ("vert",7,-2); -- rejet de production négatif
INSERT INTO Types VALUES (NULL,7,2); -- type d'hydrogène (CO2) NULL
INSERT INTO Types VALUES ("vert",NULL,2); -- prix d'hydrogène NULL
INSERT INTO Types VALUES ("vert",7,NULL); -- Rejet de production (CO2) NULL
--------------------------------------
--Usines:
INSERT INTO Usines VALUES (NULL,"usine_exemple","location_exemple","vert"); -- Auto-incrémente au lieu de produire une erreur
INSERT INTO Usines VALUES (1,"usine_exemple","location_exemple","vert"); -- L'Usine existe déjà
INSERT INTO Usines VALUES (-1,"usine_exemple","location_exemple","vert"); -- L'Usine à un numéro négatif
INSERT INTO Usines VALUES (100,NULL,"location_exemple","vert"); -- Le nom de l'usine est NULL
INSERT INTO Usines VALUES (100,"usine_exemple",NULL,"vert"); -- la location de l'Usine est NULL
INSERT INTO Usines VALUES (100,"usine_exemple","location_exemple",NULL); -- le type d'hydrogène produit par l'usine est NULL
INSERT INTO Usines VALUES (100,"usine_exemple","location_exemple","jaune"); -- le type d'hydrogène produit par l'usine n'est pas dans la table Types
--------------------------------------
--Commandes:
INSERT INTO Commandes VALUES (NULL,300,2023-03-27,1); -- Auto-incrémente au lieu de produire une erreur
INSERT INTO Commandes VALUES (1,300,2023-03-27,1); -- numéro commande déjà présent
INSERT INTO Commandes VALUES (500,-300,2023-03-27,1); -- tonne négatif
INSERT INTO Commandes VALUES (500,NULL,2023-03-27,1); -- tonne NULL
INSERT INTO Commandes VALUES (500,300,NULL,1); -------- PAS SUR
INSERT INTO Commandes VALUES (500,300,2023-03-27,1000); -- Usine inexistante
INSERT INTO Commandes VALUES (500,300,2023-03-27,NULL); -- Usine NULL
--------------------------------------
--Clients:
INSERT INTO Clients VALUES (NULL,"nom_exemple","prenom_exemple","societe_exemple"); -- Auto-incrémente au lieu de produire une erreur
INSERT INTO Clients VALUES (1,"nom_exemple","prenom_exemple","societe_exemple"); -- numéro client déjà présent 
INSERT INTO Clients VALUES (-1,"nom_exemple","prenom_exemple","societe_exemple"); -- numéro client est négatif
INSERT INTO Clients VALUES (1000,NULL,"prenom_exemple","societe_exemple"); -- le client a un nom NULL
INSERT INTO Clients VALUES (1000,"nom_exemple",NULL,"societe_exemple"); -- le client a un prenom NULL
INSERT INTO Clients VALUES (1000,"nom_exemple","prenom_exemple",NULL); -- le client a une société NULL
--------------------------------------
--Transporteurs:
INSERT INTO Transporteurs VALUES (NULL, "nom_exemple"); -- Auto-incrémente au lieu de produire une erreur
INSERT INTO Transporteurs VALUES (10000000000000, "nom_exemple"); -- DUNS a plus de 9 chiffres
INSERT INTO Transporteurs VALUES (-6, "nom_exemple"); -- DUNS négatif
INSERT INTO Transporteurs VALUES (156735638, "nom_exemple"); -- DUNS existant déjà dans la table
INSERT INTO Transporteurs VALUES (256735638, NULL); -- nom de transporteur NULL
--------------------------------------
-- Navires:
-- On ajoute une commande dans la table commande pour ne pas avoir la contrainte d'unicité
INSERT INTO Commandes VALUES (256, 300, "2023-06-20",4);
INSERT INTO Navires VALUES (NULL, 1500, 156735638, 256); -- Auto-incrémente au lieu de produire une erreur
INSERT INTO Navires VALUES (-1234567, 1500, 156735638, 256); -- Imo négative
INSERT INTO Navires VALUES (12345678, 1500, 156735638, 256); -- Imo plus grand que 7 chiffres
INSERT INTO Navires VALUES (1234567, -1500, 156735638, 256); -- capacité de Navires négative
INSERT INTO Navires VALUES (1234567, NULL, 156735638, 256); -- capacité NULL
INSERT INTO Navires VALUES (1234567, 1500, 156735338, 256); -- DUNS non présent dans la table Transporteurs 
INSERT INTO Navires VALUES (1234567, 1500, NULL, 256); -- DUNS NULL
INSERT INTO Navires VALUES (1234567, 1500, 156735638, 8); -- La commandes n'existe pas dans la table Commandes
INSERT INTO Navires VALUES (1234567, 1500, 156735638, 1); -- La commandes est déjà en cours de livraison
INSERT INTO Navires VALUES (1234567, 1500, 156735638, NULL); -- La commandes est NULL
-- On enlève notre commandes fictive
DELETE FROM Commandes WHERE numero_commande=256;
--------------------------------------
-- CommandesClients
INSERT INTO CommandesClients VALUES (NULL, 1, "2023-03-20"); -- Le numéro de client est NULL
INSERT INTO CommandesClients VALUES (1, NULL, "2023-03-20"); -- Le numéro de commandes est NULL
INSERT INTO CommandesClients VALUES (2, 6, "2023-03-20"); -- Le couple client-commande (2,6) est déjà dans la table (UNIQUE)
INSERT INTO CommandesClients VALUES (14, 1, NULL); -- La date de commandes est NULL
