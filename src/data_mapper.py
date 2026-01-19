import pandas as pd
import os

def load_csv_to_series(file_path, value_col, timestamp_col='timestamp'):
    df = pd.read_csv(file_path)
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    return pd.Series(df[value_col].values, index=df[timestamp_col])

def map_input_data(shop, data_dir):
    # 1. Map Market Prices
    price_file = os.path.join(data_dir, 'market_price.csv')
    if os.path.exists(price_file):
        print(f"Mapping market prices from {price_file}...")
        price_series = load_csv_to_series(price_file, 'price')
        
        # Ensure market object exists
        market_name = "DayAhead"
        if market_name not in shop.model.market.get_object_names():
            market = shop.model.market.add_object(market_name)
        else:
            market = shop.model.market[market_name]
            
        market.max_buy.set(1000.0)
        market.max_sale.set(1000.0)
        market.sale_price.set(price_series)
        market.buy_price.set(price_series)

    # 2. Map Reservoir Inflows
    inflow_file = os.path.join(data_dir, 'inflow.csv')
    if os.path.exists(inflow_file):
        print(f"Mapping inflows from {inflow_file}...")
        df_inflow = pd.read_csv(inflow_file)
        df_inflow['timestamp'] = pd.to_datetime(df_inflow['timestamp'])
        
        for res_name in shop.model.reservoir.get_object_names():
            if res_name in df_inflow.columns:
                inflow_series = pd.Series(df_inflow[res_name].values, index=df_inflow['timestamp'])
                shop.model.reservoir[res_name].inflow.set(inflow_series)

    # 3. Map Initial Conditions
    init_file = os.path.join(data_dir, 'initial_conditions.csv')
    if os.path.exists(init_file):
        print(f"Mapping initial conditions from {init_file}...")
        df_init = pd.read_csv(init_file).iloc[0] # Take first row
        
        for res_name in shop.model.reservoir.get_object_names():
            start_vol_key = f"{res_name}_start_vol"
            wv_key = f"{res_name}_wv"
            
            if start_vol_key in df_init:
                shop.model.reservoir[res_name].start_vol.set(float(df_init[start_vol_key]))
            
            if wv_key in df_init:
                wv = float(df_init[wv_key])
                shop.model.reservoir[res_name].water_value_input.set([{'xy': [[0.0, wv]], 'ref': 0.0}])

    # 4. Map Availability
    avail_file = os.path.join(data_dir, 'availability.csv')
    if os.path.exists(avail_file):
        print(f"Mapping availability from {avail_file}...")
        df_avail = pd.read_csv(avail_file)
        df_avail['timestamp'] = pd.to_datetime(df_avail['timestamp'])
        
        # Generator availability (Invert: 1=Avail in CSV -> 0=Maint in SHOP)
        for gen_name in shop.model.generator.get_object_names():
            if gen_name in df_avail.columns:
                series = pd.Series(1 - df_avail[gen_name].values, index=df_avail['timestamp'])
                shop.model.generator[gen_name].maintenance_flag.set(series)
                
        # Pump availability (Invert: 1=Avail in CSV -> 0=Maint in SHOP)
        for pump_name in shop.model.pump.get_object_names():
            if pump_name in df_avail.columns:
                series = pd.Series(1 - df_avail[pump_name].values, index=df_avail['timestamp'])
                shop.model.pump[pump_name].maintenance_flag.set(series)

    # 5. Map Reservoir Constraints
    constr_file = os.path.join(data_dir, 'reservoir_constraints.csv')
    if os.path.exists(constr_file):
        print(f"Mapping reservoir constraints from {constr_file}...")
        df_constr = pd.read_csv(constr_file)
        df_constr['timestamp'] = pd.to_datetime(df_constr['timestamp'])
        
        for res_name in shop.model.reservoir.get_object_names():
            min_col = f"{res_name}_min"
            max_col = f"{res_name}_max"
            pen_col = f"{res_name}_penalty"
            
            if min_col in df_constr.columns:
                series = pd.Series(df_constr[min_col].values, index=df_constr['timestamp'])
                shop.model.reservoir[res_name].tactical_limit_min.set(series)
                
            if max_col in df_constr.columns:
                series = pd.Series(df_constr[max_col].values, index=df_constr['timestamp'])
                shop.model.reservoir[res_name].tactical_limit_max.set(series)

            # Map flags and costs for tactical limits
            try:
                if min_col in df_constr.columns:
                    shop.model.reservoir[res_name].tactical_limit_min_flag.set(1)
                if max_col in df_constr.columns:
                    shop.model.reservoir[res_name].tactical_limit_max_flag.set(1)
                
                if pen_col in df_constr.columns:
                    penalty_val = float(df_constr[pen_col].mean())
                    # In many SHOP versions, tactical constraints use 'tactical_cost_max/min'
                    shop.model.reservoir[res_name].tactical_cost_min.set(penalty_val)
                    shop.model.reservoir[res_name].tactical_cost_min_flag.set(1)
                    shop.model.reservoir[res_name].tactical_cost_max.set(penalty_val)
                    shop.model.reservoir[res_name].tactical_cost_max_flag.set(1)
            except Exception as e:
                print(f"Note: Some tactical penalty attributes could not be set for {res_name}: {e}")

    # 6. Map Plant Limits (Grid Injection Limit)
    # User requested implementing this on Plant or Group instead of Market.
    # We use 'max_p_constr' on the Plant to limit active power output.
    # This acts as a physical or regulatory limit on the plant's connection.
    try:
        # Example: Limit ToyPlant to 40 MW (below its installed 50 MW)
        # You can also use a TimeSeries here for dynamic limits.
        
        # Method A: Direct Plant Constraint
        shop.model.plant.ToyPlant.max_p_constr.set(45.0)
        
        # Method B: Group Constraint (If you had multiple plants)
        # if hasattr(shop.model, 'group'):
        #     if "GridGroup" not in shop.model.group.get_object_names():
        #         g = shop.model.group.add_object("GridGroup")
        #         g.add_object(shop.model.plant.ToyPlant)
        #     shop.model.group.GridGroup.max_prod.set(45.0)
            
    except Exception as e:
        print(f"Error setting plant limits: {e}")
