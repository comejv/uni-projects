import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1000, 600, self)
        self.title('F5 : températures en isère en 2018')
        display.defineGridDisplay(self, 1, 1)

        query = """
            SELECT date_mesure, temperature_moy_mesure, temperature_min_mesure, temperature_max_mesure
            FROM Mesures
            WHERE code_departement = 38 AND strftime('%Y', date_mesure) = '2018'
        """

        # Extraction des données et affichage dans le tableau
        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))

        # Extraction et préparation des valeurs à mettre sur le graphique
        tabmoy = []
        tabmin = []
        tabmax = []
        tabx = []
        for row in result:
            tabmoy.append(row[1])
            tabx.append(row[0])
            tabmin.append(row[2])
            tabmax.append(row[3])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%Y-%m-%d') for date in tabx]

        # Ajout de la figure et du subplot qui contiendront le graphique
        fig = Figure(figsize=(10, 6), dpi=100)
        plot1 = fig.add_subplot(111)

        # Affichage des courbes
        plot1.plot(range(len(datetime_dates)), tabmoy, color='g', label='temp. moy')
        plot1.plot(range(len(datetime_dates)), tabmin, color='b', label='temp. min')
        plot1.plot(range(len(datetime_dates)), tabmax, color='r', label='temp. max')

        # Configuration de l'axe x pour n'afficher que le premier jour de chaque mois
        xticks = [i for i, date in enumerate(datetime_dates) if date.day == 1]
        xticklabels = [date.strftime('%m-%d') for date in datetime_dates if date.day == 1]
        plot1.set_xticks(xticks)
        plot1.set_xticklabels(xticklabels, rotation=45)
        plot1.legend()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig,  master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
