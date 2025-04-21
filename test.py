import sqlite3
from user_queries import *
from visualization_queries import *
from ingredient_queries import *
from recipe_queries import *
from user_queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# cursor.execute(open(r"SQL_Commands\ingredient_request_table.sql").read())


show_tables(cursor)

connection.commit()
connection.close()

