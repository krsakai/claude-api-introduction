
from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("weather-server")

# ========== ツール ==========

@mcp.tool()
def get_weather(city: str) -> str:
    """指定した都市の現在の天気を返す"""
    data = {
        "東京": "晴れ、気温22℃",
        "大阪": "曇り、気温20℃",
        "札幌": "雪、気温-2℃",
    }
    return data.get(city, f"{city} のデータは見つかりませんでした")

@mcp.tool()
def get_forecast(city: str, days: int = 3) -> str:
    """指定した都市の天気予報を返す"""
    return f"{city} の{days}日間予報: 晴れ→曇り→雨"

# ========== リソース ==========

docs = {
    "api-guide":    "# API ガイド\nこのドキュメントはAPIの使い方を説明します。\n\n## 認証\nBearerトークンを使用してください。",
    "quickstart":   "# クイックスタート\n1. パッケージをインストール\n2. APIキーを設定\n3. コードを実行",
    "faq":          "# よくある質問\nQ: レート制限は？\nA: 1分間に60リクエストまでです。",
}

@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    """利用可能なドキュメントの一覧を返す"""
    return list(docs.keys())

@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    """指定したIDのドキュメント内容を返す"""
    if doc_id not in docs:
        raise ValueError(f"ドキュメント '{doc_id}' が見つかりません")
    return docs[doc_id]

# ========== プロンプト ==========

@mcp.prompt(
    name="summarize",
    description="ドキュメントの内容を簡潔に要約する。"
)
def prompt_summarize(
    doc_id: str = Field(description="要約するドキュメントのID")
) -> str:
    # FastMCP は文字列を返すと自動的に UserMessage にラップする
    if doc_id not in docs:
        raise ValueError(f"ドキュメント '{doc_id}' が見つかりません")
    return f"""以下のドキュメントを要約してください。

要約のルール:
- 3行以内にまとめる
- 箇条書きを使う
- 専門用語はそのまま残す

--- ドキュメント: {doc_id} ---
{docs[doc_id]}
---"""

@mcp.prompt(
    name="weather-report",
    description="指定した都市の天気を丁寧なレポート形式で回答する。"
)
def prompt_weather_report(
    city: str = Field(description="天気を調べる都市名")
) -> str:
    return f"""{city}の天気を調べて、以下の形式でレポートしてください。

【天気レポートのフォーマット】
- 都市名を見出しにする
- 現在の天気と気温を最初に記載する
- 3日間の天気予報も含める
- 最後に一言アドバイス（服装・傘など）を添える"""

if __name__ == "__main__":
    mcp.run()
