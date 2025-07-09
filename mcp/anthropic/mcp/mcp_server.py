from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base


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
    name="read_doc",
    description="Read the contents of a document and return it as a string"
)
def read_documents(
    doc_id: str = Field(description = "Id of a Document to read")
):  
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]


# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit  a document by replacing its contents with the provided text"
)
def edit_document(
    doc_id: str = Field(description="Id of a Document to edit"),
    old_str: str = Field(description="Old content to be replaced in the document, Must be the exact content of the document"),
    new_str: str = Field(description="New content to replace the old content in the document")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Document '{doc_id}' has been updated."

@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    """
    Returns a list of all available document IDs.
    """
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def get_doc_content(doc_id: str) -> str:
    """
    Returns the content of a specific document by its ID.
    """
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Rewrite the document in a markdown format"
)
def format_document(
    doc_id: str = Field(description="Id of a Document to format"),
) -> list[base.Message]:
    prompt = f"""
    your goal is to reformat the document into a markdow
    
    the id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headings, bullet points, and other markdown formatting to make the document more readable.
    use the 'edit_document' tool to update the document with the new formatted content.
    """
    return [base.UserMessage(
        content=prompt)]
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
