import streamlit as st
import pandas as pd

st.set_page_config(page_title="FTTS Intelligence — Pharmevo", layout="wide")

# ============================================================
# UNIVERSAL NUMBER FORMATTER (K M B)
# ============================================================

def format_number(num):
    num = float(num)
    if abs(num) >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif abs(num) >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num/1_000:.2f}K"
    return f"{num:.0f}"

def clean_category(series):
    return series.replace(["N/P", "", "NULL"], "Unknown")

def format_dataframe(df, col):
    temp = df.copy()
    temp[col] = temp[col].apply(format_number)
    return temp

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    monthly = pd.read_csv("clean_monthly_trend.csv")
    product = pd.read_csv("clean_product_performance.csv")
    doctor = pd.read_csv("clean_doctor_spend.csv")
    gl = pd.read_csv("clean_glhead_spend.csv")
    audience = pd.read_csv("clean_target_audience.csv")
    delay = pd.read_csv("clean_execution_delay.csv")

    doctor["Doctor"] = clean_category(doctor["Doctor"])
    audience["TargetAudience"] = clean_category(audience["TargetAudience"])

    # ========================================================
    # ✅ FISCAL YEAR (START YEAR LABELING)
    # 1 July 2017 → 30 June 2018 = FY 2017
    # ========================================================

    monthly["FiscalYear"] = monthly.apply(
        lambda x: x["Year"] if x["Month"] >= 7 else x["Year"] - 1,
        axis=1
    )

    # Keep COMPLETE fiscal years only
    monthly = monthly[(monthly["FiscalYear"] >= 2017) & (monthly["FiscalYear"] <= 2024)]

    # Optional readable label
    monthly["FY_Label"] = monthly["FiscalYear"].apply(
        lambda y: f"FY {y} (Jul {y} – Jun {y+1})"
    )

    return monthly, product, doctor, gl, audience, delay

monthly, product, doctor, gl, audience, delay = load_data()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("FTTS Intelligence")
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
    st.title("Executive Overview — Fiscal Years")

    fy_spend = monthly.groupby("FY_Label")["TotalSpend"].sum()
    total_activities = monthly["Activities"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Spend", format_number(fy_spend.sum()))
    c2.metric("Total Activities", format_number(total_activities))
    c3.metric("Avg Execution Delay", f"{delay['AvgDelayDays'][0]:.1f} Days")

    st.subheader("Fiscal Year Spend Trend")
    st.line_chart(fy_spend)

    st.subheader("Fiscal Year Comparison")
    st.bar_chart(fy_spend)

# ============================================================
# YEARLY SPEND
# ============================================================

elif page == "Yearly Spend":
    st.title("Fiscal Year Spend Analysis")

    fy_spend = monthly.groupby("FY_Label")["TotalSpend"].sum()
    fy_growth = fy_spend.pct_change() * 100

    c1, c2 = st.columns(2)
    c1.metric("Highest Spend", format_number(fy_spend.max()))
    c2.metric("Highest Growth", f"{fy_growth.max():.1f}%")

    st.bar_chart(fy_spend)
    st.line_chart(fy_growth)

# ============================================================
# DOCTOR ENGAGEMENT
# ============================================================

elif page == "Doctor Engagement":
    st.title("Doctor Engagement Analysis")

    df = doctor[doctor["Doctor"] != "Unknown"]
    df = df.sort_values("TotalSpend", ascending=False)

    st.metric("Total Doctor Spend", format_number(df["TotalSpend"].sum()))

    top_n = st.slider("Show Top Doctors", 5, 30, 10)
    st.bar_chart(df.set_index("Doctor")["TotalSpend"].head(top_n))

    st.dataframe(format_dataframe(df, "TotalSpend"))

# ============================================================
# PRODUCT INTELLIGENCE
# ============================================================

elif page == "Product Intelligence":
    st.title("Product Investment Intelligence")

    df = product.sort_values("TotalSpend", ascending=False)

    st.metric("Total Product Spend", format_number(df["TotalSpend"].sum()))

    top_n = st.slider("Show Top Products", 5, 30, 10)
    st.bar_chart(df.set_index("Product")["TotalSpend"].head(top_n))

    st.dataframe(format_dataframe(df, "TotalSpend"))

# ============================================================
# FINANCIAL ALLOCATION
# ============================================================

elif page == "Financial Allocation":
    st.title("GL Head Financial Allocation")

    df = gl.sort_values("TotalSpend", ascending=False)

    st.metric("Total Budget Allocation", format_number(df["TotalSpend"].sum()))

    top_n = st.slider("Show Top GL Heads", 5, 30, 10)
    st.bar_chart(df.set_index("GLHead")["TotalSpend"].head(top_n))

    st.subheader("Inspect Specific GL Head")
    selected = st.selectbox("Select GL Head", df["GLHead"])
    value = df[df["GLHead"] == selected]["TotalSpend"].sum()
    st.metric("Selected GL Spend", format_number(value))

    st.dataframe(format_dataframe(df, "TotalSpend"))

# ============================================================
# AUDIENCE STRATEGY
# ============================================================

elif page == "Audience Strategy":
    st.title("Audience Investment Strategy")

    df = audience[audience["TargetAudience"] != "Unknown"]
    df = df.sort_values("TotalSpend", ascending=False)

    st.metric("Total Audience Spend", format_number(df["TotalSpend"].sum()))

    top_n = st.slider("Show Top Audiences", 5, 30, 10)
    st.bar_chart(df.set_index("TargetAudience")["TotalSpend"].head(top_n))

    st.subheader("Inspect Specific Audience")
    selected = st.selectbox("Select Audience", df["TargetAudience"])
    value = df[df["TargetAudience"] == selected]["TotalSpend"].sum()
    st.metric("Selected Audience Spend", format_number(value))

    st.dataframe(format_dataframe(df, "TotalSpend"))
