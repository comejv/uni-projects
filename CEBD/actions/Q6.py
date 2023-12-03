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
            temp_query = """
                    SELECT strftime('%m', date_mesure) AS month, AVG(temperature_min_mesure) AS avg_temperature
                    FROM Mesures
                    WHERE code_departement = '38' AND strftime('%Y', date_mesure) = '2022'
                    GROUP BY month;
                """
            cout_query = """
                    SELECT strftime('%m', date_travaux) AS month, SUM(cout_total_ht_travaux) AS cout_total_mensuel
                    FROM Travaux
                    WHERE code_departement = '38' AND strftime('%Y', date_travaux) = '2022'
                    GROUP BY month;
                """
            cursor = db.data.cursor()
            temp_result = cursor.execute(temp_query).fetchall()
            cout_result = cursor.execute(cout_query).fetchall()
            # On choisit d'afficher le graphique même si les données sont vides
            if temp_result == []:
                temp_result = [[0, 0]]
            if cout_result == []:
                cout_result = [[0, 0]]
            months_temp, temperatures = zip(*temp_result)
            months_cout, couts = zip(*cout_result)
        except Exception as e:
            print("Erreur : " + repr(e))
            return

        # Plot the data
        fig, ax1 = plt.subplots()

        color = "tab:red"
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Average Temperature", color=color)
        ax1.plot(months_temp, temperatures, color=color)
        ax1.tick_params(axis="y", labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = "tab:blue"
        ax2.set_ylabel(
            "Total cost", color=color
        )  # we already handled the x-label with ax1
        ax2.plot(months_cout, couts, color=color)
        ax2.tick_params(axis="y", labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title("Correlation of temperatures and costs in Isère / 2022")
        plt.show()
