# Battery Modeling in sintef-pyshop

The `battery` object in SHOP allows for the optimization of energy storage systems alongside hydro-power plants. It supports energy balance, efficiency losses, and power constraints.

## Core Attributes

To define a battery in your SHOP model (e.g., in `topology.yaml`), you typically need the following parameters:

### Capacity & Energy State
- **`max_energy`**: The maximum energy the battery can store [MWh].
- **`initial_energy`**: The energy state at the start of the optimization [MWh].
- **`min_energy_constraint`**: A time series or constant defining the minimum allowed state of charge [MWh].
- **`max_energy_constraint`**: A time series or constant defining the maximum allowed state of charge [MWh].

### Power Limits
- **`max_charge_power`**: Maximum power the battery can absorb from the grid [MW].
- **`max_discharge_power`**: Maximum power the battery can provide to the grid [MW].

### Efficiency
- **`charge_efficiency`**: Efficiency factor for charging (e.g., 0.9 for 90%).
- **`discharge_efficiency`**: Efficiency factor for discharging (e.g., 0.9 for 90%).
- **Round-trip Efficiency**: Calculated as `charge_efficiency * discharge_efficiency`.

## Operational Configuration

### Concurrent Charge/Discharge
By default, the linear solver might allow the battery to charge and discharge simultaneously to solve numerical issues or internal constraints. 
- **MIP Activation**: To prevent simultaneous charge/discharge, you can activate the Mixed-Integer Programming (MIP) formulation which uses binary variables to ensure only one state is active.

### Degradation & Costs
- **`charge_cost`**: Cost per MWh for charging.
- **`discharge_cost`**: Cost per MWh for discharging.
These are often used to represent the variable cost of battery degradation.

## Data Requirements for Optimization

To run a battery optimization in this PySHOP project, you would need to extend the system with:

1. **Topology Definition**: Add the `battery` object to `models/topology.yaml` and connect it to a `busbar` or let SHOP connect it to the market.
2. **Initial Conditions**: Add `Initial Energy` to your `initial_conditions.csv`.
3. **Availability**: (Optional) Reuse the availability logic to take the battery out of service for maintenance.
4. **Market Price**: The battery will automatically charge when prices are low and discharge when prices are high, based on the `market_price.csv`.

## Result Attributes
After optimization, you can retrieve:
- **`energy`**: The State of Charge (SoC) over time.
- **`charge`**: The charging power in each time step.
- **`discharge`**: The discharging power in each time step.
- **`net_discharge`**: The net power contribution to the grid.
