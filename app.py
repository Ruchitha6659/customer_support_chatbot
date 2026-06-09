# %% [markdown]
# ### loading files
# 

# %%
from langchain_community.document_loaders import Docx2txtLoader 
loader1=Docx2txtLoader(r"C:\Users\RUCHITHA\OneDrive\Desktop\projects\customer_support_chatbot\HP_docs\Pavilion_15\user_guide.docx")
docs1=loader1.load()
loader2=Docx2txtLoader(r"C:\Users\RUCHITHA\OneDrive\Desktop\projects\customer_support_chatbot\HP_docs\Pavilion_15\setup_instructions.docx")
docs2=loader2.load()
loader3=Docx2txtLoader(r"C:\Users\RUCHITHA\OneDrive\Desktop\projects\customer_support_chatbot\HP_docs\Pavilion_15\maintainance_service_guide.docx")
docs3=loader3.load()

all_documents=docs1+docs2+docs3
len(all_documents)

# %%
len(docs1)

# %%
len(docs1[0].page_content)

# %%
print(len(docs1[0].page_content[:500]))

# %%
len(docs1[0].page_content)

# %% [markdown]
# ### text splitters

# %%
from langchain_text_splitters import CharacterTextSplitter
splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=100
)

chunks = splitter.split_documents(all_documents)

# %%
print(f"Total chunks: {len(chunks)}")

# %% [markdown]
# ### recursive text splitters

# %%
from langchain_text_splitters import RecursiveCharacterTextSplitter

r_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n","\n"," "],
    chunk_size=2000,
    chunk_overlap=200
)

chunks = r_splitter.split_documents(all_documents)

# %%
# Check what is inside your raw document
print(all_documents[0].page_content[:5])

# %%
print(f"Total chunks: {len(chunks)}")

# %%
for chunk in chunks:
    print(len(chunk.page_content))

# %% [markdown]
# ### cleaning all the extra spaces

# %%
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

cleaned_documents = []
for doc in all_documents:
    lines = doc.page_content.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip() != ""]
    cleaned_text = "\n".join(cleaned_lines)
    
    cleaned_documents.append(Document(
        page_content=cleaned_text,
        metadata=doc.metadata
    ))
print(f"Total cleaned documents: {len(cleaned_documents)}")

## recursive text splitter
r_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " "],
    chunk_size=2000,
    chunk_overlap=200
)

chunks = r_splitter.split_documents(cleaned_documents)
print(f"Total chunks: {len(chunks)}")

# %%
print(chunks[0])

# %%
for i,chunk in enumerate(chunks[1:5]):
  print(f"\n=======chunk {i+2}=======")
  print(chunk.page_content)
  print(f"characters:{len(chunk.page_content)}")
  print(f"source:{chunk.metadata['source']}")
  print("="*40)

# %%
first_split=all_documents[0].page_content.split("\n\n")[0]
print(first_split)

# %%
second_split=first_split.split("\n")
len(second_split)

# %%
second_split[0].split(" ")

# %%



