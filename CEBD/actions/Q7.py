import tkinter as tk
from utils import display
from tkinter import ttk
from utils import db


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title("Q7 : gérer les travaux de rénovation")
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(
            self,
            text="""Proposer des fonctionnalités permettant de gérer l'ajout, modification et suppression pour un type de travaux""",
            wraplength=500,
            anchor="center",
            font=("Helvetica", "10", "bold"),
        ).grid(sticky="we", row=0)

        ttk.Button(
            self, text="Ajouter travaux Isolation", command=self.addIsolation
        ).grid(column=0, row=1)
        ttk.Button(
            self, text="Modifier travaux Isolation", command=self.updateIsolation
        ).grid(column=0, row=2)

    def addIsolation(self):
        window = AddWindow(self)
        window.grab_set()

    def updateIsolation(self):
        window = UpdateWindow(self, 1)
        window.grab_set()


class AddWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title("Ajouter un travaux d'isolation")
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(
            self,
            text="""Ajouter un travaux d'isolation""",
            wraplength=500,
            anchor="center",
            font=("Helvetica", "10", "bold"),
        ).grid(sticky="we", row=0)

        self.enums_types_logements = ["INDIVIDUEL", "COLLECTIF"]
        self.enum_postes_isolation = [
            "COMBLES PERDUES",
            "ITI",
            "ITE",
            "RAMPANTS",
            "SARKING",
            "TOITURE TERRASE",
            "PLANCHER BAS",
        ]
        self.enum_types_isolant = [
            "AUTRES",
            "LAINE VEGETALE",
            "LAINE MINERALE",
            "PLASTIQUES",
        ]

        # Département
        cursor = db.data.cursor()
        cursor.execute("SELECT code_departement, nom_departement FROM Departements")
        departements = cursor.fetchall()
        ttk.Label(self, text="Département : ").grid(column=0, row=1)
        self.departement = tk.StringVar()
        self.departement.set(departements[0][0])
        self.departementMenu = ttk.OptionMenu(
            self, self.departement, departements[0][0], *departements
        )
        self.departementMenu.grid(column=1, row=1)

        # Cout total
        ttk.Label(self, text="Cout total : ").grid(column=0, row=2)
        self.cout_total = tk.StringVar()
        self.cout_total_entry = ttk.Entry(self, textvariable=self.cout_total)
        self.cout_total_entry.grid(column=1, row=2)

        # Cout induit
        ttk.Label(self, text="Cout induit : ").grid(column=0, row=3)
        self.cout_induit = tk.StringVar()
        self.cout_induit_entry = ttk.Entry(self, textvariable=self.cout_induit)
        self.cout_induit_entry.grid(column=1, row=3)

        # Date travaux
        ttk.Label(self, text="Date travaux : ").grid(column=0, row=4)
        self.date_travaux = tk.StringVar()
        self.date_travaux_entry = ttk.Entry(self, textvariable=self.date_travaux)
        self.date_travaux_entry.grid(column=1, row=4)

        # Année construction
        ttk.Label(self, text="Année construction : ").grid(column=0, row=5)
        self.annee_constr = tk.StringVar()
        self.annee_constr_entry = ttk.Entry(self, textvariable=self.annee_constr)
        self.annee_constr_entry.grid(column=1, row=5)

        # Type logement (INDIVIDUEL ou COLLECTIF)
        ttk.Label(self, text="Type logement : ").grid(column=0, row=6)
        self.type_logement = tk.StringVar()
        self.type_logement_entry = ttk.Combobox(
            self, textvariable=self.type_logement, values=self.enums_types_logements
        )
        self.type_logement_entry.grid(column=1, row=6)

        # Poste isolation
        ttk.Label(self, text="Poste isolation : ").grid(column=0, row=7)
        self.poste_isolation = tk.StringVar()
        self.poste_isolation_entry = ttk.Combobox(
            self, textvariable=self.poste_isolation, values=self.enum_postes_isolation
        )
        self.poste_isolation_entry.grid(column=1, row=7)

        # Isolant isolation
        ttk.Label(self, text="Isolant isolation : ").grid(column=0, row=8)
        self.isolant_isolation = tk.StringVar()
        self.isolant_isolation_entry = ttk.Combobox(
            self, textvariable=self.isolant_isolation, values=self.enum_types_isolant
        )
        self.isolant_isolation_entry.grid(column=1, row=8)

        # Epaisseur isolation
        ttk.Label(self, text="Epaisseur isolation : ").grid(column=0, row=9)
        self.epaisseur_isolation = tk.StringVar()
        self.epaisseur_isolation_entry = ttk.Entry(
            self, textvariable=self.epaisseur_isolation
        )
        self.epaisseur_isolation_entry.grid(column=1, row=9)

        # Surface isolation
        ttk.Label(self, text="Surface isolation : ").grid(column=0, row=10)
        self.surface_isolation = tk.StringVar()
        self.surface_isolation_entry = ttk.Entry(
            self, textvariable=self.surface_isolation
        )
        self.surface_isolation_entry.grid(column=1, row=10)

        ttk.Button(self, text="Ajouter", command=self.add).grid(column=0, row=11)

    def add(self):
        try:
            cursor = db.data.cursor()
            cursor.execute(
                """
                INSERT INTO Travaux (
                    code_departement,
                    cout_total_ht_travaux,
                    cout_induit_ht_travaux,
                    date_travaux,
                    annee_constr_travaux,
                    type_logement_travaux
                )
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    self.departement.get(),
                    self.cout_total.get(),
                    self.cout_induit.get(),
                    self.date_travaux.get(),
                    self.annee_constr.get(),
                    self.type_logement.get(),
                ),
            )
            cursor.execute(
                """
                INSERT INTO Isolations (
                    numero_travaux,
                    poste_isolation,
                    isolant_isolation,
                    epaisseur_isolation,
                    surface_isolation
                )
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    cursor.lastrowid,
                    self.poste_isolation.get(),
                    self.isolant_isolation.get(),
                    self.epaisseur_isolation.get(),
                    self.surface_isolation.get(),
                ),
            )
            db.data.commit()
            self.destroy()
        except Exception as e:
            print("Erreur : " + repr(e))
            return


