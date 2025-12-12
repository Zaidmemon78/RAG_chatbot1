import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def create_vector_db():
    print("🚀 PDF Load ho rahi hai...")
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()

    print(f"📄 {len(documents)} Pages mile.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    print("🧠 Embeddings ban rahi hain...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = FAISS.from_documents(texts, embeddings)
    db.save_local("faiss_index")
    print("✅ Database 'faiss_index' ready hai!")


if __name__ == "__main__":
    create_vector_db()