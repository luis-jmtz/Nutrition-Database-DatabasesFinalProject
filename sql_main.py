import sqlite3
from basic_sql_commands import show_tables, view_table

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

show_tables(cursor)
view_table(cursor, "Users")

# created the SQL Table
# cursor.executescript(open(r'SQL_Commands\table_creation.sql').read())


# show_tables(cursor)


connection.close()

