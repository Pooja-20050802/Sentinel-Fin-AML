from kafka import KafkaProducer
import json
import random
import time


# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("Connected to Kafka!")


# Sample customers and accounts
customers = [
    ("C001", "A001"),
    ("C002", "A002"),
    ("C003", "A003"),
    ("C004", "A004"),
    ("C005", "A005")
]

countries = [
    "India",
    "USA",
    "UK",
    "Singapore",
    "UAE"
]


# Generate transactions continuously
transaction_number = 1

while True:

    customer_id, account_id = random.choice(customers)

    receiver_accounts = [
        "A001",
        "A002",
        "A003",
        "A004",
        "A005"
    ]

    transaction = {
        "transaction_id": f"T{transaction_number:03d}",
        "customer_id": customer_id,
        "account_id": account_id,
        "receiver_account": random.choice(receiver_accounts),
        "amount": random.randint(1000, 100000),
        "country": random.choice(countries)
    }

    # Send transaction to Kafka
    producer.send("transactions", value=transaction)
    producer.flush()

    print("Transaction sent:")
    print(transaction)

    transaction_number += 1

    # Wait 2 seconds before next transaction
    time.sleep(2)