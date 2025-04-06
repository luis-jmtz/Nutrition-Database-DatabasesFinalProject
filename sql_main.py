import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import add_user
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# show_tables(cursor)
view_table(cursor, "Users")

print_view(cursor, query_user_favorite_ingredients(cursor, 1))

add_user_favorite(cursor, "add_user_favorite.json")

print_view(cursor, query_user_favorite_ingredients(cursor, 1))


# connection.commit()
connection.close()

