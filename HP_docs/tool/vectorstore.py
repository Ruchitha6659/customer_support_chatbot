from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).parent.parent

DOCS_DIR = BASE_DIR / "Pavilion_15"
VECTORSTORE_DIR = Path(__file__).parent / "resources" / "vectorstore"

COLLECTION_NAME = "hp_laptop"

embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
)

print("Loading documents...")

loader = DirectoryLoader(
    str(DOCS_DIR),
    glob="*.docx",
    loader_cls=Docx2txtLoader
)

documents = loader.load()

print(f"Loaded {len(documents)} documents")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

Chroma.from_documents(
    documents=chunks,
    embedding=embedding_function,
    persist_directory=str(VECTORSTORE_DIR),
    collection_name=COLLECTION_NAME
)

print("✅ Vector store created successfully!")