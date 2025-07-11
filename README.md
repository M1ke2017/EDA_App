# EDA_App
Interaktywna aplikacja webowa oparta na **Streamlit**, umożliwiająca ładowanie danych z bazy danych PostgreSQL lub plików CSV/XLSX, ich eksplorację, analizę oraz tworzenie prostych modeli predykcyjnych (regresja liniowa).
---
# Funkcje 
- Wczytywanie danych z bazy danych PostgreSQL lub pliku CSV/Excel
- Interaktywna eksploracja danych: brakujące dane, korelacje, histogramy
- Prosty model predykcyjny (regresja liniowa)
- Filtry danych po kliencie, produkcie, zakresie dat
- Historia analiz zapisywana do bazy
- Generowanie danych testowych (10k rekordów)
- Czytelna i modularna struktura kodu
---
# Technologie 
- Python 3.10+
- Streamlit 
- Pandas 
- SQLAlchemy 
- PostgreSQL
- Scikit-learn
- Faker 

# Struktura bazy danych
Projekt korzysta z bazy danych PostgreSQL o nazwie `virtual_warehouse` zawierającej następujące tabele:

- **customers** — zawiera informacje o klientach (id, name, email)
- **products** — zawiera dane o produktach (id, name, category, price, stock, reorder_level)
- **orders** — zamówienia powiązane z klientami i produktami (id, customer_id, product_id, quantity, unit_price, order_date, status)
- **analysis_history** — zapis historii analiz użytkownika

Przy pierwszym uruchomieniu aplikacja może automatycznie wypełnić bazę danymi testowymi (10 000 rekordów).

# Wymagania
- Python 3.10+
- PostgreSQL (z dostępem do localhost)
- Biblioteki z `requirements.txt`

