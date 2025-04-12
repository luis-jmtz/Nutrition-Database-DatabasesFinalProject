import sqlite3
from user_queries import *
from visualization_queries import *
from ingredient_queries import *
from recipe_queries import *
from user_queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# cursor.execute("DROP TABLE IF EXISTS PendingRecipes")
# cursor.execute("DROP TABLE IF EXISTS PendingRecipeIngredients")

show_tables(cursor)
# cursor.executescript(open(r'SQL_Commands\recipe_requests_tables.sql').read())




# submit_recipe_for_approval(cursor, r"jsons\recipe_submission.json")

# view_table(cursor, "PendingRecipes")


#connection.commit()
connection.close()

