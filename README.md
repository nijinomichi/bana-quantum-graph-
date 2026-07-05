# BananaSpace-QuantumGraph 🍌⚛️

RadicanTrust™ × Hubbard Four Doors のグラフ定義・可視化・構造評価を扱うリポジトリです。  
このリポジトリの責務は、graph schema、rendering、structural metrics、artifact export に限定します。

## Repository Boundary

```yaml
repository_role:
  name: "bana-quantum-graph-"
  responsibility:
    - graph_schema
    - rendering
    - structural_metrics
    - artifact_export

  excludes:
    - laboratory_governance
    - Discord_BananaBot_implementation
    - Replit_connection_tests
    - Pinata_connection_tests
    - NFT_production_workflows
    - Notion_or_X_publication_automation
```

実験・失敗・練習・接続テストは、別リポジトリの
[`BananaSpace-Laboratory-v1`](https://github.com/nijinomichi/BananaSpace-Laboratory-v1)
で扱います。

> 正本は弄らない。実験はLaboratoryへ。PRは境界確認。

## Files

| ファイル | 役割 |
|---------|------|
| `quantum_trust_graph.yaml` | 現在のグラフ表現におけるリポジトリ内正本 |
| `render.py` | PNG生成スクリプト（v1 Legacy） |
| `render_v2.py` | 現在の推奨renderer（v2 Recommended） |
| `LICENSE.md` | ライセンス構造（CC BY-NC-SA 4.0 + MIT） |
| `quantum_trust_graph_gen{N}.png` | 世代別の派生生成物 |
| `mutation_log_gen{N}.json` | 構造評価・生成ログ |
| [`TA-001.yaml`](./QuantumCarrollNote-Thought-Graph/TA-001.yaml) | Thought Archive #001 の思考ノード定義 |
| [`thought-archive-graph.mmd`](./QuantumCarrollNote-Thought-Graph/thought-archive-graph.mmd) | QuantumCarrollNote Thought Graph のMermaid定義 |

## Graph Structure

5レイヤー構成の有向グラフです。

- **RadicanTrust** — 信頼に関するプロジェクト固有の構造的ヒューリスティック
- **FourDoors** — Hubbardモデルを参照した4つの門
- **IYQ2025** — 量子ビジュアル制作フロー
- **Meta** — 自由意志の二重構造
- **ThoughtArchive** — QuantumCarrollNote、思考アーカイブ、AI編集レビュー

### Claim Boundary

RadicanTrust、Resonance、Forgiveness、Four Doorsなどの語は、現段階では物理量・量子確率・普遍的信頼尺度ではありません。

```yaml
claim_boundary:
  RadicanTrust:
    metric_type: structural_heuristic
    is_quantum_probability: false
    is_universal_trust_measure: false
```

## Quick Start

### Legacy (Stable, v1)

```bash
pip install networkx matplotlib pyyaml
python render.py
```

### Recommended (v2)

```bash
pip install networkx matplotlib pyyaml numpy
python render_v2.py --gen 1
```

主なオプション：

| オプション | 説明 |
|-----------|------|
| `--gen N` | 世代番号 |
| `--dry-run` | YAML検証のみを実行 |
| `--colorblind` | Okabe-Itoカラーパレットを使用 |

## Canonical Model

通常の実験は `quantum_trust_graph.yaml` を変更しません。

```text
immutable canonical graph
+
append-only experiment overlay
→
memory-only composition
→
derived artifacts + provenance records
```

`render_v2.py` は、canonical graphとoverlayをメモリ上で合成し、派生生成物を出力します。通常の実験実行によって正本を書き戻すことはありません。

### Canonical Revision Rule

正本を更新する場合は、通常実験とは分離した明示的な改訂として扱います。

```yaml
canonical_revision:
  required:
    - human_review
    - explicit_diff
    - reason_for_revision
    - version_update
    - pull_request
```

## Adapter Boundary

このリポジトリではAdapterの**概念契約**だけを定義します。実装・接続テスト・失敗可能な試行は `BananaSpace-Laboratory-v1` で行います。

### Transformation Adapter

```yaml
transformation_adapter:
  responsibilities:
    - verify_input_hash
    - validate_input_schema
    - generate_new_local_artifact
    - calculate_output_hash
    - emit_provenance_record

  must_not:
    - overwrite_input_artifact
    - silently_edit_canonical_graph
    - delete_prior_provenance
    - publish_without_separate_authorization
```

### Publication Adapter

Notion、IPFS、NFT metadata submission、Xなどはpublication adapterとして分類します。

```yaml
publication_adapter:
  responsibilities:
    - receive_verified_artifact
    - publish_or_synchronize_externally
    - record_service_identifier
    - preserve_local_artifact_hash

  modifies_canonical_graph: false
```

### Chain Rule

```text
previous_step.output_hash == next_step.input_hash
```

## External Integration Boundary

接続関係は概念上、次のように扱います。

```text
Laboratory experiment
  ↓ reviewed output
bana-quantum-graph-
  ↓ derived artifact
publication adapter
  ↓
Notion / IPFS / X / other external systems
```

Discord、BananaBot、Replit、Pinataなどの実装例・接続試験は、このREADMEには置きません。

## Dependencies

### render.py

```text
networkx>=2.6
matplotlib>=3.5.0
pyyaml>=6.0
```

### render_v2.py

```text
networkx>=2.6
matplotlib>=3.5.0
pyyaml>=6.0
numpy>=1.21.0
```

```bash
pip install -r requirements.txt
```

## License

- Graph / YAML / Documentation: CC BY-NC-SA 4.0
- Code: MIT

詳細は `LICENSE.md` を参照してください。

## Principles

- `add_adapters_not_rewrites`
- `preserve_existing_entrypoints`
- `append_only_provenance`
- `sandbox_first`
- `observe_before_commit`

## Architecture Documents

- [`PHASE0_READ_ONLY_AUDIT.md`](./docs/architecture/PHASE0_READ_ONLY_AUDIT.md)
- [`ADR-001_NON_DESTRUCTIVE_ADAPTER_MODEL.md`](./docs/architecture/ADR-001_NON_DESTRUCTIVE_ADAPTER_MODEL.md)

## Roadmap

- [ ] Validator and adapter contract validation
- [ ] Laboratory-side integration experiments
- [ ] Mandatory output SHA-256 fields
- [ ] Reproducibility normalization
- [ ] Reviewed canonical versioning process

## Parent Repository

このリポジトリは
[`BananaSpace-Infra-Seeds`](https://github.com/nijinomichi/BananaSpace-Infra-Seeds)
の全体地図へ、安定後に登録されます。

---

**Last Updated:** 2026-07-06  
**Maintainer:** Sou Hashiguchi × CoPhelia³ Agents
