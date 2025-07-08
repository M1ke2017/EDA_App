import csv
import streamlit as st
import io

def download_csv(df, filename="dane_analizowane.csv"):
    df_rounded = df.copy()
    for col in df_rounded.select_dtypes(include=["float", "float64"]):
        df_rounded[col] = df_rounded[col].round(2)

    csv_buffer = io.StringIO()
    df_rounded.to_csv(csv_buffer, sep=";", index=False)

    st.download_button(
        label="Pobierz jako CSV",
        data=csv_buffer.getvalue(),
        file_name=filename,
        mime="text/csv"
    )
