# generate_data.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# -------------------------------
# Config
# -------------------------------
NUM_USERS = 2000
DAYS = 60
CITY_TIERS = ["Tier-1", "Tier-2", "Tier-3"]

# -------------------------------
# Generate synthetic dataset
# -------------------------------
def generate_data():
    data = []
    start_date = datetime.today() - timedelta(days=DAYS)

    for user_id in range(1, NUM_USERS + 1):
        city_tier = np.random.choice(CITY_TIERS, p=[0.3, 0.4, 0.3])  # More Tier-2 focus
        visits = random.randint(1, 5)  # how many sessions
        for _ in range(visits):
            date = start_date + timedelta(days=random.randint(0, DAYS))
            
            # Stage 1: visited
            data.append([user_id, city_tier, "visited", 0, date])
            
            # Stage 2: add to cart (probability)
            if np.random.rand() < 0.6:  
                data.append([user_id, city_tier, "added_to_cart", 0, date])
                
                # Stage 3: purchased (probability)
                if np.random.rand() < 0.4:
                    amount = random.randint(200, 2000)
                    data.append([user_id, city_tier, "purchased", amount, date])
                    
                    # Repeat purchase chance
                    if np.random.rand() < 0.2:
                        amount2 = random.randint(200, 2000)
                        data.append([user_id, city_tier, "purchased", amount2, date + timedelta(days=random.randint(1,5))])
    
    df = pd.DataFrame(data, columns=["user_id", "city_tier", "stage", "amount", "date"])
    return df

if __name__ == "__main__":
    df = generate_data()
    df.to_csv("data/sample_ecommerce_data.csv", index=False)
    print("✅ Sample data generated and saved to data/sample_ecommerce_data.csv")
