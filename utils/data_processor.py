import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self):
        self.macro_data = None
        self.stock_data = None
        self.processed_data = None

    def load_macro_data(self, file_path=r"./datasets/data/Daily_macro_interpolate_data.csv"):
        """
        Load and preprocess macro economic data (daily frequency recommended)
        """
        try:
            macro_df = pd.read_csv(file_path, index_col=0)
            macro_df = macro_df.reset_index()
            macro_df.rename(columns={str(macro_df.columns[0]): 'Date'}, inplace=True)
            # Ensure 'Date' is datetime, try both common formats
            try:
                macro_df['Date'] = pd.to_datetime(macro_df['Date'], format='%d-%m-%Y')
            except Exception:
                macro_df['Date'] = pd.to_datetime(macro_df['Date'])
            self.macro_data = macro_df
            print(f"Loaded macro data with shape: {self.macro_data.shape}")
            return True
        except Exception as e:
            print(f"Error loading macro data: {e}")
            return False

    def load_stock_data(self, stock_data):
        """
        Load and preprocess stock data
        """
        try:
            self.stock_data = stock_data.copy()
            # Ensure Date column is datetime, try both common formats
            try:
                self.stock_data['Date'] = pd.to_datetime(self.stock_data['Date'], format='%d-%m-%Y')
            except Exception:
                self.stock_data['Date'] = pd.to_datetime(self.stock_data['Date'])
            self.stock_data = self.stock_data.sort_values('Date').reset_index(drop=True)
            print(f"Loaded stock data with shape: {self.stock_data.shape}")
            return True
        except Exception as e:
            print(f"Error loading stock data: {e}")
            return False

    def clean_stock_data(self):
        if self.stock_data is None:
            print("No stock data loaded")
            return False

        print("Rows before cleaning:", len(self.stock_data))

        # Only drop rows with missing Date or Close
        self.stock_data = self.stock_data.dropna(subset=['Date', 'Close'])
        print("Rows after dropping missing Date/Close:", len(self.stock_data))

        # Fill missing Open/High/Low with Close (or interpolate)
        for col in ['Open', 'High', 'Low']:
            if col in self.stock_data.columns:
                self.stock_data[col] = self.stock_data[col].fillna(self.stock_data['Close'])

        # Fill missing Volume with 0
        if 'Volume' in self.stock_data.columns:
            self.stock_data['Volume'] = self.stock_data['Volume'].fillna(0)

        # Remove rows with zero or negative Close
        self.stock_data = self.stock_data[self.stock_data['Close'] > 0]
        print("Rows after removing zero/negative Close:", len(self.stock_data))

        # (Optional) Remove rows with illogical price relationships, but log how many are dropped
        before = len(self.stock_data)
        self.stock_data = self.stock_data[
            (self.stock_data['High'] >= self.stock_data['Low']) &
            (self.stock_data['High'] >= self.stock_data['Open']) &
            (self.stock_data['High'] >= self.stock_data['Close'])
        ]
        print("Rows after logical price check:", len(self.stock_data), "Dropped:", before - len(self.stock_data))

        # Calculate technical indicators
        self._calculate_technical_indicators()
        print(f"Cleaned stock data shape: {self.stock_data.shape}")
        return True

    def _calculate_technical_indicators(self):
        """
        Calculate technical indicators for the stock data
        """
        if self.stock_data is None:
            print("No stock data to calculate technical indicators.")
            return
        # Moving Averages
        self.stock_data['MA_5'] = self.stock_data['Close'].rolling(window=5).mean()
        self.stock_data['MA_20'] = self.stock_data['Close'].rolling(window=20).mean()
        self.stock_data['MA_50'] = self.stock_data['Close'].rolling(window=50).mean()
        # Buy/Sell Signal (MA Crossover)
        self.stock_data['Buy_Sell_Signal'] = np.where(self.stock_data['MA_5'] > self.stock_data['MA_20'], 'Buy', 'Sell')
        # Daily Return and Price Change
        self.stock_data['Daily_Return'] = self.stock_data['Close'].pct_change()
        self.stock_data['Price_Change'] = self.stock_data['Close'] - self.stock_data['Close'].shift(1)
        # Volatility (20-day rolling std)
        self.stock_data['Volatility'] = self.stock_data['Daily_Return'].rolling(window=20).std()
        # RSI (14-day)
        delta = self.stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        self.stock_data['RSI'] = 100 - (100 / (1 + rs))
        # Bollinger Bands (20-day)
        self.stock_data['BB_Middle'] = self.stock_data['Close'].rolling(window=20).mean()
        bb_std = self.stock_data['Close'].rolling(window=20).std()
        self.stock_data['BB_Upper'] = self.stock_data['BB_Middle'] + (bb_std * 2)
        self.stock_data['BB_Lower'] = self.stock_data['BB_Middle'] - (bb_std * 2)

    def merge_macro_data(self):
        """
        Merge macro economic data with stock data
        """
        if self.stock_data is None or self.macro_data is None:
            print("Both stock and macro data must be loaded")
            return False
        # Merge on 'Date'
        self.processed_data = pd.merge(
            self.stock_data,
            self.macro_data,
            on='Date',
            how='left',
            suffixes=('', '_macro')
        )
        # Forward fill macro columns for missing dates
        macro_columns = ['GDP', 'Unemployment Rate', 'CPI', 'Fed Funds Rate']
        for col in macro_columns:
            if col in self.processed_data.columns:
                self.processed_data[col] = self.processed_data[col].fillna(method='ffill')
        print(f"Merged data shape: {self.processed_data.shape}")
        return True

    def process_data(self, stock_data, macro_file_path=r"./datasets/data/Daily_macro_interpolate_data.csv"):
        """
        Complete data processing pipeline
        """
        # Load macro data
        if not self.load_macro_data(macro_file_path):
            return None
        # Load stock data
        if not self.load_stock_data(stock_data):
            return None
        # Clean data
        if not self.clean_stock_data():
            return None
        if self.stock_data is not None:
            print("Columns after clean_stock_data:", self.stock_data.columns.tolist())
        # Merge macro data
        if not self.merge_macro_data():
            return None
        if self.processed_data is not None:
            print("Columns after merge_macro_data:", self.processed_data.columns.tolist())

        return self.processed_data

    def get_processed_data(self):
        """
        Return the processed data
        """
        return self.processed_data

    def get_data_summary(self):
        """
        Get a summary of the processed data
        """
        if self.processed_data is None:
            return None
        summary = {
            'total_rows': len(self.processed_data),
            'date_range': {
                'start': self.processed_data['Date'].min(),
                'end': self.processed_data['Date'].max()
            },
            'columns': list(self.processed_data.columns),
            'missing_values': self.processed_data.isnull().sum().to_dict(),
            'stock_columns': ['Date', 'Close', 'Open', 'High', 'Low', 'Volume'],
            'macro_columns': ['GDP', 'Unemployment Rate', 'CPI', 'Fed Funds Rate'],
            'technical_columns': ['MA_5', 'MA_20', 'MA_50', 'Daily_Return', 'Volatility', 'RSI', 'BB_Upper', 'BB_Lower', 'Buy_Sell_Signal']
        }
        return summary 