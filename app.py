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
    df = pd.read_csv("data/sample_ecommerce_data.csv", parse_dates=["date"])
    return df

raw_df = load_data()

# -------------------------------
# Transform Data for Dashboard
# -------------------------------
def transform_data(df):
    # Aggregate users and revenue by stage
    agg_df = (
        df.groupby(["date", "city_tier", "stage"])
          .agg({"user_id": "nunique", "amount": "sum"})
          .reset_index()
    )

    # Pivot so each stage becomes a column
    pivot_df = agg_df.pivot_table(
        index=["date", "city_tier"],
        columns="stage",
        values=["user_id", "amount"],
        fill_value=0
    )

    # Flatten column names
    pivot_df.columns = [f"{metric}_{stage}" for metric, stage in pivot_df.columns]
    pivot_df = pivot_df.reset_index()

    return pivot_df

df = transform_data(raw_df)

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filters")

city_filter = st.sidebar.multiselect(
    "Select City Tier(s):",
    options=df["city_tier"].unique(),
    default=df["city_tier"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range:",
    [df["date"].min(), df["date"].max()]
)

# Apply filters
mask = (
    df["city_tier"].isin(city_filter)
    & (df["date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
)
df_filtered = df.loc[mask]

# -------------------------------
# KPI Metrics
# -------------------------------
total_visitors = df_filtered["user_id_visit"].sum() if "user_id_visit" in df_filtered else 0
total_orders = df_filtered["user_id_cart"].sum() if "user_id_cart" in df_filtered else 0
total_revenue = df_filtered["amount_purchase"].sum() if "amount_purchase" in df_filtered else 0

col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Visitors", f"{total_visitors:,}")
col2.metric("🛒 Total Orders (Cart Adds)", f"{total_orders:,}")
col3.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")

# -------------------------------
# Funnel Chart
# -------------------------------
st.subheader("📉 Funnel Conversion by Stage")

funnel_data = {
    "Stage": ["Visit", "Cart", "Purchase"],
    "Users": [
        total_visitors,
        total_orders,
        df_filtered["user_id_purchase"].sum() if "user_id_purchase" in df_filtered else 0
    ]
}
funnel_df = pd.DataFrame(funnel_data)

funnel_chart = alt.Chart(funnel_df).mark_bar().encode(
    x=alt.X("Stage", sort=["Visit", "Cart", "Purchase"]),
    y="Users",
    color="Stage"
).properties(width=600)

st.altair_chart(funnel_chart, use_container_width=True)

# -------------------------------
# Revenue Trend
# -------------------------------
st.subheader("📈 Revenue Over Time")

if "amount_purchase" in df_filtered:
    revenue_trend = (
        df_filtered.groupby("date")["amount_purchase"]
        .sum()
        .reset_index()
    )

    revenue_chart = alt.Chart(revenue_trend).mark_line(point=True).encode(
        x="date:T",
        y="amount_purchase:Q"
    ).properties(width=800)

    st.altair_chart(revenue_chart, use_container_width=True)
else:
    st.info("No purchase data available for the selected filters.")
