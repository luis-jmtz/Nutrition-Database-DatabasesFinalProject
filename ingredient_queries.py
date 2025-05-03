import pandas as pd
import sqlite3
import json
import os
from user_queries import is_admin




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


def submit_ingredient_for_approval(cursor, json_path):
    try:
        with open(json_path, 'r') as f:
            ingredient_data = json.load(f)

        # Validate required fields
        if 'ingredientName' not in ingredient_data or 'Calories_per_100g' not in ingredient_data:
            print("Error: 'ingredientName' and 'Calories_per_100g' fields are required")
            return False

        # Insert into PendingIngredientItem table
        cursor.execute("""
            INSERT INTO PendingIngredientItem (
                ingredientName, Calories_per_100g, Fat_g, SaturatedFats_g, MonounsaturatedFats_g,
                PolyunsaturatedFats_g, Carbohydrates_g, Sugars_g, Protein_g, DietaryFiber_g,
                Cholesterol_mg, Sodium_mg, Water_g, VitaminA_mg, VitaminB1_mg, VitaminB11_mg,
                VitaminB12_mg, VitaminB2_mg, VitaminB3_mg, VitaminB5_mg, VitaminB6_mg,
                VitaminC_mg, VitaminD_mg, VitaminE_mg, VitaminK_mg, Calcium_mg, Copper_mg,
                Iron_mg, Magnesium_mg, Manganese_mg, Phosphorus_mg, Potassium_mg,
                Selenium_mg, Zinc_mg, NutritionDensity
            ) VALUES (
                :ingredientName, :Calories_per_100g, :Fat_g, :SaturatedFats_g, :MonounsaturatedFats_g,
                :PolyunsaturatedFats_g, :Carbohydrates_g, :Sugars_g, :Protein_g, :DietaryFiber_g,
                :Cholesterol_mg, :Sodium_mg, :Water_g, :VitaminA_mg, :VitaminB1_mg, :VitaminB11_mg,
                :VitaminB12_mg, :VitaminB2_mg, :VitaminB3_mg, :VitaminB5_mg, :VitaminB6_mg,
                :VitaminC_mg, :VitaminD_mg, :VitaminE_mg, :VitaminK_mg, :Calcium_mg, :Copper_mg,
                :Iron_mg, :Magnesium_mg, :Manganese_mg, :Phosphorus_mg, :Potassium_mg,
                :Selenium_mg, :Zinc_mg, :NutritionDensity
            )
        """, ingredient_data)

        pending_id = cursor.lastrowid
        print(f"Ingredient submitted for approval with pendingID: {pending_id}")
        return True

    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return False
    except Exception as e:
        print(f"Error submitting ingredient for approval: {str(e)}")
        return False


def ingredient_approval_rejection(cursor, json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Extract required fields
        pending_id = data.get("pendingID")
        action = data.get("action")  # "approve" or "reject"
        username = data.get("userName")
        password = data.get("userPassword")

        # Validate required fields
        if not all([pending_id, action, username, password]):
            print("Error: Missing required fields in JSON (pendingID, action, userName, userPassword)")
            return None

        # Check if user exists and get userID
        cursor.execute(
            "SELECT userID FROM Users WHERE userName = ? AND userPassword = ?",
            (username, password)
        )
        user = cursor.fetchone()
        
        if not user:
            print("Error: Invalid username or password")
            return None

        user_id = user[0]

        # Verify admin status
        if not is_admin(cursor, user_id):
            print("Error: Only admins can approve or reject ingredients")
            return None

        # Handle approval
        if action.lower() == "approve":
            # Get the pending ingredient
            cursor.execute("""
                SELECT * FROM PendingIngredientItem 
                WHERE pendingID = ?
            """, (pending_id,))
            ingredient = cursor.fetchone()
            
            if not ingredient:
                print(f"Error: Pending ingredient with ID {pending_id} not found.")
                return None
                
            # Get column names (excluding pendingID)
            cursor.execute("PRAGMA table_info(PendingIngredientItem)")
            columns = [col[1] for col in cursor.fetchall() if col[1] != "pendingID"]
            
            # Create dictionary mapping column names to values
            ingredient_dict = dict(zip(columns, ingredient[1:]))
            
            # Insert into IngredientItem table
            cursor.execute("""
                INSERT INTO IngredientItem (
                    ingredientName, Calories_per_100g, Fat_g, SaturatedFats_g, MonounsaturatedFats_g,
                    PolyunsaturatedFats_g, Carbohydrates_g, Sugars_g, Protein_g, DietaryFiber_g,
                    Cholesterol_mg, Sodium_mg, Water_g, VitaminA_mg, VitaminB1_mg, VitaminB11_mg,
                    VitaminB12_mg, VitaminB2_mg, VitaminB3_mg, VitaminB5_mg, VitaminB6_mg,
                    VitaminC_mg, VitaminD_mg, VitaminE_mg, VitaminK_mg, Calcium_mg, Copper_mg,
                    Iron_mg, Magnesium_mg, Manganese_mg, Phosphorus_mg, Potassium_mg,
                    Selenium_mg, Zinc_mg, NutritionDensity
                ) VALUES (
                    :ingredientName, :Calories_per_100g, :Fat_g, :SaturatedFats_g, :MonounsaturatedFats_g,
                    :PolyunsaturatedFats_g, :Carbohydrates_g, :Sugars_g, :Protein_g, :DietaryFiber_g,
                    :Cholesterol_mg, :Sodium_mg, :Water_g, :VitaminA_mg, :VitaminB1_mg, :VitaminB11_mg,
                    :VitaminB12_mg, :VitaminB2_mg, :VitaminB3_mg, :VitaminB5_mg, :VitaminB6_mg,
                    :VitaminC_mg, :VitaminD_mg, :VitaminE_mg, :VitaminK_mg, :Calcium_mg, :Copper_mg,
                    :Iron_mg, :Magnesium_mg, :Manganese_mg, :Phosphorus_mg, :Potassium_mg,
                    :Selenium_mg, :Zinc_mg, :NutritionDensity
                )
            """, ingredient_dict)
            
            ingredient_id = cursor.lastrowid
            
            # Delete from pending table
            cursor.execute("DELETE FROM PendingIngredientItem WHERE pendingID = ?", (pending_id,))
            
            print(f"Ingredient approved and added to main table with ingredientID: {ingredient_id}")
            return ingredient_id

        # Handle rejection
        elif action.lower() == "reject":
            # Verify ingredient exists
            cursor.execute("SELECT 1 FROM PendingIngredientItem WHERE pendingID = ?", (pending_id,))
            if not cursor.fetchone():
                print(f"Error: Pending ingredient with ID {pending_id} not found.")
                return False
                
            # Delete from pending table
            cursor.execute("DELETE FROM PendingIngredientItem WHERE pendingID = ?", (pending_id,))
            
            print(f"Ingredient with pendingID {pending_id} rejected and removed.")
            return True

        else:
            print(f"Error: Invalid action '{action}'. Must be 'approve' or 'reject'.")
            return None

    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None
    except Exception as e:
        print(f"Error in ingredient_approval_rejection: {str(e)}")
        return None
