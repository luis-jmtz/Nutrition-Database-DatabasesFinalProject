import sqlite3
import pandas as pd

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()

# csv_files = ["user_ingredient_favorites.csv"]

csv_files = ["user_recipe_favorites.csv"]

# loops through each csv file
for csv_file in csv_files:
    
    df = pd.read_csv(csv_file)

    # Clean column names (remove spaces and special characters)
    df.columns = df.columns.str.replace(" ", "")

    # df = df.rename(columns={
    #     "UserID": "userID",
    #     "IgredientID": "ingredientID",
    #     "SavedDate": "savedDate"
    # })

    df = df.rename(columns={
        "UserID": "userID",
        "RecipeID": "recipeID",
        "SavedDate": "savedDate"
    })

    # Insert data into the FoodItem table
    df.to_sql("UserFavoriteRecipes", connection, if_exists="append", index=False)

connection.commit()
connection.close()

print("Data insertion complete")