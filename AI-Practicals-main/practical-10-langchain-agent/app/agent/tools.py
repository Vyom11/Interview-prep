"""Agent tools for calculator, mock search, and RAG retrieval."""

import ast
import math
from typing import Any

from app.rag.retriever import retriever
from langchain_core.tools import BaseTool


class CalculatorTool(BaseTool):
    """Safely evaluate simple arithmetic expressions."""

    name: str = "calculator"
    description: str = (
        "Evaluate a math expression using addition, subtraction, multiplication, division, "
        "exponentiation, and numeric functions."
    )

    def _run(self, expression: str) -> str:
        return str(self._safe_eval(expression))

    def _safe_eval(self, expression: str) -> Any:
        """Evaluate a math expression with a restricted AST."""

        def _eval(node: ast.AST) -> Any:
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                if isinstance(node.op, ast.UAdd):
                    return +operand
                if isinstance(node.op, ast.USub):
                    return -operand
            if isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                if isinstance(node.op, ast.Add):
                    return left + right
                if isinstance(node.op, ast.Sub):
                    return left - right
                if isinstance(node.op, ast.Mult):
                    return left * right
                if isinstance(node.op, ast.Div):
                    return left / right
                if isinstance(node.op, ast.Pow):
                    return left**right
                if isinstance(node.op, ast.Mod):
                    return left % right
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                func_name = node.func.id
                allowed = {
                    "sqrt": math.sqrt,
                    "pow": pow,
                    "abs": abs,
                    "round": round,
                    "floor": math.floor,
                    "ceil": math.ceil,
                }
                if func_name in allowed and len(node.args) == 1:
                    return allowed[func_name](_eval(node.args[0]))
            raise ValueError(f"Unsafe or unsupported expression: {expression}")

        tree = ast.parse(expression, mode="eval")
        return _eval(tree)


class WebSearchTool(BaseTool):
    """Mock a web search response without external network calls."""

    name: str = "web_search"
    description: str = (
        "Return a mock web search summary for the user query. "
        "Do not call external search engines; this is a local simulator."
    )

    def _run(self, query: str) -> str:
        query_lower = query.lower()
        if "langchain" in query_lower:
            return (
                "Mock search results:\n"
                "- LangChain is a framework for building LLM applications.\n"
                "- Use tools to connect models to calculators, search, and retrieval.\n"
                "- This mock search returns static background knowledge."
            )
        if "pdf" in query_lower or "document" in query_lower:
            return (
                "Mock search results:\n"
                "- The ingestion pipeline uses PDF chunking and text embeddings.\n"
                "- Retrieval is driven by semantic similarity search in OpenSearch."
            )
        return (
            f"Mock search results for: {query}\n"
            "- This is a simulated web search summary.\n"
            "- Use the document retriever tool for corpus-specific answers."
        )


class RAGRetrieverTool(BaseTool):
    """Retrieve relevant passages from the existing vector search corpus."""

    name: str = "document_retriever"
    description: str = (
        "Use the RAG retriever to search the ingested OpenSearch vector store "
        "and return the most relevant document passages."
    )

    def _run(self, query: str) -> str:
        documents = retriever.invoke(query)
        if not documents:
            return "No relevant documents were found for that query."

        passages = []
        for index, document in enumerate(documents, start=1):
            text = document.page_content.replace("\n", " ").strip()
            passages.append(f"Result {index}: {text[:500]}...")

        return "\n\n".join(passages)
