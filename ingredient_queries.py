import pandas as pd
import sqlite3
import json
import os


def query_recipes_by_ingredient(cursor, ingredient_id):
    try:
        
        cursor.execute(f"CREATE TEMP VIEW IF NOT EXISTS RecipesByIngredientView AS SELECT RecipeIngredients.recipeID, Recipes.recipeName, RecipeIngredients.ingredientQuantity FROM RecipeIngredients JOIN Recipes ON RecipeIngredients.recipeID = Recipes.recipeID WHERE RecipeIngredients.ingredientID = {ingredient_id}")
        return "RecipesByIngredientView"
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def search_ingredient_name(cursor, search_text='', order=0):
    try:
        # Determine the ORDER BY clause based on the order parameter
        order_clause = ""
        if order == 1:
            order_clause = "ORDER BY ingredientName ASC"
        elif order == 2:
            order_clause = "ORDER BY ingredientName DESC"
        
        cursor.execute(f"""
            CREATE TEMP VIEW SearchedIngredient AS
            SELECT ingredientID, ingredientName
            FROM IngredientItem 
            WHERE ingredientName LIKE '%{search_text}%'
            {order_clause}
        """)
        return "SearchedIngredient"
    
    except Exception as e:
        print(f"Error: {e}")
        return None


def loop_filter_ingredients(cursor, json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        # gets column names and their min/max values from JSON
        columns = list(data.keys())
        min_values = [data[col][0] for col in columns]
        max_values = [data[col][1] for col in columns]

        query = f"CREATE TEMP VIEW IF NOT EXISTS IngredientLoopFilterView AS "
        query += "SELECT * FROM IngredientItem WHERE "
        
        # List to store individual filter conditions
        conditions = []

        for i, column_name in enumerate(columns):
            
            # Skips ingredientID since doesn't filter it directly
            if column_name == 'ingredientID':
                continue

            # Gets the min and max values for current column
            min_val = min_values[i]
            max_val = max_values[i]

            # skips column if the max AND min are empty
            if min_val == -1 and max_val == -1:
                continue

            # List to store conditions for current column
            col_conditions = []
            if min_val != -1:
                col_conditions.append(f"{column_name} >= {min_val}")
            if max_val != -1:
                col_conditions.append(f"{column_name} <= {max_val}")

            if col_conditions:
                conditions.append("(" + " AND ".join(col_conditions) + ")")

        if not conditions:
            query = query.replace("WHERE", "")
        else:
            query += " AND ".join(conditions)

        cursor.execute(query)
        print(f"Created combined filter view: IngredientLoopFilterView")
        return "IngredientLoopFilterView"

    except Exception as e:
        print(f"Error processing JSON: {str(e)}")
        return None

def search_ingredients(cursor, json_path, search_text='', order=0):
    try:
        
        # Apply text search filter
        search_view = search_ingredient_name(cursor, search_text, order)
        if not search_view:
            return None
            
        # Apply numeric filters
        filter_view = loop_filter_ingredients(cursor, json_path)
        if not filter_view:
            return None
            
        # Create combined view
        combined_view = "FilteredIngredients"
        cursor.execute(f"""
            CREATE TEMP VIEW IF NOT EXISTS {combined_view} AS
            SELECT IngredientItem.* 
            FROM IngredientItem
            WHERE ingredientID IN (
                SELECT ingredientID FROM {search_view}
            )
            AND ingredientID IN (
                SELECT ingredientID FROM {filter_view}
            )
        """)
        
        return combined_view
        
    except Exception as e:
        print(f"Error in search_ingredients: {str(e)}")
        return None
