# Phase 0 Read-only Audit

Status: completed as a documentation-only review.

No source file, canonical YAML, renderer, generated artifact, or external integration was modified during the audit.

## Repository Responsibility

`bana-quantum-graph-` is the implementation repository for the current QuantumTrust graph schema, rendering, structural metrics, and artifact export.

It is not the canonical owner of the entire QuantumArt Protocol, scientific terminology, provenance review, or publication history.

Related responsibility map:

- `quantumart-protocol-2026-official`: protocol, terminology, claim boundaries, OARS, ethics
- `BananaSpace-Infra-Seeds`: experimental seeds, recursive prompts, proposals, lineage origins
- `BananaBot`: interaction, observation capture, story carrier, command interface
- `bana-quantum-graph-`: graph schema, rendering, structural metrics, artifact export
- `BananaMoon-QuantumTrust-Review`: provenance review, CID review, historical preservation, boundary audit
- Notion: human-readable tracking, research dashboard, narrative context

## Canonical Source Definition

`quantum_trust_graph.yaml` is the repository-local canonical source for the current graph representation.

This does not make it a universal definition of beauty, trust, quantum theory, or the complete QuantumArt Protocol.

Recommended rule:

- ordinary experiments do not rewrite the canonical graph,
- experiments are expressed as append-only overlays,
- a canonical revision requires an explicit reviewed Pull Request, reason, diff, and version change.

## `render.py` Legacy Status

`render.py` is a small legacy renderer.

Observed properties:

- reads `quantum_trust_graph.yaml`,
- uses `yaml.safe_load`,
- builds a `networkx.DiGraph`,
- uses a fixed layout seed,
- writes `quantum_trust_graph.png`,
- does not modify the YAML source.

Limitations:

- no explicit schema validation,
- limited error handling,
- no overlay support,
- no provenance record,
- no explicit scientific or metaphorical claim boundary.

Decision: preserve as a legacy entrypoint. Do not promote it as the current integration path.

## `render_v2.py` Current Status

`render_v2.py` is the current recommended implementation.

Observed strengths:

- validates graph structure,
- rejects duplicate node IDs,
- rejects unknown edge references,
- validates overlay contract fields,
- applies overlays to a deep copy in memory,
- states and records `canonical_graph_mutated: false`,
- supports dry-run validation,
- uses deterministic graph-derived layout parameters,
- labels the RadicanTrust result as `structural_heuristic`,
- states `is_quantum_probability: false`,
- emits PNG and JSON generation artifacts.

Current limitations:

- generated files do not yet include mandatory SHA-256 fields,
- the log timestamp changes on each run, so the complete JSON output hash is not deterministic even when graph-derived values are stable,
- the term `Self-Evolution Engine` can be misread as a biological or autonomous claim,
- publication adapters are not implemented as separate contracts.

## README vs Implementation Consistency

Confirmed inconsistency:

README currently documents:

```text
experiment YAML
→ adapter merge
→ canonical YAML updated
```

`render_v2.py` implements:

```text
immutable canonical YAML
+
append-only overlay
→ memory-only composition
→ generated artifacts
```

The implementation is more consistent with the stated non-destructive principle.

Recommended alignment: document the memory-only overlay model as the default. Treat canonical edits as separately reviewed versioned revisions.

## Adapter Mutation Policy

Recommended policy:

- transformation adapters are stateless,
- published inputs and outputs are not overwritten,
- overlays are append-only,
- transformation adapters should be deterministic when the transformation permits it,
- publication adapters may be non-deterministic because external systems assign IDs, timestamps, or URLs,
- external publication identifiers supplement but do not replace artifact hashes.

## Scientific and Metaphorical Claim Boundaries

Every relevant claim should be classified as one of:

- `physical`
- `computational`
- `empirical`
- `metaphorical`

Current graph terms such as RadicanTrust, Resonance, Forgiveness, Four Doors, and quantum-inspired language must not be presented as physical observables or universal measures without independent evidence.

The current RadicanTrust output is a project-specific structural heuristic, not a quantum probability, personality score, legal finding, or universal trust measurement.

## Audit Conclusion

Recommended architecture:

```text
immutable canonical graph
+
append-only overlays
+
stateless transformation adapters
+
separate publication adapters
+
provenance records
```

Guiding sentence:

> 壊さずに変化させ、変化の証拠を残し、その証拠を次の創造へ返すこと。
