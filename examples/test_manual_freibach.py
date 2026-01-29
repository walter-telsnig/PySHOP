"""
Diagnostic: Manually defined Freibach topology (No YAML)
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager

def main():
    print("=" * 70)
    print("DIAGNOSTIC: MANUAL FREIBACH (NO YAML)")
    print("=" * 70)
    
    shop_mgr = ShopManager(silent=False)
    model = shop_mgr.get_model()
    
    starttime = pd.Timestamp('2026-01-29 00:00:00')
    endtime = pd.Timestamp('2026-02-12 00:00:00')
    shop_mgr.set_time(starttime, endtime)
    
    # Reservoirs
    r1 = model.reservoir.add_object('Freibach')
    r1.max_vol.set(5.25)
    r1.lrl.set(705); r1.hrl.set(729.2)
    r1.vol_head.set(pd.Series([705, 715, 730], index=[0, 2.5, 5.86]))
    r1.start_vol.set(2.5)
    r1.energy_value_input.set(50)
    r1.inflow.set(pd.Series([1.5], index=[starttime]))
    
    r2 = model.reservoir.add_object('DrauWest')
    r2.max_vol.set(1000)
    r2.lrl.set(397); r2.hrl.set(397.5)
    r2.vol_head.set(pd.Series([396.9, 397.6], index=[0, 1000]))
    r2.start_vol.set(571)
    r2.energy_value_input.set(50)
    
    # Plant
    p = model.plant.add_object('Freibach_Plant')
    p.outlet_line.set(410)
    p.main_loss.set([0.0])
    p.penstock_loss.set([0.0, 0.0])
    
    # Gen1
    g1 = model.generator.add_object('Gen1')
    g1.connect_to(p)
    g1.penstock.set(1)
    g1.p_min.set(7); g1.p_max.set(17); g1.p_nom.set(17)
    g1.gen_eff_curve.set(pd.Series([95, 97], index=[7, 17]))
    g1.turb_eff_curves.set([pd.Series([85, 85], index=[2.2, 6.0], name=324)])
    
    # Topology
    r1.connect_to(p)
    p.connect_to(r2)
    
    # Market
    market = model.market.add_object('Market')
    prices = pd.Series([40]*337, index=pd.date_range(starttime, periods=337, freq='h'))
    market.sale_price.set(prices)
    market.buy_price.set(prices)
    
    print("Running optimization...")
    shop_mgr.run_optimization()
    print("SUCCESS!")

if __name__ == "__main__":
    main()
