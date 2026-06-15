"""
serve.py — Step A: POST /resonate endpoint
BananaSpace × RadicanTrust — Non-Destructive Resonance Architecture v1.0

Design principle:
  render_v2.py is NOT imported or modified.
  This file imports ONLY the pure functions from render_v2.py:
    load_graph, build_nx, observe, mutate, resonate
  The Flask app is ADDITIVE — it wraps the existing O→M→R pipeline.

Usage:
  pip install flask
  python serve.py
  # then: POST http://localhost:5050/resonate

Endpoint:
  POST /resonate
  Body (JSON, optional): { "gen": 3, "yaml_file": "quantum_trust_graph.yaml" }
  Response (JSON):
    {
      "generation": 3,
      "observation": { ... },
      "mutation": { ... },
      "resonance": { "RadicanTrust": 0.72, "pass": true, ... },
      "timestamp": "2026-06-15T..."
    }

NOTE:
  - No PNG is rendered in this mode (Agg backend not needed for API use).
  - No file is written (dry API mode). File writing is Step B (PostgreSQL).
  - Secrets: set BANA_YAML env var to override default yaml path.
"""

from __future__ import annotations

import datetime
import os

from flask import Flask, jsonify, request

# Import ONLY the pure functions — render_v2.py main() is NOT called
from render_v2 import load_graph, build_nx, observe, mutate, resonate

app = Flask(__name__)

DEFAULT_YAML: str = os.environ.get("BANA_YAML", "quantum_trust_graph.yaml")


@app.route("/resonate", methods=["POST"])
def resonate_endpoint():
    """Run O→M→R pipeline and return JSON. No side effects (no PNG, no DB)."""
    body = request.get_json(silent=True) or {}
    gen: int = int(body.get("gen", 2))
    yaml_file: str = body.get("yaml_file", DEFAULT_YAML)

    try:
        # O: Observe
        data = load_graph(yaml_file)
        G, _, layer_map, _ = build_nx(data)
        obs = observe(G)

        # M: Mutate
        mut = mutate(obs)

        # R: Resonate
        res = resonate(G, obs, layer_map)

        return jsonify({
            "generation":  gen,
            "timestamp":   datetime.datetime.now().isoformat(),
            "observation": obs,
            "mutation":    mut,
            "resonance":   res,
        }), 200

    except SystemExit as exc:
        # load_graph calls sys.exit on YAML error — catch and return 400
        return jsonify({"error": f"YAML load failed: {exc}"}), 400
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Liveness check."""
    return jsonify({"status": "ok", "step": "A", "version": "1.0.0"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"🍌 BananaBot serve.py — Step A running on http://localhost:{port}")
    print(f"   YAML: {DEFAULT_YAML}")
    print("   POST /resonate  →  O→M→R pipeline (no PNG, no DB)")
    app.run(host="0.0.0.0", port=port, debug=False)
