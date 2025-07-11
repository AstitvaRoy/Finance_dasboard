# New Features Documentation

## Overview
This document describes the new functionality added to the StocksViz dashboard, including company selection and data preprocessing capabilities.

## New Features

### 1. Company Selection Dropdown
- **Location**: `utils/company_selector.py`
- **Functionality**: 
  - Scans the `datasets/data/processed/` folder for individual company CSV files
  - Provides a dropdown menu to select any available company
  - Automatically loads the selected company's stock data
  - Falls back to synthetic data if a company is not found

#### Key Functions:
- `get_available_companies()`: Returns list of available companies
- `load_company_data(company_symbol)`: Loads data for a specific company
- `get_company_info(company_symbol)`: Gets metadata about company data

### 2. Data Preprocessing Pipeline
- **Location**: `utils/data_processor.py`
- **Functionality**:
  - Data cleaning (handling missing values, outliers)
  - Technical indicator calculation (Moving averages, RSI, Bollinger Bands)
  - Macro economic data merging
  - Data validation and quality checks

#### Key Features:
- **Data Cleaning**:
  - Removes rows with missing price data
  - Handles missing volume data
  - Validates price relationships (High ≥ Low, etc.)
  
- **Technical Indicators**:
  - Moving Averages (5, 20, 50 day)
  - Daily Returns and Price Changes
  - Volatility (20-day rolling std)
  - RSI (Relative Strength Index)
  - Bollinger Bands

- **Macro Data Integration**:
  - Merges stock data with macro economic indicators
  - Includes GDP, Unemployment Rate, CPI, Fed Funds Rate
  - Forward-fills macro data for missing dates

#### Key Methods:
- `process_data(stock_data, macro_file_path)`: Complete processing pipeline
- `clean_stock_data()`: Data cleaning operations
- `merge_macro_data()`: Merges with economic indicators
- `get_data_summary()`: Returns data statistics

### 3. Enhanced Data Loading
- **Location**: `utils/loader.py` (updated)
- **New Functions**:
  - `load_processed_data(company_symbol, enable_preprocessing)`: Loads and optionally preprocesses data
  - `get_company_list()`: Returns available companies for UI

## File Structure

```
final-cs661/
├── utils/
│   ├── company_selector.py    # NEW: Company selection functionality
│   ├── data_processor.py      # NEW: Data preprocessing pipeline
│   ├── loader.py              # UPDATED: Enhanced data loading
│   └── charts.py              # Existing chart functionality
├── Home.py                    # UPDATED: Added company dropdown and preprocessing options
├── test_functionality.py      # NEW: Test script for new features
└── README_NEW_FEATURES.md     # NEW: This documentation
```

## Usage

### Running the Application
1. Navigate to the project directory
2. Run: `streamlit run Home.py`

### Using the New Features
1. **Company Selection**: Use the dropdown to select any available company from the processed folder
2. **Data Preprocessing**: Toggle the "Enable Data Preprocessing" checkbox to apply cleaning and macro data merging
3. **Refresh Data**: Use the refresh button to reload and reprocess data

### Testing the Functionality
Run the test script to verify everything works:
```bash
python test_functionality.py
```

## Data Requirements

### Company Data Format
Individual company CSV files should have the following columns:
- `Date`: Date in YYYY-MM-DD format
- `Close`: Closing price
- `Open`: Opening price  
- `High`: Highest price of the day
- `Low`: Lowest price of the day
- `Volume`: Trading volume

### Macro Data Format
The macro data file (`macro_data_interpolated.csv`) should contain:
- Date index
- `GDP`: Gross Domestic Product
- `Unemployment Rate`: Unemployment percentage
- `CPI`: Consumer Price Index
- `Fed Funds Rate`: Federal Funds Rate

## Technical Details

### Data Processing Pipeline
1. **Load**: Read company CSV file
2. **Clean**: Remove invalid data, handle missing values
3. **Enhance**: Calculate technical indicators
4. **Merge**: Combine with macro economic data
5. **Validate**: Ensure data quality and consistency

### Error Handling
- Graceful fallback to synthetic data if company data is unavailable
- Warning messages for preprocessing failures
- Data validation at each step

### Performance Considerations
- Data is processed on-demand when selected
- Caching can be implemented for frequently accessed companies
- Large datasets are handled efficiently with pandas operations

## Future Enhancements
- Add more technical indicators
- Implement data caching for better performance
- Add company metadata and descriptions
- Support for real-time data feeds
- Advanced filtering and search capabilities 