class UpdateWindow(tk.Toplevel):
    def __init__(self, parent, numero_travaux):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title("Modifier un travaux d'isolation")
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(
            self,
            text="""Modifier un travaux d'isolation""",
            wraplength=500,
            anchor="center",
            font=("Helvetica", "10", "bold"),
        ).grid(sticky="we", row=0)

        # Selection travaux à modifier
        cursor = db.data.cursor()
        ttk.Label(self, text="Quel isolation voulez-vous modifier ?").grid(
            column=0, row=1
        )
        self.numero_travaux = tk.StringVar()
        self.numero_travaux.set(numero_travaux)
        self.numero_travaux_entry = ttk.Entry(self, textvariable=self.numero_travaux)
        self.numero_travaux_entry.grid(column=1, row=1)

        ttk.Button(self, text="Valider", command=self.select).grid(column=0, row=2)

    def select(self):
        numero_travaux = self.numero_travaux.get()
        cursor = db.data.cursor()
        # Get current data
        cursor.execute(
            """
            SELECT
                Travaux.code_departement,
                Travaux.cout_total_ht_travaux,
                Travaux.cout_induit_ht_travaux,
                Travaux.date_travaux,
                Travaux.annee_constr_travaux,
                Travaux.type_logement_travaux,
                Isolations.poste_isolation,
                Isolations.isolant_isolation,
                Isolations.epaisseur_isolation,
                Isolations.surface_isolation
            FROM Travaux
            JOIN Isolations ON Isolations.numero_travaux = Travaux.numero_travaux
            WHERE Travaux.numero_travaux = ?;
            """,
            (numero_travaux,),
        )

        # Département
        cursor.execute("SELECT code_departement, nom_departement FROM Departements")
        departements = cursor.fetchall()
        ttk.Label(self, text="Département : ").grid(column=0, row=2)
        self.departement = tk.StringVar()
        self.departement.set(cursor.fetchone()[0])
        self.departementMenu = ttk.OptionMenu(
            self, self.departement, self.departement.get(), *departements
        )
        self.departementMenu.grid(column=1, row=2)

        # Cout total
        ttk.Label(self, text="Cout total : ").grid(column=0, row=3)
        self.cout_total = tk.StringVar()
        self.cout_total.set(cursor.fetchone()[1])
        self.cout_total_entry = ttk.Entry(self, textvariable=self.cout_total)
        self.cout_total_entry.grid(column=1, row=3)

        # Cout induit
        ttk.Label(self, text="Cout induit : ").grid(column=0, row=4)
        self.cout_induit = tk.StringVar()
        self.cout_induit.set(cursor.fetchone()[2])
        self.cout_induit_entry = ttk.Entry(self, textvariable=self.cout_induit)
        self.cout_induit_entry.grid(column=1, row=4)

        # Date travaux
        ttk.Label(self, text="Date travaux : ").grid(column=0, row=5)
        self.date_travaux = tk.StringVar()
        self.date_travaux.set(cursor.fetchone()[3])
        self.date_travaux_entry = ttk.Entry(self, textvariable=self.date_travaux)
        self.date_travaux_entry.grid(column=1, row=5)

        # Année construction
        ttk.Label(self, text="Année construction : ").grid(column=0, row=6)
        self.annee_constr = tk.StringVar()
        self.annee_constr.set(cursor.fetchone()[4])
        self.annee_constr_entry = ttk.Entry(self, textvariable=self.annee_constr)
        self.annee_constr_entry.grid(column=1, row=6)

        # Type logement
        ttk.Label(self, text="Type logement : ").grid(column=0, row=7)
        self.type_logement = tk.StringVar()
        self.type_logement.set(cursor.fetchone()[5])
        self.type_logement_entry = ttk.Entry(self, textvariable=self.type_logement)
        self.type_logement_entry.grid(column=1, row=7)

        # Poste isolation
        ttk.Label(self, text="Poste isolation : ").grid(column=0, row=8)
        self.poste_isolation = tk.StringVar()
        self.poste_isolation.set(cursor.fetchone()[6])
        self.poste_isolation_entry = ttk.Entry(self, textvariable=self.poste_isolation)
        self.poste_isolation_entry.grid(column=1, row=8)

        # Isolant isolation
        ttk.Label(self, text="Isolant isolation : ").grid(column=0, row=9)
        self.isolant_isolation = tk.StringVar()
        self.isolant_isolation.set(cursor.fetchone()[7])
        self.isolant_isolation_entry = ttk.Entry(
            self, textvariable=self.isolant_isolation
        )
        self.isolant_isolation_entry.grid(column=1, row=9)

        # Epaisseur isolation
        ttk.Label(self, text="Epaisseur isolation : ").grid(column=0, row=10)
        self.epaisseur_isolation = tk.StringVar()
        self.epaisseur_isolation.set(cursor.fetchone()[8])
        self.epaisseur_isolation_entry = ttk.Entry(
            self, textvariable=self.epaisseur_isolation
        )
        self.epaisseur_isolation_entry.grid(column=1, row=10)

        # Surface isolation
        ttk.Label(self, text="Surface isolation : ").grid(column=0, row=11)
        self.surface_isolation = tk.StringVar()
        self.surface_isolation.set(cursor.fetchone()[9])
        self.surface_isolation_entry = ttk.Entry(
            self, textvariable=self.surface_isolation
        )
        self.surface_isolation_entry.grid(column=1, row=11)

        ttk.Button(self, text="Modifier", command=self.update).grid(column=0, row=12)

    def update(self):
        try:
            cursor = db.data.cursor()
            cursor.execute(
                """
                UPDATE Travaux
                SET
                    code_departement = ?,
                    cout_total_ht_travaux = ?,
                    cout_induit_ht_travaux = ?,
                    date_travaux = ?,
                    annee_constr_travaux = ?,
                    type_logement_travaux = ?
                WHERE numero_travaux = ?;
                """,
                (
                    self.departement.get(),
                    self.cout_total.get(),
                    self.cout_induit.get(),
                    self.date_travaux.get(),
                    self.annee_constr.get(),
                    self.type_logement.get(),
                    self.numero_travaux.get(),
                ),
            )
            cursor.execute(
                """
                UPDATE Isolations
                SET
                    poste_isolation = ?,
                    isolant_isolation = ?,
                    epaisseur_isolation = ?,
                    surface_isolation = ?
                WHERE numero_travaux = ?;
                """,
                (
                    self.poste_isolation.get(),
                    self.isolant_isolation.get(),
                    self.epaisseur_isolation.get(),
                    self.surface_isolation.get(),
                    self.numero_travaux.get(),
                ),
            )
            db.data.commit()
            self.destroy()
        except Exception as e:
            print("Erreur : " + repr(e))
            return
