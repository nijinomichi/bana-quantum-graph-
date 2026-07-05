# ADR-001: Non-Destructive Adapter Model

Status: proposed

Related issue: #4

## Context

The repository currently contains two integration models:

1. README examples that merge experiment data into `quantum_trust_graph.yaml`.
2. `render_v2.py`, which applies experiment overlays in memory and never rewrites the canonical graph during rendering.

The project requires a clear default before implementing an adapter contract.

## Decision

Adopt the following default model:

```text
immutable canonical graph
+
append-only experiment overlays
→
memory-only composition
→
new artifacts and provenance records
```

A canonical artifact may be revised only through a separate, explicit, reviewed, versioned change. Ordinary experiment execution must not mutate it.

## Contract Discussion Decisions

### Are canonical artifacts immutable?

Yes after publication, except for explicit reviewed revisions that create a new version and preserve the previous version in Git history.

### Are overlays append-only?

Yes. A published overlay is not overwritten. A correction creates a successor overlay with lineage to the previous artifact.

### Are adapters deterministic?

Transformation adapters should be deterministic when their declared transformation permits it.

Publication adapters are not assumed to be deterministic because external systems may assign timestamps, URLs, CIDs, post IDs, or page IDs.

### Are output hashes mandatory?

Yes for generated local artifacts before transfer to the next stage.

A publication identifier does not replace the local artifact hash.

### Is `parent_hash` always required?

It is required for every derived artifact.

An origin artifact may use `parent_hash: null` only when it explicitly declares itself as an origin record.

### Are `notion_sync` and `x_publish` adapters or publishers?

They are publication adapters / publishers, not graph transformation adapters.

This distinction keeps external side effects separate from deterministic local transformation.

## Adapter Classes

### Transformation Adapter

Responsibilities:

- verify the declared input hash,
- validate input schema,
- transform or normalize input,
- generate a new local artifact,
- calculate an output hash,
- emit a provenance record.

Must not:

- overwrite the input artifact,
- silently edit the canonical graph,
- delete prior provenance,
- publish externally without separate authorization.

### Publication Adapter / Publisher

Responsibilities:

- receive a verified artifact,
- publish or synchronize it to an external service,
- record the service identifier, timestamp, and result,
- preserve the local artifact hash as the identity anchor.

Examples:

- Notion tracking
- IPFS pinning
- NFT metadata submission
- X publication

## Minimum Provenance Record

```yaml
provenance:
  adapter_id: string
  adapter_version: string
  experiment_id: string
  input_hash: sha256
  output_hash: sha256
  parent_hash: sha256_or_null
  timestamp: iso8601
  claim_type:
    - physical
    - computational
    - empirical
    - metaphorical
  git_commit: optional
  ipfs_cid: optional
  notion_page: optional
  publication_url: optional
```

## Chain Rule

For derived artifacts:

```text
previous_step.output_hash == next_step.input_hash
```

## Consequences

Positive:

- canonical history remains reviewable,
- experiments can be repeated without rewriting evidence,
- transformation and publication side effects are separated,
- provenance can trace every output to an origin.

Costs:

- more files are retained,
- corrections require successor artifacts rather than silent edits,
- deterministic output requires normalization of timestamps and environment-dependent metadata,
- README and examples must be aligned with this decision.

## Phase 2 Alignment Requirement

The README adapter guide should be revised to:

- remove `merge_to_canonical` as the default experiment path,
- document `render_v2.py --overlay ...`,
- explain that canonical revisions require separate review,
- distinguish transformation adapters from publication adapters,
- state hash and parent-hash requirements,
- classify poetic, computational, empirical, and physical claims.
