import tkinter as tk
from tkinter import ttk
from utils import display
from actions import tablesData
from actions import F1, F2, F3, F4
from actions import Q1, Q2, Q3, Q4, Q5, Q6, Q7
from utils import db

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # Définition de la taille et du titre de la fenêtre
        display.centerWindow(500, 650, self)
        self.title('Mission climat')

        # Configuration des colonnes pour l'affichage grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Contrôles de la BDD
        ttk.Label(self, text='Contrôles de la base de données', background='lightgrey', anchor="center",
                  font=('Helvetica', '10', 'bold')).grid(columnspan=3, sticky="we", pady=(25, 5))
        ttk.Button(self, text='Create DB', command=db.createDB).grid(column=0, row=1, pady=5)
        ttk.Button(self, text='Insert DB', command=db.insertDB).grid(column=1, row=1, pady=5)
        ttk.Button(self, text='Delete DB', command=db.deleteDB).grid(column=2, row=1, pady=5)
        ttk.Button(self, text='Consulter les données de la base', command=self.open_tableData_window).grid(columnspan=3, pady=5)

        # Fonctions fournies
        ttk.Label(self, text='Fonctions fournies (ne pas modifier)', background='lightgrey',
                  anchor="center", font=('Helvetica', '10', 'bold')).grid(columnspan=3, sticky="we", pady=(20,5))
        ttk.Button(self, text='F1 : températures moyennes des départements au 2018-01-01',
                   command=self.open_F1_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text="F2 : départements pour une région donnée (version statique)",
                   command=self.open_F2_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text="F3 : températures par département et par année (version non optimisée)",
                   command=self.open_F3_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text="F4 : températures en Isère en 2018",
                   command=self.open_F4_window).grid(columnspan=3, pady=5)

        # Questions
        ttk.Label(self, text='Questions', background='lightgrey', anchor="center",
                  font=('Helvetica', '10', 'bold')).grid(columnspan=3, sticky="we", pady=(20,5))
        ttk.Button(self, text='Q1 : départements de la région Auvergne-Rhône-Alpes',
                   command=self.open_Q1_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text='Q2 : département le plus froid par région',
                   command=self.open_Q2_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text='Q3 : départements pour une région donnée (version dynamique)',
                   command=self.open_Q3_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text='Q4 : compléter la BD fournie (relations et données)',
                   command=self.open_Q4_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text='Q5 : températures par département et par année (version optimisée)',
                   command=self.open_Q5_window).grid(columnspan=3, pady=5)

        # Pour aller plus loin
        ttk.Label(self, text='Pour aller plus loin', background='lightgrey', anchor="center",
                  font=('Helvetica', '10', 'bold')).grid(columnspan=3, sticky="we", pady=(20,5))
        ttk.Button(self, text='Q6 : graphique sur la correlation temperatures minimales - coût de travaux (Isère / 2022)',
                   command=self.open_Q6_window).grid(columnspan=3, pady=5)
        ttk.Button(self, text="Q7 : gérer l'ajout/modification/suppression pour un type de travaux",
                   command=self.open_Q7_window).grid(columnspan=3, pady=5)

    ##################################################
    # Fonctions pour ouvrir les différentes fenêtres #
    ##################################################

    def open_tableData_window(self):
        window = tablesData.Window(self)
        window.grab_set()

    def open_F1_window(self):
        window = F1.Window(self)
        window.grab_set()

    def open_F2_window(self):
        window = F2.Window(self)
        window.grab_set()

    def open_F3_window(self):
        window = F3.Window(self)
        window.grab_set()

    def open_F4_window(self):
        window = F4.Window(self)
        window.grab_set()

    def open_Q1_window(self):
        window = Q1.Window(self)
        window.grab_set()

    def open_Q2_window(self):
        window = Q2.Window(self)
        window.grab_set()

    def open_Q3_window(self):
        window = Q3.Window(self)
        window.grab_set()

    def open_Q4_window(self):
        window = Q4.Window(self)
        window.grab_set()

    def open_Q5_window(self):
        window = Q5.Window(self)
        window.grab_set()

    def open_Q6_window(self):
        window = Q6.Window(self)
        window.grab_set()

    def open_Q7_window(self):
        window = Q7.Window(self)
        window.grab_set()

####################################
# Boucle générale de l'application #
####################################

if __name__ == "__main__":
    app = App()
    app.mainloop()