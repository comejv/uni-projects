import tkinter as tk
from utils import display
from tkinter import ttk

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q4 : compléter la BD fournie (relations et données)')
        display.defineGridDisplay(self, 1, 1)
        ttk.Label(self, text="""Créer les tables manquantes, insérer les données correspondantes depuis les fichiers CSV fournis et mettre à jour l'affichage de consultation de la BD.
        
        Note : insérer les données peut être long à cause du grand nombre de mesures. Vous avez à disposition un fichier MesuresSmall.csv qui ne contient que quelques données, vous pouvez l'utiliser le temps du développement pour faciliter les tests.""",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0)