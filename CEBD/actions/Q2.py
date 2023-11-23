import tkinter as tk
from utils import display
from tkinter import ttk

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q2 : département le plus froid par région')
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(self, text="Modifier cette fonction en s'inspirant du code de F1, pour qu'elle affiche le(s) département(s) avec la température moyenne (c.a.d. moyenne des moyennes de toutes les mesures) la plus basse par région. \nSchéma attendu : (nom_region, nom_departement, temperature_moy_min)",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0)

        #TODO Q2 Modifier la suite du code (en se basant sur le code de F1) pour répondre à Q2

        # On définit les colonnes que l'on souhaite afficher dans la fenêtre et la requête

        # On utilise la fonction createTreeViewDisplayQuery pour afficher les résultats de la requête
