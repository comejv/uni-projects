from utils import db, fmt
from sqlite3 import Connection, OperationalError

def information_client (conn : Connection) -> bool :
    fmt.clear()
    fmt.pbold("Information client :")
    fmt.pitalic("Ne rien mettre si vous de connaissez pas un parametre")
    info = fmt.form_input(["nom de la personne recherchée", "prenom de la personne recherchée", "société de la personne recherchée"])
    values = ""
    i=1
    key_list = ["nom" , "prenom", "societe"]
    
    for i,key in enumerate(key_list):
        if info[i] != "":
            values += f"{key}_client = ?{i}"

    info = [value for value in info if value != ""]
    
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
                         HAVING {values};",tuple(info))
    
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

def type_commande(conn: Connection) -> bool :
    fmt.clear()
    fmt.pbold("Information sur le type d'hydrogène des commandes :")
    fmt.pitalic("Ne rien mettre si vous voulez tous les types d'hydrogènes.")

    coul = fmt.form_input(["Types des commandes à afficher"])[0]
    while not coul in ["vert", "bleu", "gris", ""] :
        coul = fmt.form_input(["Types des commandes à afficher"])[0]
    
    cursor = conn.cursor()
    
    if coul == "":
        cursor.execute("SELECT numero_commande, nom_type\
                        FROM Commandes JOIN Usines USING (numero_usine)\
			            JOIN Types USING (nom_type);")
    else:
        cursor.execute("SELECT numero_commande, nom_type\
                        FROM Commandes JOIN Usines USING (numero_usine)\
			            JOIN Types USING (nom_type)\
                        WHERE nom_type = ?;",(coul,))

    # Affichage des données
    db.show_results(cursor)

    return True

def information_type_transporteur (conn: Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT duns_transporteur, nom_transporteur, COUNT(numero_commande) AS nombre_commande_en_cours ,nom_type\
                    FROM Transporteurs JOIN Navires USING (duns_transporteur)\
				                       JOIN Commandes USING (numero_commande)\
				                       JOIN Usines USING (numero_usine)\
				                       JOIN Types USING (nom_type)\
                    GROUP BY duns_transporteur, nom_transporteur, nom_type;")

    # Affichage des données
    db.show_results(cursor)

    return True
