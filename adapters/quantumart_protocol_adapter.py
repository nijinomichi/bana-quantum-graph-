from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ADAPTER_ID = "quantumart-to-bana-graph.v0.1"
SUPPORTED_PROTOCOL_MAJOR = 1


class AdapterError(ValueError):
    """Raised when protocol or seed input violates the adapter contract."""


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AdapterError(f"Input file not found: {path}") from exc
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise AdapterError(f"Could not read YAML {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise AdapterError(f"Top-level YAML value must be a mapping: {path}")
    return raw


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parse_major(version: str) -> int:
    try:
        return int(version.split(".", 1)[0])
    except (AttributeError, ValueError) as exc:
        raise AdapterError(f"Invalid protocol version: {version!r}") from exc


def _require_mapping(parent: dict[str, Any], key: str, context: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise AdapterError(f"Missing or invalid mapping '{context}.{key}'")
    return value


def _require_string(parent: dict[str, Any], key: str, context: str) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not value.strip():
        raise AdapterError(f"Missing or invalid string '{context}.{key}'")
    return value.strip()


def validate_protocol(raw: dict[str, Any]) -> dict[str, Any]:
    protocol = _require_mapping(raw, "protocol", "root")
    meta = _require_mapping(protocol, "meta", "protocol")

    protocol_id = _require_string(meta, "id", "protocol.meta")
    if protocol_id != "quantumart-protocol":
        raise AdapterError(
            f"Unsupported protocol id {protocol_id!r}; expected 'quantumart-protocol'"
        )

    version = _require_string(meta, "version", "protocol.meta")
    if _parse_major(version) != SUPPORTED_PROTOCOL_MAJOR:
        raise AdapterError(
            f"Unsupported protocol major version {version!r}; "
            f"adapter supports {SUPPORTED_PROTOCOL_MAJOR}.x"
        )

    declared = _require_mapping(protocol, "declared_metadata", "protocol")
    signature = _require_mapping(
        declared, "quantum_signature", "protocol.declared_metadata"
    )
    _require_string(signature, "value", "protocol.declared_metadata.quantum_signature")

    safety = _require_mapping(protocol, "safety_and_ethics", "protocol")
    automatic_demo = _require_mapping(
        safety, "automatic_demo", "protocol.safety_and_ethics"
    )
    if automatic_demo.get("enabled_by_default") is not False:
        raise AdapterError("automatic_demo.enabled_by_default must be false")

    implementation = _require_mapping(protocol, "implementation_state", "protocol")
    if not isinstance(implementation.get("operational_now"), list):
        raise AdapterError("implementation_state.operational_now must be a list")
    if not isinstance(implementation.get("not_yet_operational"), list):
        raise AdapterError("implementation_state.not_yet_operational must be a list")

    return protocol


def validate_seed(raw: dict[str, Any], execute: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    seed = _require_mapping(raw, "seed_prompt", "root")
    execution = _require_mapping(raw, "execution", "root")

    schema_version = _require_string(seed, "schema_version", "seed_prompt")
    if schema_version != "quantumart.seed.v1":
        raise AdapterError(
            f"Unsupported seed schema {schema_version!r}; expected 'quantumart.seed.v1'"
        )

    _require_string(seed, "seed_id", "seed_prompt")
    _require_string(seed, "theme", "seed_prompt")
    _require_string(seed, "desired_feel", "seed_prompt")

    keywords = seed.get("keywords")
    if not isinstance(keywords, list) or not keywords or not all(
        isinstance(item, str) and item.strip() for item in keywords
    ):
        raise AdapterError("seed_prompt.keywords must be a non-empty string list")

    if execution.get("requires_explicit_user_action") is not True:
        raise AdapterError("execution.requires_explicit_user_action must be true")

    if execution.get("automatic_demo_on_silence") is not False:
        raise AdapterError("execution.automatic_demo_on_silence must be false")

    if not execute:
        raise AdapterError(
            "Explicit execution is required. Re-run with --execute after human review."
        )

    return seed, execution


def _node(node_id: str, label: str, desc: str) -> dict[str, str]:
    return {"id": node_id, "label": label, "layer": "QuantumArt", "desc": desc}


def build_experiment(
    protocol: dict[str, Any],
    seed: dict[str, Any],
    protocol_path: Path,
    seed_path: Path,
) -> dict[str, Any]:
    meta = protocol["meta"]
    declared = protocol["declared_metadata"]
    implementation = protocol["implementation_state"]
    safety = protocol["safety_and_ethics"]

    signature = declared["quantum_signature"]["value"]
    trust = declared.get("trust_level", {})
    trust_value = trust.get("value")
    trust_interpretation = trust.get("interpretation", "declared_conceptual_score")

    seed_id = seed["seed_id"]
    theme = seed["theme"]
    desired_feel = seed["desired_feel"]
    keywords = [str(item) for item in seed["keywords"]]

    nodes = [
        _node(
            f"qa_protocol_{seed_id}",
            f"QuantumArt Protocol {meta['version']}",
            "Protocol specification and capability boundary imported read-only.",
        ),
        _node(
            f"qa_seed_{seed_id}",
            f"Seed: {theme}",
            f"Keywords: {', '.join(keywords)} / Feel: {desired_feel}",
        ),
        _node(
            f"qa_consent_{seed_id}",
            "Explicit Consent Gate",
            "Execution requires an explicit human action; silence is not consent.",
        ),
        _node(
            f"qa_capability_{seed_id}",
            "Capability State",
            (
                f"Operational: {len(implementation['operational_now'])}; "
                f"Not operational: {len(implementation['not_yet_operational'])}"
            ),
        ),
    ]

    edges = [
        {
            "from": f"qa_protocol_{seed_id}",
            "to": f"qa_seed_{seed_id}",
            "label": "defines",
            "desc": "Protocol defines the seed contract.",
        },
        {
            "from": f"qa_consent_{seed_id}",
            "to": f"qa_seed_{seed_id}",
            "label": "authorizes",
            "desc": "Explicit action authorizes this adapter run.",
        },
        {
            "from": f"qa_protocol_{seed_id}",
            "to": f"qa_capability_{seed_id}",
            "label": "bounds",
            "desc": "Capability state prevents proposed components from appearing operational.",
        },
        {
            "from": f"qa_seed_{seed_id}",
            "to": "prompt_pool",
            "label": "proposes prompt",
            "desc": "External target in the canonical graph; merge requires human review.",
        },
        {
            "from": f"qa_seed_{seed_id}",
            "to": "quantum_glimmer",
            "label": "visualization seed",
            "desc": "Seed may inform visual composition after review.",
        },
        {
            "from": f"qa_capability_{seed_id}",
            "to": "RT_index",
            "label": "metric boundary",
            "desc": "Declared trust metadata is not included in the graph structural score.",
        },
    ]

    return {
        "adapter_contract": {
            "id": ADAPTER_ID,
            "mode": "append_only_experiment",
            "canonical_graph_mutated": False,
            "human_review_required_before_merge": True,
        },
        "source_refs": {
            "protocol": {
                "repository": "nijinomichi/cophelia3",
                "path": str(protocol_path),
                "id": meta["id"],
                "version": meta["version"],
                "sha256": _sha256(protocol_path),
            },
            "seed": {
                "path": str(seed_path),
                "seed_id": seed_id,
                "schema_version": seed["schema_version"],
                "sha256": _sha256(seed_path),
            },
        },
        "declared_metadata": {
            "quantum_signature": signature,
            "trust_level": trust_value,
            "trust_interpretation": trust_interpretation,
            "audio_or_symbolic_frequency_hz": declared.get(
                "resonance_frequency_hz", {}
            ).get("value"),
        },
        "metric_semantics": {
            "declared_trust_level": {
                "type": "conceptual_metadata",
                "included_in_graph_score": False,
                "empirically_validated": bool(trust.get("empirically_validated", False)),
            },
            "radicantrust_graph": {
                "type": "structural_heuristic",
                "inputs": [
                    "transparency",
                    "inclusivity",
                    "reciprocity",
                    "density_derived_forgiveness",
                ],
                "is_quantum_probability": False,
            },
            "born_rule_probability": {
                "type": "quantum_measurement_probability",
                "computed_by_adapter": False,
            },
        },
        "consent": {
            "explicit_action_recorded": True,
            "automatic_demo_enabled": safety["automatic_demo"]["enabled_by_default"],
            "biometric_processing_requested": False,
        },
        "external_targets": ["prompt_pool", "quantum_glimmer", "RT_index"],
        "nodes": nodes,
        "edges": edges,
        "_provenance": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "adapter_id": ADAPTER_ID,
            "append_only": True,
            "review_status": "pending_human_review",
        },
    }


def write_experiment(data: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Create an append-only bana-quantum-graph experiment from a "
            "QuantumArt Protocol and Seed Prompt."
        )
    )
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Record explicit human authorization and generate the experiment YAML.",
    )
    parser.add_argument(
        "--print-json",
        action="store_true",
        help="Also print the generated experiment as JSON.",
    )
    args = parser.parse_args()

    try:
        protocol = validate_protocol(_load_yaml(args.protocol))
        seed, _execution = validate_seed(_load_yaml(args.seed), execute=args.execute)
        experiment = build_experiment(protocol, seed, args.protocol, args.seed)
        write_experiment(experiment, args.output)
    except AdapterError as exc:
        print(f"[ADAPTER ERROR] {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"[I/O ERROR] {exc}", file=sys.stderr)
        return 3

    print(f"Wrote append-only experiment: {args.output}")
    print("Canonical graph was not modified.")
    print("Human review is required before merge.")

    if args.print_json:
        print(json.dumps(experiment, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
