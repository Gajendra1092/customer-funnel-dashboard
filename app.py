# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="E-commerce BA Dashboard",
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
city_tiers = st.sidebar.multiselect(
    "Select City Tier(s):",
    options=df["city_tier"].unique(),
    default=df["city_tier"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range:",
    [df["date"].min(), df["date"].max()]
)

filtered_df = df[
    (df["city_tier"].isin(city_tiers)) &
    (df["date"].between(date_range[0], date_range[1]))
]

# -------------------------------
# KPI Section
# -------------------------------
st.title("🛍️ E-commerce Business Analysis Dashboard")
st.markdown("### Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_users = filtered_df["user_id"].nunique()
purchased_users = filtered_df[filtered_df["stage"] == "purchased"]["user_id"].nunique()
conversion_rate = round((purchased_users / total_users) * 100, 2) if total_users else 0
revenue = filtered_df[filtered_df["stage"] == "purchased"]["amount"].sum()
aov = round(revenue / purchased_users, 2) if purchased_users else 0

col1.metric("👥 Total Users", total_users)
col2.metric("✅ Conversion Rate", f"{conversion_rate}%")
col3.metric("💰 Revenue", f"₹{revenue:,.0f}")
col4.metric("📦 Avg Order Value", f"₹{aov:,.0f}")

# -------------------------------
# Funnel Visualization
# -------------------------------
st.markdown("### 📊 Funnel Analysis by Stage")

funnel_counts = (
    filtered_df.groupby("stage")["user_id"]
    .nunique()
    .reindex(["visited", "added_to_cart", "purchased"])
    .fillna(0)
)

fig_funnel = go.Figure(go.Funnel(
    y=funnel_counts.index,
    x=funnel_counts.values,
    textinfo="value+percent initial"
))
st.plotly_chart(fig_funnel, use_container_width=True)

# -------------------------------
# City Tier Comparison
# -------------------------------
st.markdown("### 🏙️ City Tier Comparison")

city_funnel = (
    filtered_df.groupby(["city_tier", "stage"])["user_id"]
    .nunique()
    .reset_index()
    .pivot(index="city_tier", columns="stage", values="user_id")
    .fillna(0)
)

fig_city = px.bar(
    city_funnel,
    barmode="group",
    title="Stage-wise Comparison by City Tier"
)
st.plotly_chart(fig_city, use_container_width=True)

# -------------------------------
# Conversion Trend Over Time
# -------------------------------
st.markdown("### 📈 Conversion Trend Over Time")

trend_df = (
    filtered_df.groupby("date")
    .agg(total_users=("user_id", "nunique"),
         purchased_users=("user_id", lambda x: (filtered_df.loc[x.index, "stage"] == "purchased").sum()))
    .reset_index()
)
trend_df["conversion_rate"] = trend_df["purchased_users"] / trend_df["total_users"]

fig_trend = px.line(
    trend_df, x="date", y="conversion_rate",
    title="Daily Conversion Rate"
)
st.plotly_chart(fig_trend, use_container_width=True)

# -------------------------------
# User Journey Drilldown
# -------------------------------
st.markdown("### 🔍 User Journey Drilldown")

user_id = st.selectbox("Select a User ID", filtered_df["user_id"].unique())
journey = filtered_df[filtered_df["user_id"] == user_id].sort_values("date")

st.write(journey[["date", "stage", "amount", "city_tier"]])
