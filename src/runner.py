import os
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt
from datetime import datetime
from model_builder import get_session
from data_mapper import map_input_data

def save_results(shop, base_dir):
    """Collects results, generates plots, and exports to Excel."""
    results_dir = os.path.join(base_dir, "results")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    print(f"\nExporting results to {results_dir}...")
    
    # 1. Collect Data
    data = {}
    
    # Inflow
    inflow_upper = shop.model.reservoir.UpperRes.inflow.get()
    inflow_lower = shop.model.reservoir.LowerRes.inflow.get()
    if inflow_upper is not None and inflow_lower is not None:
        data['Inflow'] = pd.DataFrame({
            'UpperRes_Inflow': inflow_upper,
            'LowerRes_Inflow': inflow_lower
        })

    # Market Price
    price = shop.model.market.DayAhead.sale_price.get()
    if price is not None:
        data['MarketPrice'] = pd.DataFrame({'Price': price})

    # Availability (Maintenance Flag: 0 = Available, 1 = Maintenance)
    maint_turb = shop.model.generator.Turbine1.maintenance_flag.get()
    maint_pump = shop.model.pump.Pump1.maintenance_flag.get()
    if maint_turb is not None and maint_pump is not None:
        # Convert to Availability (1 = Available, 0 = Maintenance)
        data['Availability'] = pd.DataFrame({
            'Turbine1_Avail': 1 - maint_turb,
            'Pump1_Avail': 1 - maint_pump
        })

    # Reservoir Storage
    vol_upper = shop.model.reservoir.UpperRes.storage.get()
    vol_lower = shop.model.reservoir.LowerRes.storage.get()
    if vol_upper is not None and vol_lower is not None:
        data['ReservoirStorage'] = pd.DataFrame({
            'UpperRes_Storage': vol_upper,
            'LowerRes_Storage': vol_lower
        })

    # Generation & Consumption
    gen = shop.model.generator.Turbine1.production.get()
    pump = shop.model.pump.Pump1.consumption.get()
    if gen is not None and pump is not None:
        data['Operations'] = pd.DataFrame({
            'Turbine1_Production': gen,
            'Pump1_Consumption': pump
        })

    # 2. Generate Plots
    plot_paths = {}
    
    if 'Inflow' in data:
        plt.figure(figsize=(10, 4))
        data['Inflow'].plot(title="Reservoir Inflows")
        plt.ylabel("Inflow [m3/s]")
        path = os.path.join(results_dir, "inflow.png")
        plt.savefig(path)
        plt.close()
        plot_paths['Inflow'] = path

    if 'MarketPrice' in data:
        plt.figure(figsize=(10, 4))
        data['MarketPrice'].plot(title="Market Price")
        plt.ylabel("Price [EUR/MWh]")
        path = os.path.join(results_dir, "price.png")
        plt.savefig(path)
        plt.close()
        plot_paths['MarketPrice'] = path

    if 'Availability' in data:
        plt.figure(figsize=(10, 4))
        data['Availability'].plot(drawstyle="steps-pre", title="Unit Availability")
        plt.ylabel("Available (1/0)")
        plt.ylim(-0.1, 1.1)
        path = os.path.join(results_dir, "availability.png")
        plt.savefig(path)
        plt.close()
        plot_paths['Availability'] = path

    if 'ReservoirStorage' in data:
        plt.figure(figsize=(10, 4))
        data['ReservoirStorage'].plot(title="Reservoir Storage Progress")
        plt.ylabel("Storage [Mm3]")
        path = os.path.join(results_dir, "reservoir.png")
        plt.savefig(path)
        plt.close()
        plot_paths['ReservoirStorage'] = path

    # 3. Export to Excel
    excel_path = os.path.join(results_dir, "optimization_results.xlsx")
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        for sheet_name, df in data.items():
            df.to_excel(writer, sheet_name=sheet_name)
            
            # Embed corresponding plot if it exists
            if sheet_name in plot_paths:
                worksheet = writer.sheets[sheet_name]
                # Insert the image at a specific cell
                worksheet.insert_image('G2', plot_paths[sheet_name])

    print(f"Results successfully saved to {excel_path}")

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
    print("Applying end-level constraints...")
    for res_name in ["UpperRes", "LowerRes"]:
        res = shop.model.reservoir[res_name]
        start_vol = res.start_vol.get()
        if start_vol is not None:
            # Set target at the very last time step
            res.schedule.set(pd.Series([float(start_vol)], index=[endtime]))
            res.schedule_flag.set(1) # Hard target
            res.upper_slack.set(float(start_vol) + 0.01)
            res.lower_slack.set(float(start_vol) - 0.01)
            print(f"  {res_name}: Forced to {start_vol} Mm3 (+/- 0.01) at {endtime}")

    print("Running optimization...")
    shop.execute_full_command("set_code /incremental")
    shop.execute_full_command("set_method simplex")
    shop.execute_full_command("start sim") 
    
    # 6. Check results
    print("\n--- Summary Results ---")
    gen = shop.model.generator.Turbine1.production.get()
    pump = shop.model.pump.Pump1.consumption.get()
    
    if gen is not None:
        print(f"Generator Turbine1 Production: {gen.sum():.2f} MWh")
    if pump is not None:
        print(f"Pump Pump1 Consumption: {pump.sum():.2f} MWh")

    vol_upper = shop.model.reservoir.UpperRes.storage.get()
    if vol_upper is not None and hasattr(vol_upper, 'iloc') and not vol_upper.empty:
        print(f"Final Volume UpperRes: {vol_upper.iloc[-1]:.2f} Mm3")

    vol_lower = shop.model.reservoir.LowerRes.storage.get()
    if vol_lower is not None and hasattr(vol_lower, 'iloc') and not vol_lower.empty:
        print(f"Final Volume LowerRes: {vol_lower.iloc[-1]:.2f} Mm3")

    # 7. Save and Visualize
    save_results(shop, base_dir)

if __name__ == "__main__":
    run_toy_example()
