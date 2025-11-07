import pandas as pd 
import numpy as np 
import json 


def clean_data(data):
    df = pd.DataFrame(data["recentOrders"])

    # Convert totalPrice to float
    df["totalPrice"] = df["totalPrice"].astype(float)

    # Convert createdAt to datetime
    df["createdAt"] = pd.to_datetime(df["createdAt"])

    # Replace 'null' string with proper None in SKU
    df["sku"] = df["sku"].replace("null", None)


    total_revenue = df["totalPrice"].sum()

    # Average Order Value (AOV)
    average_order_value = df["totalPrice"].mean()

    # Orders per Day
    orders_per_day = df.groupby(df["createdAt"].dt.date)["id"].count()

    # Revenue per Day
    revenue_per_day = df.groupby(df["createdAt"].dt.date)["totalPrice"].sum()

    # Top 3 Products by Revenue
    top_products = df.groupby("name")["totalPrice"].sum().sort_values(ascending=False).head(3)

    return df

    