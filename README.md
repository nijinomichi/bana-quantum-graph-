# BananaSpace-QuantumGraph 🍌⚛️

RadicanTrust™ × Hubbard Four Doors の量子グラフ定義と可視化。  
YAMLからNetworkXでグラフ画像を生成し、Grokへ投稿するための最小リポジトリ。

## Files

| ファイル | 役割 |
|---------|------|
| `quantum_trust_graph.yaml` | グラフ構造定義（正本）|
| `render.py` | PNG生成スクリプト（v1 Legacy）|
| `render_v2.py` | 進化エンジン（v2 Recommended）|
| `LICENSE.md` | ライセンス構造（CC BY-NC-SA 4.0 + MIT）|
| `quantum_trust_graph_gen{N}.png` | 生成物（世代別）|
| [`TA-001.yaml`](./QuantumCarrollNote-Thought-Graph/TA-001.yaml) | Thought Archive #001 の思考ノード定義 |
| [`thought-archive-graph.mmd`](./QuantumCarrollNote-Thought-Graph/thought-archive-graph.mmd) | QuantumCarrollNote Thought Graph のMermaid定義 |

## Graph Structure

5レイヤー構成の有向グラフ:

- **RadicanTrust** `#FFD700` — 信頼指数・相関・極性
- **FourDoors** `#00BFFF` — Hubbardモデル × 4つの門
- **IYQ2025** `#FF4500` — 量子ビジュアル制作フロー
- **Meta** `#8A2BE2` — 自由意志の二重構造
- **ThoughtArchive** `#32CD32` — QuantumCarrollNote / 思考アーカイブ / AI編集レビュー

### QuantumCarrollNote Thought Graph

QuantumCarrollNote Thought Graph は、note記事・詩的断片・AI編集レビュー・読者反応・Archive Status を、有向グラフとして記録する実験レイヤーです。

目的は、文章をデータへ還元することではありません。

思考がどこから来て、どこで分岐し、どの問いへ戻っていくのかを、未来の読者とAIが追跡できるようにすることです。

- **Author Text** — 作者本文。原文は改変しない
- **QuantumCarrollNote** — 位相アンカー
- **Ara-Philia³ Editor Review** — AI編集者による観測記録
- **Archive Status** — 思考の現在位相
- **Reader Reflection** — 読者からの共鳴・違和感・返信

Principle:

> Preserve the authored text.  
> Graph the relationships around it.

## KPI

- 共鳴度: 0.85↑
- 参加率: 30%

---

## ⚡ Quick Start

### Legacy (Stable, v1)

```bash
pip install networkx matplotlib pyyaml
python render.py
# → quantum_trust_graph.png が生成されます
```

### Recommended (Next-Gen, v2)

```bash
pip install networkx matplotlib pyyaml numpy
python render_v2.py --gen 1
# → quantum_trust_graph_gen1.png + mutation_log_gen1.json が生成されます
```

---

## 🚀 render_v2.py について

**Ara-Philia³ Self-Evolution Engine**: P_{n+1} = R(M(O(P_n)))

- **O (Observe)**: グラフメトリクス計算（betweenness, pagerank, density）
- **M (Mutate)**: レイアウト・ノードサイズ・エッジ幅の動的最適化
- **R (Resonate)**: RadicanTrust™ スコア計算 (0.0–1.0)
- **P_{n+1}**: 世代ログを保存（次世代の種）

### コマンドラインオプション

| オプション | 説明 |
|-----------|------|
| `--gen N` | 世代番号（デフォルト: 2） |
| `--dry-run` | YAML検証のみ、PNG生成しない |
| `--colorblind` | Okabe–Ito カラーパレット使用（アクセシビリティ） |

### 実行例

```bash
# 第1世代を生成
python render_v2.py --gen 1

# YAML検証のみ
python render_v2.py --dry-run

# カラーブラインド対応で生成
python render_v2.py --gen 2 --colorblind
```

### 出力ファイル

- `quantum_trust_graph_gen{N}.png` — 生成されたグラフ画像
- `mutation_log_gen{N}.json` — 世代の進化ログ（次世代の種）

