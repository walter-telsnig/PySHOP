from pyshop import ShopSession
from model_builder import get_session
import os

base_dir = r'c:\Users\User\OneDrive - Alpen-Adria Universität Klagenfurt\SS26\PySHOP'
topo_path = os.path.join(base_dir, "models", "topology.yaml")

shop = get_session(topo_path)

print("--- Connections in SHOP Model ---")
# pyshop often provides ways to see relationships. 
# Let's try to find where connections are stored.
# Many objects have 'get_relations()' or similar.

for res_name in shop.model.reservoir.get_object_names():
    res = shop.model.reservoir[res_name]
    print(f"Reservoir: {res_name}")
    # Check for downstream/upstream relations if available
    # Or just use the topology as defined in YAML which we already have.

# The easiest way is actually to parse the topology.yaml since SHOP building 
# from YAML is declarative and we have the 'connections' list there.

import yaml
with open(topo_path, 'r') as f:
    config = yaml.safe_load(f)
    if 'connections' in config:
        for conn in config['connections']:
            print(f"Connection: {conn['from']} -> {conn['to']} (Type: {conn['type']})")
