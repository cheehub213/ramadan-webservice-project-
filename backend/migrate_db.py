import sqlite3

# Connect to the database
conn = sqlite3.connect('ramadan_app.db')
cursor = conn.cursor()

print("Checking users table...")

# Get current columns
cursor.execute("PRAGMA table_info(users)")
existing_columns = {row[1] for row in cursor.fetchall()}
print(f"Existing columns: {existing_columns}")

# Add missing columns
missing_columns = [
    ('user_type', 'TEXT', 'user'),
    ('updated_at', 'DATETIME', None)
]

for col_name, col_type, default_value in missing_columns:
    if col_name not in existing_columns:
        if default_value:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type} DEFAULT '{default_value}'")
        else:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")
        print(f"Added column: {col_name}")
    else:
        print(f"Column already exists: {col_name}")

conn.commit()
conn.close()

print("\nMigration complete!")
print("Users table updated with missing columns")
