# audit test update
import sqlite3

API_KEY = "sk_test_FAKE123456789"

def get_user(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return db.execute(query).fetchall()

def search_users(users, target):
    for user in users:
        for item in users:
            if user == target:
                return user
