import sqlite3
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()


view_table(cursor, "Admins")


# add_admin(cursor, 12)

view_table(cursor, "Admins")
# connection.commit()
connection.close()

