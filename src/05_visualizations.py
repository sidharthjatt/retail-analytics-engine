import pandas as pd
import matplotlib.pyplot as plt

# Data load
df = pd.read_csv("data/sales_clean.csv", low_memory=False)
df["Revenue"] = df["Quantity"] * df["Price"]

# --- CHART 1: Top 10 countries by revenue ---
country_rev = df.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
country_rev.plot(kind="bar", color="blue")
# Title = FINDING (briefing rule), not only label
plt.title("UK Dominates Revenue — Over 80% from a Single Market", fontsize=13, fontweight="bold")
plt.xlabel("Country")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("outputs/01_top_countries.png", dpi=150)
plt.close()
print("Chart 1 saved: outputs/01_top_countries.png")


# --- CHART 2: Top 10 products by revenue ---
# remove non-products like 'POSTAGE', 'Manual'...
non_products = ["POSTAGE", "DOTCOM POSTAGE", "Manual", "Adjust bad debt"]
df_products = df[~df["Description"].isin(non_products)]

top_products = df_products.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_products.plot(kind="barh", color="seagreen")
plt.title("Top Revenue Drivers Are Decorative Homeware Products", fontsize=13, fontweight="bold")
plt.xlabel("Total Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("outputs/02_top_products.png", dpi=150)
plt.close()
print("Chart 2 saved: outputs/02_top_products.png")


# --- CHART 3: Monthly revenue trend ---
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
monthly = df.groupby("Month")["Revenue"].sum()

plt.figure(figsize=(12, 6))
monthly.plot(kind="line", marker="o", color="red")
plt.title("Revenue Peaks in Pre-Holiday Months (Nov), Then Drops", fontsize=13, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45, ha="right")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/03_monthly_trend.png", dpi=150)
plt.close()
print("Chart 3 saved: outputs/03_monthly_trend.png")


# --- CHART 4: UK vs Rest (concentration risk visual) ---
uk_rev = df[df["Country"] == "United Kingdom"]["Revenue"].sum()
rest_rev = df[df["Country"] != "United Kingdom"]["Revenue"].sum()

plt.figure(figsize=(7, 7))
plt.pie([uk_rev, rest_rev], labels=["United Kingdom", "Rest of World"],
        autopct="%1.1f%%", colors=["lightgreen", "lightgray"], startangle=90)
plt.title("Revenue Concentration Risk: UK vs Rest of World", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/04_concentration.png", dpi=150)
plt.close()
print("Chart 4 saved: outputs/04_concentration.png")