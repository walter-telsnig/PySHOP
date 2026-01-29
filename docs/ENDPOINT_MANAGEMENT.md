# Endpoint Management in SHOP - Guide

## What is "endpoint_desc"?

Based on SINTEF documentation research, `endpoint_desc` is **not an attribute**for reservoirs, but rather a **descriptive label** used in SHOP's ASCII file format to name reservoir endpoints (connections).

## Proper Endpoint Management

Instead of `endpoint_desc`, SHOP uses **water values** to manage reservoir endpoints. Here's what you need to know:

### Key Concept: Water Values

**Water values** define the economic worth of water remaining in reservoirs at the **end of the optimization period**. This tells SHOP how valuable it is to keep water stored versus using it immediately.

### Available Attributes

#### For Your YAML Configuration:

1. **`energy_value_input`** (EUR/MWh) ✅ **Recommended**
   - Defines the energy value of water at end period
   - Simple to use - just set a constant value
   - Best for most cases
   
   ```yaml
   energy_value_input: 30.0  # EUR/MWh
   ```

2. **`water_value_input`** (EUR/Mm³)
   - Alternative to `energy_value_input`
   - Defines water value directly in volume units
   - Can also use XY tables for more complex valuations
   
   ```yaml
   water_value_input: 150.0  # EUR/Mm³
   ```

### What We Added to Your Configuration

In your `simple_pump_turbine.yaml`, I added:

```yaml
reservoirs:
  - name: "UpperRes"
    # ... other attributes ...
    start_head: 95.0
    energy_value_input: 30.0  # Endpoint management
    
  - name: "LowerRes"
    # ... other attributes ...
    start_head: 42.0
    energy_value_input: 30.0  # Endpoint management
```

### What This Does

- **During optimization**: SHOP compares the value of using water now (selling power) vs. saving it for later (based on energy_value_input)
- **At endpoint**: The water remaining in reservoirs is valued at 30 EUR/MWh
- **Economic signal**: This helps SHOP make smart decisions about when to generate/pump

### Common Values

Typical `energy_value_input` values:
- **20-40 EUR/MWh**: Normal market conditions
- **50-100 EUR/MWh**: High value period (e.g., winter)
- **0-10 EUR/MWh**: Low value period (e.g., spring flood)

You should adjust based on:
- Expected future market prices
- Season (winter vs. summer)
- Inflow forecast (dry vs. wet period)

## Alternative: Constraining End Volumes

If you want to **force** specific end volumes (rather than economic valuation), you would need to:

1. Use **penalties** for deviating from target volumes
2. Set very high `energy_value_input` to strongly discourage using water
3. Or use SHOP commands to set hard constraints (more advanced)

However, for learning purposes, **water values are the standard approach**.

## What About Output?

After optimization runs, SHOP provides:
- `storage` - Time series of reservoir volumes (output)
- `sim_storage` - Simulated reservoir volumes (output)
- `water_value_global_result` - Calculated dual values (output)

These are **outputs**, not inputs. The last value in the `storage` time series would be your actual end volume.

## Updated Project Structure

Your 2-week model now has:

```yaml
time:
  starttime: "2024-01-01T00:00:00"
  endtime: "2024-01-15T00:00:00"  # 2 weeks
  timeresolution: 60  # minutes (hourly)

reservoirs:
  - name: "UpperRes"
    energy_value_input: 30.0  # ✅ Endpoint management
  - name: "LowerRes"
    energy_value_input: 30.0  # ✅ Endpoint management
```

## Running Your Model

```bash
python examples/build_model_example.py
```

Now generates:
- ✅ 2-week time period (336 hours)
- ✅ Sample inflow data for 2 weeks
- ✅ Sample price data for 2 weeks
- ✅ Endpoint water values configured

## Next Steps

1. **Experiment with values**: Try different `energy_value_input` values (10, 30, 50, 100)
2. **See the effect**: In a full optimization, higher values = more water saved at end
3. **Real scenarios**: Use forecasted market prices as your energy value
4. **Advanced**: Learn about water value tables (XY format) for more sophisticated endpoint management

## References

- SHOP Documentation: https://docs.shop.sintef.energy/
- Water value methods: Independent vs. coupled water values
- Attribute types: TXY for time-varying water values

---

**Summary**: Instead of `endpoint_desc`, use `energy_value_input` to define the economic value of water at the end of your optimization period. This is the proper way to manage reservoir endpoints in SHOP.
