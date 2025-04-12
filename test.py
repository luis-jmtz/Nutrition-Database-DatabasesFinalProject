import sqlite3
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()


# view_table(cursor, "Admins")


# add_admin(cursor, 12)
# print(is_admin(cursor, 12))

# view = search_ingredient_name(cursor, "", order = 2)

# view = search_ingredients(cursor, fr"jsons\search_ingredients.json", search_text='', order=0)
# cursor.execute("DROP TABLE IF EXISTS PendingRecipes")
# cursor.execute("DROP TABLE IF EXISTS PendingRecipeIngredients")

# show_tables(cursor)
# cursor.executescript(open(r'SQL_Commands\recipe_requests_tables.sql').read())
show_tables(cursor)


# print_view(cursor, view)

connection.commit()
connection.close()

