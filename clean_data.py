import pandas as pd
import numpy as np
import re

df = pd.read_csv("ebay_tech_deals.csv",dtype=str)


#Cleam Price and Original Price 

df["price"] = (
    df["price"]
    .str.replace("US $", "", regex=False)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["original_price"] = (
    df["original_price"]
    .str.replace("US $", "", regex=False)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["original_price"] = df["original_price"].replace(["N/A", ""], np.nan)
df["original_price"] = df["original_price"].fillna(df["price"])

#Clean Shipping
df["shipping"] = df["shipping"].replace(["N/A", ""], np.nan)
df["shipping"] = df["shipping"].fillna("Shipping info unavailable")

#Convert price columns to numeric
df["price"] = df["price"].astype(float)
df["original_price"] = df["original_price"].astype(float)

#Discount Percentage
df["discount_percentage"] = ((1 - df["price"] / df["original_price"]) * 100).round(2)
print(df["discount_percentage"])

df.to_csv("cleaned_ebay_deals.csv", index=False)