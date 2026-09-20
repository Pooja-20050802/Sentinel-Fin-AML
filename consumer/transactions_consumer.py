import json
import sys
import os

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from kafka import KafkaConsumer
from src.database.neo4j_operations import save_transaction
from src.rules.rule_engine import check_transaction
from src.database.database import get_connection


# -----------------------------------
# Kafka Consumer
# -----------------------------------

consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="sentinel-aml-group",
    value_deserializer=lambda value: json.loads(
        value.decode("utf-8")
    )
)


print("Connected to Kafka. Waiting for transactions...")


# -----------------------------------
# PostgreSQL Connection
# -----------------------------------

connection = get_connection()
cursor = connection.cursor()

print("Connected to PostgreSQL!")


# -----------------------------------
# Process Kafka Transactions
# -----------------------------------

for message in consumer:

    transaction = message.value

    print("\n--------------------------------")
    print("Received Transaction:")
    print(transaction)


    # -----------------------------------
    # AML Rule Engine
    # -----------------------------------

    result = check_transaction(transaction)

    risk_score = result["risk_score"]
    status = result["status"]
    reasons = ", ".join(result["reasons"])


    print("Risk Score:", risk_score)
    print("Status:", status)


    if result["reasons"]:

        print("Reasons:")

        for reason in result["reasons"]:
            print("-", reason)


    # -----------------------------------
    # Save Transaction to PostgreSQL
    # -----------------------------------

    insert_query = """
    INSERT INTO transactions
    (
        transaction_id,
        customer_id,
        account_id,
        receiver_account,
        amount,
        country,
        risk_score,
        status,
        reasons
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """


    print("ABOUT TO SAVE TO POSTGRESQL")


    cursor.execute(
        insert_query,
        (
            transaction["transaction_id"],
            transaction["customer_id"],
            transaction["account_id"],
            transaction["receiver_account"],
            transaction["amount"],
            transaction["country"],
            risk_score,
            status,
            reasons
        )
    )


    # IMPORTANT:
    # Commit must be inside the Kafka loop

    connection.commit()


    print("Transaction saved to PostgreSQL!")


    # -----------------------------------
    # Save Transaction to Neo4j
    # -----------------------------------

    print("ABOUT TO SAVE TO NEO4J")


    save_transaction(
        transaction,
        risk_score,
        status
    )


    print("Transaction saved to Neo4j!")


    print("--------------------------------")