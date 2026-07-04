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
  python render_v2.py --dry-run
  python render_v2.py --colorblind
  python render_v2.py --overlay experiments/quantumart_seed.yaml --gen 4

The optional overlay is merged in memory only. The canonical YAML file is never
rewritten by this renderer.

Requires: networkx matplotlib pyyaml numpy
"""

from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

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
    "ThoughtArchive": "#0072B2", # blue
    "QuantumArt":   "#F0E442",   # yellow
}

GraphData = Dict[str, Any]
ObsResult = Dict[str, Any]
MutResult = Dict[str, Any]
ResResult = Dict[str, Any]
OverlayData = Dict[str, Any]


# ── O: Observe ────────────────────────────────────────────────────────────────
def load_graph(yaml_file: str) -> GraphData:
    """Load and validate quantum_trust_graph.yaml. Non-destructive read."""
    try:
        with open(yaml_file, encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        if not isinstance(raw, dict) or "quantum_trust_graph_art" not in raw:
            raise KeyError("Missing top-level key 'quantum_trust_graph_art'")
        data = raw["quantum_trust_graph_art"]
        _validate_schema(data)
        return data
    except FileNotFoundError:
        print(f"[ERROR] YAML not found: {yaml_file}", file=sys.stderr)
        raise SystemExit(1)
    except (KeyError, ValueError, yaml.YAMLError) as exc:
        print(f"[ERROR] YAML schema: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _validate_schema(data: GraphData) -> None:
    """Minimal schema guard — raise ValueError on missing keys."""
    if not isinstance(data, dict):
        raise ValueError("Graph data must be a mapping")

    required = ("title", "nodes", "edges", "visualization_hints")
    for key in required:
        if key not in data:
            raise ValueError(f"Missing required field: '{key}'")

    if not isinstance(data["nodes"], list) or not isinstance(data["edges"], list):
        raise ValueError("'nodes' and 'edges' must be lists")

    node_ids: set[str] = set()
    for node in data["nodes"]:
        if not isinstance(node, dict):
            raise ValueError(f"Node must be a mapping: {node!r}")
        for field in ("id", "label", "layer"):
            if field not in node:
                raise ValueError(f"Node missing field '{field}': {node}")
        node_id = str(node["id"])
        if node_id in node_ids:
            raise ValueError(f"Duplicate node id: {node_id}")
        node_ids.add(node_id)

    for edge in data["edges"]:
        if not isinstance(edge, dict):
            raise ValueError(f"Edge must be a mapping: {edge!r}")
        for field in ("from", "to"):
            if field not in edge:
                raise ValueError(f"Edge missing field '{field}': {edge}")
        if str(edge["from"]) not in node_ids or str(edge["to"]) not in node_ids:
            raise ValueError(f"Edge references an unknown node: {edge}")

    hints = data["visualization_hints"]
    if not isinstance(hints, dict) or not isinstance(hints.get("colors"), dict):
        raise ValueError("visualization_hints.colors must be a mapping")


def load_overlay(path: str) -> OverlayData:
    """Load an append-only experiment overlay without modifying the source file."""
    try:
        with open(path, encoding="utf-8") as handle:
            raw = yaml.safe_load(handle)
    except FileNotFoundError:
        raise ValueError(f"Overlay not found: {path}")
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"Could not read overlay {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError("Overlay top-level value must be a mapping")

    contract = raw.get("adapter_contract")
    if not isinstance(contract, dict):
        raise ValueError("Overlay must contain adapter_contract")
    if contract.get("mode") != "append_only_experiment":
        raise ValueError("Overlay adapter_contract.mode must be append_only_experiment")
    if contract.get("canonical_graph_mutated") is not False:
        raise ValueError("Overlay must declare canonical_graph_mutated: false")

    nodes = raw.get("nodes")
    edges = raw.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("Overlay nodes and edges must be lists")

    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError(f"Overlay node must be a mapping: {node!r}")
        for field in ("id", "label", "layer"):
            if field not in node:
                raise ValueError(f"Overlay node missing field '{field}': {node}")

    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError(f"Overlay edge must be a mapping: {edge!r}")
        for field in ("from", "to"):
            if field not in edge:
                raise ValueError(f"Overlay edge missing field '{field}': {edge}")

    return raw


def apply_overlay(base: GraphData, overlay: OverlayData) -> Tuple[GraphData, Dict[str, Any]]:
    """Return a deep-copied graph with an experiment overlay applied in memory."""
    merged = copy.deepcopy(base)
    existing_ids = {str(node["id"]) for node in merged["nodes"]}
    added_ids: set[str] = set()

    for node in overlay["nodes"]:
        node_id = str(node["id"])
        if node_id in existing_ids or node_id in added_ids:
            raise ValueError(f"Overlay node id already exists: {node_id}")
        merged["nodes"].append(copy.deepcopy(node))
        added_ids.add(node_id)

    all_ids = existing_ids | added_ids
    existing_edges = {
        (str(edge["from"]), str(edge["to"]), str(edge.get("label", "")))
        for edge in merged["edges"]
    }

    added_edge_count = 0
    for edge in overlay["edges"]:
        source = str(edge["from"])
        target = str(edge["to"])
        if source not in all_ids or target not in all_ids:
            raise ValueError(f"Overlay edge references an unknown node: {edge}")
        key = (source, target, str(edge.get("label", "")))
        if key in existing_edges:
            continue
        merged["edges"].append(copy.deepcopy(edge))
        existing_edges.add(key)
        added_edge_count += 1

    colors = merged["visualization_hints"]["colors"]
    colors.setdefault("QuantumArt", "#FFD54F")

    contract = overlay["adapter_contract"]
    provenance = overlay.get("_provenance", {})
    overlay_meta = {
        "adapter_id": contract.get("id"),
        "mode": contract.get("mode"),
        "nodes_added": len(added_ids),
        "edges_added": added_edge_count,
        "source_refs": overlay.get("source_refs", {}),
        "review_status": provenance.get("review_status", "unknown"),
        "canonical_graph_mutated": False,
    }

    _validate_schema(merged)
    return merged, overlay_meta


def build_nx(
    data: GraphData,
    colorblind: bool = False,
) -> Tuple[nx.DiGraph, List[str], Dict[str, str], Dict[str, str]]:
    """Build NetworkX DiGraph from YAML data."""
    palette = (
        dict(COLORBLIND_PALETTE)
        if colorblind
        else dict(data["visualization_hints"]["colors"])
    )
    G = nx.DiGraph()
    node_color_map: List[str] = []
    layer_map: Dict[str, str] = {}

    for node in data["nodes"]:
        nid = str(node["id"])
        G.add_node(nid, label=str(node["label"]), layer=str(node["layer"]))
        layer_map[nid] = str(node["layer"])
        node_color_map.append(palette.get(str(node["layer"]), "#cccccc"))

    for edge in data["edges"]:
        G.add_edge(
            str(edge["from"]),
            str(edge["to"]),
            label=str(edge.get("label", "")),
        )

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
        "pagerank": {k: float(v) for k, v in pagerank.items()},
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
    for node_id in G.nodes:
        layer = layer_map[node_id]
        counts[layer] = counts.get(layer, 0) + 1
    std = float(np.std(list(counts.values())))
    max_count = max(counts.values()) if counts else 1
    inclusivity: float = float(1.0 - std / max_count)

    bidirectional = sum(1 for source, target in G.edges() if G.has_edge(target, source))
    reciprocity_value: float = bidirectional / max(G.number_of_edges(), 1)

    forgiveness: float = 1.0 - obs["density"]

    score = round(
        (transparency + inclusivity + reciprocity_value + forgiveness) / 4,
        4,
    )
    return {
        "transparency": round(transparency, 4),
        "inclusivity": round(inclusivity, 4),
        "reciprocity": round(reciprocity_value, 4),
        "forgiveness": round(forgiveness, 4),
        "RadicanTrust": score,
        "metric_type": "structural_heuristic",
        "is_quantum_probability": False,
        "pass": bool(score >= 0.60),
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
    overlay_meta: Optional[Dict[str, Any]] = None,
) -> str:
    """Render graph to PNG. Returns output path."""
    labels = {node_id: G.nodes[node_id]["label"] for node_id in G.nodes}
    edge_labels = nx.get_edge_attributes(G, "label")

    node_color_map = [
        palette.get(G.nodes[node_id]["layer"], "#cccccc") for node_id in G.nodes
    ]
    node_sizes = [1800 + obs["pagerank"][node_id] * 15000 for node_id in G.nodes]
    edge_widths = [
        min(
            0.8
            + (
                obs["betweenness"].get(source, 0)
                + obs["betweenness"].get(target, 0)
            )
            * 6,
            4.0,
        )
        for source, target in G.edges()
    ]

    positions = nx.spring_layout(
        G,
        seed=mut["layout_seed"],
        k=mut["k_spring"],
    )

    fig, ax = plt.subplots(figsize=(20, 14))
    fig.patch.set_facecolor("#111111")
    ax.set_facecolor("#111111")

    nx.draw_networkx_nodes(
        G,
        positions,
        node_color=node_color_map,
        node_size=node_sizes,
        alpha=0.93,
        ax=ax,
    )
    nx.draw_networkx_labels(
        G,
        positions,
        labels=labels,
        font_size=7.5,
        font_color="#111111",
        font_weight="bold",
        ax=ax,
    )
    nx.draw_networkx_edges(
        G,
        positions,
        edge_color="#bbbbbb",
        width=edge_widths,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.10",
        ax=ax,
    )
    nx.draw_networkx_edge_labels(
        G,
        positions,
        edge_labels=edge_labels,
        font_size=5.5,
        font_color="#eeeeee",
        ax=ax,
    )

    used_layers = {G.nodes[node_id]["layer"] for node_id in G.nodes}
    legend_patches = [
        mpatches.Patch(color=color, label=layer)
        for layer, color in palette.items()
        if layer in used_layers
    ]
    ax.legend(
        handles=legend_patches,
        loc="lower left",
        framealpha=0.4,
        facecolor="#222222",
        edgecolor="#555555",
        labelcolor="white",
        fontsize=9,
    )

    subtitle = (
        f"Gen {gen}  |  RadicanTrust={res['RadicanTrust']}  |  "
        f"Nodes={obs['n_nodes']}  Edges={obs['n_edges']}  "
        f"Density={obs['density']}  |  seed={mut['layout_seed']}"
    )
    if overlay_meta:
        subtitle += (
            f"  |  overlay={overlay_meta.get('adapter_id', 'unknown')}"
            f" (+{overlay_meta.get('nodes_added', 0)} nodes)"
        )

    ax.set_title(
        f"{data['title']}\n{subtitle}",
        fontsize=10,
        color="#dddddd",
        pad=12,
    )
    ax.axis("off")
    plt.tight_layout()

    suffix = "_overlay" if overlay_meta else ""
    out_png = os.path.join(
        out_dir,
        f"quantum_trust_graph_gen{gen}{suffix}.png",
    )
    try:
        plt.savefig(
            out_png,
            dpi=200,
            bbox_inches="tight",
            facecolor="#111111",
        )
    except OSError as exc:
        print(f"[ERROR] Could not save PNG: {exc}", file=sys.stderr)
        raise SystemExit(1)
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
    overlay_meta: Optional[Dict[str, Any]] = None,
) -> str:
    """Serialize full generation state as JSON seed for next cycle."""
    log: Dict[str, Any] = {
        "generation": gen,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "observation": obs,
        "mutation": mut,
        "resonance": res,
        "canonical_graph_mutated": False,
        "next_seed_hint": {
            "suggested_mutation": (
                "Add cross-layer edges to boost reciprocity"
                if not res["pass"]
                else "Fine-tune k_spring by +0.1 to reduce edge crossings"
            ),
            "next_k_spring": round(mut["k_spring"] + 0.1, 2),
        },
    }
    if overlay_meta:
        log["overlay"] = overlay_meta

    suffix = "_overlay" if overlay_meta else ""
    path = os.path.join(out_dir, f"mutation_log_gen{gen}{suffix}.json")
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(log, handle, indent=2, ensure_ascii=False)
    except OSError as exc:
        print(f"[ERROR] Could not write log: {exc}", file=sys.stderr)
        raise SystemExit(1)
    return path


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ara-Philia³ Self-Evolution Engine  P_{n+1}=R(M(O(P_n)))"
    )
    parser.add_argument(
        "--gen",
        type=int,
        default=2,
        help="Generation number (default: 2)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate YAML and optional overlay only; do not render",
    )
    parser.add_argument(
        "--colorblind",
        action="store_true",
        help="Use Okabe–Ito colorblind-safe palette",
    )
    parser.add_argument(
        "--overlay",
        help=(
            "Append an adapter experiment YAML in memory for this render. "
            "The canonical graph file is never modified."
        ),
    )
    args = parser.parse_args()

    data = load_graph(YAML_FILE)
    overlay_meta: Optional[Dict[str, Any]] = None

    if args.overlay:
        try:
            data, overlay_meta = apply_overlay(data, load_overlay(args.overlay))
        except ValueError as exc:
            print(f"[ERROR] Overlay schema: {exc}", file=sys.stderr)
            raise SystemExit(1)

    if args.dry_run:
        overlay_note = (
            f", overlay +{overlay_meta['nodes_added']} nodes"
            if overlay_meta
            else ""
        )
        print(
            f"✅ dry-run: YAML valid ({len(data['nodes'])} nodes, "
            f"{len(data['edges'])} edges{overlay_note})"
        )
        print("   canonical graph mutated: false")
        return

    graph, _node_colors, layer_map, palette = build_nx(
        data,
        colorblind=args.colorblind,
    )
    observation = observe(graph)
    mutation = mutate(observation)
    resonance = resonate(graph, observation, layer_map)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    png = render(
        graph,
        data,
        observation,
        mutation,
        resonance,
        args.gen,
        OUTPUT_DIR,
        palette,
        overlay_meta=overlay_meta,
    )
    log = save_log(
        args.gen,
        observation,
        mutation,
        resonance,
        OUTPUT_DIR,
        overlay_meta=overlay_meta,
    )

    print(f"✅ Gen {args.gen} complete")
    print(f"   PNG  → {png}")
    print(f"   LOG  → {log}")
    print(
        f"   RadicanTrust = {resonance['RadicanTrust']} "
        f"({'PASS 🕊️' if resonance['pass'] else 'MUTATE 🌱'})"
    )
    print("   Metric type → structural_heuristic")
    print("   Quantum probability → false")
    print("   Canonical graph mutated → false")


if __name__ == "__main__":
    main()
