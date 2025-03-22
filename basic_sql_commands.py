def show_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])


def view_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name};")

    rows = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    print("Columns:", column_names)

    # Print rows
    print(f"Contents of table '{table_name}':")
    for row in rows:
        print(row)
