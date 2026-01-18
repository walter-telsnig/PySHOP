import yaml
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def visualize_topology(topo_path, output_path):
    with open(topo_path, 'r') as f:
        config = yaml.safe_load(f)
    
    connections = config.get('connections', [])
    G = nx.DiGraph()
    
    # Define node types for coloring
    node_types = {}
    
    # 1. Extract nodes from models
    model = config.get('model', {})
    for obj_type, objs in model.items():
        if isinstance(objs, dict):
            for obj_name in objs.keys():
                G.add_node(obj_name)
                node_types[obj_name] = obj_type
    
    # 2. Add edges from connections
    for conn in connections:
        u, v = conn['from'], conn['to']
        ctype = conn.get('type', 'unknown')
        G.add_edge(u, v, label=ctype)
        if u not in node_types: node_types[u] = 'external'
        if v not in node_types: node_types[v] = 'external'

    # Color map
    color_map = {
        'reservoir': 'skyblue',
        'plant': 'salmon',
        'generator': 'orange',
        'pump': 'lightgreen',
        'external': 'lightgrey'
    }
    node_colors = [color_map.get(node_types.get(n, 'external'), 'lightgrey') for n in G.nodes()]

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=3000, font_size=10, font_weight='bold', 
            arrows=True, arrowsize=20)
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("PySHOP Toy Model Topology")
    plt.savefig(output_path)
    print(f"Topology visualization saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    base_dir = r'c:\Users\User\OneDrive - Alpen-Adria Universität Klagenfurt\SS26\PySHOP'
    topo_path = os.path.join(base_dir, 'models', 'topology.yaml')
    output_dir = os.path.join(base_dir, 'data', 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'topology_graph.png')
    
    visualize_topology(topo_path, output_path)
