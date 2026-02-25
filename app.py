import streamlit as st
import pandas as pd

st.set_page_config(page_title="FTTS Intelligence", layout="wide")

# ---------- Utility Functions ----------

def format_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    return f"{num:.0f}"

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

# ---------- Sidebar Navigation ----------
st.sidebar.title("FTTS Analytics Modules")

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Executive Overview",
        "Monthly Trend",
        "Product Intelligence",
        "Doctor Intelligence",
        "Activity Analytics",
        "Team Performance",
        "Financial Allocation",
        "Transfer Analysis",
        "Audience Targeting",
        "High Cost Monitoring"
    ]
)

# ---------- EXECUTIVE OVERVIEW ----------
if page == "Executive Overview":
    st.title("Executive Overview")

    total_spend = data["monthly"]["TotalSpend"].sum()
    total_activities = data["monthly"]["Activities"].sum()
    avg_delay = data["delay"]["AvgDelayDays"][0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Spend", format_number(total_spend))
    c2.metric("Total Activities", format_number(total_activities))
    c3.metric("Avg Execution Delay (Days)", f"{avg_delay:.1f}")

    st.subheader("Spend Trend")
    st.line_chart(data["monthly"].set_index("Month")["TotalSpend"])

# ---------- MONTHLY TREND ----------
elif page == "Monthly Trend":
    st.title("Monthly Spend Analysis")

    df = data["monthly"]

    c1, c2 = st.columns(2)
    c1.metric("Total Spend", format_number(df["TotalSpend"].sum()))
    c2.metric("Total Activities", format_number(df["Activities"].sum()))

    st.line_chart(df["TotalSpend"])
    st.dataframe(df)

# ---------- PRODUCT INTELLIGENCE ----------
elif page == "Product Intelligence":
    st.title("Product Performance")

    df = data["product"].sort_values("TotalSpend", ascending=False)

    c1, c2 = st.columns(2)
    c1.metric("Total Product Spend", format_number(df["TotalSpend"].sum()))
    c2.metric("Unique Products", df["Product"].nunique())

    st.bar_chart(df.set_index("Product")["TotalSpend"].head(15))
    st.dataframe(df)

# ---------- DOCTOR INTELLIGENCE ----------
elif page == "Doctor Intelligence":
    st.title("Doctor Engagement Analysis")

    df = data["doctor"].sort_values("TotalSpend", ascending=False)

    c1, c2 = st.columns(2)
    c1.metric("Total Doctor Spend", format_number(df["TotalSpend"].sum()))
    c2.metric("Total Doctors", df["Doctor"].nunique())

    st.bar_chart(df.set_index("Doctor")["TotalSpend"].head(15))
    st.dataframe(df)

# ---------- ACTIVITY ANALYTICS ----------
elif page == "Activity Analytics":
    st.title("Activity Cost Intelligence")

    df = data["activity"]

    c1, c2 = st.columns(2)
    c1.metric("Total Activity Spend", format_number(df["TotalSpend"].sum()))
    c2.metric("Total Activity Types", df["ActivityType"].nunique())

    st.bar_chart(df.set_index("ActivityType")["TotalSpend"])
    st.dataframe(df)

# ---------- TEAM PERFORMANCE ----------
elif page == "Team Performance":
    st.title("Team Performance Analysis")

    df = data["team"]

    c1, c2 = st.columns(2)
    c1.metric("Total Team Spend", format_number(df["TotalSpend"].sum()))
    c2.metric("Teams", df["RequestorTeams"].nunique())

    st.bar_chart(df.set_index("RequestorTeams")["TotalSpend"])
    st.dataframe(df)

# ---------- FINANCIAL ALLOCATION ----------
elif page == "Financial Allocation":
    st.title("GL Head Allocation")

    df = data["gl"]

    st.metric("Total Allocated Budget", format_number(df["TotalSpend"].sum()))
    st.bar_chart(df.set_index("GLHead")["TotalSpend"])
    st.dataframe(df)

# ---------- TRANSFER ANALYSIS ----------
elif page == "Transfer Analysis":
    st.title("Transfer Type Analysis")

    df = data["transfer"]

    st.metric("Total Transfer Spend", format_number(df["TotalSpend"].sum()))
    st.bar_chart(df.set_index("TransferType")["TotalSpend"])
    st.dataframe(df)

# ---------- AUDIENCE TARGETING ----------
elif page == "Audience Targeting":
    st.title("Target Audience Strategy")

    df = data["audience"]

    st.metric("Total Audience Spend", format_number(df["TotalSpend"].sum()))
    st.bar_chart(df.set_index("TargetAudience")["TotalSpend"])
    st.dataframe(df)

# ---------- HIGH COST MONITORING ----------
elif page == "High Cost Monitoring":
    st.title("High Cost Activity Monitoring")

    df = data["high_cost"]

    st.metric("Max Single Activity Cost", format_number(df["Amount"].max()))
    st.dataframe(df)
