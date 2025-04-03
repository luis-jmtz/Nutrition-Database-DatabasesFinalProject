import pandas as pd
import sqlite3

def print_view(cursor, view_name, max_rows=10, max_columns=None):
    cursor.execute(f"SELECT * FROM {view_name}") #select all from
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


def loop_filter_ingredients(cursor, csv_path, view_name="IngredientLoopFilterView"):
    try:
        df = pd.read_csv(csv_path)
        columns = df.columns
        min_values = df.iloc[0].values
        max_values = df.iloc[1].values
        
        query = f"CREATE TEMP VIEW IF NOT EXISTS {view_name} AS "
        query += "SELECT * FROM IngredientItem WHERE "
        
        conditions = []
        
        for i, column_name in enumerate(columns):
            if column_name == 'ingredientID':
                continue
                
            min_val = min_values[i]
            max_val = max_values[i]
            
            if min_val == -1 and max_val == -1:
                continue
                
            col_conditions = []
            if min_val != -1:
                col_conditions.append(f"{column_name} >= {min_val}")
            if max_val != -1:
                col_conditions.append(f"{column_name} <= {max_val}")
                
            if col_conditions:
                conditions.append("(" + " AND ".join(col_conditions) + ")")
        
        if not conditions:
            query = query.replace("WHERE", "")  # No filters case
        else:
            query += " AND ".join(conditions)
        
        cursor.execute(query)
        print(f"Created combined filter view: {view_name}")
        return view_name
        
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
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



def add_user(cursor, text_file_path):

    try:
        #extracts text data
        with open(text_file_path, 'r') as f:
            data = f.read().strip().split(',')
            
        if len(data) != 2:
            print(f"Error: Invalid format in {text_file_path}. Expected 'userName,userPassword'")
            return False
            
        username, password = data[0].strip(), data[1].strip()
        
        if check_user_exists(cursor, username, password) == False:
            print("Invalid username or password")
            return False
        
        cursor.execute(
            f"INSERT INTO Users (userName, userPassword) VALUES ('{username}', '{password}')"
        )
        print(f"User '{username}' added successfully")
        return True
        
    except FileNotFoundError:
        print(f"Error: File not found at {text_file_path}")
        return False
    except Exception as e:
        print(f"Error adding user: {str(e)}")
        return False