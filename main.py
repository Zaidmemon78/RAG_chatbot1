import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# LlamaIndex Imports
from llama_index.core import StorageContext, load_index_from_storage, Settings, PromptTemplate
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import SimilarityPostprocessor

# 1. Environment Load
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: API Key not found! Check .env file.")

# 2. FastAPI Setup
app = FastAPI(title="LlamaIndex RAG API", version="2.1")

# Global Variable
query_engine = None

# --- CUSTOM PROMPT TEMPLATE ---
qa_prompt_str = (
    "You are a helpful AI Course Assistant.\n"
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, answer the query.\n"
    "If the answer is not in the context, strictly say: 'I could not find the answer in the uploaded documents.'\n"
    "Do not hallucinate or make up facts.\n"
    "Query: {query_str}\n"
    "Answer: "
)


# 3. System Load (On Startup)
@app.on_event("startup")
async def startup_event():
    global query_engine
    print("⚙️  System Initializing...")

    try:
        # A. Settings
        Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=api_key)
        Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # B. Load Index from 'storage'
        print("📂 Loading Index from 'storage' folder...")
        if not os.path.exists("./storage"):
            raise FileNotFoundError("Storage folder not found. Run 'python ingest.py' first.")

        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)

        # C. Advanced Query Engine Configuration
        print("🔧 Configuring Retrieval Engine with Guardrails...")

        qa_prompt_tmpl = PromptTemplate(qa_prompt_str)

        query_engine = index.as_query_engine(
            similarity_top_k=5,
            text_qa_template=qa_prompt_tmpl,

            # --- FIX IS HERE ---
            # Lowered cutoff from 0.70 to 0.40.
            # This allows matches that are "Good enough" but not "Perfect".
            node_postprocessors=[
                SimilarityPostprocessor(similarity_cutoff=0.40)
            ]
        )

        print("✅ System Ready! API is running with Fixed Cutoff.")

    except Exception as e:
        print(f"❌ Error during startup: {e}")
        query_engine = None


# 4. Request Model
class QueryRequest(BaseModel):
    query: str


# 5. API Endpoint
@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    if query_engine is None:
        raise HTTPException(status_code=500, detail="System not initialized.")

    try:
        # Query Engine call
        response = query_engine.query(request.query)

        # --- DEBUGGING: Print scores to console to monitor quality ---
        # This will show you in the terminal what scores your PDF is getting.
        if response.source_nodes:
            print(f"\n🔍 Query: {request.query}")
            for node in response.source_nodes:
                print(f"   --> Score: {node.score:.4f} | File: {node.node.metadata.get('file_name')}")
        else:
            print(f"\n⚠️ Query: {request.query} - No nodes met the cutoff criteria.")

        # --- FAILURE HANDLING ---
        if not response.source_nodes:
            return {
                "response": "⚠️ I could not find any relevant information in the uploaded documents regarding this query. (Low Similarity Score)",
                "sources": []
            }

        # --- Source Extraction Logic ---
        source_data = []

        for node_with_score in response.source_nodes:
            node = node_with_score.node
            page_num = node.metadata.get("page_label", "N/A")
            file_name = node.metadata.get("file_name", "N/A")
            text_content = node.get_content()
            snippet = text_content[:200] + "..." if len(text_content) > 200 else text_content
            score = round(node_with_score.score, 2) if node_with_score.score else 0.0

            source_data.append({
                "file": file_name,
                "page": page_num,
                "text": snippet,
                "score": score
            })

        return {
            "response": str(response),
            "sources": source_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))