import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def visualize_input_data(data_dir):
    # 1. Plot Market Price
    price_file = os.path.join(data_dir, 'market_price.csv')
    if os.path.exists(price_file):
        df_price = pd.read_csv(price_file)
        df_price['timestamp'] = pd.to_datetime(df_price['timestamp'])
        
        plt.figure(figsize=(12, 6))
        plt.plot(df_price['timestamp'], df_price['price'], label='Market Price [EUR/MWh]', color='blue', alpha=0.7)
        plt.title('Yearly Market Price Trend')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        price_plot = os.path.join(data_dir, '..', 'output', 'market_price_trend.png')
        plt.savefig(price_plot)
        print(f"Saved market price plot to {price_plot}")
        plt.close()

    # 2. Plot Inflow
    inflow_file = os.path.join(data_dir, 'inflow.csv')
    if os.path.exists(inflow_file):
        df_inflow = pd.read_csv(inflow_file)
        df_inflow['timestamp'] = pd.to_datetime(df_inflow['timestamp'])
        
        plt.figure(figsize=(12, 6))
        plt.plot(df_inflow['timestamp'], df_inflow['UpperRes'], label='UpperRes Inflow', color='green', alpha=0.7)
        plt.plot(df_inflow['timestamp'], df_inflow['LowerRes'], label='LowerRes Inflow', color='orange', alpha=0.7)
        plt.title('Yearly Reservoir Inflow Trends')
        plt.xlabel('Date')
        plt.ylabel('Inflow [m3/s]')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        inflow_plot = os.path.join(data_dir, '..', 'output', 'inflow_trends.png')
        plt.savefig(inflow_plot)
        print(f"Saved inflow plot to {inflow_plot}")
        plt.close()

    # 3. Plot Availability
    avail_file = os.path.join(data_dir, 'availability.csv')
    if os.path.exists(avail_file):
        df_avail = pd.read_csv(avail_file)
        df_avail['timestamp'] = pd.to_datetime(df_avail['timestamp'])
        
        plt.figure(figsize=(12, 6))
        plt.step(df_avail['timestamp'], df_avail['Turbine1'], label='Turbine1 Availability (1=On)', where='post', color='blue', alpha=0.7)
        plt.step(df_avail['timestamp'], df_avail['Pump1'], label='Pump1 Availability (1=On)', where='post', color='cyan', alpha=0.7)
        plt.title('Unit Availability Schedule (1=Available, 0=Maintenance)')
        plt.xlabel('Date')
        plt.ylabel('Availability Status')
        plt.yticks([0, 1], ['Maint. (0)', 'Available (1)'])
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        avail_plot = os.path.join(data_dir, '..', 'output', 'availability_trends.png')
        plt.savefig(avail_plot)
        print(f"Saved availability plot to {avail_plot}")
        plt.close()

if __name__ == "__main__":
    base_dir = r'c:\Users\User\OneDrive - Alpen-Adria Universität Klagenfurt\SS26\PySHOP'
    data_dir = os.path.join(base_dir, 'data', 'input')
    os.makedirs(os.path.join(base_dir, 'data', 'output'), exist_ok=True)
    visualize_input_data(data_dir)
