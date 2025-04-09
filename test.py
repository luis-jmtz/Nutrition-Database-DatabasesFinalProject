import sqlite3
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()


# view_table(cursor, "Admins")


# add_admin(cursor, 12)
# print(is_admin(cursor, 12))

view = search_ingredient_name(cursor, "apple", order = 2)
print_view(cursor, view)

# connection.commit()
connection.close()

