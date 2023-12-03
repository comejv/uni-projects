import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from utils import display
from utils import db
from tkinter import ttk


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title(
            "Q6 : Graphique correlation temperatures minimales - coût de travaux (Isère / 2022)"
        )
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(
            self,
            text="""Pour l’Isère et l'année 2022, donner deux courbes sur le même graphique  :
   - par mois, l’évolution de la moyenne des températures minimales
   - par mois, l’évolution des totaux de coûts de travaux tout type confondu""",
            wraplength=500,
            anchor="center",
            font=("Helvetica", "10", "bold"),
        ).grid(sticky="we", row=0)

        ttk.Button(self, text="Afficher le graph", command=self.printgraph).grid(
            column=0, row=1
        )

    def printgraph(self):
        try:
            tab = []
            query = """
                    SELECT strftime('%m', date_mesure) AS month, AVG(temperature_min_mesure) AS avg_temperature
                    FROM Mesures
                    WHERE code_departement = '38' AND strftime('%Y', date_mesure) = '2022'
                    GROUP BY month;
                """
            cursor = db.data.cursor()
            result = cursor.execute(query).fetchall()
            months, temperatures = zip(*result)

        except Exception as e:
            print("Erreur : " + repr(e))
            return

        # Plot the data
        plt.plot(months, temperatures, label="Average Temperature")
        plt.xlabel("Month")
        plt.ylabel("Value")
        plt.title("Correlation of temperatures and costs in Isère / 2022")
        plt.legend()
        plt.show()
