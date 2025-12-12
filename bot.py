import os
from dotenv import load_dotenv

# LlamaIndex ke imports (LangChain se alag hain)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Environment Load
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: .env file mein API Key nahi mili!")
    exit()

print("⚙️  System Setup ho raha hai...")

# 2. Settings Config (Groq + HuggingFace)
# Hum bata rahe hain ki LLM kaunsa use karna hai aur Embeddings kaunsi
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=api_key)
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 3. Data Load & Indexing
# Ye 'data' folder se khud PDF uthayega aur Index bana lega
try:
    print("🚀 Data Load ho raha hai...")
    documents = SimpleDirectoryReader("data").load_data()

    print("🧠 Index ban raha hai (Vector Store)...")
    index = VectorStoreIndex.from_documents(documents)

    # Query Engine ready karo
    query_engine = index.as_query_engine()
    print("✅ Chatbot Ready hai! (Exit ke liye 'quit' likhein)\n")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure 'data' folder mein PDF hai.")
    exit()

# 4. Chat Loop
while True:
    user_input = input("You: ")

    if user_input.lower() in ['quit', 'exit', 'bye']:
        break

    try:
        # LlamaIndex mein bas .query() call karna hota hai
        response = query_engine.query(user_input)
        print(f"Bot: {response}\n")
    except Exception as e:
        print(f"⚠️ Error: {e}")