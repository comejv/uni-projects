import sqlite3


def new_commande(numero_commande: int, quantite_commande: int,
                 livraison_commande: str, numero_usine: int):
    """Crée une nouvelle commande

    Args:
        numero_commande (int): Numéro de la commande
        quantite_commande (int): Quantité de la commande
        livraison_commande (str): Date de livraison de la commande
        numero_usine (int): Numéro de l'usine
    """
    # Vérifier que la commande n'existe pas déjà
    if find_commande(numero_commande=numero_commande).fetchone() is not None:
        raise ValueError('La commande existe déjà')


def find_commande(cur: sqlite3.Cursor, numero_commande: int = None,
                  livraison_commande: str = None, numero_usine: int = None) -> sqlite3.Cursor:
    """Retourne une liste de tuples contenant les commandes répondant aux critères

    Args:
        cur (sqlite3.Cursor): Curseur de la DB
        numero_commande (int, optional): chercher par numéro de commande
        livraison_commande (str, optional): chercher les commandes livrées avant la date
        numero_usine (int, optional): chercher par usine
    """
    # Vérifier qu'il n'y a qu'un seul critère
    if sum([numero_commande is not None, livraison_commande is not None, numero_usine is not None]) > 1:
        raise ValueError('Un seul critère au maximum')

    # Requête
    if numero_commande is not None:
        return cur.execute('SELECT * FROM Commandes WHERE numero_commande = ?', (numero_commande,))
    elif livraison_commande is not None:
        return cur.execute('SELECT * FROM Commandes WHERE livraison_commande < ?', (livraison_commande,))
    elif numero_usine is not None:
        return cur.execute('SELECT * FROM Commandes WHERE numero_usine = ?', (numero_usine,))
    else:
        return cur.execute('SELECT * FROM Commandes')
