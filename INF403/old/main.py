import sqlite3
from tables import init_tables

# Création de la DB
con = sqlite3.connect('hydrogen.db')
cur = con.cursor()

# Support des FK
cur.execute('PRAGMA foreign_keys = ON')

# TABLES
init_tables(cur)
