# Laboratory Before Product

**Status:** Draft manifesto  
**Scope:** Experimental governance for `nijinomichi/bana-quantum-graph-`  
**Branch policy:** This document is proposed on a working branch. It does not modify `main`, canonical graph data, renderers, or external integrations.

## Manifesto

Do not optimize for rapid deployment.

Optimize for safe experimentation.

Every experiment should be reversible.

Every artifact should preserve its lineage.

Every contributor should feel safe enough to fail.

Trust grows where mistakes become observable instead of shameful.

Build the laboratory first.

Build the product second.

Never reverse this order.

## Laboratory Map

```text
Laboratory
│
├── Production   # approved works and stable releases
├── Sandbox      # reversible experiments
├── Archive      # preserved records
└── Provenance   # lineage and verification
```

## Machine-Readable Declaration

```yaml
laboratory_manifest:
  schema_version: "1.0-draft"
  title: "Laboratory Before Product"
  repository: "nijinomichi/bana-quantum-graph-"
  status: "proposal"
  main_modified: false

  message: >
    Do not optimize for rapid deployment.
    Optimize for safe experimentation.
    Every experiment should be reversible.
    Every artifact should preserve its lineage.
    Every contributor should feel safe enough to fail.
    Trust grows where mistakes become observable instead of shameful.

  core:
    first_build:
      - laboratory
    second_build:
      - product
    never_reverse_this_order: true

  laboratory:
    production:
      branch: "main"
      writable_by_default: false
      purpose: "approved works and stable releases"

    sandbox:
      writable: true
      destroyable: true
      experimental: true
      purpose: "safe and reversible experiments"

    archive:
      immutable_after_publication: true
      purpose: "preserved records"

    provenance:
      append_only: true
      purpose: "lineage and verification"

  principles:
    - non_destructive_by_default
    - append_only
    - observe_before_commit
    - provenance_over_speed
    - sandbox_first

  merge:
    requires:
      - sandbox_verified
      - human_review
      - provenance_recorded

  prohibitions:
    - direct_commit_to_main
    - silent_overwrite_of_canonical_artifact
    - deletion_without_record
    - promotion_without_review
```

## Interpretation Boundary

This manifesto defines governance and safety expectations. It does not claim that software, prompts, graphs, or artifacts are alive or autonomously evolving. Apparent evolution occurs through repeated interpretation, execution, observation, and revision by people, AI systems, and communities.

## Next Step

After this manifesto is reviewed, implementation rules may be proposed separately as a versioned laboratory contract. No production integration should be inferred from this document alone.
