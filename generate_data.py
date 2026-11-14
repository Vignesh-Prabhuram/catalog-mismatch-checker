"""Creates synthetic 1P (retailer) and 3P (seller) catalog data with planted mismatches."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 2000
cats = {"Electronics": ["Wireless Earbuds", "Smart Watch", "Bluetooth Speaker", "Power Bank"],
        "Home & Kitchen": ["Air Fryer", "Non-Stick Pan", "Water Bottle", "Mixer Grinder"],
        "Apparel": ["Cotton T-Shirt", "Running Shoes", "Denim Jeans", "Hoodie"],
        "Beauty": ["Face Wash", "Moisturizer", "Hair Serum", "Sunscreen"]}
brands = ["Nova", "Zenith", "Urbanix", "PureLife", "Kora", "Allen"]
colors = ["Black", "White", "Blue", "Red", "Grey"]

rows = []
for i in range(N):
    cat = rng.choice(list(cats))
    prod = rng.choice(cats[cat])
    brand = rng.choice(brands)
    color = rng.choice(colors)
    rows.append({"item_id": f"ITM{100000+i}", "category": cat, "brand": brand,
                 "title": f"{brand} {prod} - {color}", "color": color,
                 "price": round(float(rng.uniform(5, 250)), 2)})
p1 = pd.DataFrame(rows)

p3 = p1.copy()
n = len(p3)
def pick(frac): return rng.choice(n, int(n * frac), replace=False)

for idx in pick(0.08):  # title errors
    t = p3.at[idx, "title"]
    p3.at[idx, "title"] = rng.choice([t.upper(), t.replace(" - ", " "), t + " (New 2024)", t.replace(p3.at[idx, "brand"], "")])
for idx in pick(0.05):  # brand errors
    p3.at[idx, "brand"] = rng.choice([b for b in brands if b != p3.at[idx, "brand"]])
for idx in pick(0.07):  # price errors
    p3.at[idx, "price"] = round(p3.at[idx, "price"] * rng.uniform(0.8, 1.3), 2)
for idx in pick(0.04):  # color errors
    p3.at[idx, "color"] = rng.choice([c for c in colors if c != p3.at[idx, "color"]])
# 3P has a few items missing and a few extra
p3 = p3.drop(rng.choice(n, 25, replace=False)).reset_index(drop=True)
extra = pd.DataFrame([{"item_id": f"ITM{900000+i}", "category": "Electronics", "brand": "Nova",
                       "title": "Nova Power Bank - Black", "color": "Black", "price": 29.99} for i in range(10)])
p3 = pd.concat([p3, extra], ignore_index=True)

p1.to_csv("retailer_1p.csv", index=False)
p3.to_csv("seller_3p.csv", index=False)
print("Created", len(p1), "1P rows and", len(p3), "3P rows")
