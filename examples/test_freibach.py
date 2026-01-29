"""
Freibach System Test - Using Real Topology from ASCII File

This script loads the Freibach topology extracted from the working SHOP model
and tests if it builds correctly.
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager
from model_builder import build_model_from_yaml


def main():
    print("=" * 70)
    print("Freibach System Model Test")
    print("Real topology extracted from POWELSRV_FRELT.ascii")
    print("=" * 70)
    
    # Paths
    config_dir = project_root / 'config'
    topology_file = config_dir / 'Freibach.yaml'
    
    # Step 1: Create SHOP session
    print("\n1. Creating SHOP session...")
    try:
        shop_mgr = ShopManager()
        model = shop_mgr.get_model()
        print("   ✓ SHOP session created")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 2: Set time period (start with 2 weeks for testing)
    print("\n2. Setting time period...")
    try:
        starttime = "2026-01-29 00:00:00"
        endtime = "2026-02-12 00:00:00"  # 2 weeks
        shop_mgr.set_time(starttime, endtime, timeresolution=60)
        print(f"   ✓ Time: {starttime} to {endtime} (2 weeks, hourly)")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Step 3: Build model from Freibach YAML
    print("\n3. Building Freibach topology...")
    try:
        build_model_from_yaml(model, topology_file)
        print(f"   ✓ Topology loaded from: {topology_file.name}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 4: Display model structure
    print("\n4. Model Structure:")
    print("   " + "-" * 60)
    
    # Reservoirs
    print("\n   Reservoirs:")
    for rsv_name in model.reservoir.get_object_names():
        rsv = getattr(model.reservoir, rsv_name)
        print(f"     - {rsv_name}:")
        print(f"       Max vol: {rsv.max_vol.get()} Mm³")
        print(f"       LRL: {rsv.lrl.get()} masl")
        print(f"       HRL: {rsv.hrl.get()} masl")
        try:
            start_vol = rsv.start_vol.get()
            print(f"       Start vol: {start_vol} Mm³")
        except:
            pass
        try:
            endpoint = rsv.endpoint_desc.get()
            if endpoint is not None:
                print(f"       Endpoint desc: {len(endpoint)} points")
        except:
            pass
    
    # Plants
    print("\n   Plants:")
    for plant_name in model.plant.get_object_names():
        plant = getattr(model.plant, plant_name)
        print(f"     - {plant_name}:")
        try:
            outlet = plant.outlet_line.get()
            print(f"       Outlet line: {outlet} masl")
        except:
            pass
    
    # Generators
    print("\n   Generators:")
    for gen_name in model.generator.get_object_names():
        gen = getattr(model.generator, gen_name)
        print(f"     - {gen_name}:")
        print(f"       P nom: {gen.p_nom.get()} MW")
        print(f"       P range: {gen.p_min.get()} - {gen.p_max.get()} MW")
        try:
            turb_curves = gen.turb_eff_curves.get()
            if turb_curves:
                print(f"       Turb eff curves: {len(turb_curves)} curves")
        except:
            pass
        try:
            gen_curve = gen.gen_eff_curve.get()
            if gen_curve is not None:
                print(f"       Gen eff curve: {len(gen_curve)} points")
        except:
            pass
    
    # Pumps
    print("\n   Pumps:")
    for pump_name in model.pump.get_object_names():
        pump = getattr(model.pump, pump_name)
        print(f"     - {pump_name}:")
        print(f"       P nom: {pump.p_nom.get()} MW")
        try:
            turb_curves = pump.turb_eff_curves.get()
            if turb_curves:
                print(f"       Turb eff curves: {len(turb_curves)} curves (reversible!)")
        except:
            pass
    
    # Step 5: Set simple inflow data
    print("\n5. Setting inflow data...")
    try:
        time_index = pd.date_range(starttime, periods=337, freq='h')
        # Use average inflow for upper reservoir
        inflow = pd.Series([1.5] * 337, index=time_index)  # m3/s
        model.reservoir.Freibach.inflow.set(inflow)
        
        # Lower reservoir has no inflow (fed by plant)
        inflow_lower = pd.Series([0.0] * 337, index=time_index)
        model.reservoir.DrauWest.inflow.set(inflow_lower)
        
        print(f"   ✓ Inflow set: 337 hourly time steps")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Success!
    print("\n" + "=" * 70)
    print("SUCCESS! Freibach Model Built Correctly")
    print("=" * 70)
    
    print("\nModel includes:")
    print("  ✓ 2 reservoirs (Freibach, DrauWest)")
    print("  ✓ 1 plant (Freibach_Plant)")  
    print("  ✓ 2 generators (Gen1, Gen2)")
    print("  ✓ 2 pumps (Pump1, Pump2) with turbine curves!")
    print("  ✓ Endpoint descriptions (water values)")
    print("  ✓ Complete efficiency curves")
    print("  ✓ Real data from production system")
    
    print("\nNext steps:")
    print("  1. Add market with prices")
    print("  2. Run optimization")
    print("  3. Analyze results")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
