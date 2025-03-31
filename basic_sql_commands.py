import pandas as pd


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

def print_df(dataframe, max_rows = 10, max_columns = None):
    
    with pd.option_context('display.max_rows', max_rows,
                            'display.max_columns', max_columns):
        print(dataframe)