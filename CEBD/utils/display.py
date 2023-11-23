from utils import db
import tkinter as tk
from tkinter import ttk

# Permet de centrer une fenêtre à l'écran
def centerWindow (width, height, window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width / 2 - width / 2)
    center_y = int(screen_height / 2 - height / 2)
    window.geometry(f'{width}x{height}+{center_x}+{center_y}')

# Définit un affichage de type grid avec nbRow lignes et nbCol colonnes
def defineGridDisplay (target, nbRow, nbCol):
    for x in range(nbRow):
        target.grid_rowconfigure(x, weight=1)
    for y in range(nbCol):
        target.grid_columnconfigure(y, weight=1)

# Crée et retourne un TreeView avec les colonnes passées en paramètre et affiche les résultats de la requête
def createTreeViewDisplayQuery (target, columns, query, size=150):

    # Définition des colonnes
    tree = ttk.Treeview(target, columns=columns, show='headings')
    for column in columns:
        tree.column(column, anchor=tk.CENTER, stretch=0, width=size)
        tree.heading(column, text=column)

    # Extraction des données et affichage dans le tableau
    try:
        cursor = db.data.cursor()
        result = cursor.execute(query)
    except Exception as e:
        print("Erreur : " + repr(e))
    else:
        for row in result:
            tree.insert('', tk.END, values=row)

    return tree

# Crée et retourne un TreeView rempli avec les lignes du tableau passé en paramètre
def createTreeViewDisplay (target, columns, tabData, size=150):

    # Définition des colonnes
    tree = ttk.Treeview(target, columns=columns, show='headings')
    for column in columns:
        tree.column(column, anchor=tk.CENTER, stretch=0, width=size)
        tree.heading(column, text=column)

    # Extraction des données et affichage dans le tableau
    for row in tabData:
        tree.insert('', tk.END, values=row)

    return tree