from collections import defaultdict


# Store transactions made by each customer
customer_transactions = defaultdict(list)


def check_transaction(transaction):

    risk_score = 0
    reasons = []

    customer_id = transaction["customer_id"]
    amount = transaction["amount"]
    country = transaction["country"]


    # -----------------------------------
    # Rule 1: High Transaction Amount
    # -----------------------------------

    if amount > 75000:

        risk_score += 40

        reasons.append(
            "High transaction amount"
        )


    # -----------------------------------
    # Rule 2: High-Risk Country
    # -----------------------------------

    high_risk_countries = [
        "UAE",
        "Singapore"
    ]

    if country in high_risk_countries:

        risk_score += 30

        reasons.append(
            "High-risk country"
        )


    # -----------------------------------
    # Store Customer Transaction
    # -----------------------------------

    customer_transactions[customer_id].append(
        transaction
    )


    transaction_count = len(
        customer_transactions[customer_id]
    )


    # -----------------------------------
    # Rule 3: Frequent Transactions
    # -----------------------------------

    if transaction_count >= 3:

        risk_score += 20

        reasons.append(
            "Frequent transactions"
        )


    # -----------------------------------
    # Rule 4: Very High Transaction Frequency
    # -----------------------------------

    if transaction_count >= 5:

        risk_score += 30

        reasons.append(
            "Very high transaction frequency"
        )


    # -----------------------------------
    # Final Decision
    # -----------------------------------

    if risk_score >= 50:

        status = "SUSPICIOUS"

    else:

        status = "NORMAL"


    # -----------------------------------
    # Return Result
    # -----------------------------------

    return {

        "risk_score": risk_score,

        "status": status,

        "reasons": reasons

    }