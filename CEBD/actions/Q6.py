import tkinter as tk
import matplotlib.pyplot as mp
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

        ttk.Button(self, text="Afficher le graph", command=self.printgraph).grid(column=0, row=1)

    def printgraph(self):

        try:
            tab = []
            query = """
                    SELECT strftime('%MM', date_mesure) as mois_mesure,
                           MIN(temperature_min_mesure) as minimum
                    FROM Mesures
                    WHERE code_departement = 38 AND strftime('%YYYY', date_mesure) = 2022
                    GROUP BY strftime('%MM', date_mesure)
                """
            cursor = db.data.cursor()
            result = cursor.execute(query)

            for res in result:
                tab.append(
                    [
                        res[0],
                        res[1],
                    ]
                )
        except Exception as e:
            print("Erreur : " + repr(e))

        months = 5

        # make data
        x = months
        y = np.linspace(-5, 10, 12)

        # plot
        fig, ax = mp.subplots()

        ax.plot(x, y, linewidth=2.0)

        ax.set(xlim=(0, 11), xticks=np.arange(1, 12),
               ylim=(-15, 30), yticks=np.arange(-15, 30))

        mp.show()