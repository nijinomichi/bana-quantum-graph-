"""render.py
RadicanTrust™ Quantum Graph visualizer
Usage: python render.py
Output: quantum_trust_graph.png
Requires: networkx matplotlib pyyaml
"""
import yaml
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

YAML_FILE = "quantum_trust_graph.yaml"
OUTPUT_FILE = "quantum_trust_graph.png"

with open(YAML_FILE, encoding="utf-8") as f:
    data = yaml.safe_load(f)["quantum_trust_graph_art"]

layer_colors = data["visualization_hints"]["colors"]

G = nx.DiGraph()
node_color_map = []
layer_map = {}

for node in data["nodes"]:
    nid = node["id"]
    G.add_node(nid, label=node["label"], layer=node["layer"])
    layer_map[nid] = node["layer"]
    node_color_map.append(layer_colors.get(node["layer"], "#cccccc"))

for edge in data["edges"]:
    G.add_edge(edge["from"], edge["to"], label=edge.get("label", ""))

labels = {n: G.nodes[n]["label"] for n in G.nodes}
edge_labels = nx.get_edge_attributes(G, "label")

plt.figure(figsize=(18, 12), facecolor="#111111")
ax = plt.gca()
ax.set_facecolor("#111111")

pos = nx.spring_layout(G, seed=42, k=2.2)

nx.draw_networkx_nodes(
    G, pos,
    node_color=node_color_map,
    node_size=2200,
    alpha=0.92,
    ax=ax
)
nx.draw_networkx_labels(
    G, pos,
    labels=labels,
    font_size=6.5,
    font_color="#111111",
    font_weight="bold",
    ax=ax
)
nx.draw_networkx_edges(
    G, pos,
    edge_color="#aaaaaa",
    width=1.4,
    arrows=True,
    arrowsize=18,
    connectionstyle="arc3,rad=0.08",
    ax=ax
)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=5.5,
    font_color="#dddddd",
    ax=ax
)

# Legend
legend_patches = [
    mpatches.Patch(color=color, label=layer)
    for layer, color in layer_colors.items()
]
ax.legend(
    handles=legend_patches,
    loc="lower left",
    framealpha=0.3,
    facecolor="#222222",
    edgecolor="#555555",
    labelcolor="white",
    fontsize=8
)

plt.title(
    data["title"],
    fontsize=10,
    color="#ffffff",
    pad=12
)
plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=200, bbox_inches="tight", facecolor="#111111")
print(f"✅ saved: {OUTPUT_FILE}")
