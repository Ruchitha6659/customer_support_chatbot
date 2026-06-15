from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
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
        max_tokens=500
    )

def generate_answer(query):
    if not vector_store:
        raise RuntimeError("Vector database not initialized")

    docs = vector_store.similarity_search_with_relevance_scores(
        query,
        k=3
    )

    # Filter relevant documents
    relevant_docs = [
        doc for doc, score in docs
        if score >= 0.7
    ]

    if not relevant_docs:
        return (
            "I can only assist with HP laptop-related questions.",
            []
        )

    sources = list(
        set(
            doc.metadata.get("source", "")
            for doc in relevant_docs
        )
    )

    context = "\n\n".join(
        doc.page_content for doc in relevant_docs
    )

    messages = [
        SystemMessage(
            content=f"""
You are an HP Laptop Customer Support Assistant.

You must answer ONLY using the provided context.

You can help with:
- HP laptops
- HP products
- Troubleshooting
- Specifications
- Warranty information
- Setup and maintenance

If the question is unrelated to HP products or cannot be answered from the context, reply exactly:

"I can only assist with HP laptop-related questions."

Do not use your general knowledge.

Context:
{context}
"""
        ),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)

    return response.content, sources