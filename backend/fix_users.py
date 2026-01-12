"""Fix users with invalid password hashes"""
import sqlite3

conn = sqlite3.connect('ramadan_app.db')
cursor = conn.cursor()

# Delete users with invalid password hashes (not starting with $2)
cursor.execute("SELECT email, password_hash FROM users")
users = cursor.fetchall()

for email, pw_hash in users:
    if pw_hash and not pw_hash.startswith('$2'):
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        print(f"Deleted user with invalid hash: {email}")
    elif not pw_hash:
        print(f"User without password: {email}")
    else:
        print(f"Valid user: {email}")

conn.commit()
conn.close()
print("\nDone! Users with invalid hashes removed. They can now sign up again.")
