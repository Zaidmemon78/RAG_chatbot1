import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 AI Course Assistant")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat history dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Agar sources save kiye the toh wo bhi dikhao (Optional logic)
        if "sources" in message:
            with st.expander("📚 Reference Sources"):
                for source in message["sources"]:
                    st.markdown(f"- **Page {source['page']}** ({source['file']})")
                    st.caption(f"\"{source['text']}\"")

# Naya Input
if prompt := st.chat_input("Apna sawal yahan likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        try:
            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"query": prompt}
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("response", "No answer")
                sources = data.get("sources", [])

                # 1. Answer dikhao
                message_placeholder.markdown(answer)

                # 2. Sources dikhao (Expander ke andar)
                if sources:
                    with st.expander("📚 Sources (Kahan se uthaya?)"):
                        for source in sources:
                            st.markdown(f"**📄 Page {source['page']}** - *{source['file']}*")
                            st.info(f"Snippet: {source['text']}")
                            st.markdown("---")

                # History update with sources
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources  # Sources ko bhi history me save kar liya
                })

            else:
                message_placeholder.markdown("⚠️ Server Error")

        except Exception as e:
            message_placeholder.markdown(f"⚠️ Connection Error: {e}")