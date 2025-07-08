import streamlit as st
import pandas as pd 

def show_summary(df: pd.DataFrame):
    st.write("Statystki opisowe:")
    if not df.empty:
        st.dataframe(df.describe().T)
    else: 
        st.warning("Brak danych do opisania.")
    st.write("Rozmiar danych:")
    st.write(f"Liczba wierszy: {df.shape[0]}")
    st.write(f"Liczba kolumn: {df.shape[1]}")