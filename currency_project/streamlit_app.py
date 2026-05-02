import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

from db_manager import add_exchange_rate_to_db, get_all_exchange_rates_from_db, get_latest_exchange_rate_from_db

import yfinance as yf

CURRENCY_PAIR_TICKER = "UAH=X"

@st.cache_data(ttl=3600)
def get_exchange_rate_from_yfinance_cached(date=None):
    """
    Отримує курс валютної пари з Yahoo Finance на вказану дату.
    Якщо дата не вказана, отримує поточний курс.
    Повертає словник з датою та курсом (як datetime об'єкт), або None у разі помилки.
    Використовує кешування Streamlit.
    """
    try:
        if date is None:
            data = yf.download(CURRENCY_PAIR_TICKER, period="1d", interval="1h", progress=False)
            if not data.empty:
                latest_data = data.iloc[-1]
                rate = latest_data['Close'].item()
                date_time = latest_data.name.to_pydatetime()
                return {"Date": date_time, "USD_UAH_Rate": rate}
            else:
                st.warning(f"Data on {CURRENCY_PAIR_TICKER} not found today via yfinance.")
                return None
        else:
            start_date = date.strftime("%Y-%m-%d")
            end_date = (date + timedelta(days=1)).strftime("%Y-%m-%d") 
            data = yf.download(CURRENCY_PAIR_TICKER, start=start_date, end=end_date, progress=False)
            
            if not data.empty:
                rate = data['Close'].iloc[0].item()
                return {"Date": datetime(date.year, date.month, date.day), "USD_UAH_Rate": rate}
            else:
                return None
    except Exception as e:
        st.error(f"Error while getting rate from yfinance: {e}")
        return None

def collect_and_update_data():
    st.info("Starting data collection and update. Please wait...")
    
    current_rate_data = get_exchange_rate_from_yfinance_cached(datetime.now())
    if current_rate_data:
        add_exchange_rate_to_db(current_rate_data)
    else:
        st.warning("Unable to get current exchange rates via yfinance.")

    for i in range(30, -1, -1):
        target_date = datetime.now() - timedelta(days=i)
        historical_rate_data = get_exchange_rate_from_yfinance_cached(target_date)
        if historical_rate_data:
            add_exchange_rate_to_db(historical_rate_data)
    
    st.success("Data collection and update completed!")
    st.rerun()

st.set_page_config(
    page_title="USD/UAH exchange rate monitoring (Yahoo Finance)",
    layout="wide",
    initial_sidebar_state="expanded"
)

def perform_analysis(df):
    """Performs basic data analysis."""
    st.subheader("📊 Basic analysis")
    if df.empty:
        st.info("There is not enough data for analysis.")
        return

    st.write("Statistical description of the course:")
    st.write(df['USD_UAH_Rate'].describe())

    if len(df) > 1:
        first_rate = df['USD_UAH_Rate'].iloc[0]
        last_rate = df['USD_UAH_Rate'].iloc[-1]
        change = last_rate - first_rate
        st.write(f"**Rate change for the entire period:** `{change:.4f} UAH`")
        if change > 0:
            st.success("📈 Trend: Growth")
        elif change < 0:
            st.error("📉 Trend: Falling")
        else:
            st.info("↔️ Trend: Stable")
    
    st.subheader("🎯 Key indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Minimum rate", f"{df['USD_UAH_Rate'].min():.4f} UAH")
    with col2:
        st.metric("Maximum rate", f"{df['USD_UAH_Rate'].max():.4f} UAH")
    with col3:
        st.metric("Average course", f"{df['USD_UAH_Rate'].mean():.4f} UAH")

def main_streamlit_app():
    st.title("💸 Monitoring the US dollar to hryvnia exchange rate (Yahoo Finance)")
    st.write("This app displays historical USD/UAH exchange rate data collected from Yahoo Finance.")

    st.sidebar.header("Actions")
    if st.sidebar.button("Update course data"):
        collect_and_update_data()
        
    st.sidebar.markdown("---")
    st.sidebar.header("Display settings")
    date_filter_option = st.sidebar.radio(
        "Filter data by:",
        ('All available data', 'The last 7 days', 'Last 30 days', 'Select a range')
    )

    df_full = get_all_exchange_rates_from_db()

    if df_full.empty:
        st.warning("There is currently no USD/UAH rate data. Click 'Refresh Rate Data' to start collecting.")
        return

    df_filtered = df_full.copy()
    if date_filter_option == 'The last 7 days':
        seven_days_ago = datetime.now() - timedelta(days=7)
        df_filtered = df_full[df_full['Date'] >= seven_days_ago]
    elif date_filter_option == 'Last 30 days':
        thirty_days_ago = datetime.now() - timedelta(days=30)
        df_filtered = df_full[df_full['Date'] >= thirty_days_ago]
    elif date_filter_option == 'Select a range' and not df_full.empty:
        min_date_available = df_full['Date'].min().date()
        max_date_available = df_full['Date'].max().date()
        
        start_date = st.sidebar.date_input("Start date", value=min_date_available, min_value=min_date_available, max_value=max_date_available)
        end_date = st.sidebar.date_input("Completion date", value=max_date_available, min_value=min_date_available, max_value=max_date_available)

        if start_date <= end_date:
            df_filtered = df_full[(df_full['Date'].dt.date >= start_date) & (df_full['Date'].dt.date <= end_date)]
        else:
            st.sidebar.error("The start date must be before or equal to the end date.")
            df_filtered = pd.DataFrame()

    st.sidebar.info(f"It is displayed {len(df_filtered)} records from {len(df_full)} available.")
    
    latest_rate_data = get_latest_exchange_rate_from_db()
    if latest_rate_data:
        st.metric(
            label="Latest current USD/UAH exchange rate",
            value=f"{latest_rate_data['USD_UAH_Rate']:.4f} UAH",
            delta=f"{latest_rate_data['Date'].strftime('%Y-%m-%d %H:%M')}"
        )
        st.markdown("---")

    st.subheader("📈 USD/UAH exchange rate chart")
    if not df_filtered.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(x='Date', y='USD_UAH_Rate', data=df_filtered, marker='o', ax=ax)
        ax.set_title('Historical exchange rate of the US dollar to the hryvnia')
        ax.set_xlabel('Date')
        ax.set_ylabel('Rate (UAH)')
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("There is no data to display in the selected range.")

    st.subheader("📝 Data table")
    if not df_filtered.empty:
        df_display = df_filtered.copy()
        df_display['Date'] = df_display['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(df_display.set_index('Date').style.format({"USD_UAH_Rate": "{:.4f}"}))
    else:
        st.info("There is no data to display in the table.")

    perform_analysis(df_filtered)

if __name__ == "__main__":
    main_streamlit_app()