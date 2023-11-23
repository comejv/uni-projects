import tkinter as tk
from utils import display
from tkinter import ttk

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q7 : gérer les travaux de rénovation')
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(self, text="""Proposer des fonctionnalités permettant de gérer l'ajout, modification et suppression pour un type de travaux""",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0)
