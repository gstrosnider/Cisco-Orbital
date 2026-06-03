###This will load a SQLite database from a path and then read all rows from a provided table.

import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('{{ .databasefilename }}')
cursor = conn.cursor()

# Fetch and print all records from the table
cursor.execute("SELECT * FROM {{ .tablename }}")
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Clean up
cursor.close()
conn.close()
