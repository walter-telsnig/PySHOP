import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_synthetic_data(data_dir):
    start_date = datetime(2025, 1, 1)
    periods = 8760
    dates = [start_date + timedelta(hours=i) for i in range(periods)]

    # 1. Market Price (Seasonal + Daily variation + Noise)
    # Seasonality: higher in winter/summer
    seasonal = 20 * np.sin(2 * np.pi * np.arange(periods) / (8760)) + 50
    # Daily: higher in day
    daily = 10 * np.sin(2 * np.pi * np.arange(periods) / 24)
    # Noise
    noise = np.random.normal(0, 5, periods)
    prices = seasonal + daily + noise
    
    price_df = pd.DataFrame({'timestamp': dates, 'price': prices})
    price_df.to_csv(os.path.join(data_dir, 'market_price.csv'), index=False)
    print(f"Generated market_price.csv with {len(price_df)} rows.")

    # 2. Inflow (Spring flood peak + Seasonal + Noise)
    # Peak around May (hour 3000-4000)
    base_inflow = 1.0 + 0.5 * np.sin(2 * np.pi * np.arange(periods) / 8760)
    peak = 5.0 * np.exp(-((np.arange(periods) - 3500)**2) / (2 * 500**2))
    
    inflow_upper = base_inflow + peak + np.random.normal(0, 0.2, periods)
    inflow_lower = (base_inflow + peak) * 0.3 + np.random.normal(0, 0.1, periods)
    
    inflow_df = pd.DataFrame({
        'timestamp': dates,
        'UpperRes': np.maximum(0, inflow_upper),
        'LowerRes': np.maximum(0, inflow_lower)
    })
    inflow_df.to_csv(os.path.join(data_dir, 'inflow.csv'), index=False)
    print(f"Generated inflow.csv with {len(inflow_df)} rows.")

    # 3. Availability Data (1 = Available, 0 = Maintenance)
    avail_df = pd.DataFrame({'timestamp': dates})
    avail_df['Turbine1'] = 1
    avail_df['Pump1'] = 1
    
    # Scheduled maintenance for Turbine1 (June 1-7)
    june_start = datetime(2025, 6, 1)
    june_end = datetime(2025, 6, 8)
    avail_df.loc[(avail_df['timestamp'] >= june_start) & (avail_df['timestamp'] < june_end), 'Turbine1'] = 0
    
    # Scheduled maintenance for Pump1 (Oct 25 - Nov 1)
    oct_start = datetime(2025, 10, 25)
    oct_end = datetime(2025, 11, 1)
    avail_df.loc[(avail_df['timestamp'] >= oct_start) & (avail_df['timestamp'] < oct_end), 'Pump1'] = 0
    
    avail_df.to_csv(os.path.join(data_dir, 'availability.csv'), index=False)
    print(f"Generated availability.csv with {len(avail_df)} rows.")

if __name__ == "__main__":
    base_dir = r'c:\Users\User\OneDrive - Alpen-Adria Universität Klagenfurt\SS26\PySHOP'
    data_dir = os.path.join(base_dir, 'data', 'input')
    generate_synthetic_data(data_dir)
