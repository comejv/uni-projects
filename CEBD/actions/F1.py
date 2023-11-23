import tkinter as tk
from utils import display

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('F1 : températures moyennes des départements au 2018-01-01')
        #TODO Q1 Aller voir le code de defineGridDisplay dans utils/display.py
        display.defineGridDisplay(self, 1, 1)

        # On définit les colonnes que l'on souhaite afficher dans la fenêtre et la requête
        columns = ('code_departement', 'nom_departement','temperature_moy_mesure')
        query = """SELECT code_departement, nom_departement, temperature_moy_mesure
                    FROM Departements JOIN Mesures USING (code_departement) 
                    WHERE date_mesure = '2018-01-01'
                    ORDER BY code_departement"""

        # On utilise la fonction createTreeViewDisplayQuery pour afficher les résultats de la requête
        #TODO Q1 Aller voir le code de createTreeViewDisplayQuery dans utils/display.py
        tree = display.createTreeViewDisplayQuery(self, columns, query,200)
        tree.grid(row=0, sticky="nswe")