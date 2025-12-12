# 📚 RAG Chatbot with LlamaIndex & Groq

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-purple)
![Groq](https://img.shields.io/badge/LLM-Llama3-orange)

## 🚀 About The Project
This is a **Retrieval-Augmented Generation (RAG) Chatbot** designed to answer questions from custom PDF documents (like a University Syllabus). 

Unlike standard chatbots that hallucinate, this bot uses **your specific data** to provide accurate answers. It is built using **LlamaIndex** for data ingestion and **Groq API (Llama 3)** for ultra-fast inference.

### 🌟 Key Features
- **Custom Data:** Works with any PDF file (Syllabus, Resume, Reports).
- **Fast Inference:** Uses Groq's LPU engine for lightning-fast responses.
- **Open Source Models:** Powered by Llama 3 and HuggingFace Embeddings.
- **Privacy First:** Your API keys and data remain local.

---

## 🛠️ Tech Stack
- **Language:** Python
- **Framework:** LlamaIndex
- **LLM:** Llama 3.3 (via Groq API)
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Store:** In-memory VectorStoreIndex

---

## 📂 Project Structure
```text
RAG-Chatbot/
│
├── data/                  # Place your PDF files here
│   └── syllabus.pdf
│
├── .env                   # API Keys (Not uploaded to GitHub)
├── .gitignore             # Files to exclude from Git
├── bot.py                 # Main application script
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation