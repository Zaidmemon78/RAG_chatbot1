import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Environment Setup
load_dotenv()

# 2. Settings Config (Wohi same settings jo bot me use hogi)
print("⚙️  Configuring Embeddings...")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


# Note: Ingest karte waqt LLM ki zaroorat nahi hoti, sirf Embeddings chahiye.

def create_vector_db():
    print("🚀 PDF Load ho rahi hai 'data' folder se...")
    try:
        # Data folder se files padho
        documents = SimpleDirectoryReader("data").load_data()
        print(f"📄 Total Documents Loaded: {len(documents)}")

        print("🧠 Index aur Embeddings ban rahe hain...")
        index = VectorStoreIndex.from_documents(documents)

        # 3. Save to Disk (Sabse Important Step)
        print("💾 Index save ho raha hai 'storage' folder mein...")
        index.storage_context.persist(persist_dir="./storage")

        print("✅ Success! Database 'storage' folder me save ho gaya hai.")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    create_vector_db()