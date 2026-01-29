"""
Data input/output utilities for loading and saving CSV/XLSX files
"""

import pandas as pd
from pathlib import Path


def load_time_series(file_path, date_column=None, value_column=None):
    """
    Load time series data from CSV or XLSX file
    
    Args:
        file_path: Path to CSV or XLSX file
        date_column: Name of the date/time column (default: first column)
        value_column: Name of the value column (default: second column)
        
    Returns:
        pd.Series: Time series with datetime index
    """
    file_path = Path(file_path)
    
    # Load based on file extension
    if file_path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    # Auto-detect columns if not specified
    if date_column is None:
        date_column = df.columns[0]
    if value_column is None:
        value_column = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    # Convert to datetime and set as index
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.set_index(date_column)
    
    return df[value_column]


def load_inflow_data(file_path, reservoir_name=None):
    """
    Load inflow data for a reservoir
    
    Args:
        file_path: Path to inflow data file
        reservoir_name: Optional reservoir name (for multi-reservoir files)
        
    Returns:
        pd.Series: Inflow time series [m3/s]
    """
    return load_time_series(file_path, value_column=reservoir_name)


def load_price_data(file_path, area=None):
    """
    Load electricity price data
    
    Args:
        file_path: Path to price data file
        area: Optional price area/zone name
        
    Returns:
        pd.Series: Price time series [EUR/MWh or local currency]
    """
    return load_time_series(file_path, value_column=area)


def save_results_to_csv(results_dict, output_dir, prefix="result"):
    """
    Save SHOP results to CSV files
    
    Args:
        results_dict: Dictionary of result DataFrames/Series
        output_dir: Output directory path
        prefix: Filename prefix
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for name, data in results_dict.items():
        filename = f"{prefix}_{name}.csv"
        filepath = output_path / filename
        
        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath)
        elif isinstance(data, pd.Series):
            data.to_csv(filepath, header=True)
        else:
            print(f"Warning: Unsupported data type for {name}, skipping")


def create_sample_inflow_data(output_path, starttime, endtime, freq='h', mean_flow=50.0):
    """
    Create sample inflow data for testing
    
    Args:
        output_path: Path to save CSV file
        starttime: Start datetime
        endtime: End datetime
        freq: Frequency ('h' for hourly, 'd' for daily)
        mean_flow: Mean inflow value in m3/s
    """
    date_range = pd.date_range(start=starttime, end=endtime, freq=freq)
    
    # Create synthetic inflow with some variation
    import numpy as np
    np.random.seed(42)
    inflow = mean_flow + np.random.randn(len(date_range)) * mean_flow * 0.2
    inflow = np.maximum(inflow, 0)  # Ensure non-negative
    
    df = pd.DataFrame({
        'datetime': date_range,
        'inflow_m3s': inflow
    })
    
    df.to_csv(output_path, index=False)
    print(f"Sample inflow data saved to {output_path}")
    return df


def create_sample_price_data(output_path, starttime, endtime, freq='h', mean_price=50.0):
    """
    Create sample price data for testing
    
    Args:
        output_path: Path to save CSV file
        starttime: Start datetime
        endtime: End datetime
        freq: Frequency ('h' for hourly)
        mean_price: Mean price in EUR/MWh
    """
    date_range = pd.date_range(start=starttime, end=endtime, freq=freq)
    
    # Create synthetic price profile with daily pattern
    import numpy as np
    hours = date_range.hour
    # Higher prices during day, lower at night
    price_factor = 1.0 + 0.3 * np.sin((hours - 6) * np.pi / 12)
    price = mean_price * price_factor + np.random.randn(len(date_range)) * 5
    price = np.maximum(price, 0)  # Ensure non-negative
    
    df = pd.DataFrame({
        'datetime': date_range,
        'price_eur_mwh': price
    })
    
    df.to_csv(output_path, index=False)
    print(f"Sample price data saved to {output_path}")
    return df
