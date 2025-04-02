import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import query_ingredients_by_calories, calculate_recipe_nutrition,query_user_favorite_recipes, print_view, query_ingredients_by_NutritionDensity, query_recipes_by_ingredient, query_user_favorite_ingredients

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# created the SQL Table
#cursor.executescript(open(r'SQL_Commands\table_creation.sql').read())

# show_tables(cursor)
#view_table(cursor, "Users")

# show_tables(cursor)
# view_table(cursor, "UserFavoriteRecipes")

# q1 = query_ingredients_by_calories(cursor, 50, 100)
# q1 = query_ingredients_by_NutritionDensity(cursor, 50, 100)

# q1 =  query_recipes_by_ingredient(cursor, 625)

q1 = calculate_recipe_nutrition(cursor, 1)

print_view(cursor, q1)


connection.close()

