# ADR-002: Provenance Handoff Contract

Status: proposed

Related issue: #4

## Context

The graph repository and `BananaSpace-Laboratory-v1` record different parts of the same workflow.

The graph repository records artifact identity, hash lineage, adapter boundaries, and claim classification.

The Laboratory records experiment context, repository and branch information, inputs and outputs, observations, failures, and limits.

These records must remain separate because they serve different review purposes. They must also be connected strongly enough that an artifact can be traced back to the experiment that produced it.

This ADR defines only the handoff contract between the two records.

It does not merge their schemas into one file and does not authorize implementation or migration work.

## Decision

Use the following relationship:

```text
Laboratory Case
    ↓ experiment_id + output_hash
Graph Artifact Provenance
```

The Laboratory Case and the Graph Artifact Provenance remain separate records.

They are connected by explicit identifiers and hashes rather than by copying or silently rewriting either record.

## Ownership Boundary

### Graph repository rule

The graph repository owns:

```yaml
graph_repository_rule:
  owns:
    - artifact_identity
    - input_hash
    - output_hash
    - parent_hash
    - adapter_contract
    - claim_boundary
```

### Laboratory rule

The Laboratory owns:

```yaml
laboratory_rule:
  owns:
    - experiment_context
    - repository
    - branch
    - inputs_and_outputs
    - status
    - observations
    - failure_and_limits
```

Neither side replaces the other.

## Required Handoff Fields

```yaml
handoff_rule:
  required_link:
    - experiment_id
    - output_hash
    - laboratory_provenance_ref
    - graph_provenance_ref
```

Field meaning:

- `experiment_id`: identifies the same experiment on both sides.
- `output_hash`: identifies the exact artifact handed from the Laboratory to the graph workflow.
- `laboratory_provenance_ref`: repository path or URI for the Laboratory record.
- `graph_provenance_ref`: repository path or URI for the graph artifact provenance record.

## Matching Rules

A handoff is valid only when all applicable rules pass.

```yaml
matching_rules:
  same_experiment:
    rule: laboratory.experiment_id == graph.experiment_id
    meaning: "Both records describe the same experiment."

  same_artifact:
    rule: laboratory.output_hash == graph.output_hash
    meaning: "Both records identify the same output artifact."

  correct_parent:
    rule: graph.parent_hash == laboratory.declared_parent_hash
    meaning: "The graph artifact derives from the parent declared by the Laboratory."

  continuous_chain:
    rule: previous_step.output_hash == next_step.input_hash
    meaning: "The output of one stage is the unchanged input of the next stage."
```

For an origin artifact with no parent:

```yaml
origin_artifact:
  parent_hash: null
  origin: true
```

`parent_hash: null` is valid only when `origin: true` is explicitly declared.

## Stop Conditions

The workflow must stop when any of the following is true:

```yaml
stop_if:
  - experiment_id_mismatch
  - output_hash_mismatch
  - parent_hash_mismatch
  - chain_hash_mismatch
  - provenance_reference_missing
  - claim_type_missing
  - prior_evidence_would_be_deleted
  - repository_ownership_is_unclear
```

On mismatch, the system must not:

- automatically correct identifiers,
- silently replace an artifact,
- continue to publication,
- update the canonical graph,
- delete prior evidence.

The mismatch must be recorded as an observation and returned for human review.

## Claim Boundary

Each applicable record must classify claims as one or more of:

- `physical`
- `computational`
- `empirical`
- `metaphorical`

Poetic or project-specific values must not be presented as physical measurements or universal scientific quantities without independent evidence.

## Migration Rule

This contract changes the destination of future work. It does not rewrite history.

```yaml
migration_method:
  existing_evidence:
    action: preserve_in_place

  future_experiments:
    destination: BananaSpace-Laboratory-v1

  duplicated_material:
    action: mark_as_legacy_or_reference

  deletion:
    allowed: false
```

Existing evidence remains in its current repository. Future adapter implementation trials, connection tests, runtime logs, and temporary experiment records belong in the Laboratory.

## Non-Goals

This ADR does not authorize:

- implementation,
- file migration,
- changes to `README.md`,
- changes to ADR-001,
- changes to `quantum_trust_graph.yaml`,
- changes to `render.py` or `render_v2.py`,
- generated artifact changes,
- external connections,
- publication,
- merge.

## Review Gate

Before this ADR may be accepted, human review must confirm:

```yaml
human_review:
  handoff_fields_understood: true
  matching_rules_accepted: true
  mismatch_behavior: stop
  repository_boundary_accepted: true
```

## Consequences

Positive:

- experiment context and artifact identity remain clearly separated,
- every derived artifact can be traced to its experiment,
- hash mismatches stop the workflow before publication,
- old evidence is preserved,
- repository responsibilities remain explicit.

Costs:

- both provenance references must be maintained,
- hashes must be calculated consistently,
- incomplete records cannot advance automatically,
- human review is required when a mismatch occurs.

## Guiding Principle

> 正本は弄らない。実験はLaboratoryへ。PRは境界確認。
