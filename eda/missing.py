import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_missing_data(df: pd.DataFrame):
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    if missing.empty:
        st.info("Brak brakujących danych")
        return
    
    fig, ax = plt.subplots(figsize=(4, 3))
    missing.plot(kind='bar', ax=ax, title="Brakujące dane")
    ax.set_ylabel("Liczba brakujących wartości")
    st.pyplot(fig, clear_figure=True, use_container_width=False)