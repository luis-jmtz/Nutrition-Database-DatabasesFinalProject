import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# show_tables(cursor)
# view_table(cursor, "Users")

view = calculate_recipe_nutrition(cursor, 1)

print_view(cursor, view)


# connection.commit()
connection.close()

