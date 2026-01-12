"""
Fix users table - add missing columns
"""
import sqlite3

conn = sqlite3.connect('ramadan_app.db')
cursor = conn.cursor()

# Get current columns
cursor.execute('PRAGMA table_info(users)')
existing_cols = [col[1] for col in cursor.fetchall()]
print(f"Current columns: {existing_cols}")

# Columns to add
columns_to_add = [
    ('is_active', 'BOOLEAN DEFAULT 1'),
    ('last_login', 'DATETIME'),
    ('login_attempts', 'INTEGER DEFAULT 0'),
    ('locked_until', 'DATETIME')
]

for col_name, col_type in columns_to_add:
    if col_name not in existing_cols:
        try:
            cursor.execute(f'ALTER TABLE users ADD COLUMN {col_name} {col_type}')
            print(f"✅ Added column: {col_name}")
        except sqlite3.OperationalError as e:
            print(f"⚠️ Column {col_name} already exists or error: {e}")
    else:
        print(f"✓ Column {col_name} already exists")

conn.commit()

# Verify final state
cursor.execute('PRAGMA table_info(users)')
final_cols = [col[1] for col in cursor.fetchall()]
print(f"\nFinal columns: {final_cols}")

conn.close()
print("\n✅ Database migration complete!")
