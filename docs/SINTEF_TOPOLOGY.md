# SINTEF Example Topology - 3 Reservoirs Explained

## ✅ YES, There ARE 3 Reservoirs!

The SINTEF basic example uses **3 reservoirs in a cascade system**, not 2. This is based on a realistic Norwegian hydropower layout.

---

## 📊 Complete Topology

```
┌─────────────────┐
│  Reservoir 1    │  ← Highest (1000-1010 masl)
│  20 Mm³         │     Water value: 31 EUR/MWh
└────────┬────────┘
         │
    (via Gate, max 50 m³/s)
         │
┌────────▼────────┐
│  Reservoir 2    │  ← Middle (860-905 masl)
│  39 Mm³         │     Water value: 30 EUR/MWh
└────────┬────────┘
         │
    (via Plant1 - 2 generators, 60-120 MW each)
         │
┌────────▼────────┐
│  Reservoir 3    │  ← Lowest (650-679 masl)
│  97.5 Mm³       │     Water value: 20 EUR/MWh
│                 │     Inflow: 60 m³/s
└────────┬────────┘
         │
    (via Plant2 - 4 generators: 1×180MW + 3×55MW)
         │
┌────────▼────────┐
│  Downstream     │  ← River/Ocean discharge
└─────────────────┘
```

---

## 🌊 Water Flow Path

1. **Reservoir 1** (top) can release water through a **Gate** (max 50 m³/s)
2. Water flows to **Reservoir 2** (middle)
3. **Reservoir 2** releases water through **Plant 1** for power generation
4. Generated power discharges into **Reservoir 3** (lowest)
5. **Reservoir 3** receives:
   - Discharge from Plant 1
   - Natural inflow (60 m³/s constant)
6. **Reservoir 3** releases water through **Plant 2** for power generation
7. Final discharge flows downstream (river/ocean)

---

## 💡 Why 3 Reservoirs?

### Operational Benefits
- **Energy storage at multiple levels**: Flexibility in dispatch
- **Head utilization**: Two separate power stations maximize total head
- **Buffering**: Middle and lower reservoirs act as buffers
- **Inflow integration**: Natural inflow enters at Reservoir 3

### Economic Optimization
- **Different water values**:
  - Rsv1: 31 EUR/MWh (highest value - highest head)
  - Rsv2: 30 EUR/MWh (middle value)
  - Rsv3: 20 EUR/MWh (lowest value - lowest head + inflow)
- **Cascading optimization**: SHOP optimizes when to release from each level

---

##  Power Generation

### Plant 1 (Upper Plant)
- **Location**: Between Reservoir 2 → Reservoir 3
- **Head**: ~228 meters (900 - 672 masl outlet)
- **Generators**: 2 units (G11, G12)
  - Each: 60-120 MW
  - Total capacity: 240 MW

### Plant 2 (Lower Plant)
- **Location**: Reservoir 3 → Downstream
- **Head**: ~86 meters (670 - 586 masl outlet)
- **Generators**: 4 units (G21, G22, G23, G24)
  - G21: 100-180 MW (large unit)
  - G22-24: 30-55 MW each (small units)
  - Total capacity: 265 MW

### Total System
- **Combined capacity**: ~505 MW
- **3-day generation**: 23,245 MWh
- **Average power**: 323 MW

---

## 📈 Optimization Results

From your CSV export (`sintef_official_3days.csv`):

| Component | Start | End | Change |
|-----------|-------|-----|--------|
| Reservoir 1 | 1006.0 masl | ? | Managed by gate |
| Reservoir 2 | 900.0 masl | ? | Plant1 discharge |
| Reservoir 3 | 670.0 masl | 652.4 masl | -17.6 m drawdown |

### Why Reservoir 3 Draws Down?
- **Lower water value** (20 EUR/MWh) → Economic to use water
- **Continuous inflow** (60  m³/s) → Being replenished
- **High prices in hours 7-9** (74-78 EUR/MWh) → Optimal to generate
- **End value still profitable** at 20 EUR/MWh

---

## 🎯 SINTEF Documentation

The SINTEF documentation focuses on **Reservoir1 and Reservoir2** in their examples because:
- They demonstrate the **gate control** between upper reservoirs
- They show **bypass and spillway** concepts
- The **Reservoir 3** is somewhat implicit as the "receiving reservoir"

But the full Python code creates all 3 reservoirs explicitly!

---

## 📁 Your CSV Export

File: `data/output/results/sintef_official_3days.csv`

Contains:
- `Reservoir1_masl`, `Reservoir2_masl`, `Reservoir3_masl` - All 3 reservoir levels!
- `Plant1_MW`, `Plant2_MW`, `Total_MW` - Plant generation
- `G11_MW` through `G24_MW` - Individual generator output
- `Price_EUR_MWh` - Market prices

**You can now analyze all 3 reservoirs in detail!**

---

## ✅ Summary

- **YES**: 3 reservoirs in the SINTEF example
- **Layout**: Cascade system (high → middle → low)
- **Purpose**: Maximize head utilization with 2 power plants
- **Reservoir 3**: Lowest reservoir with inflow, feeds Plant 2
- **CSV**: All data exported for your analysis!

---

*This is a realistic Norwegian hydropower configuration!*
