from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

import os

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

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_function,
        persist_directory=str(VECTORSTORE_DIR)
    )

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

    docs = vector_store.similarity_search(query, k=3)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    sources = list(
        set(
            doc.metadata.get("source", "Unknown")
            for doc in docs
        )
    )

    messages = [
        SystemMessage(
            content=f"""
You are an HP Laptop Customer Support Assistant.

Answer ONLY using the provided context.

If the context does not contain the answer, respond exactly:

"I couldn't find relevant information in the HP support documents."

Context:
{context}
"""
        ),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)

    return response.content, sources