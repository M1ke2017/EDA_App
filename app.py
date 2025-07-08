import streamlit as st
import pandas as pd

from file_loader import load_data
from eda.filters import apply_filters
from eda.summary import show_summary
from eda.missing import show_missing_data
from eda.column_details import show_column_details
from eda.histogram import show_histogram
from eda.correlation import show_correlation_heatmap
from eda.utils import download_csv
from eda.prediction import show_prediction
from eda.database import show_analysis_history, get_orders, insert_fake_orders, log_analysis
from eda.analytics import show_top_customers, show_top_products, show_orders_trend

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame()
    
st.set_page_config(page_title="EDA App", layout="wide")
st.title("Eksploracyjna Analiza Danych (EDA)")

st.sidebar.header("Źródło danych")
data_source = st.sidebar.radio("Wybierz źródło:", ["Plik CSV / Excel", "Baza danych (PostgreSQL)"])

df = None

if data_source == "Plik CSV / Excel":
    uploaded_file = st.file_uploader("Wgraj plik CSV lub Excel", type=["csv", "xlsx"])
    if uploaded_file:
        df = load_data(uploaded_file)
        st.success("Załadowano dane z pliku.")
else:
    if st.button("Wczytaj dane z bazy"):
        df = get_orders()
        if not df.empty:
            st.session_state['data'] = df
            st.success("Dane z bazy zostały załadowane.")
    else:
            st.warning("Brak danych z bazy.")
    if st.button("Wygeneruj dane testowe (10k rekordów)"):
        insert_fake_orders()
        df = get_orders()
        st.session_state['data'] = df
        st.success("Wygenerowano i załadowano dane.")
    if st.button("Odśwież dane automatycznie"):
        insert_fake_orders()  
        st.success("Dane zostały zaktualizowane!")


if df is not None and not df.empty:
    st.subheader("Podgląd danych")
    st.dataframe(df.head())

    st.subheader("Filtrowanie danych")
    filtered_df, selected_customer, selected_product, selected_range  = apply_filters(df)
    show_full = st.checkbox("Pokaż pełne dane (bez filtrowania)")
    data_for_analysis = df if show_full else filtered_df

    if data_for_analysis is not None and not data_for_analysis.empty:
        st.subheader("Dane do analizy")
        st.dataframe(data_for_analysis.head())

        st.subheader("Statystyki opisowe")
        show_summary(data_for_analysis)

        if not df.empty:
            with st.expander("Najwięksi klienci"):
                show_top_customers(data_for_analysis)
            with st.expander("Najczęściej zamawiane produkty"):
                show_top_products(data_for_analysis)
            with st.expander("Trend zamówień w czasie"):
                show_orders_trend(data_for_analysis)

        st.subheader("Brakujące dane")
        show_missing_data(data_for_analysis)

        if st.checkbox("Usuń wiersze z brakami"):
            data_for_analysis = data_for_analysis.dropna()
            st.success("Usunięto wiersze zawierające braki danych.")

        st.subheader("Typy danych i unikalne wartości")
        show_column_details(data_for_analysis)

        st.subheader("Histogram dla wybranej kolumny")
        numeric_cols = data_for_analysis.select_dtypes(include=["int64", "float64"]).columns
        if not numeric_cols.empty:
            selected_col = st.selectbox("Wybierz kolumnę", numeric_cols)
            show_histogram(data_for_analysis, selected_col)
        else:
            st.warning("Brak kolumn numerycznych.")

        st.subheader("Korelacja między zmiennymi")
        show_correlation_heatmap(data_for_analysis)

        st.subheader("Predykcja")
        show_prediction(data_for_analysis)

        with st.expander("Historia analiz"):
            show_analysis_history()

        st.subheader("Eksport danych")
        download_csv(data_for_analysis)
    else:
        st.warning("Brak danych do analizy.")
else:
    st.info("Wgraj plik CSV lub Excel, aby rozpocząć analizę.")
