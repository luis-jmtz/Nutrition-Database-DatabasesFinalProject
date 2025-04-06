import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import add_user
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# show_tables(cursor)
view_table(cursor, "Users")

view = query_user_favorites(cursor, "query_user_favorites.json")

print_view(cursor, view)


# connection.commit()
connection.close()

