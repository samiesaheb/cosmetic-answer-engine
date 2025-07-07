from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from typing import Generator
import json

# Standard non-streaming version
def get_answer(question: str) -> dict:
    db = Chroma(
        persist_directory="vectorstore",
        embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    )
    retriever = db.as_retriever()

    llm = Ollama(model="llama3")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain(question)

    # Build citations list with product name and source file
    source_documents = result["source_documents"]
    citations = []
    for i, doc in enumerate(source_documents):
        citations.append({
            "id": i + 1,
            "source": doc.metadata.get("source", "N/A"),
            "product_name": doc.metadata.get("product_name", "Unknown Product"),
            "content": doc.page_content
        })

    citation_marks = " " + " ".join(f"[[{c['id']}]]" for c in citations) if citations else ""

    return {
        "answer": result["result"].strip() + citation_marks,
        "citations": citations
    }

# Streaming version (no citations for now)
from typing import Generator
import textwrap

def get_answer_stream(question: str) -> Generator[bytes, None, None]:
    db = Chroma(
        persist_directory="vectorstore",
        embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    )
    retriever = db.as_retriever()
    llm = Ollama(model="llama3")

    # Fetch top documents before streaming
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs[:3]])
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

    # Stream model response
    try:
        for chunk in llm.stream(prompt):
            content = chunk.content if hasattr(chunk, "content") else chunk
            yield content.encode("utf-8")
    except Exception as e:
        yield f"\n[error: {str(e)}]".encode("utf-8")

    # After streaming is done, yield formatted citations
    if docs:
        yield b"\n\nSources:\n"
        for i, doc in enumerate(docs[:5]):
            product_name = doc.metadata.get("product_name", "Unknown Product")
            source = doc.metadata.get("source", "formulations.txt")
            citation = f"[[{i+1}]] {product_name} ({source})"
            wrapped = textwrap.fill(citation, width=100)
            yield (wrapped + "\n").encode("utf-8")
