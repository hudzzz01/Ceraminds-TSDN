import sqlite3

try:
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()

    print("Connected to SQLite")

except sqlite3.Error as e:
    print(f"Error: {e}")


try:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS photo (id TEXT INTEGER PRIMARY KEY, Bounding_Box TEXT)"""

    cursor.execute(create_table_query)
    print("Table 'photo' created successfully")

except sqlite3.Error as e:
    print(f"Error: {e}")