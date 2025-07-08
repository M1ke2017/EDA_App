import pandas as pd
import plotly.express as px
import streamlit as st 


def show_top_customers(df: pd.DataFrame, top_n: int = 5):
    if "quantity" not in df.columns or "unit_price" not in df.columns:
        st.warning("Brak wymaganych kolumn: 'quantity' lub 'unit_price'. Nie można obliczyć wartości zamówień.")
        return
    
    df["total_value"] = df["quantity"] * df["unit_price"]
    top_customers = df.groupby("customer_name")["total_value"].sum().nlargest(top_n).reset_index()

    st.subheader(f"Top {top_n} klinetów wg wartości sprzedaży")
    fig = px.bar(top_customers, x="customer_name", y="total_value", labels={"customer_name": "Klient", "total_value": "Wartość sprzedaży"})
    st.plotly_chart(fig, use_container_width=True)

def show_top_products(df: pd.DataFrame, top_n: int = 5):
    if "quantity" not in df.columns or "unit_price" not in df.columns:
        st.warning("Brak wymaganych kolumn: 'quantity' lub 'unit_price'. Nie można obliczyć wartości zamówień.")
        return

    df["total_value"] = df["quantity"] * df["unit_price"]
    top_customers = df.groupby("product_name")["total_value"].sum().nlargest(top_n).reset_index()

    st.subheader(f"Top {top_n} produktów wg wartości sprzedaży")
    fig = px.bar(top_customers, x="product_name", y="total_value", labels={"product_name": "Produkt", "total_value": "Wartość sprzedaży"})
    st.plotly_chart(fig, use_container_width=True)

def show_orders_trend(df: pd.DataFrame):
    if "order_date" not in df.columns:
        st.warning("Brak kolumny 'order_date'. Nie można wyświetlić trendu zamówień.")
        return
    
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["total_value"] = df["quantity"] * df["unit_price"]
    trend = df.groupby(df["order_date"].dt.to_period("M"))["total_value"].sum().reset_index()
    trend["order_date"] = trend["order_date"].astype(str)

    st.subheader("Trend wartości zmaówień w czasie")
    fig = px.line(trend, x="order_date", y="total_value", labels={"order_date": "Miesiąc", "total_value": "Łączna wartość"})
    st.plotly_chart(fig, use_container_width=True)