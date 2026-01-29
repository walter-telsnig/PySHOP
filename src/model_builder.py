"""
Functions to build SHOP models from configuration
"""

import yaml
from pathlib import Path
import pandas as pd


def load_topology_yaml(yaml_path):
    """
    Load topology definition from YAML file
    
    Args:
        yaml_path: Path to YAML topology file
        
    Returns:
        dict: Topology configuration
    """
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def build_model_from_yaml(shop_model, yaml_path):
    """
    Build SHOP model topology from YAML configuration
    
    Args:
        shop_model: SHOP model object (from shop.model)
        yaml_path: Path to YAML topology file
    """
    config = load_topology_yaml(yaml_path)
    
    # Build reservoirs
    if 'reservoirs' in config:
        for rsv_config in config['reservoirs']:
            build_reservoir(shop_model, rsv_config)
    
    # Build plants
    if 'plants' in config:
        for plant_config in config['plants']:
            build_plant(shop_model, plant_config)
    
    # Build generators (turbines)
    if 'generators' in config:
        for gen_config in config['generators']:
            build_generator(shop_model, gen_config)
    
    # Build pumps
    if 'pumps' in config:
        for pump_config in config['pumps']:
            build_pump(shop_model, pump_config)


def build_reservoir(shop_model, config):
    """
    Add a reservoir to the SHOP model
    
    Args:
        shop_model: SHOP model object
        config: Reservoir configuration dict
    """
    name = config['name']
    rsv = shop_model.reservoir.add_object(name)
    
    # Set attributes
    if 'max_vol' in config:
        rsv.max_vol.set(config['max_vol'])
    if 'lrl' in config:
        rsv.lrl.set(config['lrl'])
    if 'hrl' in config:
        rsv.hrl.set(config['hrl'])
    
    # Set volume-head curve
    if 'vol_head' in config:
        vol_head_data = config['vol_head']
        # Convert to pandas Series format
        volumes = [point[0] for point in vol_head_data]
        heads = [point[1] for point in vol_head_data]
        vol_head_series = pd.Series(heads, index=volumes, name=0.0)
        rsv.vol_head.set(vol_head_series)
    
    # Set initial conditions
    if 'start_head' in config:
        rsv.start_head.set(config['start_head'])
    if 'start_vol' in config:
        rsv.start_vol.set(config['start_vol'])
    
    # Set water value (scalar or XY curve)
    # water_value_input typically in EUR/Mm3
    if 'water_value_input' in config:
        wv_data = config['water_value_input']
        if isinstance(wv_data, list):
            # Convert list of points [vol, value] to Series
            volumes = [point[0] for point in wv_data]
            values = [point[1] for point in wv_data]
            wv_curve = pd.Series(values, index=volumes, name=0.0)
            rsv.water_value_input.set([wv_curve])
        else:
            # Scalar value
            rsv.water_value_input.set(wv_data)
    
    if 'energy_value_input' in config:
        rsv.energy_value_input.set(config['energy_value_input'])

    # Set Volume Schedule if provided
    if 'schedule' in config:
        schedule_data = config['schedule']
        # Parse points
        raw_timestamps = [pd.Timestamp(point[0]) for point in schedule_data]
        raw_volumes = [point[1] for point in schedule_data]
        sparse_series = pd.Series(raw_volumes, index=raw_timestamps)
        
        # Expand to full simulation time resolution if possible
        try:
            time_res = shop_model.get_time_resolution()
            full_index = pd.date_range(start=time_res['starttime'], end=time_res['endtime'], freq='h')
            # Reindex and interpolate to fill gaps
            full_schedule = sparse_series.reindex(full_index).interpolate(method='time').ffill().bfill()
            rsv.schedule.set(full_schedule)
        except Exception:
            # Fallback to sparse if time resolution fails
            rsv.schedule.set(sparse_series)
    
    if 'schedule_flag' in config:
        rsv.schedule_flag.set(config['schedule_flag'])
    if 'upper_slack' in config:
        rsv.upper_slack.set(config['upper_slack'])
    if 'lower_slack' in config:
        rsv.lower_slack.set(config['lower_slack'])
    
    # Set constant inflow if provided
    if 'inflow' in config and isinstance(config['inflow'], (int, float)):
        # Will be set as time series in the example script
        pass  # Handle in calling code


