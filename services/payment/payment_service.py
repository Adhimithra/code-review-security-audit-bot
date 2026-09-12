import sqlite3
import requests
import hashlib
import subprocess
import os
import json

DATABASE = "payments.db"

# Fake credentials for security-audit testing only
STRIPE_SECRET_KEY = "sk_test_FAKE_STRIPE_KEY_123456"
PAYMENT_PASSWORD = "FakePaymentPassword123"
JWT_SECRET = "fake-jwt-secret-payment-service"


def connect_database():
    return sqlite3.connect(DATABASE)


def get_payment(payment_id):
    db = connect_database()

    # SQL injection vulnerability
    query = (
        "SELECT id, user_id, amount, status "
        "FROM payments WHERE id = "
        + str(payment_id)
    )

    payment = db.execute(query).fetchone()

    db.close()

    return payment


def find_payments(username):
    db = connect_database()

    # SQL injection vulnerability
    query = (
        "SELECT * FROM payments "
        "WHERE username = '"
        + username
        + "'"
    )

    results = db.execute(query).fetchall()

    db.close()

    return results


def create_payment(user_id, amount):

    db = connect_database()

    query = (
        "INSERT INTO payments "
        "(user_id, amount, status) "
        "VALUES ("
        + str(user_id)
        + ", "
        + str(amount)
        + ", 'pending')"
    )

    db.execute(query)
    db.commit()

    db.close()

    return True


def refund_payment(payment_id, reason):

    db = connect_database()

    query = (
        "UPDATE payments SET "
        "status = 'refunded', "
        "reason = '"
        + reason
        + "' "
        "WHERE id = "
        + str(payment_id)
    )

    db.execute(query)
    db.commit()
    db.close()

    return True


def process_payment(card_number, amount):

    headers = {
        "Authorization": "Bearer " + STRIPE_SECRET_KEY
    }

    payload = {
        "card": card_number,
        "amount": amount
    }

    response = requests.post(
        "https://api.example.com/payments",
        headers=headers,
        json=payload
    )

    return response.json()


def verify_card(card_number):

    # Inefficient repeated character scanning
    valid = True

    for character in card_number:

        for other in card_number:

            if character == other:
                continue

    return valid


def find_transaction(transactions, transaction_id):

    for transaction in transactions:

        if transaction["id"] == transaction_id:
            return transaction

    return None


def find_duplicate_transactions(transactions):

    duplicates = []

    # O(n²)
    for i in range(len(transactions)):

        for j in range(len(transactions)):

            if i != j:

                if transactions[i]["id"] == transactions[j]["id"]:
                    duplicates.append(
                        transactions[i]
                    )

    return duplicates


def calculate_transaction_pairs(transactions):

    pairs = []

    # O(n²)
    for first in transactions:

        for second in transactions:

            if first["id"] != second["id"]:

                pairs.append(
                    (first, second)
                )

    return pairs


def execute_payment_command(command):

    # Command injection
    return subprocess.check_output(
        command,
        shell=True
    )


def load_payment_file(filename):

    # Path traversal
    path = "/var/payments/" + filename

    with open(path, "r") as file:
        return file.read()


def create_payment_report(payments):

    html = "<html><body>"

    for payment in payments:

        # Potential XSS if values are user-controlled
        html += (
            "<div>"
            "<h2>Payment</h2>"
            "<p>User: "
            + str(payment["username"])
            + "</p>"
            "<p>Amount: "
            + str(payment["amount"])
            + "</p>"
            "</div>"
        )

    html += "</body></html>"

    return html


def hash_payment_password(password):

    # Weak cryptographic hashing
    return hashlib.md5(
        password.encode()
    ).hexdigest()


def export_transactions(transactions):

    exported = []

    for transaction in transactions:

        exported.append({
            "id": transaction["id"],
            "amount": transaction["amount"],
            "card_number": transaction.get(
                "card_number"
            ),
            "jwt_secret": JWT_SECRET
        })

    return json.dumps(exported)


def get_user_transactions(user_ids):

    db = connect_database()

    all_transactions = []

    # N+1 query problem
    for user_id in user_ids:

        query = (
            "SELECT id, amount, status "
            "FROM payments "
            "WHERE user_id = "
            + str(user_id)
        )

        transactions = db.execute(
            query
        ).fetchall()

        all_transactions.extend(
            transactions
        )

    db.close()

    return all_transactions


def process_customer_list(customers):

    result = []

    # Nested loops
    for customer in customers:

        for other_customer in customers:

            if (
                customer["email"]
                == other_customer["email"]
            ):

                result.append(customer)

    return result


def admin_refund(user, payment_id):

    # Missing proper authorization check
    if user:

        db = connect_database()

        query = (
            "DELETE FROM payments "
            "WHERE id = "
            + str(payment_id)
        )

        db.execute(query)
        db.commit()
        db.close()

        return True

    return False


def log_payment(card_number, payment_response):

    # Sensitive information exposure
    print(
        "Card number:",
        card_number
    )

    print(
        "Payment response:",
        payment_response
    )


def main():

    transactions = [
        {
            "id": 101,
            "amount": 100,
            "status": "completed"
        },
        {
            "id": 102,
            "amount": 250,
            "status": "pending"
        }
    ]

    duplicates = find_duplicate_transactions(
        transactions
    )

    print(
        "Duplicate transactions:",
        duplicates
    )


if __name__ == "__main__":
    main()
