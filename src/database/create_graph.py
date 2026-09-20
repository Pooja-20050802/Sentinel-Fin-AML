from neo4j_database import get_driver


driver = get_driver()


def create_transaction_graph():

    query = """
    MERGE (customer:Customer {
        customer_id: $customer_id
    })

    MERGE (account:Account {
        account_id: $account_id
    })

    MERGE (transaction:Transaction {
        transaction_id: $transaction_id
    })

    SET transaction.amount = $amount,
        transaction.country = $country,
        transaction.risk_score = $risk_score,
        transaction.status = $status

    MERGE (customer)-[:OWNS]->(account)

    MERGE (account)-[:MADE]->(transaction)

    RETURN customer, account, transaction
    """

    with driver.session() as session:

        session.run(
            query,
            customer_id="C001",
            account_id="A001",
            transaction_id="T001",
            amount=5000,
            country="India",
            risk_score=0,
            status="NORMAL"
        )

        print("Transaction graph created!")


create_transaction_graph()

driver.close()