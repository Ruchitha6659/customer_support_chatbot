from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

import os
import traceback

os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

VECTORSTORE_DIR = Path(__file__).parent / "resources" / "vectorstore"
COLLECTION_NAME = "hp_laptop"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-MiniLM-L3-v2"

vector_store = None
embedding_function = None
llm = None


def initialize_system():
    global vector_store, embedding_function, llm

    print("Initializing embedding model...")

    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False}
    )

    print("Loading vector database...")

    try:
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding_function,
            persist_directory=str(VECTORSTORE_DIR)
        )
    except Exception as e:
        print(f"Vector store error: {e}")
        traceback.print_exc()
        raise

    print("Initializing LLM...")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=500,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    print("System initialized successfully!")


def generate_answer(query):
    if vector_store is None:
        raise RuntimeError("Vector database not initialized")

    docs = vector_store.similarity_search_with_relevance_scores(
        query,
        k=3
    )

    print(f"\nQuestion: {query}")
    print(f"Retrieved {len(docs)} documents")

    relevant_docs = [
        doc for doc, score in docs
        if score >= 0.4
    ]

    if not relevant_docs:
        return (
            "I can only assist with HP laptop-related questions.",
            []
        )

    context = "\n\n".join(
        [doc.page_content for doc in relevant_docs]
    )

    sources = list(
        set(
            doc.metadata.get("source", "Unknown")
            for doc in relevant_docs
        )
    )

    messages = [
        SystemMessage(
            content=f"""
You are an HP Laptop Customer Support Assistant.

Answer ONLY using the information provided in the context below.

If the answer is not available in the context, reply exactly:

"I couldn't find relevant information in the HP support documents."

Context:
{context}
"""
        ),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)

    return response.content, sources