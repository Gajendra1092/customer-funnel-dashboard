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
    """Loads data and handles file not found errors."""
    try:
        df = pd.read_csv("data/sample_ecommerce_data.csv", parse_dates=["date"])
        return df
    except FileNotFoundError:
        st.error("Error: The data file 'data/sample_ecommerce_data.csv' was not found.")
        st.info("Please make sure the data file is in the correct directory.")
        return None # Return None to indicate failure

raw_df = load_data()

# Stop execution if data loading failed
if raw_df is None:
    st.stop()

# -------------------------------
# Transform Data for Dashboard
# -------------------------------
def transform_data(df):
    """Aggregates and pivots data, ensuring all required columns are present."""
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

    # --- FIX: Ensure all expected columns exist ---
    # This prevents errors if a stage (e.g., 'purchase') is missing from the data
    expected_cols = [
        "user_id_visit", "user_id_cart", "user_id_purchase",
        "amount_visit", "amount_cart", "amount_purchase"
    ]
    for col in expected_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0 # Add missing column and fill with 0

    return pivot_df

df = transform_data(raw_df)

# Stop if dataframe is empty after transformation
if df.empty:
    st.warning("The dataframe is empty after processing. No data to display.")
    st.stop()
    
# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "Select City Tier(s):",
    options=df["city_tier"].unique(),
    default=df["city_tier"].unique()
)

# Convert date column to date objects for the widget
min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Handle case where user selects only one date
if len(date_range) != 2:
    st.sidebar.warning("Please select a valid date range (start and end date).")
    st.stop()

start_date, end_date = date_range

# Apply filters
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
total_visitors = df_filtered["user_id_visit"].sum()
total_orders = df_filtered["user_id_cart"].sum()
total_revenue = df_filtered["amount_purchase"].sum()
total_purchasers = df_filtered["user_id_purchase"].sum()


col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Visitors", f"{total_visitors:,}")
col2.metric("🛒 Carts Created", f"{total_orders:,}")
col3.metric("🛍️ Purchases Made", f"{total_purchasers:,}")
col4.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")


# -------------------------------
# Funnel Chart
# -------------------------------
st.subheader("📉 Funnel Conversion by Stage")

funnel_data = {
    "Stage": ["Visit", "Cart", "Purchase"],
    "Users": [total_visitors, total_orders, total_purchasers]
}
funnel_df = pd.DataFrame(funnel_data)
# Prevent division by zero if there are no visitors
funnel_df['Conversion Rate'] = (
    (funnel_df['Users'] / total_visitors * 100) if total_visitors > 0 else 0
).round(2)


funnel_chart = alt.Chart(funnel_df).mark_bar().encode(
    x=alt.X("Stage", sort=["Visit", "Cart", "Purchase"], title=None),
    y=alt.Y("Users", title="Number of Unique Users"),
    color=alt.Color("Stage", legend=None)
).properties(
    width=600
)

# Add text labels for user counts and conversion rates
text_users = funnel_chart.mark_text(
    align='center',
    baseline='bottom',
    dy=-15, # Nudge text up
    size=14,
    color='black'
).encode(
    text='Users:Q'
)

text_conversion = funnel_chart.mark_text(
    align='center',
    baseline='bottom',
    dy=5, # Nudge text down
    size=12,
    color='gray'
).encode(
    text=alt.Text('Conversion Rate:Q', format='.1f', formatType='number')
)

st.altair_chart(funnel_chart + text_users + text_conversion, use_container_width=True)

# -------------------------------
# Revenue Trend
# -------------------------------
st.subheader("📈 Revenue Over Time")

revenue_trend = (
    df_filtered.groupby(df_filtered['date'].dt.date)["amount_purchase"]
    .sum()
    .reset_index()
)

revenue_chart = alt.Chart(revenue_trend).mark_line(point=True, strokeWidth=3).encode(
    x=alt.X("date:T", title="Date"),
    y=alt.Y("amount_purchase:Q", title="Revenue (₹)"),
    tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("amount_purchase:Q", title="Revenue", format=',.0f')]
).properties(
    #title="Daily Revenue Trend"
)

st.altair_chart(revenue_chart, use_container_width=True)