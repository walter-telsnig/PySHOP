"""
Simple example: Building and running a basic pump-turbine system

This example demonstrates:
1. Loading a topology from YAML
2. Creating a SHOP session
3. Setting up time series data
4. Running optimization
5. Visualizing results
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager
from model_builder import build_model_from_yaml
from data_io import create_sample_inflow_data, create_sample_price_data
from visualization import plot_reservoir_levels, plot_generation_and_pumping
import pandas as pd


def main():
    print("=" * 60)
    print("SHOP Simple Pump-Turbine Example")
    print("=" * 60)
    
    # Define paths
    config_dir = project_root / 'config'
    data_dir = project_root / 'data'
    output_dir = project_root / 'data' / 'output'
    
    topology_file = config_dir / 'simple_pump_turbine.yaml'
    
    # Step 1: Create SHOP session
    print("\n1. Creating SHOP session...")
    shop_mgr = ShopManager(silent=False)
    
    # Step 2: Set time period
    print("\n2. Setting optimization time period...")
    starttime = "2024-01-01 00:00:00"
    endtime = "2024-01-03 00:00:00"  # 2-day optimization
    shop_mgr.set_time(starttime, endtime, timeresolution=60)  # Hourly resolution
    
    # Step 3: Build model from YAML topology
    print(f"\n3. Building model from topology: {topology_file.name}")
    model = shop_mgr.get_model()
    build_model_from_yaml(model, topology_file)
    
    print("   Topology created successfully!")
    print(f"   - Reservoirs: {model.reservoir.get_object_names()}")
    print(f"   - Plants: {model.plant.get_object_names()}")
    print(f"   - Generators: {model.generator.get_object_names()}")
    print(f"   - Pumps: {model.pump.get_object_names()}")
    
    # Step 4: Generate sample input data
    print("\n4. Creating sample input data...")
    
    # Create sample inflow data
    inflow_file = data_dir / 'input' / 'inflow' / 'sample_inflow.csv'
    create_sample_inflow_data(inflow_file, starttime, endtime, freq='h', mean_flow=30.0)
    
    # Create sample price data
    price_file = data_dir / 'input' / 'prices' / 'sample_prices.csv'
    create_sample_price_data(price_file, starttime, endtime, freq='h', mean_price=50.0)
    
    # Step 5: Set inflow to upper reservoir
    print("\n5. Loading time series data into model...")
    inflow_df = pd.read_csv(inflow_file, parse_dates=['datetime'])
    inflow_series = pd.Series(
        inflow_df['inflow_m3s'].values,
        index=pd.to_datetime(inflow_df['datetime'])
    )
    model.reservoir.UpperRes.inflow.set(inflow_series)
    
    # Step 6: Set electricity prices
    price_df = pd.read_csv(price_file, parse_dates=['datetime'])
    price_series = pd.Series(
        price_df['price_eur_mwh'].values,
        index=pd.to_datetime(price_df['datetime'])
    )
    
    # Note: Setting prices requires a market object in SHOP
    # For this simple example, we'll skip market prices
    # In a real scenario, you'd create a market object and set buy/sell prices
    
    # Step 7: Plot topology (optional)
    print("\n6. Generating topology visualization...")
    try:
        shop_mgr.plot_topology(filename=str(output_dir / 'plots' / 'topology'))
        print("   Topology plot saved!")
    except Exception as e:
        print(f"   Warning: Could not generate topology plot: {e}")
    
    # Step 8: Run optimization
    print("\n7. Running SHOP optimization...")
    print("   (This may take a moment...)")
    
    try:
        shop_mgr.run_optimization()
        print("   Optimization completed successfully!")
        
        # Step 9: Extract and visualize results
        print("\n8. Extracting results...")
        
        # Get reservoir levels
        upper_res_level = model.reservoir.UpperRes.head.get()
        lower_res_level = model.reservoir.LowerRes.head.get()
        
        # Get generation and pumping
        gen_power = model.generator.Gen1.production.get()
        pump_power = model.pump.Pump1.consumption.get()
        
        print("   Results extracted successfully!")
        
        # Step 10: Create visualizations
        print("\n9. Creating visualizations...")
        plots_dir = output_dir / 'plots'
        plots_dir.mkdir(parents=True, exist_ok=True)
        
        # Plot reservoir levels
        reservoir_data = {
            'Upper Reservoir': upper_res_level,
            'Lower Reservoir': lower_res_level
        }
        plot_reservoir_levels(reservoir_data, 
                            save_path=plots_dir / 'reservoir_levels.png',
                            show=False)
        
        # Plot generation and pumping
        plot_generation_and_pumping(gen_power, pump_power,
                                  save_path=plots_dir / 'dispatch.png',
                                  show=False)
        
        print(f"   Plots saved to: {plots_dir}")
        
        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)
        print(f"\nCheck the following directories:")
        print(f"  - Input data:  {data_dir / 'input'}")
        print(f"  - Output plots: {plots_dir}")
        
    except Exception as e:
        print(f"\n   Error during optimization: {e}")
        print("\n   This might be due to:")
        print("   - Missing SHOP license file")
        print("   - Missing SHOP solver binaries")
        print("   - Incorrect model configuration")
        print(f"\n   Please check the Licence folder and ensure SHOP is properly installed.")


if __name__ == "__main__":
    main()
