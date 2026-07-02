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
| [`TA-001.yaml`](./QuantumCarrollNote%20Thought%20Graph/TA-001.yaml) | Thought Archive #001 の思考ノード定義 |
| [`thought-archive-graph.mmd`](./QuantumCarrollNote%20Thought%20Graph/thought-archive-graph.mmd) | QuantumCarrollNote Thought Graph のMermaid定義 |

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

- `quantum_trust_graph_gen{N}.png` — | `TA-001.yaml` | Thought Archive #001 の思考ノード定義 |
| `quantumcarrollnote-thought-graph.md` | QuantumCarrollNote Thought Graph のMermaid図 |
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

## 🔗 Adapter Layer 接続ガイド

### Architecture: append_only_provenance

```
Discord
  ↓ (manual trigger or webhook)
BananaBot (CSV generator)
  ↓
quantum_trust_graph_experiment_N.yaml (experiment → append)
  ↓
Adapter (validation + merge logic)
  ↓
quantum_trust_graph.yaml (canonical source updated)
  ↓
render_v2.py --gen N (generate PNG + mutation_log)
  ↓
PNG + JSON (artifacts)
  ↓
Git (provenance audit trail)
  ↓
Notion (tracking dashboard)
  ↓
IPFS + NFT (immutable distribution)
  ↓
X / Community (amplification & feedback)
  ↓
Next YAML (feedback loop)
```

### 1. Discord BananaBot 統合

```python
# Pseudocode: Discord → CSV → experiment YAML

@bot.command()
async def generate_graph(ctx, experiment_name: str):
    # ユーザー入力 → CSV
    csv_data = await fetch_discord_data(ctx)
    
    # CSV → experiment YAML (append-only)
    exp_yaml = f"quantum_trust_graph_experiment_{timestamp}.yaml"
    save_experiment_yaml(csv_data, exp_yaml)
    
    # Adapter: validate & merge
    adapter.merge_to_canonical(exp_yaml, "quantum_trust_graph.yaml")
    
    # Render
    os.system(f"python render_v2.py --gen {gen_number}")
    
    # Post result
    await ctx.send(file=discord.File("quantum_trust_graph_gen{N}.png"))
```

### 2. IPFS × NFT フロー

```
mutation_log_gen{N}.json
  ↓ (pinata/web3.storage)
  ↓ IPFS CID: Qm...
  ↓ (contract.mintNFT(ipfs_cid))
NFT metadata
  ↓ (on-chain provenance)
```

### 3. Notion ダッシュボード

```
mutation_log_gen{N}.json
  ↓ (parse RadicanTrust score)
  ↓ (Notion API)
Notion Property:
  - Generation: {N}
  - RadicanTrust: 0.85
  - Timestamp: 2025-06-15T10:30:45Z
  - Git Commit: a74b1cd0...
```

### Adapter 実装例（最小）

```python
# adapters/canonical_merge.py
def merge_to_canonical(experiment_yaml_path: str, canonical_path: str):
    """
    Principle: append_only_provenance
    - Existing nodes/edges in canonical → preserved
    - New nodes/edges from experiment → appended
    - Conflicts → human review required
    """
    exp_data = load_yaml(experiment_yaml_path)
    canonical_data = load_yaml(canonical_path)
    
    # Append new nodes
    for node in exp_data["nodes"]:
        if not node_exists(canonical_data, node["id"]):
            canonical_data["nodes"].append(node)
    
    # Append new edges
    for edge in exp_data["edges"]:
        if not edge_exists(canonical_data, edge):
            canonical_data["edges"].append(edge)
    
    # Save with provenance
    canonical_data["_provenance"] = {
        "last_experiment": experiment_yaml_path,
        "timestamp": datetime.now().isoformat(),
        "adapter_version": "v1"
    }
    
    save_yaml(canonical_path, canonical_data)
    return canonical_data
```

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

**Last Updated**: 2025-06-15  
**Maintainer**: Sou Hashiguchi × CoPhelia³ Agents
