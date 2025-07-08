import streamlit as st
import pandas as pd

def show_column_details(df: pd.DataFrame):
    col_info = pd.DataFrame({
        "Typ danych": df.dtypes,
        "Unikalne wartości": df.nunique()
    })
    st.dataframe(col_info)