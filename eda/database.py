import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st


DB_USER = "postgres"
DB_PASSWORD = "postgres12"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "virtual_warehouse"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_orders():
    try:
        query = "SELECT * FROM orders_view"
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        st.error(f"Błąd pobierania danych z bazy: {e}")
        return pd.DataFrame()
    
def insert_fake_orders(n=10000):
    from faker import Faker
    import random
    import datetime

    fake = Faker()

    with engine.begin() as conn:
        
        conn.execute(text("DELETE FROM orders"))
        conn.execute(text("DELETE FROM customers"))
        conn.execute(text("DELETE FROM products"))

     
        customers = [{"name": fake.name(), "email": fake.email()} for _ in range(100)]
        conn.execute(
            text("INSERT INTO customers (name, email) VALUES (:name, :email)"),
            customers
        )

      
        products = [{"name": fake.word(),"category": fake.word(),"stock": random.randint(10, 100),"reorder_level": random.randint(1, 10),"price": round(random.uniform(5, 100), 2)
                        } for _ in range(50)]

        conn.execute(
        text("""INSERT INTO products (name, category, stock, reorder_level, price)
            VALUES (:name, :category, :stock, :reorder_level, :price)
            """),
            products
        )

   
        customer_ids = conn.execute(text("SELECT id FROM customers")).fetchall()
        product_ids = conn.execute(text("SELECT id FROM products")).fetchall()
        product_prices = conn.execute(text("SELECT id, price FROM products")).fetchall()
        price_map = {row[0]: row[1] for row in product_prices}

        orders = []
        for _ in range(n):
            cust_id = random.choice(customer_ids)[0]
            prod_id = random.choice(product_ids)[0]
            quantity = random.randint(1, 10)
            date = fake.date_between(start_date='-1y', end_date='today')
            unit_price = price_map.get(prod_id, 0)  

            orders.append({
                "customer_id": cust_id,
                "product_id": prod_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "order_date": date
            })

        conn.execute(
            text("""
                INSERT INTO orders (customer_id, product_id, quantity, unit_price, order_date)
                VALUES (:customer_id, :product_id, :quantity, :unit_price, :order_date)
            """),
            orders
        )

    st.success(f"Wygenerowano {n} zamówień testowych.")

def log_analysis(customer, product, date_range, notes=""):
    with engine.begin() as conn:
        conn.execute(text(""" 
            INSERT INTO analysis_history (customer_filter, product_filter, date_range, user_notes)
            VALUES (:customer, :product, :date_range, :notes)
        """), {
            "customer": customer,
            "product": product,
            "date_range": str(date_range),
            "notes": notes
        })

def show_analysis_history():
    with engine.begin() as conn:
        df = pd.read_sql("SELECT * FROM analysis_history ORDER BY timestamp DESC", conn)
        st.subheader("Historia analiz")
        st.dataframe(df)