import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="E-commerce Funnel Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("📊 E-commerce Funnel Dashboard")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    """Loads data and handles potential file errors."""
    try:
        df = pd.read_csv("data/sample_ecommerce_data.csv", parse_dates=["date"])
        return df
    except FileNotFoundError:
        st.error("Error: The data file 'data/sample_ecommerce_data.csv' was not found.")
        st.info("Please run the generate_data.py script first to create the data file.")
        return None

raw_df = load_data()

# Stop execution if data loading failed
if raw_df is None:
    st.stop()

# -------------------------------
# Transform Data for Dashboard
# -------------------------------
def transform_data(df):
    """Pivots data and ensures all required columns are present to prevent errors."""
    agg_df = (
        df.groupby(["date", "city_tier", "stage"])
          .agg({"user_id": "nunique", "amount": "sum"})
          .reset_index()
    )

    pivot_df = agg_df.pivot_table(
        index=["date", "city_tier"],
        columns="stage",
        values=["user_id", "amount"],
        fill_value=0
    )

    pivot_df.columns = [f"{metric}_{stage}" for metric, stage in pivot_df.columns]
    pivot_df = pivot_df.reset_index()

    # Ensure all expected columns exist, even if data for a stage is missing
    expected_cols = [
        "user_id_visit", "user_id_cart", "user_id_purchase",
        "amount_visit", "amount_cart", "amount_purchase"
    ]
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0

    return pivot_df

df = transform_data(raw_df)

if df.empty:
    st.warning("No data to process after transformation. Please check the source file.")
    st.stop()
    
# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filters")

city_filter = st.sidebar.multoselect(
    "Select City Tier(s):",
    options=df["city_tier"].unique(),
    default=df["city_tier"].unique()
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) != 2:
    st.stop()

start_date, end_date = date_range

# Compare just the date part of the 'date' column with the selected date range.
mask = (
    df["city_tier"].isin(city_filter) &
    (df["date"].dt.date.between(start_date, end_date))
)
df_filtered = df.loc[mask]

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# -------------------------------
# KPI Metrics
# -------------------------------
# Use correct column names created during transformation
total_visitors = df_filtered["user_id_visit"].sum()
total_carts = df_filtered["user_id_cart"].sum()
total_purchasers = df_filtered["user_id_purchase"].sum()
total_revenue = df_filtered["amount_purchase"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Visitors", f"{total_visitors:,}")
col2.metric("🛒 Carts", f"{total_carts:,}")
col3.metric("🛍️ Purchases", f"{total_purchasers:,}")
col4.metric("💰 Revenue", f"₹{total_revenue:,.2f}")

# -------------------------------
# Funnel Chart
# -------------------------------
st.subheader("📉 Funnel Conversion Analysis")

funnel_data = {
    "Stage": ["Visit", "Cart", "Purchase"],
    "Users": [total_visitors, total_carts, total_purchasers]
}
funnel_df = pd.DataFrame(funnel_data)

# Calculate the conversion rate separately to avoid errors
if total_visitors > 0:
    funnel_df['Conversion Rate'] = (funnel_df['Users'] / total_visitors * 100).round(2)
else:
    funnel_df['Conversion Rate'] = 0.0

funnel_chart = alt.Chart(funnel_df).mark_bar().encode(
    x=alt.X("Stage", sort=["Visit", "Cart", "Purchase"], title=None),
    y=alt.Y("Users", title="Number of Users"),
    color="Stage"
)

st.altair_chart(funnel_chart, use_container_width=True)

# -------------------------------
# Revenue Trend
# -------------------------------
st.subheader("📈 Revenue Over Time")

revenue_trend = (
    df_filtered.groupby(df_filtered['date'].dt.date)["amount_purchase"]
    .sum()
    .reset_index()
)

revenue_chart = alt.Chart(revenue_trend).mark_line(point=True).encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("amount_purchase:Q", title="Revenue (₹)"),
    tooltip=["date:T", "amount_purchase:Q"]
).interactive()

st.altair_chart(revenue_chart, use_container_width=True)