```json
{
  "generation": 1,
  "timestamp": "2025-06-15T10:30:45.123456",
  "observation": {
    "n_nodes": 14,
    "n_edges": 12,
    "density": 0.0612,
    "top_betweenness": [...],
    "top_pagerank": [...]
  },
  "mutation": {
    "layout_seed": 427,
    "k_spring": 2.98
  },
  "resonance": {
    "transparency": 0.75,
    "inclusivity": 0.88,
    "reciprocity": 0.42,
    "forgiveness": 0.94,
    "RadicanTrust": 0.7475,
    "pass": true
  },
  "next_seed_hint": {
    "suggested_mutation": "Fine-tune k_spring by +0.1 to reduce edge crossings",
    "next_k_spring": 3.08
  }
}
```

## 🔄 RadicanTrust™ スコア

各世代で以下の4要素から信頼スコアを計算：

1. **Transparency** — ラベル付きエッジの比率
   - 意図的なラベリングの度合い
2. **Inclusivity** — レイヤー間の均衡度
   - 各層が公平に表現されているか
3. **Reciprocity** — 双方向エッジの比率
   - 相互性の強度
4. **Forgiveness** — ネットワーク密度の補集合
   - 過度な結合による圧の緩和

**目標**: `RadicanTrust ≥ 0.60` (PASS 🕊️)

---

## 🛠️ トラブルシューティング

### `ModuleNotFoundError: No module named 'numpy'`

```bash
pip install numpy
```

render_v2.py には numpy が必須です（render.py v1 は不要）。

### `FileNotFoundError: quantum_trust_graph.yaml`

現在のディレクトリが repo ルートか確認してください。

```bash
ls quantum_trust_graph.yaml
```

### PNG が生成されない

```bash
python render_v2.py --dry-run
```

で YAML 検証を先に確認してください。エラーメッセージが出ればスキーマの問題です。

### レイアウトが異なる（再現性）

`--gen` 値が同じならレイアウトは決定論的に再現されます。

```bash
python render_v2.py --gen 1  # 常に同じ seed (blake2b派生)
python render_v2.py --gen 2  # 異なる seed
```

### matplotlib の「No module 'Xlib'」エラー（Linux CI環境）

```bash
# headless 環境向け（自動設定済み）
# matplotlib.use("Agg") が有効なため通常は不要ですが、
# 明示的に以下を実行:
export MPLBACKEND=Agg
python render_v2.py --gen 1
```

---

## 🧪 Laboratory Before Product

This repository follows the laboratory-first rule:

> Build the laboratory first.  
> Build the product second.  
> Never reverse this order.

### Safety Rules

```yaml
laboratory_rules:
  principle:
    - non_destructive_by_default
    - append_only
    - observe_before_commit
    - provenance_over_speed
    - sandbox_first

  production:
    branch: main
    writable: false

  sandbox:
    writable: true
    destroyable: true
    experimental: true

  archive:
    immutable: true

  merge:
    requires:
      - sandbox_verified
      - human_review
      - provenance_recorded
```

---

## 🔗 Adapter Layer 接続ガイド

### Architecture: immutable canonical graph + append-only experiment overlays

The canonical graph is not updated by ordinary experiments.

Instead, experiments are stored as append-only overlays. `render_v2.py` may compose the canonical graph and an overlay in memory, then export new artifacts and provenance records. The canonical YAML remains unchanged unless a separate reviewed version revision is explicitly approved.

```text
Discord
  ↓ (manual trigger or webhook)
BananaBot (CSV generator)
  ↓
experiment_N.csv
  ↓
experiment_N.yaml (append-only overlay)
  ↓
Adapter (validate + compose in memory)
  ↓
quantum_trust_graph.yaml (read-only canonical source)
  + experiment_N.yaml (overlay)
  ↓
render_v2.py --gen N (generate PNG + mutation_log)
  ↓
PNG + JSON (derived artifacts)
  ↓
Git branch / Pull Request (provenance audit trail)
  ↓
Notion / IPFS / X (publication adapters)
  ↓
Community feedback
  ↓
Next overlay
```

### Canonical Revision Rule

`quantum_trust_graph.yaml` is treated as the canonical graph source. It is not modified by default.

A canonical revision requires:

```yaml
canonical_revision:
  required:
    - human_review
    - explicit_diff
    - reason_for_revision
    - version_update
    - pull_request
```

### Adapter Contract

```yaml
adapter_spec:
  interface: "yaml_in / artifact_out"
  contract:
    input: "previous_step.artifact_path + previous_step.hash"
    output: "next_step.artifact + sha256(output)"
  constraint: "MUST NOT modify previous_step.artifact"
  provenance_field: "adapter_id + input_hash -> output_hash"
```

