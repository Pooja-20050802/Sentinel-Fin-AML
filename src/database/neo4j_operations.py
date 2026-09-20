from src.database.neo4j_database import get_driver


def save_transaction(transaction, risk_score, status):

    query = """
    MERGE (c:Customer {
        customer_id: $customer_id
    })

    MERGE (sender:Account {
        account_id: $account_id
    })

    MERGE (receiver:Account {
        account_id: $receiver_account
    })

    MERGE (t:Transaction {
        transaction_id: $transaction_id
    })

    SET
        t.amount = $amount,
        t.country = $country,
        t.risk_score = $risk_score,
        t.status = $status

    MERGE (c)-[:OWNS]->(sender)

    MERGE (sender)-[:MADE]->(t)

    MERGE (sender)-[:SENT_TO]->(receiver)
    """

    driver = get_driver()

    with driver.session() as session:

        session.run(
            query,
            customer_id=transaction["customer_id"],
            account_id=transaction["account_id"],
            receiver_account=transaction["receiver_account"],
            transaction_id=transaction["transaction_id"],
            amount=transaction["amount"],
            country=transaction["country"],
            risk_score=risk_score,
            status=status
        )