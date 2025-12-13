import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Environment Setup
load_dotenv()

# 2. Settings Config (Same settings that will be used in the bot)
print("⚙️  Configuring Embeddings...")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


# Note: No LLM needed for ingestion, only Embeddings.

def create_vector_db():
    print("🚀 Loading PDFs from 'data' folder...")
    try:
        # Read files from data folder
        documents = SimpleDirectoryReader("data").load_data()
        print(f"📄 Total Documents Loaded: {len(documents)}")

        print("🧠 Creating Index and Embeddings...")
        index = VectorStoreIndex.from_documents(documents)

        # 3. Save to Disk (Most Important Step)
        print("💾 Saving Index to 'storage' folder...")
        index.storage_context.persist(persist_dir="./storage")

        print("✅ Success! Database saved in 'storage' folder.")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    create_vector_db()