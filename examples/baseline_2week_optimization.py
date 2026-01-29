"""
SINTEF 2-Week Optimization with Endpoint Management
Based on proven working SINTEF example, extended to 2 weeks

This is YOUR WORKING BASELINE for SHOP optimization!
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

from pyshop import ShopSession


def create_14day_prices(starttime):
    """Create 2 weeks of realistic price data (336 hours)"""
    prices = []
    for day in range(14):
        for hour in range(24):
            # Daily pattern with weekly variation
            if hour >= 7 and hour <= 9 or hour >= 17 and hour <= 20:
                base = 55.0  # Peak
            elif hour >= 0 and hour <= 6:
                base = 30.0  # Valley
            else:
                base = 42.0  # Mid
            
            # Weekend lower prices
            if day % 7 in [5, 6]:  # Weekend
                base *= 0.85
            
            # Add randomness
            price = base + np.random.uniform(-5, 5)
            prices.append(max(price, 20.0))
    
    time_index = [starttime + pd.Timedelta(hours=i) for i in range(336)]
    return pd.DataFrame(prices, index=time_index)


def main():
    print("=" * 80)
    print("SINTEF 2-WEEK OPTIMIZATION - YOUR WORKING BASELINE")
    print("=" * 80)
    print("Based on: https://docs.shop.sintef.energy/examples/basic/basic.html")
    print("Extended to: 2 weeks with endpoint management")
    print()
    
    # Setup paths
    output_dir = project_root / 'data' / 'output'
    plots_dir = output_dir / 'plots'
    results_dir = output_dir / 'results'
    plots_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Create SHOP session
    print("1. Creating SHOP session...")
    licence_dir = project_root / "Licence"
    shop = ShopSession(license_path=str(licence_dir), solver_path=str(licence_dir))
    print(f"   ✓ {shop.shop_api.GetVersionString()}")
    print()
    
    # Set time - 2 WEEKS!
    print("2. Setting time resolution (2 weeks)...")
    starttime = pd.Timestamp('2026-01-29 00:00:00')
    endtime = pd.Timestamp('2026-02-12 00:00:00')  # 14 days
    shop.set_time_resolution(
        starttime=starttime,
        endtime=endtime,
        timeunit="hour",
        timeresolution=pd.Series(index=[starttime], data=[1])
    )
    print(f"   ✓ Period: {starttime} to {endtime}")
    print(f"   ✓ Duration: 14 days (336 hours)")
    print()
    
    # Add reservoirs with ENDPOINT MANAGEMENT
    print("3. Adding reservoirs with endpoint water values...")
    
    # Reservoir 1
    shop.model.reservoir.add_object('Reservoir1')
    rsv1 = shop.model.reservoir.Reservoir1
    rsv1.max_vol.set(20)
    rsv1.lrl.set(1000)
    rsv1.hrl.set(1010)
    rsv1.vol_head.set(pd.Series([1000,1010,1011], index=[0,20,22]))
    rsv1.flow_descr.set(pd.Series([0,1000], index=[1010,1011]))
    rsv1.energy_value_input.set(50.0)  # EUR/MWh - ENDPOINT VALUE!
    
    # Reservoir 2
    shop.model.reservoir.add_object('Reservoir2')
    rsv2 = shop.model.reservoir.Reservoir2
    rsv2.max_vol.set(39)
    rsv2.lrl.set(860)
    rsv2.hrl.set(905)
    rsv2.vol_head.set(pd.Series([860,906,907], index=[0,39,41.66]))
    rsv2.energy_value_input.set(45.0)  # EUR/MWh
    
    # Reservoir 3
    shop.model.reservoir.add_object('Reservoir3')
    rsv3 = shop.model.reservoir.Reservoir3
    rsv3.max_vol.set(97.5)
    rsv3.lrl.set(650)
    rsv3.hrl.set(679)
    rsv3.vol_head.set(pd.Series([650,679,680], index=[0,97.5,104.15]))
    rsv3.inflow.set(pd.Series([60], index=[starttime]))  # Constant inflow
    rsv3.energy_value_input.set(40.0)  # EUR/MWh
    
    print("   ✓ 3 reservoirs with endpoint water values")
    print(f"     Rsv1: {rsv1.energy_value_input.get()} EUR/MWh")
    print(f"     Rsv2: {rsv2.energy_value_input.get()} EUR/MWh")
    print(f"     Rsv3: {rsv3.energy_value_input.get()} EUR/MWh")
    print()
    
    # Add plants (same as SINTEF)
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
    
    # Add generators (simplified for clarity)
    print("5. Adding generators...")
    
    # Plant 1 - Generator 1
    shop.model.generator.add_object('G11')
    g11 = shop.model.generator.G11
    g11.penstock.set(1)
    g11.p_min.set(60)
    g11.p_max.set(120)
    g11.p_nom.set(120)
    g11.startcost.set(300)
    g11.gen_eff_curve.set(pd.Series([100,100], index=[60,120]))
    g11.turb_eff_curves.set([pd.Series([90,90], index=[30,60], name=200)])
    
    # Plant 1 - Generator 2  
    shop.model.generator.add_object('G12')
    g12 = shop.model.generator.G12
    g12.penstock.set(1)
    g12.p_min.set(60)
    g12.p_max.set(120)
    g12.p_nom.set(120)
    g12.startcost.set(300)
    g12.gen_eff_curve.set(pd.Series([100,100], index=[60,120]))
    g12.turb_eff_curves.set([pd.Series([90,90], index=[30,60], name=200)])
    
    # Plant 2 - Generator 1 (larger)
    shop.model.generator.add_object('G21')
    g21 = shop.model.generator.G21
    g21.penstock.set(1)
    g21.p_min.set(100)
    g21.p_max.set(180)
    g21.p_nom.set(180)
    g21.startcost.set(300)
    g21.gen_eff_curve.set(pd.Series([100,100], index=[100,180]))
    g21.turb_eff_curves.set([pd.Series([92,92], index=[127,265], name=60)])
    
    # Plant 2 - Generators 2,3,4 (smaller units)
    for i in [2, 3, 4]:
        shop.model.generator.add_object(f'G2{i}')
        gen = getattr(shop.model.generator, f'G2{i}')
        gen.penstock.set(2)
        gen.p_min.set(30)
        gen.p_max.set(55)
        gen.p_nom.set(55)
        gen.startcost.set(300)
        gen.gen_eff_curve.set(pd.Series([100,100], index=[30,55]))
        gen.turb_eff_curves.set([pd.Series([85,85], index=[41,85], name=60)])
    
    print("   ✓ 6 generators added (2 at Plant1, 4 at Plant2)")
    print()
    
    # Add gate
    print("6. Adding gate...")
    shop.model.gate.add_object('Flow_gate')
    gate = shop.model.gate.Flow_gate
    gate.max_flow.set(pd.Series([50], index=[starttime]))
    print("   ✓ 1 gate added")
    print()
    
    # Connect topology
    print("7. Connecting topology...")
    rsv1.connect_to(gate)
    gate.connect_to(rsv2)
    rsv2.connect_to(p1)
    rsv3.connect_to(p2)
    p1.connect_to(rsv3)
    g11.connect_to(p1)
    g12.connect_to(p1)
    g21.connect_to(p2)
    shop.model.generator.G22.connect_to(p2)
    shop.model.generator.G23.connect_to(p2)
    shop.model.generator.G24.connect_to(p2)
    print("   ✓ All connections established")
    print()
    
    # Set initial conditions
    print("8. Setting initial reservoir levels...")
    rsv1.start_head.set(1006)
    rsv2.start_head.set(900)
    rsv3.start_head.set(670)
    print("   ✓ Initial conditions set")
    print()
    
    # Add market with 2-week prices
    print("9. Creating market with 2-week price data...")
    shop.model.market.add_object('DayAhead')
    da = shop.model.market.DayAhead
    
    prices_df = create_14day_prices(starttime)
    da.sale_price.set(prices_df)
    da.buy_price.set(prices_df + 0.002)
    da.max_buy.set(pd.Series([9999], [starttime]))
    da.max_sale.set(pd.Series([9999], [starttime]))
    da.load.set(pd.Series([0], [starttime]))
    
    print(f"   ✓ Market configured")
    print(f"     Price range: {prices_df.values.min():.1f} - {prices_df.values.max():.1f} EUR/MWh")
    print(f"     Average: {prices_df.values.mean():.1f} EUR/MWh")
    print()
    
    # RUN OPTIMIZATION
    print("=" * 80)
    print("RUNNING 2-WEEK OPTIMIZATION")
    print("=" * 80)
    print()
    
    print("Setting optimization flags...")
    shop.set_code(['full'], [])
    print("✓ Full optimization mode")
    print()
    
    print("Starting optimization (may take 1-2 minutes for 2 weeks)...")
    try:
        shop.start_sim([], ['5'])
        print("✓ Full iterations complete!")
        
        shop.set_code(['incremental'], [])
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
    
    # Extract results
    print("Extracting results...")
    
    # Reservoir levels
    r1_head = rsv1.head.get()
    r2_head = rsv2.head.get()
    r3_head = rsv3.head.get()
    
    # Generation
    g11_prod = g11.production.get()
    g12_prod = g12.production.get()
    g21_prod = g21.production.get()
    g22_prod = shop.model.generator.G22.production.get()
    g23_prod = shop.model.generator.G23.production.get()
    g24_prod = shop.model.generator.G24.production.get()
    
    total_prod = g11_prod + g12_prod + g21_prod + g22_prod + g23_prod + g24_prod
    
    # Market prices
    prices = da.sale_price.get()
    
    print("✓ All results extracted")
    print()
    
    # Calculate statistics
    total_energy = total_prod.sum()  # MWh
    revenue = (total_prod * prices.values.flatten()).sum()
    avg_price = prices.values.mean()
    
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"\n📊 Energy Production:")
    print(f"  Total generation: {total_energy:.0f} MWh")
    print(f"  Average power: {total_prod.mean():.1f} MW")
    print(f"  Peak power: {total_prod.max():.1f} MW")
    
    print(f"\n💰 Economics:")
    print(f"  Total revenue: {revenue:.0f} EUR")
    print(f"  Average price: {avg_price:.2f} EUR/MWh")
    print(f"  Energy value: {revenue/total_energy:.2f} EUR/MWh")
    
    print(f"\n💧 Reservoir Levels:")
    print(f"  Reservoir 1: {r1_head.iloc[0]:.1f} → {r1_head.iloc[-1]:.1f} masl")
    print(f"  Reservoir 2: {r2_head.iloc[0]:.1f} → {r2_head.iloc[-1]:.1f} masl") 
    print(f"  Reservoir 3: {r3_head.iloc[0]:.1f} → {r3_head.iloc[-1]:.1f} masl")
    print()
    
    # Save CSV
    print("Saving results...")
    
    # Determine actual result length
    n = len(total_prod)
    
    # Create DataFrame with all arrays same length
    results_df = pd.DataFrame({
        'Reservoir1_masl': r1_head.values[:n],
        'Reservoir2_masl': r2_head.values[:n],
        'Reservoir3_masl': r3_head.values[:n],
        'G11_MW': g11_prod.values[:n],
        'G12_MW': g12_prod.values[:n],
        'G21_MW': g21_prod.values[:n],
        'G22_MW': g22_prod.values[:n],
        'G23_MW': g23_prod.values[:n],
        'G24_MW': g24_prod.values[:n],
        'Total_MW': total_prod.values[:n],
    }, index=total_prod.index[:n])
    
    # Add prices (extend if needed)
    price_vals = list(prices.values.flatten())
    while len(price_vals) < n:
        price_vals.append(price_vals[-1] if price_vals else 40.0)
    results_df['Price_EUR_MWh'] = price_vals[:n]
    
    csv_path = results_dir / 'sintef_baseline_2weeks.csv'
    results_df.to_csv(csv_path)
    print(f"✓ CSV saved: {csv_path.name}")
    
    # Create plots
    fig, axes = plt.subplots(3, 1, figsize=(16, 12))
    fig.suptitle('SINTEF Baseline - 2 Week Optimization Results', fontsize=16, fontweight='bold')
    
    # Plot 1: Reservoirs
    ax1 = axes[0]
    ax1.plot(r1_head.index, r1_head.values, 'b-', linewidth=2, label='Reservoir 1', alpha=0.8)
    ax1.plot(r2_head.index, r2_head.values, 'g-', linewidth=2, label='Reservoir 2', alpha=0.8)
    ax1.plot(r3_head.index, r3_head.values, 'r-', linewidth=2, label='Reservoir 3', alpha=0.8)
    ax1.axhline(y=r1_head.iloc[0], color='b', linestyle='--', alpha=0.3)
    ax1.axhline(y=r2_head.iloc[0], color='g', linestyle='--', alpha=0.3)
    ax1.axhline(y=r3_head.iloc[0], color='r', linestyle='--', alpha=0.3)
    ax1.set_ylabel('Water Level (masl)', fontweight='bold', fontsize=11)
    ax1.set_title('Reservoir Levels (Endpoint Water Values Guide Final Levels)', fontweight='bold', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Generation
    ax2 = axes[1]
    ax2.fill_between(total_prod.index, 0, total_prod.values, alpha=0.6, color='green', label='Total Generation')
    ax2.plot(total_prod.index, total_prod.values, 'darkgreen', linewidth=1.5)
    ax2.set_ylabel('Power (MW)', fontweight='bold', fontsize=11)
    ax2.set_title('Generation Dispatch', fontweight='bold', fontsize=12)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Prices
    ax3 = axes[2]
    ax3.plot(prices.index, prices.values, 'orange', linewidth=1.5, label='Market Price')
    ax3.axhline(y=avg_price, color='red', linestyle='--', linewidth=1, alpha=0.5, label=f'Average: {avg_price:.1f} EUR/MWh')
    # Add water value references
    ax3.axhline(y=50, color='b', linestyle=':', alpha=0.4, label='Rsv1 water value')
    ax3.axhline(y=45, color='g', linestyle=':', alpha=0.4, label='Rsv2 water value')
    ax3.axhline(y=40, color='r', linestyle=':', alpha=0.4, label='Rsv3 water value')
    ax3.set_ylabel('Price (EUR/MWh)', fontweight='bold', fontsize=11)
    ax3.set_xlabel('Time', fontweight='bold', fontsize=11)
    ax3.set_title('Market Prices vs Endpoint Water Values', fontweight='bold', fontsize=12)
    ax3.legend(loc='best', fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    for ax in axes:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plot_path = plots_dir / 'sintef_baseline_2weeks.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved: {plot_path.name}")
    plt.close()
    
    print()
    print("=" * 80)
    print("✓✓✓ 2-WEEK OPTIMIZATION COMPLETE ✓✓✓")
    print("=" * 80)
    print()
    print("🎯 Key Features Demonstrated:")
    print("  ✓ 2-week optimization period (336 hours)")
    print("  ✓ Endpoint management with water values")
    print("  ✓ Multiple reservoirs and generators")
    print("  ✓ Realistic price patterns")
    print("  ✓ Complete results extraction")
    print("  ✓ Automated visualization")
    print()
    print("📁 Output Files:")
    print(f"  {csv_path}")
    print(f"  {plot_path}")
    print()
    print("🚀 This is YOUR WORKING BASELINE!")
    print("   Use this as the foundation for future work.")
    print("   Freibach topology is documented and ready when you need it.")
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
