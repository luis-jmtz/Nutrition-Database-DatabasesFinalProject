import pandas as pd
import sqlite3


def print_df(dataframe, max_rows = 10, max_columns = None):
    
    with pd.option_context('display.max_rows', max_rows,
                            'display.max_columns', max_columns):
        print(dataframe)


def query_ingredients_by_calories(cursor, min_calories, max_calories):

    try:
        # SQL Query
        query = f"""
        SELECT ingredientID, ingredientName, Calories_per_100g
        FROM IngredientItem
        WHERE Calories_per_100g BETWEEN {min_calories} AND {max_calories}
        """

        cursor.execute(query)

        #gets results and column names
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(rows, columns= columns)
        return df
    
    except Exception as e:
        print(f"Error querying ingredients: {str(e)}")

        return None


def query_ingredients_by_NutritionDensity(cursor, min_density, max_density):

    try:
        # SQL Query
        query = f"""
        SELECT ingredientID, ingredientName, NutritionDensity
        FROM IngredientItem
        WHERE NutritionDensity BETWEEN {min_density} AND {max_density}
        """

        cursor.execute(query)

        #gets results and column names
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(rows, columns= columns)
        return df
    
    except Exception as e:
        print(f"Error querying ingredients: {str(e)}")

        return None


def query_recipes_by_ingredient(cursor, ingredient_id):
    try:
        query = f"""
        SELECT RecipeIngredients.recipeID, Recipes.recipeName, RecipeIngredients.ingredientQuantity
        FROM RecipeIngredients
        JOIN Recipes ON RecipeIngredients.recipeID = Recipes.recipeID
        WHERE RecipeIngredients.ingredientID = {ingredient_id}
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    
    except Exception as e:
        print(f"Error querying recipes: {str(e)}")
        return None


def query_user_favorite_ingredients(cursor, user_id):

    try:
        query = f"""
        SELECT UserFavoriteIngredients.ingredientID, IngredientItem.ingredientName
        FROM UserFavoriteIngredients
        JOIN IngredientItem ON UserFavoriteIngredients.ingredientID = IngredientItem.ingredientID
        WHERE UserFavoriteIngredients.userID = {user_id}
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        print(f"Error querying favorite ingredients: {str(e)}")
        return None

def query_user_favorite_recipes(cursor, user_id):

    try:
        query = f"""
        SELECT UserFavoriteRecipes.recipeID, Recipes.recipeName
        FROM UserFavoriteRecipes
        JOIN Recipes ON UserFavoriteRecipes.recipeID = Recipes.recipeID
        WHERE UserFavoriteRecipes.userID = {user_id}
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        print(f"Error querying favorite recipes: {str(e)}")
        return None
    
    
def calculate_recipe_nutrition(cursor, recipe_id):
    try:
        query = f"""
        SELECT 
            SUM(IngredientItem.Calories_per_100g * RecipeIngredients.ingredientQuantity / 100) as TotalCalories,
            SUM(IngredientItem.Protein_g * RecipeIngredients.ingredientQuantity / 100) as TotalProtein,
            SUM(IngredientItem.Carbohydrates_g * RecipeIngredients.ingredientQuantity / 100) as TotalCarbs,
            SUM(IngredientItem.Fat_g * RecipeIngredients.ingredientQuantity / 100) as TotalFat
        FROM RecipeIngredients
        JOIN IngredientItem ON RecipeIngredients.ingredientID = IngredientItem.ingredientID
        WHERE RecipeIngredients.recipeID = {recipe_id}
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return df
    except Exception as e:
        print(f"Error calculating nutrition: {str(e)}")
        return None