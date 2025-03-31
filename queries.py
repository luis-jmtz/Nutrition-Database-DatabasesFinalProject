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