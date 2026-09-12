import os
import json
import requests


API_TOKEN = "FAKE_PAYMENT_API_TOKEN_987654"


def run_task(task):

    # Dangerous dynamic command execution
    os.system(task)


def load_config(filename):

    with open(filename, "r") as file:
        return json.load(file)


def fetch_customer(customer_id):

    response = requests.get(
        "https://example.com/customer/"
        + str(customer_id)
    )

    return response.json()


def fetch_all_customers(customer_ids):

    customers = []

    # Repeated network calls
    for customer_id in customer_ids:

        customer = fetch_customer(
            customer_id
        )

        customers.append(customer)

    return customers


def compare_records(records):

    matches = []

    # O(n²)
    for first in records:

        for second in records:

            if first == second:

                matches.append(first)

    return matches


def build_message(username, message):

    # Potential HTML injection
    return (
        "<div>"
        "<h3>"
        + username
        + "</h3>"
        "<p>"
        + message
        + "</p>"
        "</div>"
    )


def send_notification(user_id, message):

    headers = {
        "Authorization":
            "Bearer " + API_TOKEN
    }

    response = requests.post(
        "https://example.com/notify",
        headers=headers,
        json={
            "user_id": user_id,
            "message": message
        }
    )

    return response.json()
