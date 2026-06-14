"""
render_v2.py — Ara-Philia³ Self-Evolution Engine
P_{n+1} = R(M(O(P_n)))

Each run:
  O = Observe:  compute graph metrics (betweenness, pagerank, density)
  M = Mutate:   adapt layout seed / node sizes / edge widths from metrics
  R = Resonate: calculate RadicanTrust score (0.0–1.0)
  P_{n+1}:      save mutation_log_gen{N}.json as seed for next generation

Usage:
  python render_v2.py
  python render_v2.py --gen 3
  python render_v2.py --dry-run        # validate YAML only, no render
  python render_v2.py --colorblind     # accessible palette

Requires: networkx matplotlib pyyaml numpy
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sys
from typing import Any, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import yaml

# ── Config (override via environment variables) ──────────────────────────────
YAML_FILE: str = os.environ.get("BANA_YAML", "quantum_trust_graph.yaml")
OUTPUT_DIR: str = os.environ.get("BANA_OUT", ".")

# Colorblind-safe palette (Okabe–Ito)
COLORBLIND_PALETTE: Dict[str, str] = {
    "RadicanTrust": "#E69F00",   # amber
    "FourDoors":    "#56B4E9",   # sky blue
    "IYQ2025":      "#009E73",   # green
    "Meta":         "#CC79A7",   # pink-purple
}

GraphData = Dict[str, Any]
ObsResult = Dict[str, Any]
MutResult = Dict[str, Any]
ResResult = Dict[str, Any]


# ── O: Observe ────────────────────────────────────────────────────────────────
def load_graph(yaml_file: str) -> GraphData:
    """Load and validate quantum_trust_graph.yaml. Non-destructive read."""
    try:
        with open(yaml_file, encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        if "quantum_trust_graph_art" not in raw:
            raise KeyError("Missing top-level key 'quantum_trust_graph_art'")
        data = raw["quantum_trust_graph_art"]
        _validate_schema(data)
        return data
    except FileNotFoundError:
        print(f"[ERROR] YAML not found: {yaml_file}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, ValueError) as exc:
        print(f"[ERROR] YAML schema: {exc}", file=sys.stderr)
        sys.exit(1)


def _validate_schema(data: GraphData) -> None:
    """Minimal schema guard — raise ValueError on missing keys."""
    required = ("title", "nodes", "edges", "visualization_hints")
    for key in required:
        if key not in data:
            raise ValueError(f"Missing required field: '{key}'")
    for node in data["nodes"]:
        for field in ("id", "label", "layer"):
            if field not in node:
                raise ValueError(f"Node missing field '{field}': {node}")
    for edge in data["edges"]:
        for field in ("from", "to"):
            if field not in edge:
                raise ValueError(f"Edge missing field '{field}': {edge}")


def build_nx(
    data: GraphData,
    colorblind: bool = False,
) -> Tuple[nx.DiGraph, List[str], Dict[str, str], Dict[str, str]]:
    """Build NetworkX DiGraph from YAML data."""
    palette = COLORBLIND_PALETTE if colorblind else data["visualization_hints"]["colors"]
    G = nx.DiGraph()
    node_color_map: List[str] = []
    layer_map: Dict[str, str] = {}

    for node in data["nodes"]:
        nid = node["id"]
        G.add_node(nid, label=node["label"], layer=node["layer"])
        layer_map[nid] = node["layer"]
        node_color_map.append(palette.get(node["layer"], "#cccccc"))

    for edge in data["edges"]:
        G.add_edge(edge["from"], edge["to"], label=edge.get("label", ""))

    return G, node_color_map, layer_map, palette


def observe(G: nx.DiGraph) -> ObsResult:
    """Compute structural metrics — pure function, no side effects."""
    betweenness: Dict[str, float] = nx.betweenness_centrality(G)
    pagerank: Dict[str, float] = nx.pagerank(G)

    return {
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "density": round(nx.density(G), 4),
        "top_betweenness": [
            (k, round(float(v), 4))
            for k, v in sorted(betweenness.items(), key=lambda x: -x[1])[:3]
        ],
        "top_pagerank": [
            (k, round(float(v), 4))
            for k, v in sorted(pagerank.items(), key=lambda x: -x[1])[:3]
        ],
        "betweenness": {k: float(v) for k, v in betweenness.items()},
        "pagerank":    {k: float(v) for k, v in pagerank.items()},
    }


# ── M: Mutate ─────────────────────────────────────────────────────────────────
def mutate(obs: ObsResult) -> MutResult:
    """Derive layout parameters from observation. blake2b for reproducibility."""
    fingerprint = str(obs["top_pagerank"]).encode()
    seed_val = (
        int(hashlib.blake2b(fingerprint, digest_size=4).hexdigest(), 16) % 1000
    )
    k_spring = round(2.8 + (1 - obs["density"]) * 0.4, 2)
    return {"layout_seed": seed_val, "k_spring": k_spring}


# ── R: Resonate ───────────────────────────────────────────────────────────────
def resonate(
    G: nx.DiGraph,
    obs: ObsResult,
    layer_map: Dict[str, str],
) -> ResResult:
    """RadicanTrust = mean(transparency, inclusivity, reciprocity, forgiveness)."""
    labeled = sum(1 for _, _, d in G.edges(data=True) if d.get("label", ""))
    transparency: float = labeled / max(G.number_of_edges(), 1)

    counts: Dict[str, int] = {}
    for n in G.nodes:
        layer = layer_map[n]
        counts[layer] = counts.get(layer, 0) + 1
    std = float(np.std(list(counts.values())))
    max_count = max(counts.values()) if counts else 1
    inclusivity: float = float(1.0 - std / max_count)

    bi = sum(1 for u, v in G.edges() if G.has_edge(v, u))
    reciprocity_val: float = bi / max(G.number_of_edges(), 1)

    forgiveness: float = 1.0 - obs["density"]

    score = round((transparency + inclusivity + reciprocity_val + forgiveness) / 4, 4)
    return {
        "transparency": round(transparency, 4),
        "inclusivity":  round(inclusivity, 4),
        "reciprocity":  round(reciprocity_val, 4),
        "forgiveness":  round(forgiveness, 4),
        "RadicanTrust": score,
        "pass":         bool(score >= 0.60),
    }


# ── Render ────────────────────────────────────────────────────────────────────
def render(
    G: nx.DiGraph,
    data: GraphData,
    obs: ObsResult,
    mut: MutResult,
    res: ResResult,
    gen: int,
    out_dir: str,
    palette: Dict[str, str],
) -> str:
    """Render graph to PNG. Returns output path."""
    labels = {n: G.nodes[n]["label"] for n in G.nodes}
    edge_labels = nx.get_edge_attributes(G, "label")

    node_color_map = [palette.get(G.nodes[n]["layer"], "#cccccc") for n in G.nodes]
    node_sizes     = [1800 + obs["pagerank"][n] * 15000 for n in G.nodes]
    edge_widths    = [
        min(0.8 + (obs["betweenness"].get(u, 0) + obs["betweenness"].get(v, 0)) * 6, 4.0)
        for u, v in G.edges()
    ]

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

    legend_patches = [mpatches.Patch(color=c, label=l) for l, c in palette.items()]
    ax.legend(handles=legend_patches, loc="lower left", framealpha=0.4,
              facecolor="#222222", edgecolor="#555555", labelcolor="white", fontsize=9)

    subtitle = (
        f"Gen {gen}  |  RadicanTrust={res['RadicanTrust']}  |  "
        f"Nodes={obs['n_nodes']}  Edges={obs['n_edges']}  "
        f"Density={obs['density']}  |  seed={mut['layout_seed']}"
    )
    ax.set_title(f"{data['title']}\n{subtitle}", fontsize=10, color="#dddddd", pad=12)
    ax.axis("off")
    plt.tight_layout()

    out_png = os.path.join(out_dir, f"quantum_trust_graph_gen{gen}.png")
    try:
        plt.savefig(out_png, dpi=200, bbox_inches="tight", facecolor="#111111")
    except OSError as exc:
        print(f"[ERROR] Could not save PNG: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        plt.close()

    return out_png


# ── P_{n+1}: Save evolution log ───────────────────────────────────────────────
def save_log(
    gen: int,
    obs: ObsResult,
    mut: MutResult,
    res: ResResult,
    out_dir: str,
) -> str:
    """Serialize full generation state as JSON seed for next cycle."""
    log: Dict[str, Any] = {
        "generation": gen,
        "timestamp":  datetime.datetime.now().isoformat(),
        "observation": obs,
        "mutation":    mut,
        "resonance":   res,
        "next_seed_hint": {
            "suggested_mutation": (
                "Add cross-layer edges to boost reciprocity"
                if not res["pass"] else
                "Fine-tune k_spring by +0.1 to reduce edge crossings"
            ),
            "next_k_spring": round(mut["k_spring"] + 0.1, 2),
        },
    }
    path = os.path.join(out_dir, f"mutation_log_gen{gen}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        print(f"[ERROR] Could not write log: {exc}", file=sys.stderr)
        sys.exit(1)
    return path


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ara-Philia³ Self-Evolution Engine  P_{n+1}=R(M(O(P_n)))"
    )
    parser.add_argument("--gen",        type=int,  default=2,
                        help="Generation number (default: 2)")
    parser.add_argument("--dry-run",    action="store_true",
                        help="Validate YAML only — no PNG rendered")
    parser.add_argument("--colorblind", action="store_true",
                        help="Use Okabe–Ito colorblind-safe palette")
    args = parser.parse_args()

    # O
    data = load_graph(YAML_FILE)

    if args.dry_run:
        print(f"✅ dry-run: YAML valid  ({len(data['nodes'])} nodes, "
              f"{len(data['edges'])} edges)")
        return

    G, node_color_map, layer_map, palette = build_nx(data, colorblind=args.colorblind)
    obs = observe(G)

    # M
    mut = mutate(obs)

    # R
    res = resonate(G, obs, layer_map)

    # Render
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    png  = render(G, data, obs, mut, res, args.gen, OUTPUT_DIR, palette)
    log  = save_log(args.gen, obs, mut, res, OUTPUT_DIR)

    print(f"✅ Gen {args.gen} complete")
    print(f"   PNG  → {png}")
    print(f"   LOG  → {log}")
    print(f"   RadicanTrust = {res['RadicanTrust']} "
          f"({'PASS 🕊️' if res['pass'] else 'MUTATE 🌱'})")
    print(f"   Next k_spring → {log}")


if __name__ == "__main__":
    main()
