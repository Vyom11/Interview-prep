"""
Streamlit frontend.
"""

import uuid

import requests
import streamlit as st

# FastAPI endpoint
API_URL = "http://localhost:8000/agent"

# App title
st.title("AWS Bedrock LangChain Agent Chat")

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me anything. I can use calculator, mock web search, and document retrieval tools.",
        }
    ]

max_iterations = st.sidebar.slider(
    "Max agent iterations",
    min_value=1,
    max_value=10,
    value=6,
    help="Set a safety limit for tool use to prevent runaway agent loops.",
)

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            payload = {
                "question": prompt,
                "conversation_id": st.session_state.conversation_id,
                "max_iterations": max_iterations,
            }
            response = requests.post(API_URL, json=payload)
            data = response.json()
            answer = data.get("answer", "No answer returned.")
            st.session_state.conversation_id = data.get(
                "conversation_id", st.session_state.conversation_id
            )
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
