import pandas as pd 
# step 1 : data load

df = pd.read_csv("data/online_retail_II.csv")

# step 2 : show first five rows
print("first five rows ")
print(df.head())

# step 3 : shape (how many rows and columns)
print("shape ")
print(df.shape)

# step 4 : name of columns and data types
print("info")
print(df.info())

# step 5 : summary of numeric columns
print("describe ")
print(df.describe())
