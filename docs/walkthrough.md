# PySHOP: Freibach System Optimization Walkthrough

This walkthrough documents the final state of the **PySHOP** project, featuring a consolidated, scenario-driven architecture for the Freibach pump-turbine system.

## 📊 2025 Production Baseline Results

The final 1-year optimization for the Freibach system using real market prices (2025) with **Periodic Storage** (target 2.5 Mm³) and **Binary Pump Arbitrage** produced:

| Metric | Value |
| :--- | :--- |
| **Generation** | 107.39 GWh |
| **Pumping (5 MW)** | 1.94 GWh |
| **Net Revenue** | 10.55 Million EUR |
| **Final Reservoir Level** | **721.295 masl** (Target matched) |

### Periodic Reservoir Profile
The profile below shows the reservoir maintaining its year-end periodic balance:
![Freibach 1-Year Profile](../data/output/plots/freibach_optimization_1year.png)

## 🏗️ New Scenario-Driven Architecture

The project is now organized to separate the physical model from simulation data:

1.  **Topologies** (`data/input/topology/`): Static physical system layouts (e.g., `Freibach.yaml`).
2.  **Scenarios** (`config/simulation/`): Run-specific configurations (dates, data mappings).
3.  **Data IO** (`src/data_io.py`): Multi-format loader supporting **Excel (.xlsx)** and CSV.
4.  **Universal Runner** (`examples/optimize_freibach.py`): Executes any scenario defined in a YAML file.

## 🚀 Running a Simulation
To run the production baseline, simply point the runner to the scenario config:
```bash
python examples/optimize_freibach.py --config config/simulation/freibach_2025_baseline.yaml
```

---
**Verification Date**: 2026-01-29
**Status**: CONSOLIDATION COMPLETE
