from database import get_connection


connection = get_connection()
cursor = connection.cursor()


create_table_query = """
CREATE TABLE IF NOT EXISTS transactions (

    id SERIAL PRIMARY KEY,

    transaction_id VARCHAR(50),

    customer_id VARCHAR(50),

    account_id VARCHAR(50),

    amount NUMERIC(12, 2),

    country VARCHAR(50),

    risk_score INTEGER,

    status VARCHAR(20),

    reasons TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


cursor.execute(create_table_query)

connection.commit()

cursor.close()
connection.close()

print("Transactions table created successfully!")