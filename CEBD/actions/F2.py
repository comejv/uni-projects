import tkinter as tk
from tkinter import ttk
from utils import display
from utils import db

class Window(tk.Toplevel):

    # Attributs de la classe (pour être en mesure de les utiliser dans les différentes méthodes)
    treeView = None
    input = None
    errorLabel = None

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre et des lignes/colonnes
        display.centerWindow(600, 450, self)
        self.title('F2 : départements pour une région donnée (version statique)')
        display.defineGridDisplay(self, 2, 3)
        self.grid_rowconfigure(2, weight=10) #On donne un poids plus important à la dernière ligne pour l'affichage du tableau

        # Affichage du label, de la case de saisie et du bouton valider
        ttk.Label(self, text='Veuillez indiquer une région :', anchor="center", font=('Helvetica', '10', 'bold')).grid(row=0, column=0)
        self.input = ttk.Entry(self)
        self.input.grid(row=0, column=1)
        self.input.bind('<Return>', self.searchRegion) # On bind l'appui de la touche entrée sur la case de saisie, on peut donc utiliser soit la touche entrée soit le bouton valider
        ttk.Button(self, text='Valider', command=self.searchRegion).grid(row=0, column=2)

        # On place un label sans texte, il servira à afficher les erreurs
        self.errorLabel = ttk.Label(self, anchor="center", font=('Helvetica', '10', 'bold'))
        self.errorLabel.grid(columnspan=3, row=1, sticky="we")

        # On prépare un treeView vide pour l'affichage de nos résultats
        columns = ('code_departement', 'nom_departement',)
        self.treeView = ttk.Treeview(self, columns=columns, show='headings')
        for column in columns:
            self.treeView.column(column, anchor=tk.CENTER, width=15)
            self.treeView.heading(column, text=column)
        self.treeView.grid(columnspan=3, row=2, sticky='nswe')

    # Fonction qui récupère la valeur saisie, exécute la requête et affiche les résultats
    # La fonction prend un argument optionnel event car elle peut être appelée de deux manières :
    # Soit via le bouton Valider, dans ce cas aucun event n'est fourni
    # Soit via le bind qui a été fait sur la case de saisie quand on appuie sur Entrée, dans ce cas bind fournit un event (que l'on utilise pas ici)
    def searchRegion(self, event = None):

        # On vide le treeView (pour rafraichir les données si quelque chose était déjà présent)
        self.treeView.delete(*self.treeView.get_children())

        # On récupère la valeur saisie dans la case
        region = self.input.get()

        # Si la saisie est vide, on affiche une erreur
        if len(region) == 0:
            self.errorLabel.config(foreground='red', text="Veuillez saisir une région !")

        # Si la saisie contient quelque chose
        else :

            # On essai d'exécuter notre requête
            try:
                cursor = db.data.cursor()
                result = cursor.execute("""SELECT code_departement, nom_departement
                                            FROM Departements JOIN Regions USING (code_region)
                                            WHERE nom_region = ?
                                            ORDER BY code_departement""", [region])

            # S'il y a une erreur, on l'affiche à l'utilisateur
            except Exception as e:
                self.errorLabel.config(foreground='red', text="Erreur : " + repr(e))

            # Si tout s'est bien passé
            else:

                # On affiche les résultats de la requête dans le tableau
                i = 0
                for row in result:
                    self.treeView.insert('', tk.END, values=row)
                    i += 1

                # On affiche un message à l'utilisateur en fonction du nombre de résultats de la requête
                if i == 0:
                    self.errorLabel.config(foreground='orange', text="Aucun résultat pour la région \"" + region + "\" !")
                else :
                    self.errorLabel.config(foreground='green', text="Voici les résultats pour la région \"" + region + "\" :")