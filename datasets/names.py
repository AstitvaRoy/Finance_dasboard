from pathlib import Path

# Get the directory where this script is located
current_dir = Path(__file__).parent
DUMMY_DATA = str(current_dir / "data" / "stock_data.csv")