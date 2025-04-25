import pandas as pd
import sqlite3
import json
from user_queries import is_admin


def show_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])

def view_table(cursor, table_name, max_rows=10, max_columns=None):
    
    try:        
        cursor.execute(f"SELECT * FROM {table_name};")

        #gets all rows and column names
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        df = pd.DataFrame(rows, columns=column_names)

        # Configure pandas display options
        pd.set_option("display.max_rows", max_rows)  # Limit the number of rows displayed
        if max_columns:
            pd.set_option("display.max_columns", max_columns)  # Limit the number of columns displayed

        print(f"Contents of table '{table_name}':")
        print(df)
    except:
        print(f"'{table_name}' could not be printed. Check that table exists and that the name is spelled correctly")

def print_view(cursor, view_name, max_rows=10, max_columns=None):
    cursor.execute(f"SELECT * FROM {view_name}") #select all from
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    with pd.option_context('display.max_rows', max_rows, 'display.max_columns', max_columns):
        print(pd.DataFrame(rows, columns=columns))


def drop_data(cursor, json_path):

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Validate required fields
        required_fields = ['userName', 'userPassword', 'table', 'rowId']
        for field in required_fields:
            if field not in data:
                print(f"Error: Missing required field '{field}' in JSON")
                return False

        username = data['userName']
        password = data['userPassword']
        table = data['table']
        row_id = data['rowId']
        
        # Default ID column name if not specified
        id_column = data.get('idColumn', f"{table[:-1]}ID" if table.endswith('s') else f"{table}ID")

        # Check if user exists and is admin
        cursor.execute(
            "SELECT userID FROM Users WHERE userName = ? AND userPassword = ?",
            (username, password)
        )
        user = cursor.fetchone()
        
        if not user:
            print("Error: Invalid username or password")
            return False

        if not is_admin(cursor, user[0]):
            print("Error: Only admins can delete data")
            return False

        # Verify table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table,)
        )
        if not cursor.fetchone():
            print(f"Error: Table '{table}' does not exist")
            return False

        # Verify column exists in table
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        
        if id_column not in columns:
            print(f"Error: Column '{id_column}' not found in table '{table}'")
            return False

        # Verify row exists
        cursor.execute(
            f"SELECT 1 FROM {table} WHERE {id_column} = ?",
            (row_id,)
        )
        if not cursor.fetchone():
            print(f"Error: Row with {id_column}={row_id} not found in table '{table}'")
            return False

        # Perform deletion
        cursor.execute(
            f"DELETE FROM {table} WHERE {id_column} = ?",
            (row_id,)
        )

        print(f"Successfully deleted row {row_id} from table '{table}'")
        return True

    except FileNotFoundError:
        print(f"Error: File not found at {json_path}")
        return False
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False