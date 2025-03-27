import sqlite3
import pandas as pd

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()

csv_files = ["recipes.csv"]

for csv_file in csv_files:
    
    df = pd.read_csv(csv_file)

    # Clean column names (remove spaces and special characters)
    df.columns = df.columns.str.replace(" ", "")

    df = df.rename(columns={
        "RecipeName": "recipeName",
        "RecipeDescription": "recipeDescription"
    })

    df.to_sql("Recipes", connection, if_exists="append", index=False)

connection.commit()
connection.close()

print("Data insertion complete")