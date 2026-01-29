"""
Minimal 1-Day Test - Ultra Simplified

Absolute minimum for SHOP to work:
- 1 reservoir
- 1 generator  
- 1 market
- 24 hours only
"""

import sys
from pathlib import Path
import pandas as pd

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager


def main():
    print("=" * 70)
    print("MINIMAL 1-DAY TEST")
    print("=" * 70)
    
    # Create session
    print("\n1. Creating SHOP session...")
    shop_mgr = ShopManager(silent=False)
    model = shop_mgr.get_model()
    print("   ✓ Created")
    
    #  Set time - just 1 day!
    print("\n2. Setting time (24 hours)...")
    starttime = pd.Timestamp("2026-01-29 00:00:00")
    endtime = pd.Timestamp("2026-01-30 00:00:00")
    shop_mgr.shop.set_time_resolution(
        starttime=starttime,
        endtime=endtime,
        timeunit="hour",
        timeresolution=pd.Series(index=[starttime], data=[1])
    )
    print("   ✓ 24 hours")
    
    # Create simple reservoir
    print("\n3. Creating reservoir...")
    rsv = model.reservoir.add_object("Upper")
    rsv.max_vol.set(10.0)  # 10 Mm3
    rsv.lrl.set(700.0)
    rsv.hrl.set(750.0)
    rsv.vol_head.set(pd.Series([700, 750], index=[0, 10], name=0))
    rsv.start_head.set(725.0)
    rsv.energy_value_input.set(50.0)  # EUR/MWh endpoint value
    print("   ✓ Upper reservoir: 10 Mm³, 700-750 masl")
    
    # Set inflow
    time_idx = pd.date_range("2026-01-29", periods=25, freq='h')
    inflow = pd.Series([2.0] * 25, index=time_idx)
    rsv.inflow.set(inflow)
    print("   ✓ Inflow: 2 m³/s constant")
    
    # Create plant
    print("\n4. Creating plant...")
    plant = model.plant.add_object("Plant1")
    plant.connect_to(rsv)
    plant.outlet_line.set(650.0)
    plant.main_loss.set([0.0])
    plant.penstock_loss.set([0.0])
    print("   ✓ Plant1")
    
    # Create generator
    print("\n5. Creating generator...")
    gen = model.generator.add_object("Gen1")
    gen.connect_to(plant)
    gen.penstock.set(1)
    gen.p_min.set(0.0)
    gen.p_max.set(10.0)
    gen.p_nom.set(10.0)
    
    # Simple efficiency curves
    gen.gen_eff_curve.set(pd.Series([95, 95], index=[0, 10], name=1.0))
    gen.turb_eff_curves.set([pd.Series([90, 90], index=[5, 10], name=50.0)])
    print("   ✓ Gen1: 0-10 MW")
    
    # Create market
    print("\n6. Creating market...")
    market = model.market.add_object("Market")
    prices = pd.Series([40.0] * 24, index=time_idx[:24])
    market.sale_price.set(prices)
    market.buy_price.set(prices)
    print("   ✓ Market: 40 EUR/MWh constant")
    
    # Run optimization
    print("\n7. Running optimization...")
    print("   Setting code flag: full")
    shop_mgr.shop.set_code(['full'], [])
    print("   ✓ Code set")
    
    print("   Command: start sim 3")
    print()
    
    try:
        shop_mgr.shop.start_sim([], ['3'])
        print("\n✓ ✓ ✓ OPTIMIZATION SUCCESSFUL! ✓ ✓ ✓\n")
        
        # Get results
        prod = gen.production.get()
        head = rsv.head.get()
        
        print(f"Results:")
        print(f"  Production: {prod.min():.1f} - {prod.max():.1f} MW")
        print(f"  Average: {prod.mean():.1f} MW") 
        print(f"  Total energy: {prod.sum():.0f} MWh")
        print(f"  Reservoir: {head.min():.1f} - {head.max():.1f} masl")
        
        print("\n" + "=" * 70)
        print("SUCCESS! Basic SHOP optimization works!")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
