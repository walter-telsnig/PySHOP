"""
Minimal SHOP optimization test - extremely simple case
Just 1 reservoir and 1 generator, no pump
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager

def main():
    print("Minimal SHOP Test")
    print("=" * 60)
    
    # Create session
    print("\n1. Creating session...")
    shop = ShopManager()
    model = shop.get_model()
    
    # Set time
    print("2. Setting time...")
    shop.set_time("2024-01-01 00:00:00", "2024-01-02 00:00:00", 60)
    
    # Create simple topology
    print("3. Creating simple topology...")
    
    # One reservoir
    rsv = model.reservoir.add_object("Reservoir1")
    rsv.max_vol.set(10.0)
    rsv.lrl.set(90.0)
    rsv.hrl.set(100.0)
    rsv.vol_head.set(pd.Series([90.0, 100.0], index=[0.0, 10.0], name=0.0))
    rsv.start_head.set(95.0)
    rsv.energy_value_input.set(30.0)
    
    # Simple inflow
    time_index = pd.date_range("2024-01-01", periods=25, freq='h')
    inflow = pd.Series([5.0] * 25, index=time_index)
    rsv.inflow.set(inflow)
    
    # One plant
    plant = model.plant.add_object("Plant1")
    plant.outlet_line.set(9)  # drainage level
    plant.main_loss.set([0.0002])
    plant.penstock_loss.set([0.0])
    
    # Connection
    model.connection.add_object("Reservoir1", "Plant1")
    
    # One generator
    gen = model.generator.add_object("Gen1")
    gen.penstock.set(1)
    gen.p_min.set(10.0)
    gen.p_max.set(50.0)
    gen.p_nom.set(50.0)
    gen.startcost.set(100)
    
    # Simple efficiency curve
    eff_curve = pd.Series([0.85, 0.90, 0.88], index=[10.0, 30.0, 50.0], name=50.0)
    gen.turb_eff_curves.set([eff_curve])
    
    # Market with prices
    print("4. Adding market...")
    market = model.market.add_object("DayAhead")
    prices = pd.Series([40.0] * 25, index=time_index)
    market.sale_price.set(prices)
    market.buy_price.set(prices)
    
    # Connect plant to market
    model.connection.add_object("Plant1", "DayAhead")
    
    # Run optimization
    print("5. Running optimization...")
    try:
        shop.shop.start_sim([], ['3'])
        print("SUCCESS! Optimization completed")
        
        # Get results
        print("\n6. Getting results...")
        head = rsv.head.get()
        production = gen.production.get()
        
        print(f"   Reservoir head: {head.min():.2f} - {head.max():.2f} masl")
        print(f"   Production: {production.min():.2f} - {production.max():.2f} MW")
        
        # Save to CSV
        output_dir = project_root / 'data' / 'output' / 'results'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = pd.DataFrame({
            'head_masl': head,
            'production_mw': production
        })
        results.to_csv(output_dir / 'minimal_test_results.csv')
        print(f"\n   Results saved to: {output_dir / 'minimal_test_results.csv'}")
        
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
