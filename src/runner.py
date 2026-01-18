import os
import pandas as pd
from datetime import datetime
from model_builder import get_session
from data_mapper import map_input_data

def run_toy_example():
    # 1. Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    topo_path = os.path.join(base_dir, "models", "topology.yaml")
    
    # 2. Initialize Session
    shop = get_session(topo_path)
    
    # 3. Time Horizon (1 year)
    starttime = datetime(2025, 1, 1, 0, 0)
    endtime = datetime(2026, 1, 1, 0, 0)
    shop.set_time_resolution(starttime=starttime, endtime=endtime, timeunit="hour")
    
    # 4. Set Input Data (from CSV)
    data_dir = os.path.join(base_dir, 'data', 'input')
    map_input_data(shop, data_dir)
    
    # 5. Execute optimization
    print("Running optimization...")
    shop.execute_full_command("set_code /incremental")
    shop.execute_full_command("set_method simplex")
    shop.execute_full_command("start sim") 
    
    # 6. Check results
    print("\n--- Results ---")
    gen = shop.model.generator.Turbine1.production.get()
    pump = shop.model.pump.Pump1.consumption.get()
    
    if gen is not None:
        print(f"Generator Turbine1 Production: {gen.sum()} MWh")
    else:
        print("No turbine generation data found.")
        
    if pump is not None:
        print(f"Pump Pump1 Consumption: {pump.sum()} MWh")
    else:
        print("No pumping data found.")

    vol_upper = shop.model.reservoir.UpperRes.storage.get()
    if vol_upper is not None:
        # Check if it's a series and has values
        if hasattr(vol_upper, 'empty') and not vol_upper.empty:
            print(f"Final Volume UpperRes: {vol_upper.iloc[-1]} Mm3")
        else:
            print(f"Volume series is empty or not found. Raw output: {vol_upper}")

if __name__ == "__main__":
    run_toy_example()
