import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# LlamaIndex Imports
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. Environment Load
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: API Key not found! Check .env file.")

# 2. FastAPI Setup
app = FastAPI(title="LlamaIndex RAG API", version="1.0")

# Global Variable
query_engine = None


# 3. System Load (On Startup)
@app.on_event("startup")
async def startup_event():
    global query_engine
    print("⚙️  System Initializing...")

    try:
        # A. Settings (Same settings used in ingest.py)
        Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=api_key)
        Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # B. Load Index from 'storage'
        print("📂 Loading Index from 'storage' folder...")

        # Check if folder exists
        if not os.path.exists("./storage"):
            raise FileNotFoundError("Storage folder not found. Run 'python ingest.py' first.")

        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)

        # C. Engine Ready
        query_engine = index.as_query_engine()
        print("✅ System Ready! API is running.")

    except Exception as e:
        print(f"❌ Error during startup: {e}")
        query_engine = None


# 4. Request Model
class QueryRequest(BaseModel):
    query: str


# 5. API Endpoint (Updated with Sources)
@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    if query_engine is None:
        raise HTTPException(status_code=500, detail="System not initialized. Check server logs.")

    try:
        # Query Engine call
        response = query_engine.query(request.query)

        # --- Source Extraction Logic ---
        source_data = []

        # LlamaIndex stores references in response.source_nodes
        if response.source_nodes:
            for node_with_score in response.source_nodes:
                # Actual node data
                node = node_with_score.node

                # Metadata (Page number, Filename)
                page_num = node.metadata.get("page_label", "N/A")
                file_name = node.metadata.get("file_name", "N/A")

                # Text Snippet (First 200 chars)
                text_content = node.get_content()
                snippet = text_content[:200] + "..." if len(text_content) > 200 else text_content

                # Similarity Score
                score = round(node_with_score.score, 2) if node_with_score.score else 0.0

                source_data.append({
                    "file": file_name,
                    "page": page_num,
                    "text": snippet,
                    "score": score
                })

        # Return JSON with answer AND sources
        return {
            "response": str(response),
            "sources": source_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run command: uvicorn main:app --reload