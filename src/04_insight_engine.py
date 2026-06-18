import pandas as pd 

# load cleaned data
df = pd.read_csv("data/online_retail_II.csv", low_memory = False)
df["Revenue"] = df["Quantity"] * df["Price"]

# Collect insights in a list(output of engine)
insights = []

# --- Insight 1 : Revenue concentration(country) ---
country_rev = df.groupby("Country")["Revenue"].sum().sort_values(ascending = False)
total_rev = country_rev.sum()
top_country = country_rev.index[0]
top_country_share = (country_rev.iloc[0] / total_rev ) * 100

if top_country_share > 50: # Make "RISK" insight only when share more than 50%.
    insights.append(
        f" Risk: {top_country} alone contributes {top_country_share:.1f}% of total revenue" # .1f means upto one decimal.
        f"- heavy market concentration, a business risk."
    )

"""
My engine automatically detected that the UK contributes 84.9% of revenue and 
flagged it as a concentration risk — without me hardcoding anything. 
On a different dataset, it would flag whatever the actual concentration is.
"""

# --- Insight 2 : Top Products ---
top_product = df.groupby("Description")["Revenue"].sum().sort_values(ascending = False).index[0]
top_product_rev = df.groupby("Description")["Revenue"].sum().sort_values(ascending = False).iloc[0]
insights.append(
    f" Top Product : '{top_product}' is the highest revenue generator "
    f"with {top_product_rev:,.0f} in total revenue."
)



# --- Insight 3 : Return/Cancellation rate ---
# Load original data and count cancellation
df_all = pd.read_csv("data/online_retail_II.csv", low_memory = False)
total_orders = len(df_all)
cancellations = df_all["Invoice"].astype(str).str.startswith("C").sum()
return_rate = (cancellations / total_orders) * 100
insights.append(
    f" Return Rate : {return_rate:.1f}% of all transactions are cancellations "
    f"- worth monitoring for product or service issues."
)



# --- Insight 4 : Revenue Trend(monthly) ---
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M")
monthly = df.groupby("Month")["Revenue"].sum()

# Last month vs pichla month(LAG jesa)
last_month_change = ((monthly.iloc[-1] - monthly.iloc[-2]) / monthly.iloc[-2]) * 100
direction = "incerased" if last_month_change > 0 else "decreased"
insights.append(
    f" Trend : Revenue {direction} by {abs(last_month_change):.1f}% "
    f"in the most recent month compared to the previous one."
)

"""
My engine flagged a 70% revenue drop in the last month — but I investigated 
rather than reporting it blindly. The last month's data was incomplete, 
only partial days, so the drop was an artifact of incomplete data, 
not a real business decline. A naive analysis would have reported a false alarm. 
I'd either exclude incomplete periods or flag them explicitly.
"""


# --- print all insights ---
print("--- AUTO-GENERATED INSIGHTS --- \n")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}\n")
