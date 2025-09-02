import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="E-Commerce Funnel Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_ecommerce_data.csv", parse_dates=["date"])
    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔎 Filters")

# Date range filter
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Convert to pandas Timestamps
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# City tier filter
city_tiers = st.sidebar.multiselect(
    "Select City Tier(s)",
    options=sorted(df["city_tier"].unique()),
    default=sorted(df["city_tier"].unique())
)

# Apply filters
df = df[
    (df["date"].between(start_date, end_date)) &
    (df["city_tier"].isin(city_tiers))
]

# -------------------------------
# KPIs
# -------------------------------
st.title("🛍️ E-Commerce Funnel Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Visitors", f"{df['visitors'].sum():,}")
with col2:
    st.metric("🛒 Total Orders", f"{df['orders'].sum():,}")
with col3:
    st.metric("💰 Total Revenue", f"₹{df['revenue'].sum():,.0f}")

st.markdown("---")

# -------------------------------
# Funnel by City Tier
# -------------------------------
st.subheader("📊 Funnel by City Tier")

funnel_df = df.groupby("city_tier")[["visitors", "orders"]].sum().reset_index()
funnel_df["conversion_rate"] = funnel_df["orders"] / funnel_df["visitors"] * 100

fig_funnel = go.Figure(go.Funnel(
    y=funnel_df["city_tier"],
    x=funnel_df["visitors"],
    textinfo="value+percent initial",
    name="Visitors"
))
fig_funnel.add_trace(go.Funnel(
    y=funnel_df["city_tier"],
    x=funnel_df["orders"],
    textinfo="value+percent initial",
    name="Orders"
))
st.plotly_chart(fig_funnel, use_container_width=True)

# -------------------------------
# Revenue Trend
# -------------------------------
st.subheader("📈 Revenue Trend Over Time")

revenue_trend = df.groupby("date")["revenue"].sum().reset_index()
fig_revenue = px.line(revenue_trend, x="date", y="revenue", title="Daily Revenue")
st.plotly_chart(fig_revenue, use_container_width=True)

# -------------------------------
# Conversion Rate by City Tier
# -------------------------------
st.subheader("🏙️ Conversion Rate by City Tier")

fig_conv = px.bar(
    funnel_df,
    x="city_tier",
    y="conversion_rate",
    text="conversion_rate",
    title="Conversion Rate (%)",
    labels={"conversion_rate": "Conversion Rate (%)"}
)
st.plotly_chart(fig_conv, use_container_width=True)

# -------------------------------
# Raw Data Toggle
# -------------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df)
