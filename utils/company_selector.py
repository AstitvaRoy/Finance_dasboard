import os
import pandas as pd
from pathlib import Path

def get_available_companies():
    """
    Scan the processed folder and return a list of available companies
    Returns a list of tuples: (company_symbol, company_name)
    """
    processed_dir = Path('./datasets/data/processed')
    
    if not processed_dir.exists():
        return []
    
    companies = []
    for file_path in processed_dir.glob('*.csv'):
        company_symbol = file_path.stem  # Get filename without extension
        companies.append((company_symbol, company_symbol))
    
    # Sort companies alphabetically
    companies.sort(key=lambda x: x[0])
    return companies

def load_company_data(company_symbol):
    """
    Load data for a specific company
    Args:
        company_symbol (str): The company symbol (e.g., 'AAPL')
    Returns:
        pandas.DataFrame: The company's stock data
    """
    file_path = f'./datasets/data/processed/{company_symbol}.csv'
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file for {company_symbol} not found")
    
    df = pd.read_csv(file_path)
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date
    df = df.sort_values('Date')
    
    return df

def get_company_info(company_symbol):
    """
    Get basic information about a company's data
    Args:
        company_symbol (str): The company symbol
    Returns:
        dict: Company information including date range, data points, etc.
    """
    df = load_company_data(company_symbol)
    
    info = {
        'symbol': company_symbol,
        'start_date': df['Date'].min(),
        'end_date': df['Date'].max(),
        'total_days': len(df),
        'columns': list(df.columns)
    }
    
    return info 