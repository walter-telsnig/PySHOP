# Analysis of Working SHOP ASCII File

## File: POWELSRV_FRELT.ascii

This is a real, working SHOP model exported from a production system. Here are the critical findings:

---

## System Overview

**Structure** (from line 5-7):
- 2 Reservoirs: "Freibach" and "DrauWest"
- 1 Plant: "FB(279)"
- 2 Generators (units 1 and 2)
- 2 Pumps (units 1 and 2)
- 2 Gates
- Time period: 1 year (2026-01-29 to 2027-01-01)

---

## Critical Discovery #1: `endpoint_desc` IS Real!

**Lines 49-53** show `endpoint_desc` for reservoir:

```
RESERVOIR endpoint_desc Freibach
#Id;Number;Reference;Pts;X_unit;Y_unit
     0      0      0.000      1 MM3 NOK_MWH
#  x_value;   y_value
   5.25260     100.00
```

**What this means:**
- `endpoint_desc` is an **XY curve**, not a simple value
- X-axis: Volume (MM3)
- Y-axis: Price/Value (NOK/MWh or EUR/MWh)
- In this case: At 5.25 Mm³, water value is 100 NOK/MWh
- This is **more sophisticated** than `energy_value_input`

**For pyshop**, this would be set as:
```python
# XY curve for water value
endpoint_curve = pd.Series([100.0], index=[5.25260], name=0.0)
rsv.endpoint_desc.set(endpoint_curve)
```

---

## Critical Discovery #2: Pumps NEED turb_eff_curves!

**Lines 479-489** show pumps with TURBINE efficiency curves:

```
PUMP turb_eff_curves FB(279) 1
#Id;Number;Reference;Pts;X_unit;Y_unit
     0      0    304.000      1 M3/S %
#  x_value;   y_value
   1.35000   80.50000
```

**Why:**
- Pumps in SHOP are **reversible** (pump-turbine units)
- They can work as BOTH pumps AND turbines
- Need efficiency curves for BOTH modes:
  - `turb_eff_curves`: When working as turbine (generating)
  - Pump efficiency: When working as pump (consuming)

**This explains our warning!**

---

## Critical Discovery #3: Generator Configuration

**Lines 186-206** show proper generator setup:

```
GENERATOR attributes FB(279)      1
#Id Type Penstock Nom_prod Min_prod Max_prod Start_cost
   280      0      1     17.000      7.000     17.000      0.000

GENERATOR gen_eff_curve FB(279)      1
# Generator efficiency curve (power-based)
# 13 points from 5 MW to 17 MW

GENERATOR turb_eff_curves FB(279)      1
# Turbine efficiency curve (discharge-based)  
# 13 points from 2.2 to 6.08 m³/s
# Reference head: 324 m
```

**Key insights:**
-  BOTH `gen_eff_curve` AND `turb_eff_curves` are used
- gen_eff_curve: Power (MW) vs efficiency (%)
- turb_eff_curves: Discharge (m³/s) vs efficiency (%)
- Reference head matters for turbine curves

---

## Critical Discovery #4: Plant Configuration

**Lines 152-161**:

```
PLANT attributes FB(279)
#Id;Water_course;Type;Bid_area;Prod_area;Num_units;Num_pumps
   279      0      1      1      1      2      2
#Num_main_seg;Num_penstock;Time_delay;Prod_factor;Outlet_line
     1      2      0      0.000    410.000
#Main tunnel loss
0.00000000
#Penstock loss
0.00000000 0.00000000
```

**Key points:**
- `Num_units`: 2 (generators)
- `Num_pumps`: 2 (pumps)
- `Num_penstock`: 2 (one per unit)
- `Outlet_line`: 410.0 masl (discharge point elevation)
- Loss factors for main tunnel and penstocks

---

## Critical Discovery #5: Reservoir Constraints

The working model uses MULTIPLE constraint types:

1. **`endpoint_desc`** (lines 49-53): Water value at end
2. **`schedule`** (lines 67-71): Target end volume
3. **`schedule_flag`** (lines 73-77): Enforce schedule (0=soft, 1=hard)
4. **`tactical_limit_min/max`** (lines 79-97): Seasonal bounds
5. **`tactical_cost_min/max`** (lines 87-103): Penalties for violations

This is much more sophisticated than we implemented!

---

## Critical Discovery #6: Market Definition

**Line 708+**: Hourly market prices for entire year (8088 hours)

```
MARKET      1
#Num_func
8088
#Start_time
20260129000000000
#Id;Number;Reference;Pts;X_unit;Y_unit
     0      0      0.000      2 MW NOK
#  x_value;   y_value
-1000.00000  148.70900
1000.00000  148.71100
```

**Format:**
- XY curve for each hour
- X: Power (MW), Y: Price (NOK or EUR)
- Allows buy/sell at different prices
- In this case: essentially constant price per hour

---

## Critical Discovery #7: Connections

**Lines 695-700**:

```
CONNECT RESERVOIR/PLANT Freibach FB(279)
CONNECT RESERVOIR/BYPASS Freibach b_SpeicherFreibach_Drau(286)
CONNECT RESERVOIR/GATE DrauWest w_DrauWest_Drau(285)
CONNECT PLANT/RESERVOIR FB(279) DrauWest
```

**Topology:**
```
Freibach (upper) 
    ├─> FB plant (generates/pumps) ─> DrauWest (lower)
    └─> bypass gate ─> (discharge)
    
DrauWest
    └─> spillway gate ─> (discharge)
```

---

## What We Need to Fix

### 1. Add `endpoint_desc` properly
```python
# In model_builder.py
if 'endpoint_desc' in config:
    # endpoint_desc is an XY curve: volume → water_value
    curve_data = config['endpoint_desc']
    volumes = [p[0] for p in curve_data]
    values = [p[1] for p in curve_data]
    endpoint_curve = pd.Series(values, index=volumes, name=0.0)
    rsv.endpoint_desc.set(endpoint_curve)
```

### 2. Add turbine efficiency to pumps
```yaml
pumps:
  - name: "Pump1"
    plant: "Plant1"
    penstock: 1
    p_nom: 80.0
    # Pump mode efficiency
    pump_eff_curves:
      - ref: 50.0  # reference head
        points:
          - [20.0, 0.75]
          - [40.0, 0.85]
    # Turbine mode efficiency (when pump works as turbine)
    turb_eff_curves:
      - ref: 50.0
        points:
          - [15.0, 0.78]
          - [30.0, 0.82]
```

### 3. Simplify first - remove pump!
For learning, start with generator-only:
- Remove pumps from YAML
- Get optimization working
- Add pumps back later

---

## Recommended Next Steps

1. **Try endpoint_desc attribute** instead of energy_value_input
2. **Simplify to generator-only** (remove pump temporarily)
3. **Add market properly** with hourly prices
4. **Set outlet_line** on plant (discharge elevation)
5. **Test with simple 1-day optimization** first

---

## Summary

The working model shows:
- `endpoint_desc` IS a real attribute (XY curve format)
- Pumps need `turb_eff_curves` (they're reversible)
- Multiple efficiency curves are needed
- Proper market configuration is essential
- Constraints are more complex than we thought

**The good news:** Our model structure is correct! We just need to add these missing pieces.
