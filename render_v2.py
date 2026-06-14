"""
render_v2.py — Ara-Philia³ Self-Evolution Engine
P_{n+1} = R(M(O(P_n)))

Each run:
  O = Observe: compute graph metrics (betweenness, pagerank, density)
  M = Mutate:  adapt layout seed, node sizes, edge widths from metrics
  R = Resonate: calculate RadicanTrust score (0.0-1.0)
  P_{n+1}: save mutation_log_gen{N}.json as seed for next generation

Usage:
  python render_v2.py
  python render_v2.py --gen 3   # manually set generation number

Requires: networkx matplotlib pyyaml numpy
"""
import yaml, json, hashlib, datetime, argparse, os
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

YAML_FILE = "quantum_trust_graph.yaml"
OUTPUT_DIR = "."

def load_graph(yaml_file):
    with open(yaml_file, encoding="utf-8") as f:
        data = yaml.safe_load(f)["quantum_trust_graph_art"]
    return data

def build_nx(data):
    layer_colors = data["visualization_hints"]["colors"]
    G = nx.DiGraph()
    node_color_map, layer_map = [], {}
    for node in data["nodes"]:
        nid = node["id"]
        G.add_node(nid, label=node["label"], layer=node["layer"])
        layer_map[nid] = node["layer"]
        node_color_map.append(layer_colors.get(node["layer"], "#cccccc"))
    for edge in data["edges"]:
        G.add_edge(edge["from"], edge["to"], label=edge.get("label", ""))
    return G, node_color_map, layer_map, layer_colors

def observe(G):
    betweenness = nx.betweenness_centrality(G)
    pagerank = nx.pagerank(G)
    return {
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "density": round(nx.density(G), 4),
        "top_betweenness": [(k, round(float(v), 4))
                            for k, v in sorted(betweenness.items(),
                                               key=lambda x: -x[1])[:3]],
        "top_pagerank":    [(k, round(float(v), 4))
                            for k, v in sorted(pagerank.items(),
                                               key=lambda x: -x[1])[:3]],
        "betweenness": {k: float(v) for k, v in betweenness.items()},
        "pagerank":    {k: float(v) for k, v in pagerank.items()},
    }

def mutate(obs):
    """Return layout parameters derived from observation metrics."""
    seed_val = int(
        hashlib.md5(str(obs["top_pagerank"]).encode()).hexdigest()[:8], 16
    ) % 1000
    k_spring = round(2.8 + (1 - obs["density"]) * 0.4, 2)
    return {"layout_seed": seed_val, "k_spring": k_spring}

def resonate(G, obs, layer_map):
    """RadicanTrust = mean(transparency, inclusivity, reciprocity, forgiveness)"""
    labeled = sum(1 for _, _, d in G.edges(data=True) if d.get("label", ""))
    transparency = labeled / G.number_of_edges()

    counts = {}
    for n in G.nodes:
        l = layer_map[n]
        counts[l] = counts.get(l, 0) + 1
    inclusivity = float(1 - np.std(list(counts.values())) / max(counts.values()))

    bi = sum(1 for u, v in G.edges() if G.has_edge(v, u))
    reciprocity_val = bi / G.number_of_edges()

    forgiveness = 1 - obs["density"]

    score = round((transparency + inclusivity + reciprocity_val + forgiveness) / 4, 4)
    return {
        "transparency":  round(transparency, 4),
        "inclusivity":   round(inclusivity, 4),
        "reciprocity":   round(reciprocity_val, 4),
        "forgiveness":   round(forgiveness, 4),
        "RadicanTrust":  score,
        "pass":          bool(score >= 0.60),
    }

def render(G, data, obs, mut, res, gen, out_dir):
    layer_colors = data["visualization_hints"]["colors"]
    labels = {n: G.nodes[n]["label"] for n in G.nodes}
    edge_labels = nx.get_edge_attributes(G, "label")
    node_color_map = [layer_colors.get(G.nodes[n]["layer"], "#cccccc")
                      for n in G.nodes]
    node_sizes = [1800 + obs["pagerank"][n] * 15000 for n in G.nodes]
    edge_widths = [min(0.8 + (obs["betweenness"].get(u, 0) +
                               obs["betweenness"].get(v, 0)) * 6, 4.0)
                   for u, v in G.edges()]

    pos = nx.spring_layout(G, seed=mut["layout_seed"], k=mut["k_spring"])

    fig, ax = plt.subplots(figsize=(20, 14))
    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")

    nx.draw_networkx_nodes(G, pos, node_color=node_color_map,
                           node_size=node_sizes, alpha=0.93, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7.5,
                            font_color="#111111", font_weight="bold", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="#bbbbbb", width=edge_widths,
                           arrows=True, arrowsize=20,
                           connectionstyle="arc3,rad=0.10", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                  font_size=5.5, font_color="#eeeeee", ax=ax)

    legend_patches = [mpatches.Patch(color=c, label=l)
                      for l, c in layer_colors.items()]
    ax.legend(handles=legend_patches, loc="lower left", framealpha=0.4,
              facecolor="#222222", edgecolor="#555555",
              labelcolor="white", fontsize=9)

    subtitle = (f"Gen {gen}  |  RadicanTrust={res['RadicanTrust']}  |  "
                f"Nodes={obs['n_nodes']}  Edges={obs['n_edges']}  "
                f"Density={obs['density']}  |  seed={mut['layout_seed']}")
    ax.set_title(f"{data['title']}\n{subtitle}",
                 fontsize=10, color="#dddddd", pad=12)
    ax.axis("off")
    plt.tight_layout()

    out_png = os.path.join(out_dir, f"quantum_trust_graph_gen{gen}.png")
    plt.savefig(out_png, dpi=200, bbox_inches="tight", facecolor="#111111")
    plt.close()
    return out_png

def save_log(gen, obs, mut, res, out_dir):
    log = {
        "generation": gen,
        "timestamp": datetime.datetime.now().isoformat(),
        "observation": obs,
        "mutation": mut,
        "resonance": res,
        "next_seed_hint": {
            "suggested_mutation": (
                "Add cross-layer edges if RadicanTrust < 0.7"
                if not res["pass"] else
                "Fine-tune k_spring by +0.1 to reduce edge crossings"
            ),
            "next_k_spring": round(mut["k_spring"] + 0.1, 2),
        },
    }
    path = os.path.join(out_dir, f"mutation_log_gen{gen}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gen", type=int, default=2)
    args = parser.parse_args()

    data = load_graph(YAML_FILE)
    G, node_color_map, layer_map, layer_colors = build_nx(data)
    obs  = observe(G)
    mut  = mutate(obs)
    res  = resonate(G, obs, layer_map)
    png  = render(G, data, obs, mut, res, args.gen, OUTPUT_DIR)
    log  = save_log(args.gen, obs, mut, res, OUTPUT_DIR)

    print(f"✅ Gen {args.gen} complete")
    print(f"   PNG  → {png}")
    print(f"   LOG  → {log}")
    print(f"   RadicanTrust = {res['RadicanTrust']} ({'PASS' if res['pass'] else 'MUTATE'})")
    print(f"   Next hint    : {log}")
