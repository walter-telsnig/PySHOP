# Quick Reference Guide for PySHOP_AG

## 🎯 Common Tasks

### 1. Activating the Virtual Environment

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
.venv\Scripts\activate.bat
```

### 2. Running the Simple Example

```bash
python examples\simple_example.py
```

### 3. Creating a New Topology

1. Create a new YAML file in `config/`, for example `my_topology.yaml`
2. Follow the structure of `simple_pump_turbine.yaml`
3. Define your reservoirs, plants, generators, pumps, etc.
4. Load it with:
   ```python
   from model_builder import build_model_from_yaml
   build_model_from_yaml(model, "config/my_topology.yaml")
   ```

### 4. Loading Your Own Data

**Inflow data:**
```python
from data_io import load_inflow_data
inflow = load_inflow_data("data/input/inflow/my_file.csv")
model.reservoir.MyReservoir.inflow.set(inflow)
```

**Price data:**
```python
from data_io import load_price_data
prices = load_price_data("data/input/prices/my_prices.csv")
```

### 5. Extracting Results

After running optimization:

```python
# Reservoir levels
level = model.reservoir.UpperRes.head.get()

# Generation
generation = model.generator.Gen1.production.get()

# Pumping
pumping = model.pump.Pump1.consumption.get()

# Discharge
discharge = model.generator.Gen1.discharge.get()
```

### 6. Plotting Results

```python
from visualization import plot_reservoir_levels

plot_reservoir_levels(
    {'Upper': upper_level, 'Lower': lower_level},
    save_path="data/output/plots/my_plot.png",
    show=True
)
```

## 📊 SHOP Object Types

Common SHOP object types you can use:

- `model.reservoir` - Water reservoirs
- `model.plant` - Hydropower plants
- `model.generator` - Turbines/generators
- `model.pump` - Pumps
- `model.gate` - Discharge gates
- `model.junction` - Water junctions
- `model.market` - Electricity markets
- `model.reserve_group` - Reserve capacity groups

## 🔑 Key SHOP Attributes

### Reservoir Attributes
- `max_vol` - Maximum volume [Mm³]
- `lrl` - Lower regulation limit [masl]
- `hrl` - Higher regulation limit [masl]
- `vol_head` - Volume-head curve
- `start_head` - Initial water level [masl]
- `inflow` - Inflow time series [m³/s]

### Generator Attributes
- `p_min` - Minimum power [MW]
- `p_max` - Maximum power [MW]
- `p_nom` - Nominal power [MW]
- `penstock` - Penstock number
- `startcost` - Start-up cost
- `turb_eff_curves` - Turbine efficiency curves
- `production` - Production time series (OUTPUT)
- `discharge` - Discharge time series (OUTPUT)

### Pump Attributes
- `p_min` - Minimum pumping power [MW]
- `p_max` - Maximum pumping power [MW]
- `p_nom` - Nominal power [MW]
- `pump_eff` - Pump efficiency curves
- `consumption` - Power consumption (OUTPUT)

## 🔧 Troubleshooting

### License Issues
```python
# Specify custom license path
shop = ShopManager(license_path="path/to/licence")
```

### Solver Path Issues
```python
# Specify custom solver path
shop = ShopManager(solver_path="path/to/shop/binaries")
```

### Enable Logging for Debugging
```python
shop = ShopManager(
    silent=False,
    log_file="debug.log"
)
```

## 📝 YAML Topology Example

```yaml
reservoirs:
  - name: "MyReservoir"
    max_vol: 15.0
    lrl: 80.0
    hrl: 100.0
    vol_head:
      - [0.0, 80.0]
      - [15.0, 100.0]
    start_head: 90.0

plants:
  - name: "MyPlant"
    inlet_reservoir: "MyReservoir"
    outlet_reservoir: "Ocean"
    main_loss: [0.0001]

generators:
  - name: "MyGen"
    plant: "MyPlant"
    penstock: 1
    p_min: 10.0
    p_max: 50.0
    p_nom: 50.0
    turb_eff_curves:
      - ref: 90.0
        points:
          - [10.0, 0.75]
          - [30.0, 0.90]
          - [50.0, 0.88]
```

## 📚 Useful Links

- SHOP Documentation: https://docs.shop.sintef.energy/
- pyshop Reference: https://docs.shop.sintef.energy/examples/pyshop/pyshop.html
- SHOP Portal: https://shop.sintef.energy/

## 💡 Tips

1. **Start simple**: Begin with the provided example and gradually add complexity
2. **Check data formats**: Ensure CSV files have datetime columns that pandas can parse
3. **Validate topology**: Use `model.build_connection_tree()` to visualize your topology
4. **Save incrementally**: Save results after each step to avoid losing work
5. **Use logging**: Enable SHOP logging when debugging model issues
