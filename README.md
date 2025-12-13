# 🎓 AI Course Assistant — Enterprise‑Grade RAG Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-0.10-EF2D5E?style=for-the-badge)
![Groq](https://img.shields.io/badge/LLM-Groq%20(Llama3)-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)

---

## 📌 What This Project Solves
University students often struggle to search large PDF-based course material efficiently. This project delivers a **production-style Retrieval‑Augmented Generation (RAG) system** that answers questions **strictly from academic PDFs**, ensuring **accurate, syllabus‑aligned responses**.

This is **not a toy chatbot** — it demonstrates **industry‑relevant system design**, clean separation of concerns, and low‑latency inference suitable for real deployments.

---

## 🧠 Core Highlights

- 📚 **PDF‑Grounded Answers** — No hallucinations, responses are retrieved from indexed documents
- ⚡ **Ultra‑Low Latency** — Powered by **Groq LPU inference**
- 🧩 **Modular Microservices Architecture** — Backend & frontend fully decoupled
- 🗂️ **Persistent Vector Store** — One‑time indexing, instant restarts
- 🎯 **Curriculum‑Focused** — Optimized for *Artificial Intelligence (GTU – Subject Code: 3161608)*

---

## 🏗️ System Architecture

The application follows a **Client–Server architecture** with clear responsibility boundaries.

```mermaid
graph LR
    A[User] -->|Query| B[Streamlit Frontend]
    B -->|HTTP POST| C[FastAPI Backend]
    C -->|Search| D[LlamaIndex Query Engine]
    D -->|Retrieve| E[(Vector Store / Storage)]
    D -->|Context + Prompt| F[Groq API (Llama‑3)]
    F -->|LLM Response| C
    C -->|JSON| B
```

### 🔑 Key Technical Decisions

- **FastAPI over Flask**  
  Chosen for async support, automatic OpenAPI docs, and production‑grade performance.

- **LlamaIndex (not LangChain)**  
  Used for its superior document indexing, chunking, and retrieval abstractions.

- **Persistent Vector Storage**  
  Embeddings are generated once via `ingest.py` and reused across sessions.

- **Groq LPU Inference**  
  Uses `llama‑3.3‑70b‑versatile` for near‑instant responses.

---

## 📂 Project Structure

```bash
RAG_CHATBOT/
├── data/               # Source PDFs (Knowledge Base)
├── storage/            # Persisted Vector Index (Auto‑generated)
├── ingest.py           # PDF ingestion & embedding pipeline
├── main.py             # FastAPI backend (RAG inference)
├── frontend.py         # Streamlit UI
├── requirements.txt    # Dependencies
├── .env                # API keys (ignored by git)
└── README.md           # Documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python **3.10+**
- Groq API Key

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-course-assistant.git
cd ai-course-assistant
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=gsk_your_api_key_here
```

---

## ⚡ Usage Guide

### 1️⃣ Data Ingestion (Run Once)

Convert PDFs into vector embeddings:

```bash
python ingest.py
```

📌 This generates the `storage/` directory.

---

### 2️⃣ Start Backend API

```bash
uvicorn main:app --reload
```

- API URL: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`

---

### 3️⃣ Start Frontend UI

```bash
streamlit run frontend.py
```

- Web App: `http://localhost:8501`

---

## 🔌 API Reference

### `POST /chat`

Handles user queries using RAG pipeline.

**Request**
```json
{
  "query": "What are the subfields of Artificial Intelligence?"
}
```

**Response**
```json
{
  "response": "Artificial Intelligence includes subfields such as NLP, Game Playing, Expert Systems, and Connectionist Models..."
}
```

---

## 🔮 Future Enhancements

- 🐳 Docker & Docker‑Compose deployment
- 💾 Chat history with PostgreSQL
- 🔍 Hybrid Search (BM25 + Vector)
- 📊 RAG Evaluation using **RAGAS / DeepEval**
- 🔐 Authentication & multi‑user support

---

## 👨‍💻 Author

**Memon Mohammad Zaid Mohammad Azaz**  
🎓 B.Tech IT | AI & Data Enthusiast

- GitHub: https://github.com/Zaidmemon78
- LinkedIn: www.linkedin.com/in/zaid-memon-analyst


---

⭐ If this project helped you, consider giving it a star!

