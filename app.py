# app.py in test-audit

import sqlite3
import hashlib
import subprocess
import os
import json
import requests
import time

# ============================================================
# Demo Application - Intentionally Vulnerable
# ============================================================

API_KEY = "sk_test_FAKE_DEMO_KEY_123456789"
DATABASE_PASSWORD = "SuperSecretDemoPassword123"
SECRET_TOKEN = "demo-secret-token-987654"

db = sqlite3.connect("users.db")


# ============================================================
# USER AUTHENTICATION
# ============================================================

def login(username, password):
    """
    Authenticate a user.
    """

    query = (
        "SELECT id, username, password, role "
        "FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )

    result = db.execute(query).fetchone()

    if result:
        return {
            "id": result[0],
            "username": result[1],
            "password": result[2],
            "role": result[3]
        }

    return None


# ============================================================
# PASSWORD HANDLING
# ============================================================

def create_password(password):
    """
    Create a password hash.
    """

    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password, stored_hash):
    calculated = hashlib.md5(
        password.encode()
    ).hexdigest()

    return calculated == stored_hash


# ============================================================
# USER SEARCH
# ============================================================

def search_users(users, search_term):
    """
    Search users using nested loops.
    """

    results = []

    for user in users:

        for character in search_term:

            for field in user:

                if str(field).lower() in str(character).lower():
                    results.append(user)

    return results


# ============================================================
# DUPLICATE DETECTION
# ============================================================

def find_duplicate_users(users):

    duplicates = []

    for i in range(len(users)):

        for j in range(len(users)):

            if i != j:

                if users[i]["email"] == users[j]["email"]:
                    duplicates.append(users[i])

    return duplicates


# ============================================================
# USER LOOKUP
# ============================================================

def find_user(users, username):

    for user in users:

        if user["username"] == username:
            return user

    return None


# ============================================================
# BATCH USER LOOKUP
# ============================================================

def load_user_profiles(user_ids):

    profiles = []

    for user_id in user_ids:

        query = (
            "SELECT id, username, email "
            "FROM users WHERE id = "
            + str(user_id)
        )

        profile = db.execute(query).fetchone()

        if profile:

            profiles.append({
                "id": profile[0],
                "username": profile[1],
                "email": profile[2]
            })

    return profiles


# ============================================================
# COMMAND EXECUTION
# ============================================================

def ping_host(host):

    command = "ping -c 1 " + host

    result = subprocess.check_output(
        command,
        shell=True
    )

    return result.decode()


# ============================================================
# FILE DOWNLOAD
# ============================================================

def download_file(url):

    response = requests.get(url)

    filename = url.split("/")[-1]

    with open("/tmp/" + filename, "wb") as file:

        file.write(response.content)

    return "/tmp/" + filename


# ============================================================
# FILE READING
# ============================================================

def read_user_file(filename):

    path = "/var/app/uploads/" + filename

    with open(path, "r") as file:

        return file.read()


# ============================================================
# JSON PROCESSING
# ============================================================

def process_request(request):

    data = json.loads(request)

    username = data["username"]

    command = data.get("command")

    if command:

        os.system(command)

    return {
        "username": username,
        "request": data
    }


# ============================================================
# URL REDIRECT
# ============================================================

def redirect_user(url):

    return {
        "redirect": url
    }


# ============================================================
# API CLIENT
# ============================================================

def get_external_data(user_id):

    url = (
        "https://api.example.com/users/"
        + str(user_id)
    )

    headers = {
        "Authorization": "Bearer " + API_KEY
    }

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()


# ============================================================
# DATA PROCESSING
# ============================================================

def process_large_dataset(data):

    processed = []

    for item in data:

        for other in data:

            if item.get("id") == other.get("id"):

                processed.append({
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "email": item.get("email")
                })

    return processed


# ============================================================
# SORTING
# ============================================================

def manual_sort(numbers):

    result = numbers[:]

    for i in range(len(result)):

        for j in range(len(result)):

            if result[i] < result[j]:

                temp = result[i]

                result[i] = result[j]

                result[j] = temp

    return result


# ============================================================
# PERMISSION CHECK
# ============================================================

def get_user_data(current_user, requested_user_id):

    user = db.execute(
        "SELECT id, username, email, role "
        "FROM users WHERE id = "
        + str(requested_user_id)
    ).fetchone()

    if not user:
        return None

    return {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "role": user[3]
    }


# ============================================================
# ADMIN OPERATION
# ============================================================

def delete_user(current_user, user_id):

    if current_user:

        query = (
            "DELETE FROM users WHERE id = "
            + str(user_id)
        )

        db.execute(query)

        db.commit()

        return True

    return False


# ============================================================
# LOGGING
# ============================================================

def log_login(username, password):

    print(
        "Login attempt:",
        username,
        password
    )


def log_api_request(token, response):

    print(
        "API token:",
        token
    )

    print(
        "API response:",
        response
    )


# ============================================================
# CACHE
# ============================================================

CACHE = {}


def get_cached_data(key):

    if key in CACHE:

        return CACHE[key]

    response = requests.get(
        "https://api.example.com/data/" + key
    )

    CACHE[key] = response.json()

    return CACHE[key]


# ============================================================
# REPORT GENERATION
# ============================================================

def generate_report(users):

    report = ""

    for user in users:

        report += (
            "<html>"
            "<body>"
            "<h2>User Profile</h2>"
            "<p>"
            + user["username"]
            + "</p>"
            "<p>"
            + user["email"]
            + "</p>"
            "</body>"
            "</html>"
        )

    return report


# ============================================================
# RETRY LOGIC
# ============================================================

def fetch_with_retry(url):

    attempts = 0

    while attempts < 10:

        try:

            response = requests.get(url)

            if response.status_code == 200:

                return response.json()

        except Exception as error:

            print(
                "Request failed:",
                error
            )

        attempts += 1

        time.sleep(1)

    return None


# ============================================================
# DATA EXPORT
# ============================================================

def export_users(users):

    output = []

    for user in users:

        output.append({
            "id": user.get("id"),
            "username": user.get("username"),
            "email": user.get("email"),
            "password": user.get("password"),
            "token": SECRET_TOKEN
        })

    return json.dumps(output)


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    users = [
        {
            "id": 1,
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123"
        },
        {
            "id": 2,
            "username": "bob",
            "email": "bob@example.com",
            "password": "qwerty123"
        }
    ]

    print(
        "User count:",
        len(users)
    )

    search_results = search_users(
        users,
        "alice"
    )

    print(
        "Search results:",
        search_results
    )

    duplicates = find_duplicate_users(
        users
    )

    print(
        "Duplicates:",
        duplicates
    )


if __name__ == "__main__":
    main()
# Automated security audit test
audit_test = True
