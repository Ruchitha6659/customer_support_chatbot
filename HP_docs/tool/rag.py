from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

### env variables
load_dotenv()

### configuration
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "hp_laptop"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

## global objects
vector_store = None
embedding_function = None
llm = None


### initializing system
def initialize_system():
    global vector_store, embedding_function, llm

    print("Initializing embedding model...")
    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"trust_remote_code": True}
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

    print("\nSearching knowledge base...\n")

    ### Searching vector database
    docs = vector_store.similarity_search(query, k=3)

    ### sources
    sources = list(set([doc.metadata.get("source", "") for doc in docs]))

    context = "\n\n".join([doc.page_content for doc in docs])

    ### asking llm
    messages = [
        SystemMessage(content=f"""You are an HP laptop support assistant.
Answer questions based only on this context:
{context}"""),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)
    answer = response.content

    return answer, sources


### running chatbot
if __name__ == "__main__":
    initialize_system()

    print("\nHP Support Chatbot Ready\n")

    while True:
        query = input("Ask question: ")

        if query.lower() == "exit":
            print("Exiting chatbot...")
            break

        answer, sources = generate_answer(query)

        print("\nAnswer:\n")
        print(answer)

        print("\nSources used:\n")
        print(sources)
        print("\n----------------------------------")
