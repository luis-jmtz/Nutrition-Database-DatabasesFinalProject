import pandas as pd
import sqlite3
import json

def calculate_recipe_nutrition(cursor, recipe_id):
    try:
        cursor.execute(f"""
        CREATE TEMP VIEW IF NOT EXISTS RecipeNutritionView AS 
        SELECT 
            -- Calculated totals
            SUM(IngredientItem.Calories_per_100g * RecipeIngredients.ingredientQuantity / 100) as TotalCalories,
            SUM(IngredientItem.Protein_g * RecipeIngredients.ingredientQuantity / 100) as TotalProtein,
            SUM(IngredientItem.Carbohydrates_g * RecipeIngredients.ingredientQuantity / 100) as TotalCarbs,
            SUM(IngredientItem.Fat_g * RecipeIngredients.ingredientQuantity / 100) as TotalFat,
            
            -- All other nutritional columns with their calculated totals
            SUM(IngredientItem.SaturatedFats_g * RecipeIngredients.ingredientQuantity / 100) as TotalSaturatedFats,
            SUM(IngredientItem.MonounsaturatedFats_g * RecipeIngredients.ingredientQuantity / 100) as TotalMonounsaturatedFats,
            SUM(IngredientItem.PolyunsaturatedFats_g * RecipeIngredients.ingredientQuantity / 100) as TotalPolyunsaturatedFats,
            SUM(IngredientItem.Sugars_g * RecipeIngredients.ingredientQuantity / 100) as TotalSugars,
            SUM(IngredientItem.DietaryFiber_g * RecipeIngredients.ingredientQuantity / 100) as TotalDietaryFiber,
            SUM(IngredientItem.Cholesterol_mg * RecipeIngredients.ingredientQuantity / 100) as TotalCholesterol,
            SUM(IngredientItem.Sodium_mg * RecipeIngredients.ingredientQuantity / 100) as TotalSodium,
            SUM(IngredientItem.Water_g * RecipeIngredients.ingredientQuantity / 100) as TotalWater,
            SUM(IngredientItem.VitaminA_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminA,
            SUM(IngredientItem.VitaminB1_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminB1,
            SUM(IngredientItem.VitaminB11_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminB11,
            SUM(IngredientItem.VitaminB12_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminB12,
            SUM(IngredientItem.VitaminB2_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminB2,
            SUM(IngredientItem.VitaminB3_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminB3,
            SUM(IngredientItem.VitaminB5_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminB5,
            SUM(IngredientItem.VitaminB6_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminB6,
            SUM(IngredientItem.VitaminC_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminC,
            SUM(IngredientItem.VitaminD_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminD,
            SUM(IngredientItem.VitaminE_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminE,
            SUM(IngredientItem.VitaminK_mg * RecipeIngredients.ingredientQuantity / 100) as TotalVitaminK,
            SUM(IngredientItem.Calcium_mg * RecipeIngredients.ingredientQuantity / 100) as TotalCalcium,
            SUM(IngredientItem.Copper_mg * RecipeIngredients.ingredientQuantity / 100) as TotalCopper,
            SUM(IngredientItem.Iron_mg * RecipeIngredients.ingredientQuantity / 100) as TotalIron,
            SUM(IngredientItem.Magnesium_mg * RecipeIngredients.ingredientQuantity / 100) as TotalMagnesium,
            SUM(IngredientItem.Manganese_mg * RecipeIngredients.ingredientQuantity / 100) as TotalManganese,
            SUM(IngredientItem.Phosphorus_mg * RecipeIngredients.ingredientQuantity / 100) as TotalPhosphorus,
            SUM(IngredientItem.Potassium_mg * RecipeIngredients.ingredientQuantity / 100) as TotalPotassium,
            SUM(IngredientItem.Selenium_mg * RecipeIngredients.ingredientQuantity / 100) as TotalSelenium,
            SUM(IngredientItem.Zinc_mg * RecipeIngredients.ingredientQuantity / 100) as TotalZinc,
            SUM(IngredientItem.NutritionDensity * RecipeIngredients.ingredientQuantity / 100) as TotalNutritionDensity,
            
            -- Include recipe information for reference
            Recipes.recipeID,
            Recipes.recipeName,
            Recipes.recipeDescription
            
        FROM RecipeIngredients
        JOIN IngredientItem ON RecipeIngredients.ingredientID = IngredientItem.ingredientID
        JOIN Recipes ON RecipeIngredients.recipeID = Recipes.recipeID
        WHERE RecipeIngredients.recipeID = {recipe_id}
        GROUP BY Recipes.recipeID, Recipes.recipeName, Recipes.recipeDescription
        """)
        return "RecipeNutritionView"
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def submit_recipe_for_approval(cursor, json_path):
    try:
        with open(json_path, 'r') as f:  # opens and reads files
            recipe_data = json.load(f)

        # validates required fields
        required_fields = ['recipeName', 'recipeDescription', 'ingredients']
        
        for field in required_fields:
            if field not in recipe_data:
                print(f"Error: Missing {field} field")
                return False
            
        # checks that all of the ingredients exist in the database
        for ingredient in recipe_data['ingredients']:
            cursor.execute(
                "SELECT 1 FROM IngredientItem WHERE ingredientID = ?", 
                (ingredient['ingredientID'],)
            )
            if not cursor.fetchone():
                print(f"IngredientID {ingredient['ingredientID']} does not exist")
                return False
    
        # insert into PendingRecipes
        cursor.execute(
            """INSERT INTO PendingRecipes 
               (recipeName, recipeDescription) 
               VALUES (?, ?)""",
            (recipe_data['recipeName'], recipe_data['recipeDescription'])
        )
        pending_id = cursor.lastrowid  # saves id so it can be referenced for pendingIngredients

        # inserts ingredients into PendingRecipeIngredients
        for ingredient in recipe_data['ingredients']:
            cursor.execute(
                """INSERT INTO PendingRecipeIngredients 
                   (pendingID, ingredientID, ingredientQuantity) 
                   VALUES (?, ?, ?)""",
                (pending_id, ingredient['ingredientID'], ingredient['ingredientQuantity'])
            )

        print(f"Recipe submitted for approval with pendingID: {pending_id}")
        return True

    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return False
    except Exception as e:
        print(f"Error submitting recipe for approval: {str(e)}")
        return False