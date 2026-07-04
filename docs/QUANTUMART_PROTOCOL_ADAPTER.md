# QuantumArt Protocol Adapter v0.1

## Role / 役割

`bana-quantum-graph-` can act as a visualization and structural-observation layer for the QuantumArt Protocol maintained in [`nijinomichi/cophelia3`](https://github.com/nijinomichi/cophelia3).

`bana-quantum-graph-` は、[`nijinomichi/cophelia3`](https://github.com/nijinomichi/cophelia3) で管理されるQuantumArt Protocolの可視化・構造観測層として機能できます。

Canonical reciprocal contract:

- `cophelia3/docs/integrations/BANA_QUANTUM_GRAPH_ADAPTER.md`
- this document

## Ownership boundary / 正本境界

| Concern / 対象 | Canonical owner / 正本 |
|---|---|
| QuantumArt protocol, consent, capability state | `cophelia3` |
| Seed Prompt and declared metadata | `cophelia3` |
| Graph schema, rendering, structural metrics | `bana-quantum-graph-` |
| Generated experiment YAML | `bana-quantum-graph-` |
| Canonical graph merge approval | human review in `bana-quantum-graph-` |

The adapter reads the QuantumArt files. It does not rewrite them.

AdapterはQuantumArt側ファイルを読み取りますが、書き換えません。

## Implementation / 実装

- [`adapters/quantumart_protocol_adapter.py`](../adapters/quantumart_protocol_adapter.py)
- Contract ID: `quantumart-to-bana-graph.v0.1`
- Compatible protocol: `quantumart-protocol 1.x`
- Mode: `append_only_experiment`

## Usage / 使用方法

Place the repositories next to one another:

```text
workspace/
├── cophelia3/
└── bana-quantum-graph-/
```

Run from the `bana-quantum-graph-` directory:

```bash
python adapters/quantumart_protocol_adapter.py \
  --protocol ../cophelia3/prompts/protocols/quantumart-protocol.v1.0.yaml \
  --seed ../cophelia3/prompts/seeds/forgiving-dark-matter.seed.yaml \
  --output experiments/quantumart_forgiving_dark_matter.yaml \
  --execute
```

`--execute` records an explicit human action. Without it, the adapter stops and produces no experiment artifact.

`--execute` は人間による明示実行を記録します。指定がない場合、Adapterは停止し、実験ファイルを生成しません。

## Output / 出力

The adapter creates an experiment YAML containing:

- source paths and SHA-256 digests;
- protocol and seed identifiers;
- declared artistic metadata;
- explicit metric semantics;
- consent state;
- QuantumArt nodes and candidate edges;
- pending human-review status.

Adapterは、入力ファイルのパスとSHA-256、Protocol/Seed識別子、宣言メタデータ、指標意味、同意状態、候補ノード・エッジ、人間レビュー待ち状態を含むYAMLを生成します。

It does **not** modify `quantum_trust_graph.yaml`.

`quantum_trust_graph.yaml` は変更しません。

## Metric separation / 指標の意味分離

```text
QuantumArt declared Trust Level
≠ RadicanTrust graph score
≠ Born-rule probability
```

### QuantumArt declared Trust Level

```yaml
metric_type: conceptual_metadata
included_in_graph_score: false
```

This value remains author-declared until a validated measurement method exists.

検証済み測定法が確立するまで、作者宣言の概念メタデータです。

### RadicanTrust graph score

```yaml
metric_type: structural_heuristic
inputs:
  - transparency
  - inclusivity
  - reciprocity
  - density_derived_forgiveness
is_quantum_probability: false
```

This score describes properties of the graph implementation. It is not a physical quantum probability.

このスコアはグラフ実装の構造的性質を表し、物理的な量子確率ではありません。

## Review before merge / 正本マージ前のレビュー

```text
adapter output
→ YAML validation
→ source digest check
→ consent review
→ metric-semantics review
→ graph-node review
→ human approval
→ optional append-only merge
```

No generated node or edge becomes canonical merely because the script ran successfully. Software can confirm syntax. It cannot confer philosophical citizenship upon a node.

スクリプトが成功しただけで、生成ノードやエッジが正本になるわけではありません。ソフトウェアは構文を確認できますが、ノードに哲学的市民権を授与することはできません。

## Safety boundaries / 安全境界

The adapter does not:

- start an automatic demo when instructions are absent;
- collect or process EEG or other biometric data;
- activate haptic or holographic hardware;
- call an image-generation service;
- publish outputs;
- convert `528 Hz`, Trust Level, or Co-Creation Index into validated measurements;
- calculate Born-rule probability.

Adapterは、無指示時の自動実行、生体情報処理、EEG、触覚・ホログラム機器、画像生成サービス、自動公開、概念値の実測値化、Born則確率の計算を行いません。

## Change policy / 変更方針

- Preserve `quantum_trust_graph.yaml` as the canonical graph source.
- Generate experiment files first.
- Require review for conflicts and semantic changes.
- Record source digests and adapter version.
- Introduce a new contract version for breaking changes.

- `quantum_trust_graph.yaml` を正本として保持する
- まず実験ファイルを生成する
- 衝突・意味変更は人間がレビューする
- 入力digestとAdapter versionを記録する
- 破壊的変更では契約versionを更新する
