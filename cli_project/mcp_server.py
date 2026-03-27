from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(
    doc_id: str = Field(description="Id of the document to read"),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document's content with a new string.",
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text."),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Document '{doc_id}' updated successfully."


@mcp.resource(
    "docs://documents",
    mime_type="application/json",  # JSON形式でリスト返却
)
def list_documents() -> list[str]:
    """全ドキュメントのIDリストを返す"""
    return list(docs.keys())


@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",  # プレーンテキストで内容返却
)
def get_document(doc_id: str) -> str:
    """指定されたドキュメントの内容を返す"""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.prompt()
def rewrite_as_markdown(doc_id: str) -> str:
    """ドキュメントをMarkdown形式に書き直すプロンプト"""
    content = docs.get(doc_id, f"Document '{doc_id}' not found.")
    return f"Please rewrite the following document in well-structured Markdown format:\n\n{content}"


@mcp.prompt()
def summarize(doc_id: str) -> str:
    """ドキュメントを要約するプロンプト"""
    content = docs.get(doc_id, f"Document '{doc_id}' not found.")
    return f"Please provide a concise summary of the following document:\n\n{content}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
