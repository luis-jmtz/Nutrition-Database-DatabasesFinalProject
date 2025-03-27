import sqlite3
import pandas as pd

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()

csv_files = ["users.csv"]

# loops through each csv file
for csv_file in csv_files:
    
    df = pd.read_csv(csv_file)

    # Clean column names (remove spaces and special characters)
    df.columns = df.columns.str.replace(" ", "")

    df = df.rename(columns={
        "username": "userName",
        "password": "userPassword"
    })

    # Insert data into the FoodItem table
    df.to_sql("Users", connection, if_exists="append", index=False)

connection.commit()
connection.close()

print("Data insertion complete")