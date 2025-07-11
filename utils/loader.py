# utils/loader.py
import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from datetime import timedelta
from .company_selector import load_company_data, get_available_companies
from .data_processor import DataProcessor
from .charts import (
    overview_chart, analysis_chart, reports_chart, notifications_chart,
    price_macro_overlay_chart, moving_average_crossover_chart, bollinger_bands_volume_chart,
    rsi_chart, correlation_matrix_chart, returns_histogram_chart, scatter_return_vs_macro_chart
)

def load_data(company_symbol=None):
    """
    Load data - either synthetic data or specific company data
    Args:
        company_symbol (str): Company symbol to load. If None, loads synthetic data
    """
    if company_symbol:
        # Load specific company data
        try:
            df = load_company_data(company_symbol)
            return df
        except Exception as e:
            st.error(f"Error loading data for {company_symbol}: {e}")
            # Fallback to synthetic data
            return load_synthetic_data()
    else:
        # Load synthetic data
        return load_synthetic_data()

def load_synthetic_data():
    """
    Load the original synthetic stock data
    """
    df = pd.read_csv('./datasets/data/stock_data.csv')
    start_date = pd.Timestamp.today() - pd.Timedelta(days=len(df) - 1)
    df['Date'] = pd.date_range(start=start_date, periods=len(df), freq='D')
    return df

def load_processed_data(company_symbol=None, enable_preprocessing=True):
    """
    Load and optionally preprocess data
    Args:
        company_symbol (str): Company symbol to load
        enable_preprocessing (bool): Whether to apply data preprocessing
    """
    # Load raw data
    raw_data = load_data(company_symbol)
    
    if enable_preprocessing and company_symbol:
        # Apply data preprocessing
        processor = DataProcessor()
        processed_data = processor.process_data(raw_data)
        
        if processed_data is not None:
            return processed_data
        else:
            st.warning("Data preprocessing failed, using raw data")
            return raw_data
    else:
        return raw_data

def filter_by_time_range(df, selection):
    if selection == "1 Week":
        return df[df['Date'] >= pd.Timestamp.today() - pd.Timedelta(weeks=1)]
    elif selection == "1 Month":
        return df[df['Date'] >= pd.Timestamp.today() - pd.DateOffset(months=1)]
    elif selection == "3 Months":
        return df[df['Date'] >= pd.Timestamp.today() - pd.DateOffset(months=3)]
    else:
        return df

def get_company_list():
    """
    Get list of available companies for dropdown
    """
    return get_available_companies()

# --- New: Get all advanced charts for a given DataFrame ---
def get_all_charts(df):
    """
    Returns a dictionary of all advanced chart figures for the given DataFrame.
    """
    charts = {}
    # Macro overlay: try both CPI and GDP if available
    macro_col = 'CPI' if 'CPI' in df.columns else ('GDP' if 'GDP' in df.columns else None)
    if macro_col:
        charts['Price + Macro Overlay'] = price_macro_overlay_chart(df, macro_col=macro_col)
    charts['Moving Average Crossover'] = moving_average_crossover_chart(df)
    charts['Bollinger Bands + Volume'] = bollinger_bands_volume_chart(df)
    charts['RSI'] = rsi_chart(df)
    charts['Correlation Matrix'] = correlation_matrix_chart(df)
    charts['Histogram of Returns'] = returns_histogram_chart(df)
    # Scatter: Daily Return vs Macro (CPI or GDP)
    if macro_col:
        charts['Return vs Macro'] = scatter_return_vs_macro_chart(df, macro_col=macro_col)
    return charts
