import pandas as pd

COLUMN_MAPPING ={
    "Customer": "customer_name",
    "Product": "product_name",
    "OrderID": "order_id",
    "Quantity": "quantity",
    "UnitPrice": "unit_price",
    "TotalPrice": "total_value",
    "OrderDate": "order_date",
}

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={k: v for k, v in COLUMN_MAPPING.items() if k in df.columns})

def load_data(uploaded_file):
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else: 
        df = pd.read_csv(uploaded_file)

    df = standardize_columns(df)
    return df
