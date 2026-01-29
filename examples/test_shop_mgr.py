"""
Diagnostic script: SINTEF topology using ShopManager
"""
import sys
from pathlib import Path
import pandas as pd

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from shop_session import ShopManager

def main():
    print("=" * 70)
    print("DIAGNOSTIC: SINTEF VIA SHOPMANAGER")
    print("=" * 70)
    
    shop_mgr = ShopManager(silent=False)
    model = shop_mgr.get_model()
    
    starttime = pd.Timestamp('2018-01-23 00:00:00')
    endtime = pd.Timestamp('2018-01-26 00:00:00')
    shop_mgr.set_time(starttime, endtime)
    
    # Rsv1
    rsv1 = model.reservoir.add_object('Reservoir1')
    rsv1.max_vol.set(39)
    rsv1.lrl.set(860)
    rsv1.hrl.set(905)
    rsv1.vol_head.set(pd.Series([860,906,907], index=[0,39,41.66]))
    rsv1.energy_value_input.set(30)
    rsv1.start_head.set(900)
    
    # Rsv2
    rsv2 = model.reservoir.add_object('Reservoir2')
    rsv2.max_vol.set(97.5)
    rsv2.lrl.set(650)
    rsv2.hrl.set(679)
    rsv2.vol_head.set(pd.Series([650,679,680], index=[0,97.5,104.15]))
    rsv2.inflow.set(pd.Series([60], index=[starttime]))
    rsv2.energy_value_input.set(10)
    rsv2.start_head.set(670)
    
    # Plants
    p1 = model.plant.add_object('Plant1')
    p1.outlet_line.set(672)
    p1.main_loss.set([0.0])
    p1.penstock_loss.set([0.001])
    
    p2 = model.plant.add_object('Plant2')
    p2.outlet_line.set(586)
    p2.main_loss.set([0.0])
    p2.penstock_loss.set([0.0001, 0.0002])
    
    # Gens
    g11 = model.generator.add_object('G11')
    g11.connect_to(p1)
    g11.p_min.set(60); g11.p_max.set(120); g11.p_nom.set(120)
    g11.gen_eff_curve.set(pd.Series([100,100], index=[60,120]))
    g11.turb_eff_curves.set([pd.Series([90,90], index=[30,60], name=200)])
    
    g21 = model.generator.add_object('G21')
    g21.connect_to(p2)
    g21.p_min.set(100); g21.p_max.set(180); g21.p_nom.set(180)
    g21.gen_eff_curve.set(pd.Series([100,100], index=[100,180]))
    g21.turb_eff_curves.set([pd.Series([92,92], index=[127,265], name=60)])
    
    # Topology
    rsv1.connect_to(p1)
    p1.connect_to(rsv2)
    rsv2.connect_to(p2)
    
    # Market
    market = model.market.add_object('Day_ahead')
    prices = pd.Series([40]*72, index=pd.date_range(starttime, periods=72, freq='h'))
    market.sale_price.set(prices)
    market.buy_price.set(prices)
    
    print("Running optimization...")
    shop_mgr.run_optimization()
    print("SUCCESS!")

if __name__ == "__main__":
    main()
