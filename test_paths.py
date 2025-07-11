#!/usr/bin/env python3
"""
Test script to verify all file paths are working correctly
"""
import os
from pathlib import Path

def test_paths():
    print("=== Testing File Paths ===")
    
    # Test 1: Current working directory
    print(f"Current working directory: {Path.cwd()}")
    
    # Test 2: Script location
    script_dir = Path(__file__).parent
    print(f"Script directory: {script_dir}")
    
    # Test 3: Check if files exist
    files_to_check = [
        script_dir / "datasets" / "data" / "stock_data.csv",
        script_dir / "datasets" / "data" / "Daily_macro_interpolate_data.csv",
        script_dir / "datasets" / "data" / "processed",
        script_dir / "assets" / "background.jpg"
    ]
    
    for file_path in files_to_check:
        exists = file_path.exists()
        print(f"{'✅' if exists else '❌'} {file_path} - {'EXISTS' if exists else 'NOT FOUND'}")
    
    # Test 4: Check processed folder contents
    processed_dir = script_dir / "datasets" / "data" / "processed"
    if processed_dir.exists():
        csv_files = list(processed_dir.glob("*.csv"))
        print(f"📁 Found {len(csv_files)} CSV files in processed folder")
        if csv_files:
            print(f"   First 5 files: {[f.stem for f in csv_files[:5]]}")
    else:
        print("❌ Processed folder not found")
    
    # Test 5: Try to read stock_data.csv
    stock_file = script_dir / "datasets" / "data" / "stock_data.csv"
    if stock_file.exists():
        try:
            import pandas as pd
            df = pd.read_csv(stock_file)
            print(f"✅ Successfully read stock_data.csv: {df.shape}")
        except Exception as e:
            print(f"❌ Error reading stock_data.csv: {e}")
    else:
        print("❌ stock_data.csv not found")

if __name__ == "__main__":
    test_paths() 