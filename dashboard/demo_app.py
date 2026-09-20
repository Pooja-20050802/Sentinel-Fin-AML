import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sentinel Finance AML",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Sentinel Finance")
st.subheader("Anti-Money Laundering Monitoring Dashboard")

st.info(
    "Public Demo Dashboard — demonstrating AML transaction monitoring "
    "using sample transaction data."
)

# Sample transaction data
data = [
    ["T001", "C001", "A001", "A003", 15000, "India", 0, "NORMAL", "No suspicious activity"],
    ["T002", "C002", "A002", "A004", 82000, "India", 40, "NORMAL", "High transaction amount"],
    ["T003", "C003", "A003", "A001", 91000, "UAE", 70, "SUSPICIOUS", "High transaction amount, High-risk country"],
    ["T004", "C001", "A001", "A002", 45000, "USA", 0, "NORMAL", "No suspicious activity"],
    ["T005", "C004", "A004", "A001", 78000, "Singapore", 70, "SUSPICIOUS", "High transaction amount, High-risk country"],
    ["T006", "C005", "A005", "A003", 12000, "India", 0, "NORMAL", "No suspicious activity"],
    ["T007", "C003", "A003", "A005", 95000, "UAE", 70, "SUSPICIOUS", "High transaction amount, High-risk country"],
    ["T008", "C002", "A002", "A003", 25000, "UK", 0, "NORMAL", "No suspicious activity"],
]

df = pd.DataFrame(
    data,
    columns=[
        "transaction_id",
        "customer_id",
        "account_id",
        "receiver_account",
        "amount",
        "country",
        "risk_score",
        "status",
        "reasons"
    ]
)

# Metrics
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

# Charts
col1, col2 = st.columns(2)

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

# Country chart
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

# Suspicious transactions
st.subheader("🚨 Suspicious Transactions")

suspicious_df = df[
    df["status"] == "SUSPICIOUS"
]

st.dataframe(
    suspicious_df,
    use_container_width=True,
    hide_index=True
)

# All transactions
with st.expander("View All Transactions"):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.caption(
    "Sentinel Finance AML — Public Demonstration Dashboard"
)