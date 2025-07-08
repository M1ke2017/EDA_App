import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_histogram(df, col):
    fig, ax = plt.subplots(figsize=(4, 3))
    sns.histplot(df[col], kde=True, ax=ax)
    ax.set_title(f"Histogram: {col}")
    st.pyplot(fig, clear_figure=True, use_container_width=False)
