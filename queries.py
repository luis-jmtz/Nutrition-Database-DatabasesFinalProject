import pandas as pd
import sqlite3
import json


def show_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])


def view_table(cursor, table_name, max_rows=10, max_columns=None):
    
    try:        
        cursor.execute(f"SELECT * FROM {table_name};")

        #gets all rows and column names
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        df = pd.DataFrame(rows, columns=column_names)

        # Configure pandas display options
        pd.set_option("display.max_rows", max_rows)  # Limit the number of rows displayed
        if max_columns:
            pd.set_option("display.max_columns", max_columns)  # Limit the number of columns displayed

        print(f"Contents of table '{table_name}':")
        print(df)
    except:
        print(f"'{table_name}' could not be printed. Check that table exists and that the name is spelled correctly")


def print_view(cursor, view_name, max_rows=10, max_columns=None):
    cursor.execute(f"SELECT * FROM {view_name}") #select all from
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_columns):
        print(pd.DataFrame(rows, columns=columns))


def query_recipes_by_ingredient(cursor, ingredient_id):
    try:
        
        cursor.execute(f"CREATE TEMP VIEW IF NOT EXISTS RecipesByIngredientView AS SELECT RecipeIngredients.recipeID, Recipes.recipeName, RecipeIngredients.ingredientQuantity FROM RecipeIngredients JOIN Recipes ON RecipeIngredients.recipeID = Recipes.recipeID WHERE RecipeIngredients.ingredientID = {ingredient_id}")
        return "RecipesByIngredientView"
    
    except Exception as e:
        print(f"Error: {str(e)}")
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


