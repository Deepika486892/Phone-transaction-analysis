import streamlit as st
import plotly.express as px
import pandas as pd
import pymysql
import requests

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="phone_pe"
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# STREAMLIT LAYOUT
st.set_page_config(page_title="PhonePe Dashboard", layout="wide")

menu = st.sidebar.radio("📊 Main Menu", ["🏠 Home", "💸 Transactions", "👥 Users", "🛡️ Insurance"])

# -------------------
# HOME PAGE
# -------------------
if menu == "🏠 Home":
    st.markdown(
        """
        <div style="background-color:black;padding:30px;border-radius:10px;">
        <h1 style="text-align:center;color:white;">PhonePe Transaction Insights</h1>
        <h3 style="text-align:center;color:white;">100% Safe & Secure | Banking 24/7 | Cashback & Rewards</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------
# TRANSACTIONS
# -------------------
elif menu == "💸 Transactions":
    st.sidebar.header("Filter Transactions")
    year = st.sidebar.selectbox("Select Year", list(range(2018, 2025)))
    quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])

    ques = st.selectbox("Select Transaction Question", [
        "Top 10 States by Transactions",
        "Lowest 10 States by Transactions",
        "Top 10 Districts by Transactions",
        "Lowest 10 Districts by Transactions",
        "Top 10 Pincodes by Transactions",
        "Lowest 10 Pincodes by Transactions",
        "Top 5 Mobile Brands by Transactions"
    ])

    # ---------- STATES ----------
    if "States" in ques:
        query = f"""
        SELECT State, SUM(Transaction_amount) as Amount
        FROM agg_transaction
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY State
        ORDER BY Amount {"DESC" if "Top" in ques else "ASC"}
        LIMIT 10;
        """
        df = run_query(query)
        total_amount = df["Amount"].sum()
        st.metric("💰 Total Transaction Amount", f"{total_amount:,.0f}")
        st.plotly_chart(px.bar(df, x="State", y="Amount", title=ques, color_discrete_sequence=["green"]))
        st.dataframe(df)

    # ---------- DISTRICTS ----------
    elif "Districts" in ques:
        query = f"""
        SELECT District, SUM(Transaction_amount) as Amount
        FROM map_transaction
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY District
        ORDER BY Amount {"DESC" if "Top" in ques else "ASC"}
        LIMIT 10;
        """
        df = run_query(query)
        total_amount = df["Amount"].sum()
        st.metric("💰 Total Transaction Amount", f"{total_amount:,.0f}")
        st.plotly_chart(px.bar(df, x="District", y="Amount", title=ques, color_discrete_sequence=["pink"]))
        st.dataframe(df)

    # ---------- PINCODES ----------
    elif "Pincodes" in ques:
        query = f"""
        SELECT Pincode, SUM(Transaction_amount) as Amount
        FROM top_transaction
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY Pincode
        ORDER BY Amount {"DESC" if "Top" in ques else "ASC"}
        LIMIT 10;
        """
        df = run_query(query)
        total_amount = df["Amount"].sum()
        st.metric("💰 Total Transaction Amount", f"{total_amount:,.0f}")
        st.plotly_chart(px.bar(df, x="Pincode", y="Amount", title=ques, color_discrete_sequence=["orange"]))
        st.dataframe(df)

    # ---------- BRANDS ----------
    elif "Brands" in ques:
        query = f"""
        SELECT Brand, SUM(Transaction_count) as Count
        FROM agg_user
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY Brand
        ORDER BY Count DESC
        LIMIT 5;
        """
        df = run_query(query)
        total_count = df["Count"].sum()
        st.metric("📱 Total Transactions (Brands)", f"{total_count:,.0f}")
        st.plotly_chart(px.bar(df, x="Brand", y="Count", title=ques, color_discrete_sequence=["purple"]))
        st.dataframe(df)

# -------------------
# USERS
# -------------------
elif menu == "👥 Users":
    st.sidebar.header("Filter Users")
    year = st.sidebar.selectbox("Select Year", list(range(2018, 2025)))
    quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])

    ques = st.selectbox("Select User Question", [
        "Top 15 States by Users",
        "Lowest 10 States by Users",
        "Top 15 Districts by Users",
        "Lowest 10 Districts by Users",
        "Top 15 Pincodes by Users",
        "Lowest 10 Pincodes by Users"
    ])

    # ---------- STATES ----------
    if "States" in ques:
        query = f"""
        SELECT State, SUM(RegisteredUser) as Users
        FROM map_user
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY State
        ORDER BY Users {"DESC LIMIT 15" if "Top" in ques else "ASC LIMIT 10"};
        """
        df = run_query(query)
        total_users = df["Users"].sum()
        st.metric("👥 Total Users", f"{total_users:,.0f}")
        fig = px.line(df, x="State", y="Users", title=ques, color_discrete_sequence=["green"])
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)

    # ---------- DISTRICTS ----------
    elif "Districts" in ques:
        query = f"""
        SELECT District, SUM(RegisteredUser) as Users
        FROM map_user
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY District
        ORDER BY Users {"DESC LIMIT 15" if "Top" in ques else "ASC LIMIT 10"};
        """
        df = run_query(query)
        total_users = df["Users"].sum()
        st.metric("👥 Total Users", f"{total_users:,.0f}")
        fig = px.line(df, x="District", y="Users", title=ques, color_discrete_sequence=["pink"])
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)

    # ---------- PINCODES ----------
    elif "Pincodes" in ques:
        query = f"""
        SELECT Pincode, SUM(RegisteredByUsers) as Users
        FROM top_user
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY Pincode
        ORDER BY Users {"DESC LIMIT 15" if "Top" in ques else "ASC LIMIT 10"};
        """
        df = run_query(query)
        total_users = df["Users"].sum()
        st.metric("👥 Total Users", f"{total_users:,.0f}")
        fig = px.line(df, x="Pincode", y="Users", title=ques, color_discrete_sequence=["orange"])
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)

# -------------------
# INSURANCE
# -------------------
elif menu == "🛡️ Insurance":
    st.sidebar.header("Filter Insurance")
    year = st.sidebar.selectbox("Select Year", list(range(2020, 2025)))
    quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])

    ques = st.selectbox("Select Insurance Question", [
        "Top 10 States by Insurance",
        "Lowest 10 States by Insurance",
        "Top 10 Districts by Insurance",
        "Lowest 10 Districts by Insurance",
        "Top 10 Pincodes by Insurance",
        "Lowest 10 Pincodes by Insurance"
    ])

    if "States" in ques:
        query = f"""
        SELECT State, SUM(Insurance_amount) as Amount
        FROM agg_insurance
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY State
        ORDER BY Amount {"DESC LIMIT 10" if "Top" in ques else "ASC LIMIT 10"};
        """
        df = run_query(query)
        total_insurance = df["Amount"].sum()
        st.metric("🛡️ Total Insurance Amount", f"{total_insurance:,.0f}")
        st.plotly_chart(px.pie(df, names="State", values="Amount", title=ques))
        st.dataframe(df)

    elif "Districts" in ques:
        query = f"""
        SELECT District, SUM(Transaction_amount) as Amount
        FROM map_insurance
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY District
        ORDER BY Amount {"DESC LIMIT 10" if "Top" in ques else "ASC LIMIT 10"};
        """
        df = run_query(query)
        total_insurance = df["Amount"].sum()
        st.metric("🛡️ Total Insurance Amount", f"{total_insurance:,.0f}")
        st.plotly_chart(px.pie(df, names="District", values="Amount", title=ques))
        st.dataframe(df)

    elif "Pincodes" in ques:
        query = f"""
        SELECT Pincode, SUM(Transaction_amount) as Amount
        FROM top_insurance
        WHERE Year = {year} AND Quarter = {quarter}
        GROUP BY Pincode
        ORDER BY Amount {"DESC LIMIT 10" if "Top" in ques else "ASC LIMIT 10"};
        """
        df = run_query(query)
        total_insurance = df["Amount"].sum()
        st.metric("🛡️ Total Insurance Amount", f"{total_insurance:,.0f}")
        st.plotly_chart(px.pie(df, names="Pincode", values="Amount", title=ques))
        st.dataframe(df)

# -------------------
# CUSTOM STYLES
# -------------------
st.markdown("""
    <style>
    /* App background */
    .stApp { background-color: #add8e6; }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f4e1d2; /* light peach */
        color: #000000;
    }

    /* Sidebar radio & selectbox label color */
    section[data-testid="stSidebar"] label {
        color: #4b0082;  /* dark purple */
        font-weight: bold;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 { 
        color: #003366; 
    }
    </style>
""", unsafe_allow_html=True) 