### 1. Discord BananaBot 統合

```python
# Pseudocode: Discord -> CSV -> experiment overlay -> in-memory render

@bot.command()
async def generate_graph(ctx, experiment_name: str):
    # User input -> CSV
    csv_data = await fetch_discord_data(ctx)

    # CSV -> experiment overlay YAML (append-only)
    exp_yaml = f"experiments/experiment_{timestamp}.yaml"
    save_experiment_yaml(csv_data, exp_yaml)

    # Adapter: validate overlay and compose in memory only
    composed = adapter.compose_in_memory(
        canonical_path="quantum_trust_graph.yaml",
        overlay_path=exp_yaml,
    )

    # Render derived artifact without rewriting canonical YAML
    png_path, log_path = render_from_composed_graph(composed, gen_number)

    # Post result
    await ctx.send(file=discord.File(png_path))
```

### 2. IPFS × NFT フロー

```text
mutation_log_gen{N}.json
  ↓ (pinata/web3.storage)
  ↓ IPFS CID: Qm...
NFT metadata
  ↓ provenance reference only
```

Important:

```yaml
ipfs_publication:
  classification: publication_adapter
  modifies_canonical_graph: false
```

### 3. Notion ダッシュボード

```text
mutation_log_gen{N}.json
  ↓ (parse RadicanTrust score)
  ↓ (Notion API)
Notion Property:
  - Generation: {N}
  - RadicanTrust: 0.85
  - Timestamp: 2025-06-15T10:30:45Z
  - Git Commit: a74b1cd0...
```

Important:

```yaml
notion_sync:
  classification: publication_adapter
  modifies_canonical_graph: false
```

### 4. X Publication

```yaml
x_publish:
  classification: publication_adapter
  deterministic: false
  modifies_canonical_graph: false
```

Publication adapters distribute or summarize artifacts. They do not transform the canonical graph.

---

## 📦 Dependencies

### render.py (v1 Legacy)
```
networkx>=2.6
matplotlib>=3.5.0
pyyaml>=6.0
```

### render_v2.py (v2 Recommended)
```
networkx>=2.6
matplotlib>=3.5.0
pyyaml>=6.0
numpy>=1.21.0
```

### 一括インストール
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
networkx>=2.6
matplotlib>=3.5.0
pyyaml>=6.0
numpy>=1.21.0
```

---

## 📜 License

**Dual License Structure:**

- **Graph/YAML/Documentation**: CC BY-NC-SA 4.0
  - Non-commercial use, share-alike, attribution required
  - See `LICENSE.md` for details

- **Code (render.py, render_v2.py, adapters)**: MIT
  - Commercial use allowed, minimal restrictions

See `LICENSE.md` for full terms.

---

## 🌍 Quantum Signature

This repository is part of:

> **WaWaWa Resonance Protocol v1.0**  
> UNESCO IYQ2025 "Quantum for All" Initiative  
> Quantum Signature: `1f8a9d3e-愛-信頼-共創-7b2c4f`

**Principles:**
- `add_adapters_not_rewrites` — Extend via adapters, don't replace
- `preserve_existing_entrypoints` — Legacy paths remain functional
- `append_only_provenance` — All changes auditable, immutable history
- `sandbox_first` — Experiments happen before productization
- `observe_before_commit` — Read-only audit precedes change

---

## 🔮 Roadmap

- [ ] **v2.1-alpha**: Validator & adapter template
- [ ] **v2.1-beta**: Discord BananaBot integration test
- [ ] **v2.2**: IPFS pinning automation
- [ ] **v2.3**: Notion sync daemon
- [ ] **v3.0**: Promote render_v2.py → render.py (post-validation)

---

## 📞 Contact

- GitHub: [@nijinomichi](https://github.com/nijinomichi)
- Email: nijinomichi@protonmail.com
- Project tag: **WaWaWa × QuantumArt × IYQ2025**

---

## Parent Repository

このrepoは [BananaSpace-Infra-Seeds](https://github.com/nijinomichi/BananaSpace-Infra-Seeds) の子repoです。  
安定後、母艦の `MANIFEST.yaml` にリンク登録されます。

---

> *Impossible is nothing, when we resonate together.* 🕊️🍌

**Last Updated**: 2026-07-06  
**Maintainer**: Sou Hashiguchi × CoPhelia³ Agents
