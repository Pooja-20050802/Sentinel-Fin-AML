import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Sentinel Finance AML",
    page_icon="🔍",
    layout="wide"
)


# -----------------------------------
# Database Connection
# -----------------------------------

def get_connection():

    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="sentinel_finance",
        user="sentinel",
        password="sentinelpassword"
    )


# -----------------------------------
# Load Transaction Data
# -----------------------------------

@st.cache_data(ttl=5)
def load_data():

    connection = get_connection()

    query = """
    SELECT
        transaction_id,
        customer_id,
        account_id,
        receiver_account,
        amount,
        country,
        risk_score,
        status,
        reasons,
        created_at
    FROM transactions
    ORDER BY created_at DESC
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df


# -----------------------------------
# Title
# -----------------------------------

st.title("🔍 Sentinel Finance")
st.subheader("Real-Time Anti-Money Laundering Monitoring System")

st.markdown(
    "Monitor financial transactions, identify suspicious activity "
    "and investigate transaction risk."
)


# -----------------------------------
# Load Data
# -----------------------------------

try:

    df = load_data()

except Exception as e:

    st.error(
        f"Unable to connect to PostgreSQL: {e}"
    )

    st.stop()


# -----------------------------------
# Check Data
# -----------------------------------

if df.empty:

    st.warning(
        "No transactions found in the database."
    )

    st.stop()


# -----------------------------------
# Dashboard Metrics
# -----------------------------------

total_transactions = len(df)

suspicious_transactions = len(
    df[df["status"] == "SUSPICIOUS"]
)

normal_transactions = len(
    df[df["status"] == "NORMAL"]
)

average_amount = df["amount"].mean()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Transactions",
        total_transactions
    )


with col2:

    st.metric(
        "Suspicious Transactions",
        suspicious_transactions
    )


with col3:

    st.metric(
        "Normal Transactions",
        normal_transactions
    )


with col4:

    st.metric(
        "Average Amount",
        f"₹{average_amount:,.2f}"
    )


st.divider()


# -----------------------------------
# Charts
# -----------------------------------

col1, col2 = st.columns(2)


# Suspicious vs Normal
with col1:

    st.subheader("Transaction Status")

    status_count = (
        df["status"]
        .value_counts()
        .reset_index()
    )

    status_count.columns = [
        "Status",
        "Count"
    ]

    fig_status = px.pie(
        status_count,
        names="Status",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# Risk Score Distribution
with col2:

    st.subheader("Risk Score Distribution")

    fig_risk = px.histogram(
        df,
        x="risk_score",
        nbins=10,
        title="Transaction Risk Scores"
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True
    )


# -----------------------------------
# Country Analysis
# -----------------------------------

st.subheader("Transactions by Country")

country_count = (
    df["country"]
    .value_counts()
    .reset_index()
)

country_count.columns = [
    "Country",
    "Transactions"
]

fig_country = px.bar(
    country_count,
    x="Country",
    y="Transactions"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)


# -----------------------------------
# Suspicious Transactions
# -----------------------------------

st.subheader("🚨 Suspicious Transactions")

suspicious_df = df[
    df["status"] == "SUSPICIOUS"
]


if suspicious_df.empty:

    st.success(
        "No suspicious transactions detected."
    )

else:

    st.dataframe(
        suspicious_df[
            [
                "transaction_id",
                "customer_id",
                "account_id",
                "receiver_account",
                "amount",
                "country",
                "risk_score",
                "reasons",
                "created_at"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------
# All Transactions
# -----------------------------------

with st.expander("View All Transactions"):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )