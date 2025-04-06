import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# show_tables(cursor)
# view_table(cursor, "Users")

# view = loop_filter_ingredients(cursor, "jsons\ingredient_filter.json")

# print_view(cursor, view, max_columns= 4)


# connection.commit()
connection.close()

