import os
from pyshop import ShopSession
from dotenv import load_dotenv

def get_session(topology_path=None):
    # Load environment variables from .env file
    load_dotenv()
    
    # Initialize ShopSession
    # ShopSession will look for SHOP_BINARY_PATH and SHOP_LICENSE_PATH in environment
    shop = ShopSession()
    
    if topology_path:
        if not os.path.exists(topology_path):
            raise FileNotFoundError(f"Topology file not found: {topology_path}")
        
        print(f"Loading topology from {topology_path}...")
        shop.load_yaml(file_path=topology_path)
        print("Topology loaded successfully.")
    
    return shop

if __name__ == "__main__":
    # Test loading
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    topo_path = os.path.join(base_dir, "models", "topology.yaml")
    
    try:
        session = get_session(topo_path)
        print(f"SHOP Version: {session.get_shop_version()}")
        print(f"Objects in model: {len(session.model.reservoir.get_names())} reservoirs found.")
    except Exception as e:
        print(f"Error: {e}")
