import sqlite3
from user_queries import *
from general_queries import *
from ingredient_queries import *
from recipe_queries import *
from user_queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# removes whitespaces from when the data was added
# cursor.execute("UPDATE Users SET userPassword = TRIM(userPassword)")
# cursor.execute("UPDATE Users SET userName = TRIM(userName)")
# connection.commit()


view_table(cursor, "Users")

view = query_user_favorites(cursor, r"jsons\query_user_favorites.json")
print_view(cursor, view)


drop_user_favorite(cursor, r"jsons\drop_user_favorite.json")


view = query_user_favorites(cursor, r"jsons\query_user_favorites.json")
print_view(cursor, view)


connection.commit()


connection.close()

