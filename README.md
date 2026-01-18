# PySHOP Project: Toy Model & 1-Year Optimization

This project implements a hydro-power optimization system using `sintef-pyshop`, featuring a Toy Model with two reservoirs, a plant, a turbine, and a pump. It supports standardized CSV input data and full 1-year (8760 hours) optimization runs.

## Project Structure

- `models/`:
  - `topology.yaml`: Declarative definition of the physical system (reservoirs, plants, connections).
- `src/`:
  - `model_builder.py`: Core logic for initializing `ShopSession` and loading the YAML topology.
  - `data_mapper.py`: Handles loading time-series data from CSVs into the SHOP model.
  - `generate_data.py`: Utility to generate synthetic 1-year input data (prices, inflows).
  - `visualizer.py`: Tool to plot input data trends (Headless Matplotlib).
  - `runner.py`: Main entry point for executing optimization scenarios.
- `data/`:
  - `input/`: Standardized CSV data files (market prices, inflows, initial conditions, availability).
  - `output/`: Optimization results and diagnostic plots.
- `Licence/`: Contains necessary SHOP binaries and license file.

## Toy Model Parameters

The parameters used in the initial verification are defined in `models/topology.yaml`:

### Reservoirs
| Reservoir | Max Volume [Mm3] | LRL [m] | HRL [m] | Vol-Head Range [m] |
| :--- | :--- | :--- | :--- | :--- |
| **UpperRes** | 10.0 | 90.0 | 100.0 | 90 - 100 |
| **LowerRes** | 20.0 | 40.0 | 50.0 | 40 - 50 |

### Plant & Components
- **ToyPlant**: Outlet line at 40.0m.
- **Turbine1**:
  - P_max: 50.0 MW, P_min: 0.0 MW.
  - Efficiency: ~95% Generator, ~90% Turbine (at 40-60m head).
  - **Penstock**: 1 (Required).
- **Pump1**:
  - P_max: 30.0 MW, P_min: 10.0 MW.
  - Efficiency: ~95% Generator, ~85% Turbine/Pump (at 40-60m head).
  - **Penstock**: 1 (Required).

## How to Run

1. **Setup Environment**:
   Ensure you have a `.venv` with `sintef-pyshop`, `pandas`, and `matplotlib` installed.

2. **Generate Data**:
   ```powershell
   .\.venv\Scripts\python.exe src/generate_data.py
   ```

3. **Visualize Input Trends**:
   ```powershell
   .\.venv\Scripts\python.exe src/visualizer.py
   ```

4. **Run Optimization**:
   ```powershell
   .\.venv\Scripts\python.exe src/runner.py
   ```

## Verification Summary
- **Horizon**: 1 Year (8760 hours).
- **Optimization Results**: Successfully generates non-zero production (~28 GWh) and pumping (~32 GWh) using synthetic price and inflow trends.
- **Critical Fix**: All generators and pumps are explicitly assigned to `penstock: 1` to ensure valid topology recognition by the SHOP engine.
