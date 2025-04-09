import sqlite3
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()


# view_table(cursor, "Users")


cursor.executescript(open(r'SQL_Commands\table_creation.sql').read())


connection.commit()
show_tables(cursor)
connection.close()

