# Sentinel Finance — Real-Time Anti-Money Laundering System

A real-time financial transaction monitoring and Anti-Money Laundering (AML) system that processes transactions through Apache Kafka, evaluates suspicious activity using rule-based risk scoring, stores transaction data in PostgreSQL, analyzes transaction relationships using Neo4j, and visualizes results through an interactive Streamlit dashboard.

---

## 📌 Project Overview

Financial institutions process a large number of transactions every day. Identifying suspicious transactions manually can be difficult and time-consuming.

**Sentinel Finance** demonstrates a real-time AML monitoring pipeline that:

* Receives financial transactions in real time
* Streams transactions using Apache Kafka
* Applies AML detection rules
* Calculates a risk score
* Classifies transactions as `NORMAL` or `SUSPICIOUS`
* Stores transaction records in PostgreSQL
* Creates customer/account/transaction relationships in Neo4j
* Provides an interactive monitoring dashboard using Streamlit

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────────┐
                 │   Transaction Producer  │
                 │        Python           │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │      Apache Kafka       │
                 │    Transactions Topic   │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   Kafka Consumer        │
                 │        Python           │
                 └────────────┬────────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │    AML Rule Engine      │
                 │                         │
                 │  • Amount Rule          │
                 │  • Country Rule         │
                 │  • Frequency Rule       │
                 │  • Sender/Receiver Rule │
                 └────────────┬────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │ Risk Score  │
                       └──────┬──────┘
                              │
                     ┌────────┴────────┐
                     ▼                 ▼
             ┌──────────────┐   ┌──────────────┐
             │ PostgreSQL   │   │    Neo4j     │
             │ Transactions │   │ Relationships│
             └──────┬───────┘   └──────┬───────┘
                    │                  │
                    └────────┬─────────┘
                             ▼
                   ┌───────────────────┐
                   │ Streamlit         │
                   │ AML Dashboard     │
                   └───────────────────┘
```

---

## 🚀 Key Features

### 1. Real-Time Transaction Streaming

Transactions are generated using Python and published to an Apache Kafka topic.

Each transaction contains information such as:

```text
Transaction ID
Customer ID
Sender Account
Receiver Account
Amount
Country
```

---

### 2. AML Rule Engine

The system evaluates transactions using multiple risk rules.

#### High Transaction Amount

Transactions above the configured threshold receive additional risk points.

#### High-Risk Country

Transactions involving configured high-risk countries receive additional risk points.

#### Frequent Transactions

Repeated transactions by the same customer increase the risk score.

#### Multiple Senders to Same Receiver

The system tracks sender-to-receiver relationships and identifies receiver accounts that receive transactions from multiple different accounts.

---

## 📊 Risk Scoring

Each rule contributes points to the transaction's risk score.

Example:

```text
High transaction amount        +40
High-risk country              +30
Frequent transactions          +20
Multiple sender accounts       +30
------------------------------------
Total Risk Score               120
```

Transactions reaching the configured risk threshold are classified as:

```text
SUSPICIOUS
```

Otherwise:

```text
NORMAL
```

The system also stores the reasons that contributed to the risk score.

---

## 🗄️ PostgreSQL

PostgreSQL stores processed transaction information.

The transaction table contains fields such as:

```text
transaction_id
customer_id
account_id
receiver_account
amount
country
risk_score
status
reasons
created_at
```

This provides a persistent relational record of the transactions processed by the AML pipeline.

---

## 🔗 Neo4j Graph Database

Neo4j is used to represent financial relationships as a graph.

The system creates relationships such as:

```text
Customer
   │
   │ OWNS
   ▼
Account
   │
   │ MADE
   ▼
Transaction
   │
   │
   ▼
Receiver Account
```

The system also creates:

```text
Sender Account ──SENT_TO──> Receiver Account
```

This makes it possible to investigate transaction relationships that are difficult to understand from individual transaction records alone.

### Example

```text
A001 ──────────┐
               │
A003 ──────────┼──> A005
               │
A004 ──────────┘
```

This represents multiple accounts sending transactions to the same receiver account.

---

## 📈 Streamlit Dashboard

The project includes an interactive dashboard for monitoring transaction activity.

The dashboard displays:

* Total transactions
* Suspicious transactions
* Normal transactions
* Average transaction amount
* Transaction status distribution
* Risk score distribution
* Transactions by country
* Suspicious transaction details
* Complete transaction records

### Dashboard Flow

```text
PostgreSQL
     │
     ▼
Streamlit
     │
     ├── Transaction Metrics
     ├── Risk Analysis
     ├── Country Analysis
     └── Suspicious Transactions
```

---

## 🛠️ Technologies Used

| Technology   | Purpose                         |
| ------------ | ------------------------------- |
| Python       | Application and AML logic       |
| Apache Kafka | Real-time transaction streaming |
| PostgreSQL   | Transaction storage             |
| Neo4j        | Relationship and graph analysis |
| Streamlit    | Interactive dashboard           |
| Pandas       | Data processing                 |
| Plotly       | Dashboard visualizations        |
| Docker       | Containerized infrastructure    |
| Git/GitHub   | Version control                 |

---

## 📁 Project Structure

```text
sentinel-finance-aml/
│
├── producer/
│   └── transactions_producer.py
│
├── consumer/
│   └── transactions_consumer.py
│
├── src/
│   ├── rules/
│   │   └── rule_engine.py
│   │
│   └── database/
│       ├── database.py
│       ├── create_table.py
│       ├── neo4j_database.py
│       └── neo4j_operations.py
│
├── dashboard/
│   └── app.py
│
├── data/
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/sentinel-finance-aml.git
```

```bash
cd sentinel-finance-aml
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🐳 Start Infrastructure

The project uses Docker for Kafka, PostgreSQL, and Neo4j.

Start the services with:

```bash
docker compose up -d
```

Check running containers:

```bash
docker ps
```

Expected services:

```text
sentinel-kafka
sentinel-postgres
sentinel-neo4j
```

---

## ▶️ Running the Project

### Start the Producer

```bash
python producer/transactions_producer.py
```

The producer generates financial transactions and sends them to Kafka.
