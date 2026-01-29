"""
OFFICIAL SINTEF BASIC EXAMPLE
Adapted from: https://docs.shop.sintef.energy/examples/basic/basic.html

This is the official SINTEF example to verify SHOP works correctly.
"""

import sys
from pathlib import Path
import pandas as pd

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from pyshop import ShopSession

def main():
    print("=" * 70)
    print("OFFICIAL SINTEF BASIC EXAMPLE")
    print("=" * 70)
    print("Source: https://docs.shop.sintef.energy/examples/basic/basic.html")
    print()
    
    # Create SHOP session
    print("1. Creating SHOP session...")
    licence_dir = project_root / "Licence"
    shop = ShopSession(license_path=str(licence_dir), solver_path=str(licence_dir))
    print(f"   ✓ SHOP version: {shop.shop_api.GetVersionString()}")
    print()
    
    # Set time
    print("2. Setting time resolution...")
    starttime = pd.Timestamp('2018-01-23 00:00:00')
    endtime = pd.Timestamp('2018-01-26')  # 3 days
    shop.set_time_resolution(
        starttime=starttime,
        endtime=endtime,
        timeunit="hour",
        timeresolution=pd.Series(index=[starttime], data=[1])
    )
    print(f"   ✓ Period: {starttime} to {endtime} (3 days)")
    print()
    
    # Add reservoirs - ONLY 2 as shown in SINTEF diagram!
    print("3. Adding reservoirs...")
    shop.model.reservoir.add_object('Reservoir1')
    rsv1 = shop.model.reservoir.Reservoir1
    rsv1.max_vol.set(39)  # Mm³
    rsv1.lrl.set(860)
    rsv1.hrl.set(905)
    rsv1.vol_head.set(pd.Series([860,906,907], index=[0,39,41.66]))
    rsv1.energy_value_input.set(30)
    
    shop.model.reservoir.add_object('Reservoir2')
    rsv2 = shop.model.reservoir.Reservoir2
    rsv2.max_vol.set(97.5)  # Mm³
    rsv2.lrl.set(650)
    rsv2.hrl.set(679)
    rsv2.vol_head.set(pd.Series([650,679,680], index=[0,97.5,104.15]))
    rsv2.inflow.set(pd.Series([60], index=[starttime]))  # m³/s
    rsv2.energy_value_input.set(10)
    print("   ✓ 2 reservoirs added (matching SINTEF diagram)")
    print()
    
    # Add plants
    print("4. Adding plants...")
    shop.model.plant.add_object('Plant1')
    p1 = shop.model.plant.Plant1
    p1.outlet_line.set(672)
    p1.main_loss.set([0.0])
    p1.penstock_loss.set([0.001])
    p1.mip_flag.set(1)
    
    shop.model.plant.add_object('Plant2')
    p2 = shop.model.plant.Plant2
    p2.outlet_line.set(586)
    p2.main_loss.set([0.0])
    p2.penstock_loss.set([0.0001, 0.0002])
    p2.mip_flag.set(1)
    print("   ✓ 2 plants added")
    print()
    
    # Add generators
    print("5. Adding generators...")
    # Plant 1, Generator 1
    shop.model.generator.add_object('G11')
    g11 = shop.model.generator.G11
    g11.penstock.set(1)
    g11.p_min.set(60)
    g11.p_max.set(120)
    g11.p_nom.set(120)
    g11.startcost.set(300)
    g11.gen_eff_curve.set(pd.Series([100,100], index=[60,120]))
    g11.turb_eff_curves.set([
        pd.Series([85.87,87.03,88.09,89.05,89.94,90.77,91.55,92.26,92.82,93.11,93.22,93.04,92.66,92.17],
                 index=[28.12,30.45,32.78,35.11,37.45,39.78,42.11,44.44,46.77,49.1,51.43,53.76,56.1,58.83],
                 name=170),
        pd.Series([86.73,87.90,88.97,89.95,90.84,91.68,92.46,93.19,93.75,94.04,94.15,93.97,93.58,93.10],
                 index=[28.12,30.45,32.78,35.11,37.45,39.78,42.11,44.44,46.77,49.1,51.43,53.76,56.1,58.83],
                 name=200),
        pd.Series([87.59,88.77,89.85,90.84,91.74,92.59,93.38,94.11,94.68,94.97,95.08,94.90,94.51,94.02],
                 index=[28.12,30.45,32.78,35.11,37.45,39.78,42.11,44.44,46.77,49.1,51.43,53.76,56.1,58.83],
                 name=230)
    ])
    
    # Plant 1, Generator 2
    shop.model.generator.add_object('G12')
    g12 = shop.model.generator.G12
    g12.penstock.set(1)
    g12.p_min.set(60)
    g12.p_max.set(120)
    g12.p_nom.set(120)
    g12.startcost.set(300)
    g12.gen_eff_curve.set(pd.Series([100,100], index=[60,120]))
    g12.turb_eff_curves.set(g11.turb_eff_curves.get())  # Same as G11
    
    # Plant 2 generators (simplified)
    for i in range(1, 5):  # G21, G22, G23, G24
        shop.model.generator.add_object(f'G2{i}')
        gen = getattr(shop.model.generator, f'G2{i}')
        gen.penstock.set(1 if i == 1 else 2)
        gen.p_min.set(100 if i == 1 else 30)
        gen.p_max.set(180 if i == 1 else 55)
        gen.p_nom.set(180 if i == 1 else 55)
        gen.startcost.set(300)
        gen.gen_eff_curve.set(pd.Series([100,100], index=[gen.p_min.get(), gen.p_max.get()]))
        
        # Simple turbine efficiency curve
        head_ref = 60
        if i == 1:
            discharges = [126.54,137.03,147.51,158,168.53,179.01,189.5,199.98,210.47,220.95,231.44,241.92,252.45,264.74]
            effs = [92.72,93.26,93.73,94.14,94.48,94.75,94.96,95.10,95.18,95.19,95.13,95.01,94.82,94.52]
        else:
            discharges = [40.82,44.2,47.58,50.97,54.36,57.75,61.13,64.51,67.89,71.27,74.66,78.04,81.44,85.4]
            effs = [83.87,85.19,86.38,87.44,88.36,89.14,89.79,90.30,90.68,90.92,91.03,91.01,90.84,90.48]
        gen.turb_eff_curves.set([pd.Series(effs, index=discharges, name=head_ref)])
    
    print("   ✓ 6 generators added")
    print()
    
    # Connect topology - SINTEF diagram: Rsv1 → Plant1 → Rsv2 → Plant2 → Ocean
    print("6. Connecting topology...")
    rsv1.connect_to(p1)  # Reservoir1 to Plant1
    p1.connect_to(rsv2)  # Plant1 discharges to Reservoir2
    rsv2.connect_to(p2)  # Reservoir2 to Plant2
    # Plant2 discharges to ocean (no downstream reservoir modeled)
    
    g11.connect_to(p1)
    g12.connect_to(p1)
    shop.model.generator.G21.connect_to(p2)
    shop.model.generator.G22.connect_to(p2)
    shop.model.generator.G23.connect_to(p2)
    shop.model.generator.G24.connect_to(p2)
    print("   ✓ Connections established (Rsv1 → Plant1 → Rsv2 → Plant2 → Ocean)")
    print()
    
    # Set initial volumes
    print("7. Setting initial reservoir levels...")
    rsv1.start_head.set(900)  # masl
    rsv2.start_head.set(670)  # masl
    print("   ✓ Initial conditions set")
    print()
    
    # Add market
    print("7. Adding market...")
    shop.model.market.add_object('Day_ahead')
    da = shop.model.market.Day_ahead
    
    # Price data (72 hours from SINTEF example)
    prices = [32.992,31.122,29.312,28.072,30.012,33.362,42.682,74.822,77.732,62.332,
              55.892,46.962,42.582,40.942,39.212,39.142,41.672,46.922,37.102,32.992,
              31.272,29.752,28.782,28.082,27.242,26.622,25.732,25.392,25.992,27.402,
              28.942,32.182,33.082,32.342,30.912,30.162,30.062,29.562,29.462,29.512,
              29.672,30.072,29.552,28.862,28.412,28.072,27.162,25.502,26.192,25.222,
              24.052,23.892,23.682,26.092,28.202,30.902,31.572,31.462,31.172,30.912,
              30.572,30.602,30.632,31.062,32.082,36.262,34.472,32.182,31.492,30.732,
              29.712,28.982]
    
    price_index = [starttime + pd.Timedelta(hours=i) for i in range(72)]
    da.sale_price.set(pd.DataFrame(prices, index=price_index))
    da.buy_price.set(da.sale_price.get() + 0.002)
    da.max_buy.set(pd.Series([9999], [starttime]))
    da.max_sale.set(pd.Series([9999], [starttime]))
    da.load.set(pd.Series([0], [starttime]))
    print("   ✓ Market configured with 72-hour prices")
    print()
    
    # RUN OPTIMIZATION - THE CRITICAL PART!
    print("=" * 70)
    print("RUNNING SHOP OPTIMIZATION")
    print("=" * 70)
    print()
    
    print("Setting 'full' code flag...")
    shop.set_code(['full'], [])
    print("✓ Full optimization mode set")
    print()
    
    print("Starting 5 full iterations...")
    try:
        shop.start_sim([], ['5'])
        print("✓ Full iterations completed!")
    except Exception as e:
        print(f"✗ Full iterations failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("Setting 'incremental' code flag...")
    shop.set_code(['incremental'], [])
    print("✓ Incremental mode set")
    print()
    
    print("Starting 3 incremental iterations...")
    try:
        shop.start_sim([], ['3'])
        print("✓ Incremental iterations completed!")
    except Exception as e:
        print(f"✗ Incremental iterations failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("=" * 70)
    print("✓✓✓ OPTIMIZATION SUCCESSFUL! ✓✓✓")
    print("=" * 70)
    print()
    
    # Get complete results for export
    print("Results:")
    
    # All generators
    prod_g11 = g11.production.get()
    prod_g12 = g12.production.get()
    prod_g21 = shop.model.generator.G21.production.get()
    prod_g22 = shop.model.generator.G22.production.get()
    prod_g23 = shop.model.generator.G23.production.get()
    prod_g24 = shop.model.generator.G24.production.get()
    
    # Only 2 reservoirs!
    head_rsv1 = rsv1.head.get()
    head_rsv2 = rsv2.head.get()
    
    # Plants
    prod_p1 = p1.production.get()
    prod_p2 = p2.production.get()
    total_prod = prod_p1 + prod_p2
    
    # Prices
    market_prices = da.sale_price.get()
    
    print(f"  Generator G11:")
    print(f"    Min: {prod_g11.min():.2f} MW")
    print(f"    Max: {prod_g11.max():.2f} MW")
    print(f"    Total energy: {prod_g11.sum():.0f} MWh")
    
    print(f"  Reservoir 2 (lower):")
    print(f"    Start: {head_rsv2.iloc[0]:.2f} masl")
    print(f"    End: {head_rsv2.iloc[-1]:.2f} masl")
    
    print(f"\n  Total generation: {total_prod.sum():.0f} MWh")
    print(f"  Average power: {total_prod.mean():.1f} MW")
    
    # Export to CSV
    print()
    print("Exporting results to CSV...")
    output_dir = project_root / 'data' / 'output' / 'results'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine length (results include endpoint hour)
    n = len(total_prod)
    
    # Create DataFrame with all results - ONLY 2 RESERVOIRS
    results_df = pd.DataFrame({
        'Reservoir1_masl': head_rsv1.values[:n],
        'Reservoir2_masl': head_rsv2.values[:n],
        'Plant1_MW': prod_p1.values[:n],
        'Plant2_MW': prod_p2.values[:n],
        'Total_MW': total_prod.values[:n],
        'G11_MW': prod_g11.values[:n],
        'G12_MW': prod_g12.values[:n],
        'G21_MW': prod_g21.values[:n],
        'G22_MW': prod_g22.values[:n],
        'G23_MW': prod_g23.values[:n],
        'G24_MW': prod_g24.values[:n],
    }, index=total_prod.index[:n])
    
    # Add prices (extend if needed for endpoint)
    price_vals = list(market_prices.values.flatten())
    while len(price_vals) < n:
        price_vals.append(price_vals[-1] if price_vals else 0)
    results_df['Price_EUR_MWh'] = price_vals[:n]
    
    csv_path = output_dir / 'sintef_official_3days.csv'
    results_df.to_csv(csv_path)
    print(f"✓ CSV saved: {csv_path}")
    
    print()
    print("=" * 70)
    print("SINTEF OFFICIAL EXAMPLE WORKS!")
    print("=" * 70)
    print()
    print("📊 Topology (2 reservoirs as per SINTEF diagram):")
    print("   Reservoir1 (860-905 masl)")
    print("       ↓ (via Plant1)")
    print("   Reservoir2 (650-679 masl)")
    print("       ↓ (via Plant2)")
    print("   Ocean/Downstream")
    print()
    print(f"📁 Results exported: {csv_path.name}")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
