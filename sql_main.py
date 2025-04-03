import sqlite3
from basic_sql_commands import show_tables, view_table
from queries import add_user
from queries import *

connection = sqlite3.connect("nutrition.db")

cursor = connection.cursor()

# created the SQL Table
# cursor.executescript(open(r'SQL_Commands\table_creation.sql').read())

show_tables(cursor)
view_table(cursor, "Users", max_rows= None)


# print(check_user_exists(cursor, "function_tester_1", "password_test_1"))


connection.commit()
connection.close()

