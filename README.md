# Claude API 入門

Anthropic の Claude API を学ぶための演習ノートブック集です。

## セットアップ

```bash
# 仮想環境の作成・有効化
python -m venv .venv
source .venv/bin/activate

# 依存パッケージのインストール
pip install anthropic python-dotenv mcp

# 環境変数の設定
cp .env.example .env
# .env を編集して ANTHROPIC_API_KEY を設定する
```

## ノートブック一覧

| ファイル | 内容 |
|---|---|
| `000_basic_api.ipynb` | API基礎：リクエスト・会話履歴・システムプロンプト・Temperature・ストリーミング・構造化出力 |
| `001_prompt_evals.ipynb` | プロンプト評価：評価データセットの作成・スコアリング・改善サイクル |
| `002_tool_use.ipynb` | ツール使用：ツール定義・並列ツール呼び出し・エージェントループ |
| `003_rag.ipynb` | RAG：ベクトル検索・ドキュメント取得・コンテキスト付き回答 |
| `004_claude_features.ipynb` | Claude機能：ビジョン・引用・拡張思考・プロンプトキャッシュ |
| `005_mcp.ipynb` | MCP：MCPサーバー実装・ツール/リソース/プロンプトの定義と利用 |
| `006_agents.ipynb` | エージェント：ワークフローパターン・並列化・チェイニング・ルーティング |

## 関連ファイル

- `mcp_server.py` - `005_mcp.ipynb` で使用するMCPサーバー
- `cli_project/` - MCP CLIアプリのサンプルプロジェクト
