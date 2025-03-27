import sqlite3
import pandas as pd

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()

csv_files = ["subset1.csv", "subset2.csv", "subset3.csv", "subset4.csv", "subset5.csv"]

# loops through each csv file
for csv_file in csv_files:
    
    df = pd.read_csv(csv_file)

    # Clean column names (remove spaces and special characters)
    df.columns = df.columns.str.replace(" ", "")

    df = df.rename(columns={
        "food": "ingredientName",
        "CaloricValue": "Calories_per_100g",
        "Fat": "Fat_g",
        "SaturatedFats": "SaturatedFats_g",
        "MonounsaturatedFats": "MonounsaturatedFats_g",
        "PolyunsaturatedFats": "PolyunsaturatedFats_g",
        "Carbohydrates": "Carbohydrates_g",
        "Sugars": "Sugars_g",
        "Protein": "Protein_g",
        "DietaryFiber": "DietaryFiber_g",
        "Cholesterol": "Cholesterol_mg",
        "Sodium": "Sodium_mg",
        "Water": "Water_g",
        "VitaminA": "VitaminA_mg",
        "VitaminB1": "VitaminB1_mg",
        "VitaminB11": "VitaminB11_mg",
        "VitaminB12": "VitaminB12_mg",
        "VitaminB2": "VitaminB2_mg",
        "VitaminB3": "VitaminB3_mg",
        "VitaminB5": "VitaminB5_mg",
        "VitaminB6": "VitaminB6_mg",
        "VitaminC": "VitaminC_mg",
        "VitaminD": "VitaminD_mg",
        "VitaminE": "VitaminE_mg",
        "VitaminK": "VitaminK_mg",
        "Calcium": "Calcium_mg",
        "Copper": "Copper_mg",
        "Iron": "Iron_mg",
        "Magnesium": "Magnesium_mg",
        "Manganese": "Manganese_mg",
        "Phosphorus": "Phosphorus_mg",
        "Potassium": "Potassium_mg",
        "Selenium": "Selenium_mg",
        "Zinc": "Zinc_mg",
        "NutritionDensity": "NutritionDensity"
    })

    # Insert data into the FoodItem table
    df.to_sql("IngredientItem", connection, if_exists="append", index=False)

connection.commit()
connection.close()

print("Data insertion complete")