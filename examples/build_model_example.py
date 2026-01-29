"""
Simplified example: Building a basic pump-turbine system WITHOUT running optimization

This example demonstrates:
1. Loading a topology from YAML
2. Creating a SHOP session  
3. Building the model
4. Creating sample data
5. Visualizing the topology (if possible)

This is safer for initial testing as it doesn't require running the full SHOP optimization.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager
from model_builder import build_model_from_yaml
from data_io import create_sample_inflow_data, create_sample_price_data


def main():
    print("="  * 60)
    print("SHOP Model Building Example (No Optimization)")
    print("=" * 60)
    
    # Define paths
    config_dir = project_root / 'config'
    data_dir = project_root / 'data'
    output_dir = project_root / 'data' / 'output'
    
    topology_file = config_dir / 'simple_pump_turbine.yaml'
    
    # Step 1: Create SHOP session
    print("\n1. Creating SHOP session...")
    try:
        shop_mgr = ShopManager(silent=False)
        print("   ✓ SHOP session created successfully!")
    except Exception as e:
        print(f"   ✗ Error creating SHOP session: {e}")
        return
    
    # Step 2: Set time period
    print("\n2. Setting optimization time period...")
    starttime = "2024-01-01 00:00:00"
    endtime = "2024-01-15 00:00:00"  # 2 weeks = 14 days
    try:
        shop_mgr.set_time(starttime, endtime, timeresolution=60)  # Hourly
        print(f"   ✓ Time period set: {starttime} to {endtime} (2 weeks)")
    except Exception as e:
        print(f"   ✗ Error setting time: {e}")
        return
    
    # Step 3: Build model from YAML topology
    print(f"\n3. Building model from topology: {topology_file.name}")
    try:
        model = shop_mgr.get_model()
        build_model_from_yaml(model, topology_file)
        
        print("   ✓ Topology created successfully!")
        print(f"     - Reservoirs: {model.reservoir.get_object_names()}")
        print(f"     - Plants: {model.plant.get_object_names()}")
        print(f"     - Generators: {model.generator.get_object_names()}")
        print(f"     - Pumps: {model.pump.get_object_names()}")
    except Exception as e:
        print(f"   ✗ Error building model: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Generate sample input data
    print("\n4. Creating sample input data files...")
    
    # Create sample inflow data
    try:
        inflow_file = data_dir / 'input' / 'inflow' / 'sample_inflow.csv'
        inflow_file.parent.mkdir(parents=True, exist_ok=True)
        create_sample_inflow_data(inflow_file, starttime, endtime, freq='h', mean_flow=30.0)
        print(f"   ✓ Created: {inflow_file}")
    except Exception as e:
        print(f"   ✗ Error creating inflow data: {e}")
    
    # Create sample price data
    try:
        price_file = data_dir / 'input' / 'prices' / 'sample_prices.csv'
        price_file.parent.mkdir(parents=True, exist_ok=True)
        create_sample_price_data(price_file, starttime, endtime, freq='h', mean_price=50.0)
        print(f"   ✓ Created: {price_file}")
    except Exception as e:
        print(f"   ✗ Error creating price data: {e}")
    
    # Step 5: Show model information
    print("\n5. Model Information:")
    print("   ----------------------")
    
    # Upper Reservoir
    upper_res = model.reservoir.UpperRes
    print(f"\n   Upper Reservoir:")
    print(f"     - Max volume: {upper_res.max_vol.get()} Mm³")
    print(f"     - LRL: {upper_res.lrl.get()} masl")
    print(f"     - HRL: {upper_res.hrl.get()} masl")
    print(f"     - Start head: {upper_res.start_head.get()} masl")
    try:
        print(f"     - Energy value (endpoint): {upper_res.energy_value_input.get()} EUR/MWh")
    except:
        pass
    
    # Lower Reservoir
    lower_res = model.reservoir.LowerRes
    print(f"\n   Lower Reservoir:")
    print(f"     - Max volume: {lower_res.max_vol.get()} Mm³")
    print(f"     - LRL: {lower_res.lrl.get()} masl")
    print(f"     - HRL: {lower_res.hrl.get()} masl")
    print(f"     - Start head: {lower_res.start_head.get()} masl")
    try:
        print(f"     - Energy value (endpoint): {lower_res.energy_value_input.get()} EUR/MWh")
    except:
        pass
    
    # Generator
    gen1 = model.generator.Gen1
    print(f"\n   Generator Gen1:")
    print(f"     - P min: {gen1.p_min.get()} MW")
    print(f"     - P max: {gen1.p_max.get()} MW")
    print(f"     - P nom: {gen1.p_nom.get()} MW")
    
    # Pump
    pump1 = model.pump.Pump1
    print(f"\n   Pump Pump1:")
    print(f"     - P min: {pump1.p_min.get()} MW")
    print(f"     - P max: {pump1.p_max.get()} MW")
    print(f"     - P nom: {pump1.p_nom.get()} MW")
    
    print("\n" + "=" * 60)
    print("Model Building Completed Successfully!")
    print("=" * 60)
    print(f"\nNext steps:")
    print(f"  1. Check the sample data in: {data_dir / 'input'}")
    print(f"  2. Review the topology configuration: {topology_file}")
    print(f"  3. Modify the YAML file to create your own topologies")
    print(f"  4. Check SHOP documentation for running optimizations")
    print("\n Note: This example doesn't run optimization to avoid potential")
    print("       crashes. Once you're comfortable with model building,")
    print("       refer to SHOP documentation for optimization examples.")


if __name__ == "__main__":
    main()
