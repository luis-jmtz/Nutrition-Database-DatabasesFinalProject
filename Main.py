import sqlite3
from user_queries import *
from general_queries import *
from ingredient_queries import *
from recipe_queries import *
from user_queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()


# show_tables(cursor)
# view_table(cursor, "PendingIngredientItem")



connection.commit()
connection.close()

