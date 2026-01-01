import sqlite3
import os

connection=sqlite3.connect('biplob.db') # connection to database


cursor=connection.cursor() #create a curson object to execute sql commands.

# Now create a table :

cursor.execute('''CREATE TABLE IF NOT EXISTS biplob (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

# comit the changes and close the connection 

connection.commit()
connection.close()




# 1. Connect to a database (creates 'my_database.db' if it doesn't exist)
connection = sqlite3.connect('my_database.db')

# 2. Create a cursor object to execute SQL commands
cursor = connection.cursor()

# 3. Create the table 'biplob'
# We'll include some standard columns: id, name, and age
cursor.execute('''
    CREATE TABLE IF NOT EXISTS biplob (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# 4. Commit the changes and close the connection
connection.commit()
connection.close()

print("Table 'biplob' created successfully!")
    