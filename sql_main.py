import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import add_user
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# show_tables(cursor)
view_table(cursor, "Users")

add_user(cursor, "add_user.json")


view_table(cursor, "Users")

add_user(cursor, "add_user.json")

# connection.commit()
connection.close()

