import sqlite3
import csv

# Path to your SQLite database
db_path = fr"nutrition.db"

# Output CSV file path
csv_path = 'ingredients.csv'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL query to get the data
query = "SELECT ingredientID, ingredientName FROM IngredientItem"

# Execute query and fetch data
cursor.execute(query)
rows = cursor.fetchall()

# Write data to CSV
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ingredientID', 'ingredientName'])  # Header
    writer.writerows(rows)

# Clean up
cursor.close()
conn.close()

print(f"Data successfully exported to {csv_path}")
