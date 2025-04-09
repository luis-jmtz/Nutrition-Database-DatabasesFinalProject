import sqlite3
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()


view_table(cursor, "Users")


# connection.commit()
connection.close()

