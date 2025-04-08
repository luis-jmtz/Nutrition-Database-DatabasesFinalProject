from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from queries import *
import json
import os

app = Flask(__name__)




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


@app.route("/")
def index():
    if request.method == 'POST':
        filters = {} 

        selected_columns =  request.form.getlist('columns')

        for column in selected_columns:
            min_val = request.form.get(f"{column}_min", "").strip()
            max_val = request.form.get(f"{column}_max").strip()
            # get the min and max values from the json per column

            #only add to column to filter if at least one value is provided
            if min_val or max_val:
                filters[column] = []
                if min_val:
                    filters[column].append(float(min_val))
                else:
                    filters[column].append(-1)
                if max_val:
                    filters[column].append(float(max_val))
                else:
                    filters[column].append(-1)

        # Save filters to a temporary JSON file
        temp_json_path = 'temp_filters.json'
        with open(temp_json_path, 'w') as f:
            json.dump(filters, f)   


        connection = sqlite3.connect("nutrition.db")

        cursor = connection.cursor()

        view_name = loop_filter_ingredients(cursor, temp_json_path) #call the function


        if view_name:
            # Get the filtered results
            cursor.execute(f"SELECT * FROM {view_name}")
            columns = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()


            # Clean up the temporary file
            if os.path.exists(temp_json_path):
                os.remove(temp_json_path)
            
            connection.close()
            return render_template('results.html', 
                                columns=columns, 
                                results=results,
                                num_results=len(results))
        
        connection.close()
        return redirect(url_for('index'))
    

    # GET request - show the filter form
    return render_template('filter_form.html', columns=filter_columns)     


if __name__ == '__main__':
	app.run(debug = True)

# connection.commit()
