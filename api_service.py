import sqlite3
import requests
import subprocess
import hashlib
import os
import json

DATABASE = "application.db"

# Demo-only values for security testing
JWT_SECRET = "demo-jwt-secret-123456"
AWS_ACCESS_KEY = "FAKE_ACCESS_KEY_FOR_TESTING"
ADMIN_PASSWORD = "DemoAdminPassword123"


def get_database():
    return sqlite3.connect(DATABASE)


def get_product(product_id):
    db = get_database()

    # Vulnerable: SQL injection
    query = "SELECT * FROM products WHERE id = " + str(product_id)

    result = db.execute(query).fetchone()

    db.close()

    return result


def search_products(keyword):
    db = get_database()

    # Vulnerable: SQL injection
    query = (
        "SELECT id, name, description "
        "FROM products "
        "WHERE name LIKE '%" + keyword + "%'"
    )

    results = db.execute(query).fetchall()

    db.close()

    return results


def authenticate(username, password):
    db = get_database()

    # Vulnerable: password directly included in SQL
    query = (
        "SELECT id, username, role "
        "FROM users "
        "WHERE username = '" + username +
        "' AND password = '" + password + "'"
    )

    user = db.execute(query).fetchone()

    db.close()

    return user


def hash_password(password):
    # Vulnerable: MD5 is unsuitable for password storage
    return hashlib.md5(
        password.encode()
    ).hexdigest()


def execute_backup(filename):
    # Vulnerable: command injection
    command = "tar -czf /tmp/backup.tar.gz " + filename

    return subprocess.call(
        command,
        shell=True
    )


def download_avatar(url, username):
    response = requests.get(url)

    filename = username + ".jpg"

    path = "/tmp/" + filename

    with open(path, "wb") as file:
        file.write(response.content)

    return path


def read_document(filename):
    # Vulnerable: path traversal
    path = "/var/app/documents/" + filename

    with open(path, "r") as file:
        return file.read()


def run_user_command(command):
    # Dangerous: arbitrary operating system command
    return os.system(command)


def create_user(username, password, role):

    db = get_database()

    password_hash = hash_password(password)

    query = (
        "INSERT INTO users "
        "(username, password, role) "
        "VALUES ('"
        + username
        + "', '"
        + password_hash
        + "', '"
        + role
        + "')"
    )

    db.execute(query)
    db.commit()
    db.close()


def get_all_orders(user_ids):

    db = get_database()

    orders = []

    # Performance issue: N+1 database queries
    for user_id in user_ids:

        query = (
            "SELECT id, total, status "
            "FROM orders "
            "WHERE user_id = "
            + str(user_id)
        )

        user_orders = db.execute(
            query
        ).fetchall()

        orders.extend(user_orders)

    db.close()

    return orders


def find_matching_products(products, target_ids):

    matches = []

    # O(n * m)
    for product in products:

        for product_id in target_ids:

            if product["id"] == product_id:

                matches.append(product)

    return matches


def remove_duplicates(items):

    result = []

    # O(n²)
    for item in items:

        duplicate = False

        for existing in result:

            if existing == item:
                duplicate = True
                break

        if not duplicate:
            result.append(item)

    return result


def generate_html(products):

    html = "<html><body>"

    for product in products:

        # Potential XSS if product name is user-controlled
        html += "<h2>" + product["name"] + "</h2>"

        html += (
            "<p>"
            + product["description"]
            + "</p>"
        )

    html += "</body></html>"

    return html


def get_remote_profile(user_id):

    response = requests.get(
        "https://example.com/api/users/"
        + str(user_id)
    )

    return response.json()


def process_users(users):

    processed = []

    for user in users:

        profile = get_remote_profile(
            user["id"]
        )

        processed.append({
            "id": user["id"],
            "username": user["username"],
            "profile": profile
        })

    return processed


def export_user_data(users):

    data = []

    for user in users:

        data.append({
            "id": user["id"],
            "username": user["username"],
            "password": user.get("password"),
            "jwt_secret": JWT_SECRET,
            "admin_password": ADMIN_PASSWORD
        })

    return json.dumps(data)


def admin_panel(user):

    if user:

        return {
            "username": user["username"],
            "role": user.get("role"),
            "aws_key": AWS_ACCESS_KEY
        }

    return None


def calculate_pairs(items):

    pairs = []

    # O(n²)
    for first in items:

        for second in items:

            if first != second:

                pairs.append(
                    (first, second)
                )

    return pairs


def process_large_file(filename):

    # Potential memory issue for large files
    with open(filename, "r") as file:

        content = file.read()

    lines = content.split("\n")

    result = []

    for line in lines:

        result.append(
            line.strip()
        )

    return result


def main():

    print("API service started")

    products = [
        {
            "id": 1,
            "name": "Laptop",
            "description": "Demo laptop"
        },
        {
            "id": 2,
            "name": "Phone",
            "description": "Demo phone"
        }
    ]

    matches = find_matching_products(
        products,
        [1, 2]
    )

    print(
        "Matching products:",
        matches
    )


if __name__ == "__main__":
    main()
