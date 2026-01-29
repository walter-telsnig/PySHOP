"""
Freibach Generator-Only Optimization - SIMPLIFIED VERSION

This script runs optimization WITHOUT pumps for reliable results.
Perfect for learning SHOP optimization basics.

Uses real Freibach topology data but simplified to generators only.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager
from model_builder import build_model_from_yaml


def create_prices(start, end, freq='h'):
    """Create realistic hourly price pattern"""
    time_index = pd.date_range(start, end, freq=freq, inclusive='left')
    prices = []
    
    for dt in time_index:
        hour = dt.hour
        # Peak hours: higher prices
        if 7 <= hour <= 9 or 17 <= hour <= 20:
            base = 55.0
        elif 0 <= hour <= 6:
            base = 30.0  # Night valley
        else:
            base = 42.0
        
        price = base + np.random.uniform(-3, 3)
        prices.append(max(price, 25.0))
    
    return pd.Series(prices, index=time_index)


def main():
    print("=" * 80)
    print("FREIBACH GENERATOR-ONLY OPTIMIZATION (Simplified)")
    print("=" * 80)
    print("Real topology, NO pumps - Stable optimization for learning")
    print()
    
    # Paths
    config_dir = project_root / 'config'
    output_dir = project_root / 'data' / 'output'
    plots_dir = output_dir / 'plots'
    results_dir = output_dir / 'results'
    
    plots_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    topology_file = config_dir / 'Freibach.yaml'
    # topology_file = config_dir / 'Freibach_simple.yaml'
    
    # Step 1: Create SHOP session
    print("STEP 1: Creating SHOP Session")
    print("-" * 80)
    shop_mgr = ShopManager(silent=False)
    model = shop_mgr.get_model()
    print("✓ Session created\n")
    
    # Step 2: Set time
    print("STEP 2: Time Period")
    print("-" * 80)
    starttime = "2026-01-29 00:00:00"
    endtime = "2026-02-12 00:00:00"
    shop_mgr.set_time(starttime, endtime, timeresolution=1, timeunit='hour')
    print(f"✓ 2 weeks: {starttime} to {endtime}\n")
    
    # Step 3: Build model
    print("STEP 3: Building Simplified Topology")
    print("-" * 80)
    build_model_from_yaml(model, topology_file)
    print(f"✓ Loaded: {topology_file.name}")
    print(f"  Reservoirs: {', '.join(model.reservoir.get_object_names())}")
    print(f"  Generators: {', '.join(model.generator.get_object_names())}")
    print(f"  Pumps: None (simplified version)")
    print()
    
    # Step 4: Set inflow
    print("STEP 4: Inflow Data")
    print("-" * 80)
    time_index = pd.date_range(starttime, periods=337, freq='h')
    inflow_upper = pd.Series([1.5] * 337, index=time_index)
    model.reservoir.Freibach.inflow.set(inflow_upper)
    
    inflow_lower = pd.Series([0.0] * 337, index=time_index)
    model.reservoir.DrauWest.inflow.set(inflow_lower)
    print(f"✓ Freibach: 1.5 m³/s, DrauWest: 0 m³/s\n")
    
    # Step 5: Create market
    print("STEP 5: Market & Prices")
    print("-" * 80)
    market = model.market.add_object("SpotMarket")
    prices = create_prices(starttime, endtime, freq='h')
    market.sale_price.set(prices)
    market.buy_price.set(prices)
    start_ts = pd.to_datetime(time_index[0])
    market.max_buy.set(pd.Series([9999], [start_ts]))
    market.max_sale.set(pd.Series([9999], [start_ts]))
    market.load.set(pd.Series([0], [start_ts]))
    print(f"✓ Price range: {prices.min():.1f} - {prices.max():.1f} EUR/MWh")
    print(f"✓ Average: {prices.mean():.1f} EUR/MWh\n")
    
    # Step 6: RUN OPTIMIZATION
    print("=" * 80)
    print("STEP 6: RUNNING OPTIMIZATION")
    print("=" * 80)
    print("Starting SHOP optimization sequence (full + incremental)...")
    print()
    
    try:
        shop_mgr.run_optimization(full_iterations=5, incremental_iterations=3)
        print("\n" + "=" * 80)
        print("✓ OPTIMIZATION SUCCESSFUL!")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 7: Extract results
    print("STEP 7: Extracting Results")
    print("-" * 80)
    
    # Get results
    upper_head = model.reservoir.Freibach.head.get()
    lower_head = model.reservoir.DrauWest.head.get()
    upper_vol = model.reservoir.Freibach.storage.get()
    
    gen1_prod = model.generator.Gen1.production.get()
    gen2_prod = model.generator.Gen2.production.get()
    total_gen = gen1_prod + gen2_prod
    
    gen1_discharge = model.generator.Gen1.discharge.get()
    gen2_discharge = model.generator.Gen2.discharge.get()
    
    print(f"✓ Reservoir levels extracted")
    print(f"  Freibach: {upper_head.min():.2f} - {upper_head.max():.2f} masl")
    print(f"  Storage: {upper_vol.min():.2f} - {upper_vol.max():.2f} Mm³")
    print(f"✓ Generation extracted")
    print(f"  Total: 0 - {total_gen.max():.2f} MW")
    print(f"  Average: {total_gen.mean():.2f} MW")
    print()
    
    # Calculate statistics
    total_energy = total_gen.sum()  # MWh
    revenue = (total_gen * prices).sum()  # EUR
    avg_price = prices.mean()
    
    print("Energy & Economics:")
    print(f"  Total generation: {total_energy:.0f} MWh")
    print(f"  Revenue: {revenue:.0f} EUR")
    print(f"  Average value: {revenue/total_energy:.2f} EUR/MWh")
    print()
    
    # Step 8: Save results
    print("STEP 8: Saving Results")
    print("-" * 80)
    
    # Save CSV
    results_df = pd.DataFrame({
        'Freibach_head_masl': upper_head,
        'Freibach_storage_Mm3': upper_vol,
        'DrauWest_head_masl': lower_head,
        'Gen1_MW': gen1_prod,
        'Gen2_MW': gen2_prod,
        'Total_Gen_MW': total_gen,
        'Gen1_discharge_m3s': gen1_discharge,
        'Gen2_discharge_m3s': gen2_discharge,
        'Price_EUR_MWh': prices
    })
    
    csv_path = results_dir / 'freibach_simple_2weeks.csv'
    results_df.to_csv(csv_path)
    print(f"✓ CSV saved: {csv_path.name}")
    
    # Create plots
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle('Freibach Generator-Only - 2 Week Results', fontsize=16, fontweight='bold')
    
    # Plot 1: Reservoir
    axes[0].plot(upper_vol.index, upper_vol.values, 'b-', linewidth=2, label='Storage')
    axes[0].axhline(y=upper_vol.iloc[0], color='gray', linestyle='--', alpha=0.5, label='Start')
    axes[0].axhline(y=upper_vol.iloc[-1], color='orange', linestyle='--', alpha=0.5, label='End')
    axes[0].set_ylabel('Storage (Mm³)', fontweight='bold')
    axes[0].set_title('Freibach Reservoir Storage', fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Generation
    axes[1].fill_between(total_gen.index, 0, total_gen.values, alpha=0.6, color='green', label='Generation')
    axes[1].set_ylabel('Power (MW)', fontweight='bold')
    axes[1].set_title('Generation Dispatch', fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Prices
    axes[2].plot(prices.index, prices.values, 'orange', linewidth=1.5, label='Spot Price')
    axes[2].set_ylabel('Price (EUR/MWh)', fontweight='bold')
    axes[2].set_xlabel('Time', fontweight='bold')
    axes[2].set_title('Market Prices', fontweight='bold')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    for ax in axes:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plot_path = plots_dir / 'freibach_simple_2weeks.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {plot_path.name}")
    plt.close()
    
    print()
    print("=" * 80)
    print("SUCCESS! OPTIMIZATION COMPLETED")
    print("=" * 80)
    print()
    print("📊 Summary:")
    print(f"  System: Freibach (generator-only)")
    print(f"  Period: 2 weeks (336 hours)")
    print(f"  Generation: {total_energy:.0f} MWh")
    print(f"  Revenue: {revenue:.0f} EUR")
    print(f"  Start storage: {upper_vol.iloc[0]:.2f} Mm³")
    print(f"  End storage: {upper_vol.iloc[-1]:.2f} Mm³")
    print(f"  Storage change: {upper_vol.iloc[-1] - upper_vol.iloc[0]:.2f} Mm³")
    print()
    print("📁 Files:")
    print(f"  {csv_path}")
    print(f"  {plot_path}")
    print()
    print("🎯 Next: Add pumps back for full pump-turbine optimization!")
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
