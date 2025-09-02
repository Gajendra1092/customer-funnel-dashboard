# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load():
    return pd.read_csv("data/events.csv", parse_dates=["timestamp"])

df = load()
st.title("E-commerce Funnel Dashboard")

# KPIs
views = df[df.event=="view"].session_id.nunique()
adds = df[df.event=="add_to_cart"].session_id.nunique()
checkouts = df[df.event=="checkout_start"].session_id.nunique()
purchases = df[df.event=="purchase"].session_id.nunique()
aov = df[df.event=="purchase"].order_value.mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Views", views)
c2.metric("Add to Carts", adds)
c3.metric("Checkouts", checkouts)
c4.metric("Purchases", purchases)
st.metric("AOV (avg order value)", f"₹{aov:.2f}")

# Filters
tier = st.selectbox("City tier", options=["All"] + sorted(df.city_tier.unique().tolist()))
if tier != "All":
    dff = df[df.city_tier==int(tier)]
else:
    dff = df

# Funnel chart
funnel_counts = {
    'view': dff[dff.event=="view"].session_id.nunique(),
    'add_to_cart': dff[dff.event=="add_to_cart"].session_id.nunique(),
    'checkout_start': dff[dff.event=="checkout_start"].session_id.nunique(),
    'purchase': dff[dff.event=="purchase"].session_id.nunique()
}
funnel_df = pd.DataFrame({"step": list(funnel_counts.keys()), "sessions": list(funnel_counts.values())})
fig = px.bar(funnel_df, x="step", y="sessions", title="Funnel counts")
st.plotly_chart(fig)

# Conversion by category
cat = dff[dff.event=="purchase"].groupby("category").order_value.agg(["count","mean"]).reset_index().sort_values("count", ascending=False)
st.subheader("Purchases by category")
st.dataframe(cat)
