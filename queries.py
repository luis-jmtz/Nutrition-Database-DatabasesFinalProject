import pandas as pd
import sqlite3

def print_view(cursor, view_name, max_rows=10, max_columns=None):
    cursor.execute(f"SELECT * FROM {view_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_columns):
        print(pd.DataFrame(rows, columns=columns))

def filter_ingredient_column(cursor, column_name, min_val=None, max_val=None):
    try:
        query = f"CREATE TEMP VIEW IF NOT EXISTS FilteredIngredientView AS "
        query += f"SELECT ingredientID, ingredientName, {column_name} FROM IngredientItem"
        
        range = []
        
        if min_val is not None:
            range.append(f"{column_name} >= {min_val}")
        if max_val is not None:
            range.append(f"{column_name} <= {max_val}")
        if range:
            query += " WHERE " + " AND ".join(range)
        
        cursor.execute(query)
        return "FilteredIngredientView"
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def query_recipes_by_ingredient(cursor, ingredient_id):
    try:
        cursor.execute(f"CREATE TEMP VIEW IF NOT EXISTS RecipesByIngredientView AS SELECT RecipeIngredients.recipeID, Recipes.recipeName, RecipeIngredients.ingredientQuantity FROM RecipeIngredients JOIN Recipes ON RecipeIngredients.recipeID = Recipes.recipeID WHERE RecipeIngredients.ingredientID = {ingredient_id}")
        return "RecipesByIngredientView"
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def query_user_favorite_ingredients(cursor, user_id):
    try:
        cursor.execute(f"CREATE TEMP VIEW IF NOT EXISTS UserFavIngredientsView AS SELECT UserFavoriteIngredients.ingredientID, IngredientItem.ingredientName FROM UserFavoriteIngredients JOIN IngredientItem ON UserFavoriteIngredients.ingredientID = IngredientItem.ingredientID WHERE UserFavoriteIngredients.userID = {user_id}")
        return "UserFavIngredientsView"
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def query_user_favorite_recipes(cursor, user_id):
    try:
        cursor.execute(f"CREATE TEMP VIEW IF NOT EXISTS UserFavRecipesView AS SELECT UserFavoriteRecipes.recipeID, Recipes.recipeName FROM UserFavoriteRecipes JOIN Recipes ON UserFavoriteRecipes.recipeID = Recipes.recipeID WHERE UserFavoriteRecipes.userID = {user_id}")
        return "UserFavRecipesView"
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def calculate_recipe_nutrition(cursor, recipe_id):
    try:
        cursor.execute(f"""
        CREATE TEMP VIEW IF NOT EXISTS RecipeNutritionView AS 
        SELECT 
            SUM(IngredientItem.Calories_per_100g * RecipeIngredients.ingredientQuantity / 100) as TotalCalories,
            SUM(IngredientItem.Protein_g * RecipeIngredients.ingredientQuantity / 100) as TotalProtein,
            SUM(IngredientItem.Carbohydrates_g * RecipeIngredients.ingredientQuantity / 100) as TotalCarbs,
            SUM(IngredientItem.Fat_g * RecipeIngredients.ingredientQuantity / 100) as TotalFat
        FROM RecipeIngredients
        JOIN IngredientItem ON RecipeIngredients.ingredientID = IngredientItem.ingredientID
        WHERE RecipeIngredients.recipeID = {recipe_id}
        """)
        return "RecipeNutritionView"
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()

q1 = filter_ingredient_column(cursor, "Cholesterol_mg", 20, 100)
print_view(cursor, q1)

connection.close()