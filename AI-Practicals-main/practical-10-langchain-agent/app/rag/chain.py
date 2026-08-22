"""
RAG chain implementation.
"""

# Import Bedrock chat model
# Import Bedrock client
from app.core.aws_clients import bedrock_client

# Import config
from app.core.config import BEDROCK_LLM_MODEL

# Import retriever
from app.rag.retriever import retriever
from langchain_aws import ChatBedrock

# Create LLM
llm = ChatBedrock(client=bedrock_client, model_id=BEDROCK_LLM_MODEL)


def ask_question(question: str) -> str:
    """
    Ask question using RAG.
    """

    # Retrieve documents
    docs = retriever.invoke(question)

    # Print retrieval quality
    for index, doc in enumerate(docs):

        print(f"\nChunk {index + 1}")

        print(doc.page_content[:500])

    # Combine context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Create prompt
    prompt = f"""
    You are a helpful AI assistant.

    Use ONLY the provided context.

    Context:
    {context}

    Question:
    {question}
    """

    # Generate response
    response = llm.invoke(prompt)

    return response.content
