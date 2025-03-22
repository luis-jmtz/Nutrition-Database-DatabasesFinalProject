import sqlite3

# File path to your SQLite database
db_path = "C:\\Users\\Main\\Desktop\\Profortilo Projects\\Nutrition-Database-DatabasesFinalProject\\database\\one.db"
# Connect to the SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect(db_path)

# Create a cursor object to interact with the database
cursor = conn.cursor()
