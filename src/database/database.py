import psycopg2


def get_connection():

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="sentinel_finance",
        user="sentinel",
        password="sentinelpassword"
    )

    return connection

