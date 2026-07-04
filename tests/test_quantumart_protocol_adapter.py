from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "adapters"
    / "quantumart_protocol_adapter.py"
)
SPEC = importlib.util.spec_from_file_location("quantumart_protocol_adapter", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load adapter module from {MODULE_PATH}")
ADAPTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPTER)


class QuantumArtProtocolAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.protocol_path = self.root / "protocol.yaml"
        self.seed_path = self.root / "seed.yaml"

        self.protocol_data = {
            "protocol": {
                "meta": {
                    "id": "quantumart-protocol",
                    "version": "1.0.0",
                },
                "declared_metadata": {
                    "quantum_signature": {"value": "test-signature"},
                    "resonance_frequency_hz": {"value": 528},
                    "trust_level": {
                        "value": 0.92,
                        "interpretation": "declared_conceptual_score",
                        "empirically_validated": False,
                    },
                },
                "safety_and_ethics": {
                    "automatic_demo": {"enabled_by_default": False}
                },
                "implementation_state": {
                    "operational_now": ["seed_prompt_schema"],
                    "not_yet_operational": ["EEG emotion mapping"],
                },
            }
        }
        self.seed_data = {
            "seed_prompt": {
                "schema_version": "quantumart.seed.v1",
                "seed_id": "test-seed",
                "theme": "Forgiving Dark Matter",
                "keywords": ["AI", "赦し"],
                "desired_feel": "静かな高揚",
            },
            "execution": {
                "requires_explicit_user_action": True,
                "automatic_demo_on_silence": False,
            },
        }

        self.protocol_path.write_text(
            yaml.safe_dump(self.protocol_data, allow_unicode=True),
            encoding="utf-8",
        )
        self.seed_path.write_text(
            yaml.safe_dump(self.seed_data, allow_unicode=True),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_explicit_execution_is_required(self) -> None:
        with self.assertRaisesRegex(ADAPTER.AdapterError, "Explicit execution"):
            ADAPTER.validate_seed(self.seed_data, execute=False)

    def test_build_experiment_separates_metric_meanings(self) -> None:
        protocol = ADAPTER.validate_protocol(self.protocol_data)
        seed, _execution = ADAPTER.validate_seed(self.seed_data, execute=True)
        result = ADAPTER.build_experiment(
            protocol,
            seed,
            self.protocol_path,
            self.seed_path,
        )

        declared = result["metric_semantics"]["declared_trust_level"]
        graph = result["metric_semantics"]["radicantrust_graph"]
        born = result["metric_semantics"]["born_rule_probability"]

        self.assertEqual(declared["type"], "conceptual_metadata")
        self.assertFalse(declared["included_in_graph_score"])
        self.assertEqual(graph["type"], "structural_heuristic")
        self.assertFalse(graph["is_quantum_probability"])
        self.assertFalse(born["computed_by_adapter"])

    def test_canonical_graph_is_never_marked_mutated(self) -> None:
        protocol = ADAPTER.validate_protocol(self.protocol_data)
        seed, _execution = ADAPTER.validate_seed(self.seed_data, execute=True)
        result = ADAPTER.build_experiment(
            protocol,
            seed,
            self.protocol_path,
            self.seed_path,
        )

        contract = result["adapter_contract"]
        self.assertEqual(contract["mode"], "append_only_experiment")
        self.assertFalse(contract["canonical_graph_mutated"])
        self.assertTrue(contract["human_review_required_before_merge"])
        self.assertEqual(result["_provenance"]["review_status"], "pending_human_review")

    def test_automatic_demo_must_be_disabled(self) -> None:
        self.protocol_data["protocol"]["safety_and_ethics"]["automatic_demo"][
            "enabled_by_default"
        ] = True
        with self.assertRaisesRegex(ADAPTER.AdapterError, "enabled_by_default"):
            ADAPTER.validate_protocol(self.protocol_data)


if __name__ == "__main__":
    unittest.main()
