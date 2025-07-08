import streamlit as st
import pandas as pd
from eda.database import log_analysis

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
   
    if "customer_name" not in df.columns or "product_name" not in df.columns:
        st.warning("Brak kolumn 'Customer' lub 'Product' w danych.")
        return df, "", "", None 

    customers = ["Wszyscy"] + sorted(df["customer_name"].dropna().unique())
    selected_customer = st.selectbox("Filtruj po kliencie", customers)

    products = ["Wszystkie"] + sorted(df["product_name"].dropna().unique())
    selected_product = st.selectbox("Filtruj po produkcie", products)

    if "order_date" in df.columns:
        min_date = pd.to_datetime(df["order_date"]).min()
        max_date = pd.to_datetime(df["order_date"]).max()
        selected_range = st.date_input("Zakres dat zamówień", [min_date, max_date])
    else:
        selected_range = None

    filtered_df = df.copy()
    if selected_customer != "Wszyscy":
        filtered_df = filtered_df[filtered_df["customer_name"] == selected_customer]
    if selected_product != "Wszystkie":
        filtered_df = filtered_df[filtered_df["product_name"] == selected_product]
    if selected_range:
        start, end = pd.to_datetime(selected_range[0]), pd.to_datetime(selected_range[1])
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df["order_date"]) >= start) & 
            (pd.to_datetime(filtered_df["order_date"]) <= end)
        ]

    if not filtered_df.empty:
        log_analysis(
        customer=selected_customer if selected_customer != "Wszyscy" else "",
        product=selected_product if selected_product != "Wszystkie" else "",
        date_range=selected_range,
        notes="Użytkownik wykonał analizę"
    )

    return filtered_df, selected_customer, selected_product, selected_range



   