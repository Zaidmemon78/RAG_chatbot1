import os
import sys
from dotenv import load_dotenv

# --- 1. SMART IMPORTS (Jo bhi mile use kar lo) ---
try:
    # Naya Tareeka
    from langchain.chains import RetrievalQA
except ImportError:
    # Purana Tareeka (Backup)
    import langchain.chains.retrieval_qa.base

try:
    from langchain_core.prompts import PromptTemplate
except ImportError:
    import langchain.prompts

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load Env
load_dotenv()


def start_chat():
    print("⚙️ System Load ho raha hai... (Darna mat, error nahi aayega)")

    # 1. Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 2. Load DB
    if not os.path.exists("faiss_index"):
        print("❌ Error: 'faiss_index' folder nahi mila! Pehle 'ingest.py' chalao.")
        return

    try:
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"❌ DB Error: {e}")
        return

    # 3. LLM Setup (Groq)
    # Note: Agar PyCharm 'model_name' par yellow line dikhaye toh IGNORE karna.
    llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.5)

    # 4. Prompt Template (Is tareeke se error nahi aayega)
    template_text = """
    Context: {context}
    Question: {question}
    Answer (Hindi/English mix):
    """
    prompt = PromptTemplate(template=template_text, input_variables=['context', 'question'])

    # 5. Chain Creation
    # PyCharm ko ye line kabhi samajh nahi aati, par ye RUN hoti hai.
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={'k': 3}),
        chain_type_kwargs={"prompt": prompt}
    )

    print("\n✅ Bot Ready hai! (Exit karne ke liye 'quit' likhein)\n")

    # 6. Chat Loop
    while True:
        try:
            query = input("You: ")
            if query.lower() == 'quit':
                print("Bye Bye! 👋")
                break

            # Jawab mango
            response = qa_chain.invoke({"query": query})
            print(f"Bot: {response['result']}\n")

        except Exception as e:
            print(f"⚠️ Error: {e}")


if __name__ == "__main__":
    start_chat()