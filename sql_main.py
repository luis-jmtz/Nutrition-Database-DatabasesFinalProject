import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import query_ingredients_by_calories, print_df, query_ingredients_by_NutritionDensity

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# created the SQL Table
#cursor.executescript(open(r'SQL_Commands\table_creation.sql').read())

# show_tables(cursor)
# view_table(cursor, "RecipeIngredients")

# show_tables(cursor)
# view_table(cursor, "UserFavoriteRecipes")

# q1 = query_ingredients_by_calories(cursor, 50, 100)
q1 = query_ingredients_by_NutritionDensity(cursor, 50, 100)

print_df(q1)


connection.close()

