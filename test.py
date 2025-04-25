import sqlite3
from user_queries import *
from general_queries import *
from ingredient_queries import *
from recipe_queries import *
from user_queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

view_table(cursor, "Recipes")
drop_data(cursor, r"jsons\drop_data.json")

view_table(cursor, "Recipes")

connection.commit()


connection.close()

