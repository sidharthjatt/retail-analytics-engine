import pandas as pd 

# Load cleaned master data
df = pd.read_csv("data/sales_clean.csv", low_memory = False)
# I set low_memory=False to handle mixed-type columns in a large CSV.
print("shape : ", df.shape)

# New column : every transaction's total value (every row's total revenue)
df["Revenue"] = df["Quantity"] * df["Price"]
print(df[["Quantity", "Price", "Revenue"]].head())

# --- Q1 top 10 products by revenue ---
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending = False)
    .head(10)
)

print("\n --- Top 10 Products by Revenue --- ")
print(top_products)

"""
My initial top-products query surfaced entries like 'POSTAGE' and 'Manual',
which aren't actual products — they're shipping charges and manual adjustments.
So I realized the data needs further filtering to separate genuine products 
from operational line items. This is exactly the kind of nuance that blind 
aggregation misses.
"""

# --- Q2 top 10 countries by revenue ---
top_countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending = False)
    .head(10)
)

print("\n --- Top 10 Countries by Revenue --- ")
print(top_countries)

# --- Q3 Customer-level data load (subset with valid IDs) ---
df_cust = pd.read_csv("data/customers_clean.csv", low_memory = False)
df_cust["Revenue"] = df_cust["Quantity"] * df_cust["Price"]

# Total revenue of every customer
customer_revenue = (
    df_cust.groupby("Customer ID")["Revenue"]
    .sum()
    .sort_values(ascending = False)
    .head(10)
)

print("\n --- Top 10 Customers by Revenue --- ")
print(customer_revenue)

"""
The UK accounts for over 90% of revenue — the next country is nearly 27 times smaller. 
This is a major business risk: the company is heavily concentrated in one market. 
A strategic recommendation would be international expansion to reduce this dependency.
"""

# --- Q4 top 3 customers for every country ---
# step 1 : country + customer total revenue
country_customer = (
    df_cust.groupby(["Country", "Customer ID"])["Revenue"]
    .sum()
    .reset_index()
)
# step 2 : Give rank to customers in every country
country_customer["Rank"] = (
    country_customer.groupby("Country")["Revenue"]
    .rank(method = "dense", ascending = False)
)
# step 3 : show only top 3 per country
top3_per_country = country_customer[country_customer["Rank"] <= 3]
top3_per_country = top3_per_country.sort_values(["Country", "Rank"])

print("\n --- Top 3 Customers per Country --- ")
print(top3_per_country.head(20))

"""
I implemented top-N-per-group to find each country's top customers. 
In SQL that's DENSE_RANK with PARTITION BY filtered in a CTE; 
in Pandas it's groupby-rank-filter. Same analytical pattern.
"""