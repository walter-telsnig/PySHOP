import pandas as pd
from pathlib import Path
from typing import Union, List, Optional

def load_timeseries(
    file_path: Union[str, Path],
    column_mappings: dict,
    sheet_name: Optional[str] = None,
    time_col: str = "time"
) -> pd.DataFrame:
    """
    Universal loader for CSV and Excel time-series data.
    
    Args:
        file_path: Path to the .csv or .xlsx file.
        column_mappings: Dict mapping raw columns to standardized names (e.g., {'MarketPrice': 'price'}).
        sheet_name: Target sheet for Excel files.
        time_col: Column name to use as DateTime index.
    """
    path = Path(file_path)
    
    if path.suffix.lower() == '.xlsx':
        df = pd.read_excel(path, sheet_name=sheet_name)
    else:
        df = pd.read_csv(path)
        
    # Standardize column names
    df = df.rename(columns=column_mappings)
    
    # Ensure time index
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col])
        # Handle potential duplicates (common in DST shifts)
        df = df.drop_duplicates(subset=[time_col], keep='first')
        df = df.set_index(time_col)
        df = df.sort_index()
    
    return df[list(column_mappings.values())]
