import sqlite3
from user_queries import *
from general_queries import *
from ingredient_queries import *
from recipe_queries import *
from user_queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# cursor.execute(open(r"SQL_Commands\ingredient_request_table.sql").read())




# submit_ingredient_for_approval(cursor, r"jsons\ingredient_submission.json")




connection.commit()

# view_table(cursor, r"PendingIngredientItem")

connection.close()