def query_user_favorites(cursor, json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        #type: recipe OR ingredient

        user_id = data.get("userID")
        favorite_type = data.get("type")

        # gets fields from JSON data
        if not user_id or not favorite_type:
            print("Error: 'userID' and 'type' fields are required in the JSON file.")
            return None

        # Checks if user exists
        cursor.execute(f"SELECT 1 FROM Users WHERE userID = {user_id}")
        if not cursor.fetchone():
            print(f"Error: User with ID {user_id} doesn't exist.")
            return None

        view_name = f"UserFavoritesView_{user_id}"

        # handles ingredient favorites
        if favorite_type.lower() == "ingredient":
            cursor.execute(f"""
                CREATE TEMP VIEW IF NOT EXISTS {view_name} AS 
                SELECT 
                    UserFavoriteIngredients.ingredientID as itemID, 
                    IngredientItem.ingredientName as itemName,
                    'ingredient' as itemType
                FROM UserFavoriteIngredients 
                JOIN IngredientItem ON UserFavoriteIngredients.ingredientID = IngredientItem.ingredientID 
                WHERE UserFavoriteIngredients.userID = {user_id}
            """)
            
            print(f"Created view for user {user_id}'s favorite ingredients")
            return view_name

        elif favorite_type.lower() == "recipe": # handles recipes
            cursor.execute(f"""
                CREATE TEMP VIEW IF NOT EXISTS {view_name} AS 
                SELECT 
                    UserFavoriteRecipes.recipeID as itemID, 
                    Recipes.recipeName as itemName,
                    'recipe' as itemType
                FROM UserFavoriteRecipes 
                JOIN Recipes ON UserFavoriteRecipes.recipeID = Recipes.recipeID 
                WHERE UserFavoriteRecipes.userID = {user_id}
            """)
            print(f"Created view for user {user_id}'s favorite recipes")
            return view_name

        # Handle both favorites case
        elif favorite_type.lower() == "both":
            cursor.execute(f"""
                CREATE TEMP VIEW IF NOT EXISTS {view_name} AS
                -- Combine favorite ingredients with their names
                SELECT 
                    UserFavoriteIngredients.ingredientID as itemID,
                    IngredientItem.ingredientName as itemName,
                    'ingredient' as itemType
                FROM UserFavoriteIngredients
                JOIN IngredientItem ON UserFavoriteIngredients.ingredientID = IngredientItem.ingredientID
                WHERE UserFavoriteIngredients.userID = {user_id}
                
                UNION ALL
                
                -- Combine favorite recipes with their names
                SELECT 
                    UserFavoriteRecipes.recipeID as itemID,
                    Recipes.recipeName as itemName,
                    'recipe' as itemType
                FROM UserFavoriteRecipes
                JOIN Recipes ON UserFavoriteRecipes.recipeID = Recipes.recipeID
                WHERE UserFavoriteRecipes.userID = {user_id}
                
                -- Optional: Add sorting if desired
                ORDER BY itemType, itemName
            """)
            print(f"Created combined view for user {user_id}'s favorite ingredients and recipes")
            return view_name


        else:
            print(f"Error: Invalid type '{favorite_type}'. Must be 'ingredient' or 'recipe'.")
            return None

    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return None
    except Exception as e:
        print(f"Error querying user favorites: {str(e)}")
        return None


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


def check_user_exists(cursor, username, password = None):
    try:
        if password:
            cursor.execute(
                f"SELECT 1 FROM Users WHERE userName = '{username}' AND userPassword = '{password}'"
            )
        else:
            cursor.execute(
                f"SELECT 1 FROM Users WHERE userName = '{username}'"
            )
            
        return cursor.fetchone() is not None
        
    except Exception as e:
        print(f"Error checking user existence: {str(e)}")
        return False


def add_user(cursor, json_path):
    try:
        with open(json_path, 'r') as f:
            user_data = json.load(f)

        username = user_data.get("userName")
        password = user_data.get("userPassword")

        if not username or not password:
            print("Error: 'userName' and 'userPassword' fields are required in the JSON file.")
            return False

        if check_user_exists(cursor, username):
            print(f"User '{username}' already exists.")
            return False

        cursor.execute(
            "INSERT INTO Users (userName, userPassword) VALUES (?, ?)", (username, password)
        )
        print(f"User '{username}' added successfully")
        return True

    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return False
    except Exception as e:
        print(f"Error adding user: {str(e)}")
        return False


def add_admin(cursor, userID):
    query = "INSERT INTO Admins (userID) VALUES (?)"
    cursor.execute(query, (userID,))
    
    
def is_admin(cursor, user_id):
    try:
        cursor.execute("SELECT 1 FROM Admins WHERE userID = ?", (user_id,))
        return cursor.fetchone() is not None #returns true if the value it got is not-None
    
    except Exception as e:
        print(f"Error checking admin status: {str(e)}")
        return False



def add_user_favorite(cursor, json_path):

    try:
        with open(json_path, 'r') as f:
            favorite_data = json.load(f)

        user_id = favorite_data.get("userID")
        favorite_type = favorite_data.get("type")
        item_id = favorite_data.get("itemID")

        if not all([user_id, favorite_type, item_id]):
            print("Error: 'userID', 'type', and 'itemID' fields are required in the JSON file.")
            return False

        # Check if user exists
        cursor.execute(f"SELECT 1 FROM Users WHERE userID = {user_id}")
        if not cursor.fetchone():
            print(f"Error: User with ID {user_id} doesn't exist.")
            return False

        if favorite_type.lower() == "ingredient":
            # Check if ingredient exists
            cursor.execute(f"SELECT 1 FROM IngredientItem WHERE ingredientID = {item_id}")
            if not cursor.fetchone():
                print(f"Error: Ingredient with ID {item_id} doesn't exist.")
                return False
            
            # Check if favorite already exists
            cursor.execute(
                f"SELECT 1 FROM UserFavoriteIngredients WHERE userID = {user_id} AND ingredientID = {item_id}"
            )
            if cursor.fetchone():
                print(f"Error: Ingredient {item_id} is already a favorite for user {user_id}.")
                return False
            
            # Add favorite ingredient
            cursor.execute(
                "INSERT INTO UserFavoriteIngredients (userID, ingredientID) VALUES (?, ?)",
                (user_id, item_id)
            )
            print(f"Added ingredient {item_id} to favorites for user {user_id}")
            return True

        elif favorite_type.lower() == "recipe":
            # Check if recipe exists
            cursor.execute(f"SELECT 1 FROM Recipes WHERE recipeID = {item_id}")
            if not cursor.fetchone():
                print(f"Error: Recipe with ID {item_id} doesn't exist.")
                return False
            
            # Check if favorite already exists
            cursor.execute(
                f"SELECT 1 FROM UserFavoriteRecipes WHERE userID = {user_id} AND recipeID = {item_id}"
            )
            if cursor.fetchone():
                print(f"Error: Recipe {item_id} is already a favorite for user {user_id}.")
                return False
            
            # Add favorite recipe
            cursor.execute(
                "INSERT INTO UserFavoriteRecipes (userID, recipeID) VALUES (?, ?)",
                (user_id, item_id)
            )
            print(f"Added recipe {item_id} to favorites for user {user_id}")
            return True

        else:
            print(f"Error: Invalid type '{favorite_type}'. Must be 'ingredient' or 'recipe'.")
            return False

    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return False
    except Exception as e:
        print(f"Error adding user favorite: {str(e)}")
        return False