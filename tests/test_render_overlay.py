from __future__ import annotations

import copy
import unittest

import networkx as nx

import render_v2


class RenderOverlayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = {
            "title": "Test Graph",
            "nodes": [
                {"id": "RT_index", "label": "RT", "layer": "RadicanTrust"},
                {"id": "prompt_pool", "label": "Pool", "layer": "IYQ2025"},
                {"id": "quantum_glimmer", "label": "Glimmer", "layer": "IYQ2025"},
            ],
            "edges": [
                {"from": "RT_index", "to": "prompt_pool", "label": "base"}
            ],
            "visualization_hints": {
                "colors": {
                    "RadicanTrust": "#FFD700",
                    "IYQ2025": "#FF4500",
                }
            },
        }
        self.overlay = {
            "adapter_contract": {
                "id": "quantumart-to-bana-graph.v0.1",
                "mode": "append_only_experiment",
                "canonical_graph_mutated": False,
                "human_review_required_before_merge": True,
            },
            "source_refs": {
                "protocol": {"sha256": "a" * 64},
                "seed": {"sha256": "b" * 64},
            },
            "nodes": [
                {
                    "id": "qa_seed_test",
                    "label": "Seed: Test",
                    "layer": "QuantumArt",
                    "desc": "test",
                }
            ],
            "edges": [
                {
                    "from": "qa_seed_test",
                    "to": "prompt_pool",
                    "label": "proposes prompt",
                },
                {
                    "from": "qa_seed_test",
                    "to": "quantum_glimmer",
                    "label": "visualization seed",
                },
            ],
            "_provenance": {"review_status": "pending_human_review"},
        }

    def test_apply_overlay_does_not_mutate_base(self) -> None:
        before = copy.deepcopy(self.base)
        merged, meta = render_v2.apply_overlay(self.base, self.overlay)

        self.assertEqual(self.base, before)
        self.assertEqual(len(merged["nodes"]), len(before["nodes"]) + 1)
        self.assertEqual(len(merged["edges"]), len(before["edges"]) + 2)
        self.assertFalse(meta["canonical_graph_mutated"])
        self.assertEqual(meta["review_status"], "pending_human_review")

    def test_overlay_adds_quantumart_palette(self) -> None:
        merged, _meta = render_v2.apply_overlay(self.base, self.overlay)
        self.assertEqual(
            merged["visualization_hints"]["colors"]["QuantumArt"],
            "#FFD54F",
        )

    def test_duplicate_node_is_rejected(self) -> None:
        duplicate = copy.deepcopy(self.overlay)
        duplicate["nodes"][0]["id"] = "RT_index"
        with self.assertRaisesRegex(ValueError, "already exists"):
            render_v2.apply_overlay(self.base, duplicate)

    def test_unknown_edge_target_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.overlay)
        invalid["edges"][0]["to"] = "missing-node"
        with self.assertRaisesRegex(ValueError, "unknown node"):
            render_v2.apply_overlay(self.base, invalid)

    def test_structural_score_is_not_quantum_probability(self) -> None:
        merged, _meta = render_v2.apply_overlay(self.base, self.overlay)
        graph, _colors, layer_map, _palette = render_v2.build_nx(merged)
        self.assertIsInstance(graph, nx.DiGraph)
        observation = render_v2.observe(graph)
        result = render_v2.resonate(graph, observation, layer_map)

        self.assertEqual(result["metric_type"], "structural_heuristic")
        self.assertFalse(result["is_quantum_probability"])


if __name__ == "__main__":
    unittest.main()
