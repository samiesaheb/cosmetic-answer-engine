import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

docs_dir = "documents"
all_docs = []

for filename in os.listdir(docs_dir):
    filepath = os.path.join(docs_dir, filename)
    if not filename.endswith(".txt"):
        continue

    loader = TextLoader(filepath, encoding="utf-8")
    try:
        docs = loader.load()
        for doc in docs:
            # Extract product name from first line
            first_line = doc.page_content.splitlines()[0]
            if first_line.startswith("Product:"):
                product_name = first_line.replace("Product:", "").strip()
            else:
                product_name = "Unknown Product"

            doc.metadata["source"] = filename
            doc.metadata["product_name"] = product_name
        all_docs.extend(docs)
        print(f"✅ Loaded: {filename}")
    except Exception as e:
        print(f"❌ Failed to load {filename}: {e}")

if not all_docs:
    raise ValueError("No documents found.")

# Split and embed
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(all_docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma.from_documents(split_docs, embeddings, persist_directory="vectorstore")
db.persist()

print(f"📚 Ingested {len(split_docs)} chunks from {len(all_docs)} files.")
