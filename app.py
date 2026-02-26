import streamlit as st
import pandas as pd

st.set_page_config(page_title="FTTS Intelligence", layout="wide")

# ---------- Utility ----------

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

# ---------- Load Data ----------

@st.cache_data
def load_data():
    monthly = pd.read_csv("clean_monthly_trend.csv")
    product = pd.read_csv("clean_product_performance.csv")
    doctor = pd.read_csv("clean_doctor_spend.csv")
    gl = pd.read_csv("clean_glhead_spend.csv")
    audience = pd.read_csv("clean_target_audience.csv")
    delay = pd.read_csv("clean_execution_delay.csv")

    # Clean categories
    doctor["Doctor"] = clean_category(doctor["Doctor"])
    audience["TargetAudience"] = clean_category(audience["TargetAudience"])

    # ---------- Fiscal Year Calculation ----------
    monthly["FiscalYear"] = monthly.apply(
        lambda x: x["Year"] + 1 if x["Month"] >= 7 else x["Year"], axis=1
    )

    # Keep complete fiscal years only
    monthly = monthly[(monthly["FiscalYear"] >= 2018) & (monthly["FiscalYear"] <= 2025)]

    return monthly, product, doctor, gl, audience, delay

monthly, product, doctor, gl, audience, delay = load_data()

# ---------- Sidebar ----------
st.sidebar.title("FTTS Analytics")
page = st.sidebar.radio("Select Module", [
    "Executive Overview",
    "Yearly Spend",
    "Doctor Engagement",
    "Product Intelligence",
    "Financial Allocation",
    "Audience Strategy"
])

# ============================================================
# EXECUTIVE OVERVIEW (FISCAL YEARS)
# ============================================================

if page == "Executive Overview":
    st.title("Executive Overview (Fiscal Years)")

    fy_spend = monthly.groupby("FiscalYear")["TotalSpend"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Spend", format_number(fy_spend.sum()))
    c2.metric("Total Activities", format_number(monthly["Activities"].sum()))
    c3.metric("Avg Execution Delay", f"{delay['AvgDelayDays'][0]:.1f} Days")

    st.subheader("Fiscal Year Spend Trend")
    st.line_chart(fy_spend)

    st.subheader("Fiscal Year Comparison")
    st.bar_chart(fy_spend)

# ============================================================
# YEARLY SPEND (FISCAL)
# ============================================================

elif page == "Yearly Spend":
    st.title("Fiscal Year Spend Analysis")

    fy_spend = monthly.groupby("FiscalYear")["TotalSpend"].sum()
    fy_growth = fy_spend.pct_change() * 100

    c1, c2 = st.columns(2)
    c1.metric("Best Fiscal Year", format_number(fy_spend.max()))
    c2.metric("Highest Growth", f"{fy_growth.max():.1f}%")

    st.bar_chart(fy_spend)
    st.line_chart(fy_growth)

# ============================================================
# DOCTOR ENGAGEMENT (DESCENDING + NON-CONGESTED)
# ============================================================

elif page == "Doctor Engagement":
    st.title("Doctor Engagement")

    df = doctor[doctor["Doctor"] != "Unknown"]
    df = df.sort_values("TotalSpend", ascending=False)

    top_n = st.slider("Show Top Doctors", 5, 30, 10)
    st.metric("Total Doctor Spend", format_number(df["TotalSpend"].sum()))

    st.bar_chart(df.set_index("Doctor")["TotalSpend"].head(top_n))
    st.dataframe(df)

# ============================================================
# PRODUCT INTELLIGENCE (DESCENDING)
# ============================================================

elif page == "Product Intelligence":
    st.title("Product Investment")

    df = product.sort_values("TotalSpend", ascending=False)

    top_n = st.slider("Show Top Products", 5, 30, 10)
    st.metric("Total Product Spend", format_number(df["TotalSpend"].sum()))

    st.bar_chart(df.set_index("Product")["TotalSpend"].head(top_n))
    st.dataframe(df)

# ============================================================
# FINANCIAL ALLOCATION (DECONGESTED + FULL ACCESS)
# ============================================================

elif page == "Financial Allocation":
    st.title("GL Head Financial Allocation")

    df = gl.sort_values("TotalSpend", ascending=False)

    st.metric("Total Budget", format_number(df["TotalSpend"].sum()))

    top_n = st.slider("Show Top GL Heads", 5, 30, 10)
    st.bar_chart(df.set_index("GLHead")["TotalSpend"].head(top_n))

    st.subheader("Inspect Specific GL Head")
    selected = st.selectbox("Select GL Head", df["GLHead"])
    st.line_chart(df[df["GLHead"] == selected]["TotalSpend"])

    st.dataframe(df)

# ============================================================
# AUDIENCE STRATEGY (TOP + SELECTABLE)
# ============================================================

elif page == "Audience Strategy":
    st.title("Audience Investment Strategy")

    df = audience[audience["TargetAudience"] != "Unknown"]
    df = df.sort_values("TotalSpend", ascending=False)

    st.metric("Total Audience Spend", format_number(df["TotalSpend"].sum()))

    top_n = st.slider("Show Top Audiences", 5, 30, 10)
    st.bar_chart(df.set_index("TargetAudience")["TotalSpend"].head(top_n))

    st.subheader("Analyze Specific Audience")
    selected = st.selectbox("Select Audience", df["TargetAudience"])
    st.line_chart(df[df["TargetAudience"] == selected]["TotalSpend"])

    st.dataframe(df)
