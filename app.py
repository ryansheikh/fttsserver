import streamlit as st
import pandas as pd

st.set_page_config(page_title="FTTS Intelligence Dashboard", layout="wide")
st.title("Pharmevo FTTS Commercial Intelligence")

@st.cache_data
def load_data():
    return {
        "monthly": pd.read_csv("clean_monthly_trend.csv"),
        "product": pd.read_csv("clean_product_performance.csv"),
        "doctor": pd.read_csv("clean_doctor_spend.csv"),
        "activity": pd.read_csv("clean_activity_analysis.csv"),
        "team": pd.read_csv("clean_team_performance.csv"),
        "transfer": pd.read_csv("clean_transfer_type.csv"),
        "gl": pd.read_csv("clean_glhead_spend.csv"),
        "audience": pd.read_csv("clean_target_audience.csv"),
        "mix": pd.read_csv("clean_product_activity_mix.csv"),
        "high_cost": pd.read_csv("clean_high_cost_activities.csv"),
        "delay": pd.read_csv("clean_execution_delay.csv"),
    }

data = load_data()

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Total Spend", f"{data['monthly']['TotalSpend'].sum():,.0f}")
c2.metric("Total Activities", f"{data['monthly']['Activities'].sum():,}")
c3.metric("Avg Execution Delay (Days)", f"{data['delay']['AvgDelayDays'][0]:.2f}")

# Trend
st.subheader("Monthly Spend Trend")
st.line_chart(data["monthly"]["TotalSpend"])

# Product Performance
st.subheader("Top Products")
st.bar_chart(data["product"].set_index("Product")["TotalSpend"].head(10))

# Doctor Spend
st.subheader("Top Doctors")
st.bar_chart(data["doctor"].set_index("Doctor")["TotalSpend"].head(10))

# Activity Type
st.subheader("Activity Cost Distribution")
st.bar_chart(data["activity"].set_index("ActivityType")["TotalSpend"])

# Team Performance
st.subheader("Team Performance")
st.bar_chart(data["team"].set_index("RequestorTeams")["TotalSpend"])

# Transfer Type
st.subheader("Transfer Type Spend")
st.bar_chart(data["transfer"].set_index("TransferType")["TotalSpend"])

# GL Head
st.subheader("Financial Allocation by GL Head")
st.bar_chart(data["gl"].set_index("GLHead")["TotalSpend"])

# Target Audience
st.subheader("Target Audience Spend")
st.bar_chart(data["audience"].set_index("TargetAudience")["TotalSpend"])

# Product Activity Mix Table
st.subheader("Product Activity Mix")
st.dataframe(data["mix"])

# High Cost Activities Table
st.subheader("Top Cost Activities")
st.dataframe(data["high_cost"])