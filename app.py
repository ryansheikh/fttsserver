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

def clean_category(series):
    return series.replace(["N/P", "", "NULL"], "Unknown")

@st.cache_data
def load_data():
    monthly = pd.read_csv("clean_monthly_trend.csv")
    product = pd.read_csv("clean_product_performance.csv")
    doctor = pd.read_csv("clean_doctor_spend.csv")
    activity = pd.read_csv("clean_activity_analysis.csv")
    team = pd.read_csv("clean_team_performance.csv")
    transfer = pd.read_csv("clean_transfer_type.csv")
    gl = pd.read_csv("clean_glhead_spend.csv")
    audience = pd.read_csv("clean_target_audience.csv")
    high_cost = pd.read_csv("clean_high_cost_activities.csv")
    delay = pd.read_csv("clean_execution_delay.csv")

    # Year filter → complete years only
    monthly = monthly[(monthly["Year"] >= 2018) & (monthly["Year"] <= 2025)]

    # Clean categories
    doctor["Doctor"] = clean_category(doctor["Doctor"])
    audience["TargetAudience"] = clean_category(audience["TargetAudience"])
    high_cost["Doctor"] = clean_category(high_cost["Doctor"])

    return monthly, product, doctor, activity, team, transfer, gl, audience, high_cost, delay

monthly, product, doctor, activity, team, transfer, gl, audience, high_cost, delay = load_data()

# ---------- Sidebar ----------
st.sidebar.title("Analytics Navigation")

page = st.sidebar.radio("Select Module", [
    "Executive Overview",
    "Yearly Performance",
    "Doctor Engagement",
    "Product Intelligence",
    "Activity Efficiency",
    "Financial Allocation",
    "Audience Strategy",
    "Risk Monitoring"
])

# ---------- EXECUTIVE OVERVIEW ----------
if page == "Executive Overview":
    st.title("Executive Overview (2018–2025)")

    total_spend = monthly["TotalSpend"].sum()
    total_activities = monthly["Activities"].sum()
    avg_delay = delay["AvgDelayDays"][0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Spend", format_number(total_spend))
    c2.metric("Total Activities", format_number(total_activities))
    c3.metric("Avg Execution Delay", f"{avg_delay:.1f} Days")

    yearly = monthly.groupby("Year")["TotalSpend"].sum()
    st.subheader("Yearly Spend Trend")
    st.line_chart(yearly)

    st.subheader("Spend Distribution by Year")
    st.bar_chart(yearly)

# ---------- YEARLY PERFORMANCE ----------
elif page == "Yearly Performance":
    st.title("Year-over-Year Performance")

    yearly_spend = monthly.groupby("Year")["TotalSpend"].sum()
    yoy_growth = yearly_spend.pct_change() * 100

    c1, c2 = st.columns(2)
    c1.metric("Best Year Spend", format_number(yearly_spend.max()))
    c2.metric("Highest Growth %", f"{yoy_growth.max():.1f}%")

    st.subheader("YoY Spend Comparison")
    st.bar_chart(yearly_spend)

    st.subheader("Growth Rate %")
    st.line_chart(yoy_growth)

# ---------- DOCTOR ENGAGEMENT ----------
elif page == "Doctor Engagement":
    st.title("Doctor Engagement Intelligence")

    df = doctor[doctor["Doctor"] != "Unknown"]
    df = df.sort_values("TotalSpend", ascending=False)

    c1, c2 = st.columns(2)
    c1.metric("Total Doctor Spend", format_number(df["TotalSpend"].sum()))
    c2.metric("Active Doctors", df["Doctor"].nunique())

    st.subheader("Top Doctors by Investment")
    st.bar_chart(df.set_index("Doctor")["TotalSpend"].head(15))

    st.subheader("Doctor Spend Distribution")
    st.line_chart(df["TotalSpend"])

# ---------- PRODUCT INTELLIGENCE ----------
elif page == "Product Intelligence":
    st.title("Product Investment Strategy")

    df = product.sort_values("TotalSpend", ascending=False)

    st.metric("Total Product Investment", format_number(df["TotalSpend"].sum()))
    st.bar_chart(df.set_index("Product")["TotalSpend"].head(15))

    st.subheader("Product Activity Comparison")
    st.line_chart(df["TotalSpend"])

# ---------- ACTIVITY EFFICIENCY ----------
elif page == "Activity Efficiency":
    st.title("Activity Cost Intelligence")

    st.metric("Total Activity Spend", format_number(activity["TotalSpend"].sum()))
    st.bar_chart(activity.set_index("ActivityType")["TotalSpend"])
    st.line_chart(activity["AvgCost"])

# ---------- FINANCIAL ----------
elif page == "Financial Allocation":
    st.title("Budget Allocation by GL Head")

    st.metric("Total Budget", format_number(gl["TotalSpend"].sum()))
    st.bar_chart(gl.set_index("GLHead")["TotalSpend"])

# ---------- AUDIENCE ----------
elif page == "Audience Strategy":
    st.title("Audience Targeting Analysis")

    df = audience[audience["TargetAudience"] != "Unknown"]
    st.metric("Total Audience Spend", format_number(df["TotalSpend"].sum()))

    st.bar_chart(df.set_index("TargetAudience")["TotalSpend"])
    st.line_chart(df["TotalSpend"])

# ---------- RISK ----------
elif page == "Risk Monitoring":
    st.title("High Cost Activity Monitoring")

    df = high_cost[high_cost["Doctor"] != "Unknown"]

    st.metric("Maximum Activity Cost", format_number(df["Amount"].max()))
    st.dataframe(df.sort_values("Amount", ascending=False))
