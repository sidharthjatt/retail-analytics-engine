import pandas as pd

# data load
df = pd.read_csv("data/online_retail_II.csv")
print("data shape : ", df.shape)

"""
I didn't blindly delete rows. Negative quantities are cancellations — meaningful 
business events, not errors — so I separated them rather than dropping them. 
Negative prices are genuine errors, so those I removed. The cleaning decision 
depends on what the data represents, not a one-size-fits-all rule.
"""

# step 1 : Seperate all cancellations
# Invoice that starts from 'c' = cancellations
# .str.startwith('C') : it makes True/False mask
cancellations = df[df["Invoice"].str.startswith("C")]
print("cancellations : ", cancellations.shape)

# actual sales = non cancellation
df_sales = df[~df["Invoice"].str.startswith("C")]
print("After removing cancellations: " , df_sales.shape)

"""
I isolated about 19,000 cancellation records into a separate dataset 
rather than deleting them, so I can analyze return behavior later while 
keeping my sales analysis clean.
"""

# step 2 : remove negative and zreo price 
print("\n before price filter : ", df_sales.shape)

# price must be more than 0
df_sales = df_sales[df_sales["Price"] > 0]
print("After price filter : ", df_sales.shape)

# step 3 : remove negative and zero quantity
# In sales , quantities always positi e needed
print("\n Before quantity filter : ", df_sales.shape)
df_sales = df_sales[df_sales["Quantity"] > 0]
print("After quantity filter : ", df_sales.shape)

"""
My quantity filter removed zero rows — which actually confirmed 
something useful: the negative quantities were almost entirely cancellations, 
which I'd already separated in step one. So I kept the quantity filter as a 
safety check, but the data showed my cancellation logic had already handled it. 
This kind of cross-validation tells me my cleaning steps are consistent.
"""

"""
About 23% of rows had missing Customer IDs. I didn't drop them globally, 
because for product and revenue analysis the customer ID isn't needed — those 
rows still hold valid sales data. I also didn't fill them, because there's no 
information to fill from, and assigning a placeholder would create a fake 
mega-customer that distorts the analysis. Instead, I kept the full dataset 
for sales-level work, and created a separate filtered subset with valid 
customer IDs only when doing customer-level analysis like segmentation.
"""

# step 4 : master clean dataset ready
# here df_sales already cleaned(no cancellations, no neg/zero price/qty)
# thats our master dataset
print("------ Master clean dataset ------")
print("Master shape : ", df_sales.shape)

# How many missing customer ID in master (not deleted) 
print("Missing customer ID in master : ", df_sales["Customer ID"].isnull().sum())

# step 5 : Customer analysis subset ------
# Only valid customer ID rows 
df_customers = df_sales[df_sales["Customer ID"].notnull()]
print("\n --- CUSTOMER SUBSET ---")
print("Customer subset shape : ", df_customers.shape)

# step 6 : Save both 
df_sales.to_csv("data/sales_clean.csv", index = False)
df_customers.to_csv("data/customers_clean.csv", index = False)
print("\n Saved : sales_clean.csv aur customers_clean.csv")

"""
My final clean dataset has about 1.04 million valid sales records. 
I kept missing-customer rows in the master for revenue analysis, and created 
a separate 805K-row subset with valid IDs for customer-level work.
"""