def build_plant(shop_model, config):
    """
    Add a plant to the SHOP model and connect it to reservoirs
    
    Args:
        shop_model: SHOP model object
        config: Plant configuration dict
    """
    name = config['name']
    plant = shop_model.plant.add_object(name)
    
    # Connect to inlet reservoir if specified
    if 'inlet_reservoir' in config:
        inlet_rsv = getattr(shop_model.reservoir, config['inlet_reservoir'])
        inlet_rsv.connect_to(plant)
    
    # Connect to outlet reservoir if specified
    if 'outlet_reservoir' in config:
        outlet_rsv = getattr(shop_model.reservoir, config['outlet_reservoir'])
        plant.connect_to(outlet_rsv)
    
    # Set attributes
    if 'outlet_line' in config:
        plant.outlet_line.set(config['outlet_line'])
    if 'main_loss' in config:
        plant.main_loss.set(config['main_loss'])
    if 'penstock_loss' in config:
        plant.penstock_loss.set(config['penstock_loss'])
    # num_units and num_pumps are informational in YAML, not direct SHOP attributes


def build_generator(shop_model, config):
    """
    Add a generator (turbine) to the SHOP model
    
    Args:
        shop_model: SHOP model object
        config: Generator configuration dict
    """
    name = config['name']
    gen = shop_model.generator.add_object(name)
    
    # Connect to plant
    if 'plant' in config:
        plant = getattr(shop_model.plant, config['plant'])
        gen.connect_to(plant)
    
    # Set basic attributes
    if 'penstock' in config:
        gen.penstock.set(config['penstock'])
    if 'p_min' in config:
        gen.p_min.set(config['p_min'])
    if 'p_max' in config:
        gen.p_max.set(config['p_max'])
    if 'p_nom' in config:
        gen.p_nom.set(config['p_nom'])
    if 'startcost' in config:
        gen.startcost.set(config['startcost'])
    
    # Set generator efficiency curve (power-based)
    if 'gen_eff_curve' in config:
        curve_config = config['gen_eff_curve']
        ref = curve_config.get('ref', 1.0)
        points = curve_config['points']
        powers = [p[0] for p in points]
        efficiencies = [p[1] for p in points]
        curve_series = pd.Series(efficiencies, index=powers, name=ref)
        gen.gen_eff_curve.set(curve_series)
    
    # Set turbine efficiency curves
    if 'turb_eff_curves' in config:
        curves = config['turb_eff_curves']
        curve_list = []
        for curve in curves:
            ref = curve['ref']
            points = curve['points']
            discharges = [p[0] for p in points]
            efficiencies = [p[1] for p in points]
            curve_series = pd.Series(efficiencies, index=discharges, name=ref)
            curve_list.append(curve_series)
        gen.turb_eff_curves.set(curve_list)


def build_pump(shop_model, config):
    """
    Add a pump to the SHOP model
    
    Args:
        shop_model: SHOP model object
        config: Pump configuration dict
    """
    name = config['name']
    pump = shop_model.pump.add_object(name)
    
    # Connect to plant
    if 'plant' in config:
        plant = getattr(shop_model.plant, config['plant'])
        pump.connect_to(plant)
    
    # Set basic attributes
    if 'penstock' in config:
        pump.penstock.set(config['penstock'])
    if 'p_min' in config:
        pump.p_min.set(config['p_min'])
    if 'p_max' in config:
        pump.p_max.set(config['p_max'])
    if 'p_nom' in config:
        pump.p_nom.set(config['p_nom'])
    if 'startcost' in config:
        pump.startcost.set(config['startcost'])
    
    # CRITICAL: Pumps need turbine efficiency curves!
    # Pumps in SHOP can work as turbines (reversible pump-turbines)
    if 'turb_eff_curves' in config:
        curves = config['turb_eff_curves']
        curve_list = []
        for curve in curves:
            ref = curve['ref']
            points = curve['points']
            discharges = [p[0] for p in points]
            efficiencies = [p[1] for p in points]
            curve_series = pd.Series(efficiencies, index=discharges, name=ref)
            curve_list.append(curve_series)
        pump.turb_eff_curves.set(curve_list)

