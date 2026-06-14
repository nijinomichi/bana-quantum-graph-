# BananaSpace-QuantumGraph 🍌⚛️

RadicanTrust™ × Hubbard Four Doors の量子グラフ定義と可視化。  
YAMLからNetworkXでグラフ画像を生成し、Grokへ投稿するための最小リポジトリ。

## Files

| ファイル | 役割 |
|---------|------|
| `quantum_trust_graph.yaml` | グラフ構造定義（正本）|
| `render.py` | PNG生成スクリプト |
| `quantum_trust_graph.png` | 生成物（.gitignore対象外・手動追加可）|

## Usage

```bash
pip install networkx matplotlib pyyaml
python render.py
# → quantum_trust_graph.png が生成されます
```

## Graph Structure

4レイヤー構成の有向グラフ:

- **RadicanTrust** `#FFD700` — 信頼指数・相関・極性
- **FourDoors** `#00BFFF` — Hubbardモデル × 4つの門
- **IYQ2025** `#FF4500` — 量子ビジュアル制作フロー
- **Meta** `#8A2BE2` — 自由意志の二重構造

## KPI

- 共鳴度: 0.85↑
- 参加率: 30%

## License

CC BY-NC-SA 4.0 — 共有任意・匿名可・取り消し可

## Parent Repository

このrepoは [BananaSpace-Infra-Seeds](https://github.com/nijinomichi/BananaSpace-Infra-Seeds) の子repoです。  
安定後、母艦の `MANIFEST.yaml` にリンク登録されます。
