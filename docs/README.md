# PySHOP_AG - Hydropower Optimization with SINTEF SHOP

A learning project for working with SINTEF's SHOP (Short-term Hydro Optimization Program) using the `sintef-pyshop` Python package.

## 📋 Project Overview

This project provides a structured framework for:
- Building hydropower system topologies from YAML configuration files
- Running short-term optimization with SHOP
- Loading input data from CSV/XLSX files
- Visualizing optimization results

### Current Features

- ✅ Simple pump-turbine topology (1 reservoir → plant with turbine + pump → reservoir)
- ✅ YAML-based topology definitions for easy expansion
- ✅ CSV/XLSX data I/O utilities
- ✅ Automated visualization of results
- ✅ Example scripts to get started

## 🏗️ Project Structure

```
PySHOP_AG/
├── config/                     # Topology definitions (YAML)
│   └── simple_pump_turbine.yaml
│
├── data/                       # Input/output data
│   ├── input/
│   │   ├── inflow/            # Inflow time series
│   │   ├── prices/            # Electricity price data
│   │   └── topology/          # Additional topology data
│   └── output/
│       ├── results/           # Optimization results
│       └── plots/             # Generated visualizations
│
├── src/                        # Source code modules
│   ├── shop_session.py        # SHOP session management
│   ├── model_builder.py       # Build models from YAML
│   ├── data_io.py             # Data loading/saving utilities
│   └── visualization.py       # Plotting functions
│
├── scripts/                    # Executable scripts
│
├── examples/                   # Example scripts
│   └── simple_example.py      # Basic pump-turbine example
│
├── tests/                      # Unit tests
│
├── Licence/                    # SHOP license files
│
├── .venv/                      # Virtual environment
├── .gitignore
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+** installed
2. **SHOP License**: Valid SHOP license in the `Licence/` directory
3. **SHOP Binaries**: Download from [SHOP Portal](https://shop.sintef.energy/) (if needed)

### Installation

1. **Activate the virtual environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies** (already done if setup was followed):
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```python
   python -c "import pyshop; print('pyshop installed successfully!')"
   ```

### Running the Simple Example

```bash
python examples/simple_example.py
```

This will:
1. Create a SHOP session
2. Build a simple pump-turbine topology from `config/simple_pump_turbine.yaml`
3. Generate sample inflow and price data
4. Run optimization (if SHOP license is valid)
5. Create visualization plots in `data/output/plots/`

## 📚 Key Concepts

### SHOP Model Hierarchy

```
ShopSession
    └── model
        ├── reservoir (object type)
        │   ├── UpperRes (object instance)
        │   └── LowerRes
        ├── plant
        │   └── Plant1
        ├── generator
        │   └── Gen1
        └── pump
            └── Pump1
```

### Creating Topologies

Topologies are defined in YAML files in `config/`. See `simple_pump_turbine.yaml` for the structure:

```yaml
reservoirs:
  - name: "UpperRes"
    max_vol: 12.0
    lrl: 90.0
    hrl: 100.0
    # ... more attributes

plants:
  - name: "Plant1"
    inlet_reservoir: "UpperRes"
    outlet_reservoir: "LowerRes"

generators:
  - name: "Gen1"
    plant: "Plant1"
    p_min: 25.0
    p_max: 100.0
    # ... efficiency curves

pumps:
  - name: "Pump1"
    plant: "Plant1"
    p_min: 20.0
    p_max: 80.0
```

### Input Data Format

**Inflow data** (`data/input/inflow/*.csv`):
```csv
datetime,inflow_m3s
2024-01-01 00:00:00,45.2
2024-01-01 01:00:00,47.1
...
```

**Price data** (`data/input/prices/*.csv`):
```csv
datetime,price_eur_mwh
2024-01-01 00:00:00,35.5
2024-01-01 01:00:00,32.8
...
```

## 🔧 Usage Examples

### Basic Workflow

```python
from shop_session import ShopManager
from model_builder import build_model_from_yaml

# 1. Create session
shop = ShopManager()

# 2. Set time period
shop.set_time("2024-01-01 00:00:00", "2024-01-02 00:00:00", timeresolution=60)

# 3. Build model from YAML
model = shop.get_model()
build_model_from_yaml(model, "config/simple_pump_turbine.yaml")

# 4. Set input data
model.reservoir.UpperRes.inflow.set(inflow_series)

# 5. Run optimization
shop.run_optimization()

# 6. Extract results
reservoir_level = model.reservoir.UpperRes.head.get()
generation = model.generator.Gen1.production.get()
```

### Loading Data

```python
from data_io import load_inflow_data, load_price_data

inflow = load_inflow_data("data/input/inflow/my_inflow.csv")
prices = load_price_data("data/input/prices/my_prices.csv")
```

### Visualization

```python
from visualization import plot_reservoir_levels, plot_generation_and_pumping

# Plot reservoir levels
plot_reservoir_levels(
    {'Upper': upper_level, 'Lower': lower_level},
    save_path="data/output/plots/levels.png"
)

# Plot generation and pumping
plot_generation_and_pumping(
    gen_data, 
    pump_data,
    save_path="data/output/plots/dispatch.png"
)
```

## 🎯 Next Steps

### Expanding the Project

1. **Add more complex topologies**: Create new YAML files in `config/`
   - Multiple reservoirs in series/parallel
   - Multiple plants and generators
   - Include gates, junctions, etc.

2. **Real data integration**: Replace sample data with actual:
   - Historical inflow data
   - Market price data
   - Operational constraints

3. **Advanced features**:
   - Add market objects for bidding strategies
   - Implement rolling horizon optimization
   - Add uncertainty handling (stochastic optimization)

4. **Automation**: Create scripts in `scripts/` for:
   - Batch processing multiple scenarios
   - Automated reporting
   - Data preprocessing pipelines

## 📖 Resources

- [SHOP Documentation](https://docs.shop.sintef.energy/)
- [pyshop API Reference](https://docs.shop.sintef.energy/examples/pyshop/pyshop.html)
- [SHOP Portal](https://shop.sintef.energy/) - Download binaries and documentation
- [SHOP Examples](https://docs.shop.sintef.energy/examples/index.html)

## ⚠️ Troubleshooting

### "License not found" error
- Ensure you have a valid SHOP license in the `Licence/` directory
- Check the license path in `ShopManager` initialization

### "Solver binaries not found"
- Download SHOP binaries from SHOP Portal
- Specify `solver_path` when creating `ShopManager`

### Import errors
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

## 📝 License

This project structure is for learning purposes. SHOP itself requires a valid license from SINTEF Energy Research.

---

**Happy Optimizing! 💧⚡**
