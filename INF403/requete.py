from utils import db, fmt
from sqlite3 import Connection, OperationalError

def information_client (conn : Connection) -> bool :
    fmt.clear()
    fmt.pbold("Information client :")
    fmt.pitalic("Ne rien mettre si vous de connaissez pas un parametre")
    info = fmt.form_input(["nom de la personne recherchée", "prenom de la personne recherchée", "société de la personne recherchée"])
    values = ""
    if info[0] != "":
        values = values + f"nom_client = \"{info[0]}\""
    if info[1] != "":
        values = values + f"prenom_client = \"{info[1]}\""
    if info[2] != "":
        values = values + f"societe_client = \"{info[2]}\""

    cursor = conn.cursor()
    if values == "":
        cursor.execute("SELECT numero_client, nom_client, prenom_client, societe_client, COUNT(numero_commande) AS nombre_de_commandes_passe, SUM(prix_total_commande) AS argent_depense, nom_type AS type_hydrogene_commande \
                        FROM Clients JOIN CommandesClients USING (numero_client)\
                                     JOIN Commandes USING (numero_commande)\
                                     JOIN Usines USING (numero_usine)\
                        GROUP BY nom_type, numero_client, nom_client, prenom_client, societe_client;")
    else:
        cursor.execute(f"SELECT numero_client, nom_client, prenom_client, societe_client, COUNT(numero_commande) AS nombre_de_commandes_passe, SUM(prix_total_commande) AS argent_depense, nom_type AS type_hydrogene_commande \
                         FROM Clients JOIN CommandesClients USING (numero_client)\
                                      JOIN Commandes USING (numero_commande)\
                                      JOIN Usines USING (numero_usine)\
                         GROUP BY nom_type, numero_client, nom_client, prenom_client, societe_client\
                         HAVING {values};")
    
    # Affichage des données
    db.show_results(cursor)

    return True

def information_navire (conn: Connection) -> bool :
    cursor = conn.cursor()
    cursor.execute("SELECT duns_transporteur, nom_transporteur, COUNT(imo_navire) AS nombre_de_navire_en_livraison, SUM(quantite_commande) AS quantite_hydrogen_en_livraison, SUM(capacite_navire) AS capacite_cumule_des_navires_fournis\
                    FROM Transporteurs LEFT JOIN Navires USING (duns_transporteur)\
				                       LEFT JOIN Commandes USING (numero_commande)\
                    GROUP BY duns_transporteur, nom_transporteur;")
    
    # Affichage des données
    db.show_results(cursor)

    return True
