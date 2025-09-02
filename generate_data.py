# generate_data.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

N_SESSIONS = 20000
start = datetime(2025,1,1)

categories = ["fashion","home","beauty","electronics","mobiles"]
city_tiers = [1,2,3]

rows = []
for s in range(1, N_SESSIONS+1):
    session_id = f"S{s}"
    user_id = random.randint(1,6000)
    seller_id = random.randint(1,800)
    category = random.choice(categories)
    city_tier = random.choices(city_tiers, weights=[0.5,0.3,0.2])[0]
    ts = start + timedelta(days=random.randint(0,180), seconds=random.randint(0,86400))
    price = round(max(30, np.random.exponential(800)),2)
    # events probabilities (tweak if you want)
    saw = True
    added = np.random.rand() < 0.28
    checkout = added and (np.random.rand() < 0.45)
    purchased = checkout and (np.random.rand() < 0.6)

    # view
    rows.append({
        "session_id": session_id, "user_id": user_id, "seller_id": seller_id,
        "category": category, "city_tier": city_tier, "event":"view", "timestamp": ts, "order_value": None
    })
    if added:
        rows.append({**rows[-1], "event":"add_to_cart", "timestamp": ts + timedelta(seconds=30)})
    if checkout:
        rows.append({**rows[-1], "event":"checkout_start", "timestamp": ts + timedelta(seconds=90)})
    if purchased:
        rows.append({**rows[-1], "event":"purchase", "timestamp": ts + timedelta(seconds=180), "order_value": price})

df = pd.DataFrame(rows)
df = df.sort_values("timestamp")
df.to_csv("data/events.csv", index=False)
print("Saved data/events.csv with", df['session_id'].nunique(), "sessions and", len(df), "rows")
