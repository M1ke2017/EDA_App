import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_correlation_heatmap(df):
    corr = df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(4, 3))
    sns.heatmap(corr, annot=True, cmap="coolwarm",fmt=".2f", ax=ax)
    st.pyplot(fig, clear_figure=True, use_container_width=False)