import sqlite3

connection = sqlite3.connect("data/movements.db")
cur = connection.cursor()

f = open("data/create.sql", "r")
query = f.read()

print(query)

try:
    cur.execute(query)
except sqlite3.Error as e:
    print("Se ha producido el error", e)