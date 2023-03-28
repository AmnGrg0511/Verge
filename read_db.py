import sqlite3

# Connect to the database (create a new database if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object
cursor = conn.cursor()

# Select data from the table
cursor.execute("SELECT id, date, link FROM mytable ORDER BY id")

# Fetch all rows as a list of tuples
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the cursor and the connection
cursor.close()
conn.close()
