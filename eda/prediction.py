import streamlit as st
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt

def show_prediction(df: pd.DataFrame):
    st.subheader("Prosty model predykcyjny (Regresja liniowa)")
    if 'data' in st.session_state and not st.session_state['data'].empty:
        df = st.session_state['data']

        numeric_col = df.select_dtypes(include=["float64", "int64"]).columns

        if len(numeric_col) < 2:
            st.warning("Potrzeba co najmniej dwóch kolumn numerycznych")
            return

        x_col = st.selectbox("Wybierz cechę wejściową (X)", numeric_col)
        y_col = st.selectbox("Wybierz wartość docelową (y)", [col for col in numeric_col if col != x_col])

        X = df[[x_col]].dropna()
        y = df[y_col].loc[X.index]

        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        st.write(f"**Współczynnik regresji (slope):** {model.coef_[0]:.2f}")
        st.write(f"**Wartość przecięcia (intercept):** {model.intercept_:.2f}")

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.scatter(X, y, label="Dane rzeczywiste")
        ax.plot(X, y_pred, color='red', label="Regresja liniowa")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.legend()
        st.pyplot(fig, clear_figure=True, use_container_width=False)

    else:
        st.warning("Brak danych. Załaduj dane z pliku lub bazy.")
