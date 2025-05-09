import pandas as pd
import sqlite3
import json
import os


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


def drop_user_favorite(cursor, json_path):
    try:
        with open(json_path, 'r') as f:
            favorite_data = json.load(f)

        # Validate required fields
        required_fields = ['userName', 'userPassword', 'type', 'itemID']
        for field in required_fields:
            if field not in favorite_data:
                print(f"Error: Missing required field '{field}' in JSON file.")
                return False

        username = favorite_data['userName']
        password = favorite_data['userPassword']
        favorite_type = favorite_data['type'].lower()
        item_id = favorite_data['itemID']

        # Get userID from credentials
        cursor.execute(
            "SELECT userID FROM Users WHERE userName = ? AND userPassword = ?",
            (username, password)
        )
        user = cursor.fetchone()
        
        if not user:
            print("Error: Invalid username or password")
            return False
            
        user_id = user[0]

        if favorite_type == "ingredient":
            # Check if favorite exists
            cursor.execute(
                "SELECT 1 FROM UserFavoriteIngredients WHERE userID = ? AND ingredientID = ?",
                (user_id, item_id))
            if not cursor.fetchone():
                print(f"Error: Ingredient {item_id} is not in user {username}'s favorites.")
                return False
            
            # Remove favorite ingredient
            cursor.execute(
                "DELETE FROM UserFavoriteIngredients WHERE userID = ? AND ingredientID = ?",
                (user_id, item_id)
            )
            print(f"Removed ingredient {item_id} from favorites for user {username}")
            return True

        elif favorite_type == "recipe":
            # Check if favorite exists
            cursor.execute(
                "SELECT 1 FROM UserFavoriteRecipes WHERE userID = ? AND recipeID = ?",
                (user_id, item_id))
            if not cursor.fetchone():
                print(f"Error: Recipe {item_id} is not in user {username}'s favorites.")
                return False
            
            # Remove favorite recipe
            cursor.execute(
                "DELETE FROM UserFavoriteRecipes WHERE userID = ? AND recipeID = ?",
                (user_id, item_id)
            )
            print(f"Removed recipe {item_id} from favorites for user {username}")
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
        print(f"Error removing user favorite: {str(e)}")
        return False