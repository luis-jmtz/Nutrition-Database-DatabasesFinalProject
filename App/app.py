from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from queries import loop_filter_ingredients, print_view
import json
import os
app = Flask(__name__)

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()


# List of all the filterable columns from IngredientItem table
filter_columns = [
    'Calories_per_100g', 'Protein_g', 'Fat_g', 'SaturatedFats_g',
    'MonounsaturatedFats_g', 'PolyunsaturatedFats_g', 'Carbohydrates_g',
    'Sugars_g', 'DietaryFiber_g', 'Cholesterol_mg', 'Sodium_mg',
    'Water_g', 'VitaminA_mg', 'VitaminB1_mg', 'VitaminB11_mg',
    'VitaminB12_mg', 'VitaminB2_mg', 'VitaminB3_mg', 'VitaminB5_mg',
    'VitaminB6_mg', 'VitaminC_mg', 'VitaminD_mg', 'VitaminE_mg',
    'VitaminK_mg', 'Calcium_mg', 'Copper_mg', 'Iron_mg', 'Magnesium_mg',
    'Manganese_mg', 'Phosphorus_mg', 'Potassium_mg', 'Selenium_mg',
    'Zinc_mg', 'NutritionDensity'
]


# @app.route("/")
# def hello():
#     return "Hello, World!"


# if __name__ == '__main__':
# 	app.run(debug = True)

# connection.commit()
connection.close()