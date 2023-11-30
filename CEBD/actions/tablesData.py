import tkinter as tk
from tkinter import ttk
from utils import display


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(800, 500, self)
        self.title("Consultation des données de la base")
        display.defineGridDisplay(self, 1, 1)

        # Définition des onglets
        # TODO Q4 Créer des nouveaux onglets pour les nouvelles tables
        tabControl = ttk.Notebook(self)
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tab3 = ttk.Frame(tabControl)
        tab4 = ttk.Frame(tabControl)
        tab5 = ttk.Frame(tabControl)
        tab6 = ttk.Frame(tabControl)
        tab7 = ttk.Frame(tabControl)
        tab8 = ttk.Frame(tabControl)
        tabControl.add(tab1, text="Mesures (1000 1ères valeurs)")
        tabControl.add(tab2, text="Départements")
        tabControl.add(tab3, text="Régions")
        tabControl.add(tab4, text="Communes")
        tabControl.add(tab5, text="Travaux")
        tabControl.add(tab6, text="Isolations")
        tabControl.add(tab7, text="Chauffages")
        tabControl.add(tab8, text="Photovoltaïques")
        display.defineGridDisplay(tab1, 1, 2)
        display.defineGridDisplay(tab2, 1, 2)
        display.defineGridDisplay(tab3, 1, 2)
        display.defineGridDisplay(tab4, 1, 2)
        display.defineGridDisplay(tab5, 1, 2)
        display.defineGridDisplay(tab6, 1, 2)
        display.defineGridDisplay(tab7, 1, 2)
        display.defineGridDisplay(tab8, 1, 2)
        tabControl.grid(row=0, column=0, sticky="nswe")

        # Mesures
        columns = (
            "code_departement",
            "date_mesure",
            "temperature_min_mesure",
            "temperature_max_mesure",
            "temperature_moy_mesure",
        )
        query = """
            SELECT code_departement, date_mesure, temperature_min_mesure, temperature_max_mesure, temperature_moy_mesure
            FROM Mesures
            ORDER BY date_mesure
            LIMIT 1,1000
        """
        tree = display.createTreeViewDisplayQuery(tab1, columns, query)
        scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Départements
        columns = (
            "code_departement",
            "nom_departement",
            "code_region",
            "zone_climatique",
        )
        query = """
            SELECT code_departement, nom_departement, code_region, zone_climatique_departement
            FROM Departements
            ORDER BY code_departement
        """
        tree = display.createTreeViewDisplayQuery(tab2, columns, query, 200)
        scrollbar = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Régions
        columns = ("code_region", "nom_region")
        query = """
            SELECT code_region, nom_region
            FROM Regions
            ORDER BY code_region
        """
        tree = display.createTreeViewDisplayQuery(tab3, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # TODO Q4 Afficher les données des nouvelles tables

        # Communes
        columns = ("nom_commune", 
                   "code_departement", 
                   "arrondissement_commune", 
                   "canton_commune", 
                   "population_commune", 
                   "superficie_commune", 
                   "altitude_moy_commune")
        query = """
            SELECT nom_commune, code_departement, arrondissement_commune, canton_commune, population_commune, superficie_commune, altitude_moy_commune
            FROM Communes
            ORDER BY nom_commune, code_departement
        """
        tree = display.createTreeViewDisplayQuery(tab4, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Travaux
        columns = ("numero_travaux", 
                   "code_departement", 
                   "cout_total_ht_travaux", 
                   "cout_induit_ht_travaux", 
                   "annee_travaux", 
                   "annee_constr_travaux", 
                   "type_logement_travaux")

        query = """
            SELECT numero_travaux,
                   code_departement, 
                   cout_total_ht_travaux, 
                   cout_induit_ht_travaux, 
                   annee_travaux, 
                   annee_constr_travaux, 
                   type_logement_travaux
            FROM Travaux
            ORDER BY numero_travaux, code_departement
        """

        tree = display.createTreeViewDisplayQuery(tab5, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Isolations
        columns = ("numero_travaux", 
                   "poste_isolation", 
                   "isolant_isolation", 
                   "epaisseur_isolation", 
                   "surface_isolation")

        query = """
            SELECT numero_travaux,
                   poste_isolation, 
                   isolant_isolation, 
                   epaisseur_isolation, 
                   surface_isolation
            FROM Isolations
            ORDER BY numero_travaux
        """

        tree = display.createTreeViewDisplayQuery(tab6, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Chauffage
        columns = ("numero_travaux", 
                   "energie_chauffage_avant_travaux", 
                   "energie_chauffage_installee", 
                   "generateur_chauffage", 
                   "type_chaudiere_chauffage")

        query = """
            SELECT numero_travaux,
                   energie_chauffage_avt_chauffage, 
                   energie_chauffage_inst_chauffage, 
                   generateur_chauffage, 
                   type_chaudiere_chauffage
            FROM Chauffages
            ORDER BY numero_travaux
        """

        tree = display.createTreeViewDisplayQuery(tab7, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Photovoltaïque
        columns = ("numero_travaux", 
                   "poste_isolation", 
                   "isolant_isolation", 
                   "epaisseur_isolation", 
                   "surface_isolation")

        query = """
            SELECT numero_travaux,
                   puissance_installee_photovoltaique, 
                   type_panneau_photovoltaique
            FROM Photovoltaiques
            ORDER BY numero_travaux
        """

        tree = display.createTreeViewDisplayQuery(tab8, columns, query, 250)
        scrollbar = ttk.Scrollbar(tab3, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, sticky="nswe")
        scrollbar.grid(row=0, column=1, sticky="ns")