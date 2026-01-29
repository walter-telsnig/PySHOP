"""
EXACT SINTEF BASIC EXAMPLE REPLICA
Source: https://docs.shop.sintef.energy/examples/basic/basic.html

This script replicates the SINTEF example EXACTLY using their precise parameters
for direct comparison of results.

Differences from sintef_official_example.py:
- Uses EXACT reservoir parameters from documentation
- Uses EXACT generator efficiency curves
- Uses EXACT 72-hour price data
- 2 reservoirs instead of 3 (simpler version)
- Can compare results directly with SINTEF documentation
"""

import sys
from pathlib import Path
import pandas as pd

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from pyshop import ShopSession


def main():
    print("=" * 80)
    print("EXACT SINTEF BASIC EXAMPLE REPLICA")
    print("=" * 80)
    print("Source: https://docs.shop.sintef.energy/examples/basic/basic.html")
    print("Using EXACT parameters from SINTEF documentation for comparison")
    print()
    
    # Create SHOP session
    print("1. Creating SHOP session...")
    licence_dir = project_root / "Licence"
    shop = ShopSession(license_path=str(licence_dir), solver_path=str(licence_dir))
    print(f"   ✓ {shop.shop_api.GetVersionString()}")
    print()
    
    # Set time - EXACT from SINTEF (3 days)
    print("2. Setting time resolution...")  
    starttime = pd.Timestamp('2018-01-23 00:00:00')
    endtime = pd.Timestamp('2018-01-26')  # 3 days (72 hours)
    shop.set_time_resolution(
        starttime=starttime,
        endtime=endtime,
        timeunit="hour",
        timeresolution=pd.Series(index=[starttime], data=[1])
    )
    print(f"   ✓ Period: {starttime} to {endtime} (3 days)")
    print()
    
    # Add reservoirs - EXACT from SINTEF documentation
    print("3. Adding reservoirs (EXACT SINTEF parameters)...")
    
    # Reservoir 1 - EXACT values from SINTEF
    rsv1 = shop.model.reservoir.add_object('Reservoir1')
    rsv1.max_vol.set(39)  # Mm³
    rsv1.lrl.set(860)  # masl
    rsv1.hrl.set(905)  # masl
    
    # Vol-head curve - EXACT from SINTEF
    rsv1.vol_head.set(pd.Series(
        [860, 862, 864, 866, 870, 872, 874, 876, 878, 880, 882, 884, 886, 888, 890, 894, 896, 898, 902, 904, 905, 907],
        index=[0, 0.91, 1.87, 2.88, 5.07, 6.27, 7.56, 8.91, 10.34, 11.87, 13.53, 15.27, 17.11, 19.05, 21.1, 25.65, 27.96, 30.36, 35.18, 37.68, 39, 41.66],
        name=0
    ))
    
    rsv1.flow_descr.set(pd.Series([0, 132], index=[906, 907], name=0))
    rsv1.start_head.set(900)  # masl
    rsv1.energy_value_input.set(30)  # NOK/MWh (SINTEF uses NOK)
    
    # Reservoir 2 - EXACT values from SINTEF
    rsv2 = shop.model.reservoir.add_object('Reservoir2')
    rsv2.max_vol.set(97.5)  # Mm³
    rsv2.lrl.set(650)  # masl
    rsv2.hrl.set(679)  # masl
    
    # Vol-head curve - EXACT from SINTEF
    rsv2.vol_head.set(pd.Series(
        [650, 651.28, 652.55, 653.83, 656.38, 657.66, 658.94, 660.21, 661.49, 662.77, 664.04, 665.32, 666.6, 667.87, 669.15, 671.70, 672.98, 674.26, 676.81, 678.09, 679, 680],
        index=[0, 2.275, 4.675, 7.2, 12.675, 15.675, 18.9, 22.275, 25.85, 29.675, 33.825, 38.175, 42.775, 47.625, 52.75, 64.125, 69.9, 75.9, 87.95, 94.2, 97.5, 104.15],
        name=0
    ))
    
    rsv2.flow_descr.set(pd.Series([0, 132], index=[679, 680], name=0))
    rsv2.inflow.set(pd.Series([60], [starttime]))  # m³/s
    rsv2.start_head.set(670)  # masl
    rsv2.energy_value_input.set(10)  # NOK/MWh
    
    print("   ✓ Reservoir1: 39 Mm³, 860-905 masl, water value: 30 NOK/MWh")
    print("   ✓ Reservoir2: 97.5 Mm³, 650-679 masl, water value: 10 NOK/MWh")
    print()
    
    # Add plants - EXACT from SINTEF  
    print("4. Adding plants...")
    
    plant1 = shop.model.plant.add_object('Plant1')
    plant1.outlet_line.set(672)  # masl
    plant1.main_loss.set([0.0])
    plant1.penstock_loss.set([0.001])
    plant1.mip_flag.set(1)
    
    plant2 = shop.model.plant.add_object('Plant2')
    plant2.outlet_line.set(586)  # masl
    plant2.main_loss.set([0.0])
    plant2.penstock_loss.set([0.0001, 0.0002])
    plant2.mip_flag.set(1)
    
    print("   ✓ Plant1: outlet 672 masl")
    print("   ✓ Plant2: outlet 586 masl")
    print()
    
    # Add generators - EXACT from SINTEF
    print("5. Adding generators...")
    
    # Plant 1 - Generator 1
    p1g1 = shop.model.generator.add_object('Plant1_Generator1')
    p1g1.connect_to(plant1)
    p1g1.penstock.set(1)
    p1g1.p_min.set(60)  # MW
    p1g1.p_max.set(120)  # MW
    p1g1.p_nom.set(120)  # MW
    p1g1.startcost.set(300)
    
    # EXACT efficiency curves from SINTEF
    p1g1.gen_eff_curve.set(pd.Series([100, 100], index=[60, 120]))
    
    # EXACT turbine efficiency curves from SINTEF documentation
    p1g1.turb_eff_curves.set([
        pd.Series(
            [85.87, 87.03, 88.09, 89.05, 89.94, 90.77, 91.55, 92.26, 92.82, 93.11, 93.22, 93.04, 92.66, 92.17],
            index=[28.12, 30.45, 32.78, 35.11, 37.45, 39.78, 42.11, 44.44, 46.77, 49.1, 51.43, 53.76, 56.1, 58.83],
            name=170
        ),
        pd.Series(
            [86.73, 87.90, 88.97, 89.95, 90.84, 91.68, 92.46, 93.19, 93.75, 94.04, 94.15, 93.97, 93.58, 93.10],
            index=[28.12, 30.45, 32.78, 35.11, 37.45, 39.78, 42.11, 44.44, 46.77, 49.1, 51.43, 53.76, 56.1, 58.83],
            name=200
        ),
        pd.Series(
            [87.59, 88.77, 89.85, 90.84, 91.74, 92.59, 93.38, 94.11, 94.68, 94.97, 95.08, 94.90, 94.51, 94.02],
            index=[28.12, 30.45, 32.78, 35.11, 37.45, 39.78, 42.11, 44.44, 46.77, 49.1, 51.43, 53.76, 56.1, 58.83],
            name=230
        )
    ])
    
    # Plant 1 - Generator 2 (same as G1)
    p1g2 = shop.model.generator.add_object('Plant1_Generator2')
    p1g2.connect_to(plant1)
    p1g2.penstock.set(1)
    p1g2.p_min.set(60)
    p1g2.p_max.set(120)
    p1g2.p_nom.set(120)
    p1g2.startcost.set(300)
    p1g2.gen_eff_curve.set(pd.Series([100, 100], index=[60, 120]))
    p1g2.turb_eff_curves.set(p1g1.turb_eff_curves.get())  # Same as G1
    
    # Plant 2 - Generator 1 (large unit)
    p2g1 = shop.model.generator.add_object('Plant2_Generator1')
    p2g1.connect_to(plant2)
    p2g1.penstock.set(1)
    p2g1.p_min.set(100)  # MW
    p2g1.p_max.set(180)  # MW
    p2g1.p_nom.set(180)  # MW
    p2g1.startcost.set(300)
    p2g1.gen_eff_curve.set(pd.Series([100, 100], index=[100, 180]))
    
    # EXACT turbine efficiency for Plant2 Generator1
    p2g1.turb_eff_curves.set([
        pd.Series(
            [92.72, 93.26, 93.73, 94.14, 94.48, 94.75, 94.96, 95.10, 95.18, 95.19, 95.13, 95.01, 94.82, 94.52],
            index=[126.54, 137.03, 147.51, 158, 168.53, 179.01, 189.5, 199.98, 210.47, 220.95, 231.44, 241.92, 252.45, 264.74],
            name=60
        )
    ])
    
    # Plant 2 - Generators 2, 3, 4 (smaller identical units)
    for i in [2, 3, 4]:
        gen = shop.model.generator.add_object(f'Plant2_Generator{i}')
        gen.connect_to(plant2)
        gen.penstock.set(2)
        gen.p_min.set(30)  # MW
        gen.p_max.set(55)  # MW
        gen.p_nom.set(55)  # MW
        gen.startcost.set(300)
        gen.gen_eff_curve.set(pd.Series([100, 100], index=[30, 55]))
        
        # EXACT turbine efficiency for small units
        gen.turb_eff_curves.set([
            pd.Series(
                [83.87, 85.19, 86.38, 87.44, 88.36, 89.14, 89.79, 90.30, 90.68, 90.92, 91.03, 91.01, 90.84, 90.48],
                index=[40.82, 44.2, 47.58, 50.97, 54.36, 57.75, 61.13, 64.51, 67.89, 71.27, 74.66, 78.04, 81.44, 85.4],
                name=60
            )
        ])
    
    print("   ✓ Plant1: 2 generators (60-120 MW each)")
    print("   ✓ Plant2: 1 large (100-180 MW) + 3 small (30-55 MW)")
    print()
    
    # Connect topology - EXACT from SINTEF
    print("6. Connecting topology...")
    plant1.connect_to(rsv1)
    plant2.connect_to(rsv2)
    print("   ✓ Reservoir1 → Plant1")
    print("   ✓ Reservoir2 → Plant2")
    print()
    
    # Add market with EXACT 72-hour prices from SINTEF
    print("7. Creating market with EXACT SINTEF prices (72 hours)...")
    da = shop.model.market.add_object('Day_ahead')
    
    # EXACT price data from SINTEF documentation
    prices = [
        32.992, 31.122, 29.312, 28.072, 30.012, 33.362, 42.682, 74.822, 77.732, 62.332,
        55.892, 46.962, 42.582, 40.942, 39.212, 39.142, 41.672, 46.922, 37.102, 32.992,
        31.272, 29.752, 28.782, 28.082, 27.242, 26.622, 25.732, 25.392, 25.992, 27.402,
        28.942, 32.182, 33.082, 32.342, 30.912, 30.162, 30.062, 29.562, 29.462, 29.512,
        29.672, 30.072, 29.552, 28.862, 28.412, 28.072, 27.162, 25.502, 26.192, 25.222,
        24.052, 23.892, 23.682, 26.092, 28.202, 30.902, 31.572, 31.462, 31.172, 30.912,
        30.572, 30.602, 30.632, 31.062, 32.082, 36.262, 34.472, 32.182, 31.492, 30.732,
        29.712, 28.982
    ]
    
    price_index = [starttime + pd.Timedelta(hours=i) for i in range(72)]
    da.sale_price.set(pd.DataFrame(prices, index=price_index))
    da.buy_price.set(da.sale_price.get() + 0.002)
    da.max_buy.set(pd.Series([9999], [starttime]))
    da.max_sale.set(pd.Series([9999], [starttime]))
    da.load.set(pd.Series([0], [starttime]))
    
    print(f"   ✓ Market configured")
    print(f"     Price range: {min(prices):.2f} - {max(prices):.2f} EUR/MWh")
    print(f"     Average: {sum(prices)/len(prices):.2f} EUR/MWh")
    print()
    
    # RUN OPTIMIZATION - EXACT from SINTEF
    print("=" * 80)
    print("RUNNING OPTIMIZATION (EXACT SINTEF METHOD)")
    print("=" * 80)
    print()
    
    print("Setting 'full' code flag...")
    shop.set_code(['full'], [])
    print("✓ Full optimization mode")
    print()
    
    print("Starting 5 full iterations...")
    try:
        shop.start_sim([], ['5'])
        print("✓ Full iterations complete!")
    except Exception as e:
        print(f"✗ Optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("Setting 'incremental' code flag...")
    shop.set_code(['incremental'], [])
    print("✓ Incremental mode")
    print()
    
    print("Starting 3 incremental iterations...")
    try:
        shop.start_sim([], ['3'])
        print("✓ Incremental iterations complete!")
    except Exception as e:
        print(f"✗ Optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("=" * 80)
    print("✓✓✓ OPTIMIZATION SUCCESSFUL! ✓✓✓")
    print("=" * 80)
    print()
    
    # Extract results for comparison
    print("RESULTS FOR COMPARISON WITH SINTEF:")
    print("-" * 80)
    
    # Plant production
    p1_prod = plant1.production.get()
    p2_prod = plant2.production.get()
    total_prod = p1_prod + p2_prod
    
    # Generator production per unit
    p1g1_prod = p1g1.production.get()
    p1g2_prod = p1g2.production.get()
    p2g1_prod = p2g1.production.get()
    
    # Reservoir levels
    rsv1_head = rsv1.head.get()
    rsv2_head = rsv2.head.get()
    
    print(f"\n📊 Energy Production (3 days):")
    print(f"  Plant1 total: {p1_prod.sum():.0f} MWh")
    print(f"  Plant2 total: {p2_prod.sum():.0f} MWh")
    print(f"  TOTAL: {total_prod.sum():.0f} MWh")
    print(f"  Average power: {total_prod.mean():.1f} MW")
    print(f"  Peak power: {total_prod.max():.1f} MW")
    
    print(f"\n💰 Economics:")
    revenue = (total_prod * pd.Series(prices, index=total_prod.index[:len(prices)])).sum()
    print(f"  Total revenue: {revenue:.0f} EUR")
    print(f"  Average price: {sum(prices)/len(prices):.2f} EUR/MWh")
    print(f"  Energy value: {revenue/total_prod.sum():.2f} EUR/MWh")
    
    print(f"\n💧 Reservoir Levels:")
    print(f"  Reservoir1: {rsv1_head.iloc[0]:.1f} → {rsv1_head.iloc[-1]:.1f} masl")
    print(f"  Reservoir2: {rsv2_head.iloc[0]:.1f} → {rsv2_head.iloc[-1]:.1f} masl")
    
    print(f"\n🔧 Generator Dispatch (first 24 hours):")
    print(f"  Plant1_Gen1 max: {p1g1_prod.iloc[:24].max():.1f} MW")
    print(f"  Plant1_Gen2 max: {p1g2_prod.iloc[:24].max():.1f} MW")
    print(f"  Plant2_Gen1 max: {p2g1_prod.iloc[:24].max():.1f} MW")
    
    # Save for comparison
    output_dir = project_root / 'data' / 'output' / 'results'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_df = pd.DataFrame({
        'Plant1_MW': p1_prod.values,
        'Plant2_MW': p2_prod.values,
        'Total_MW': total_prod.values,
        'Reservoir1_masl': rsv1_head.values,
        'Reservoir2_masl': rsv2_head.values,
    }, index=total_prod.index)
    
    # Add prices (match length)
    price_vals = prices.copy()
    while len(price_vals) < len(results_df):
        price_vals.append(price_vals[-1])
    results_df['Price_EUR_MWh'] = price_vals[:len(results_df)]
    
    csv_path = output_dir / 'sintef_exact_replica_3days.csv'
    results_df.to_csv(csv_path)
    
    print()
    print("=" * 80)
    print("COMPARISON READY!")
    print("=" * 80)
    print(f"\n✓ Results saved: {csv_path.name}")
    print()
    print("📋 Compare these results with SINTEF documentation:")
    print("   https://docs.shop.sintef.energy/examples/basic/basic.html")
    print()
    print("🎯 Key comparison points:")
    print("  • Total energy generated (should match SINTEF)")
    print("  • Reservoir end levels (guided by water values)")
    print("  • Generation patterns vs. price peaks")
    print("  • Plant dispatch optimization")
    print()
    print("=" * 80)
    
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
