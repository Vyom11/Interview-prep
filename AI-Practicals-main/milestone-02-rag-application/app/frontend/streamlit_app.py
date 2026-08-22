"""
Streamlit frontend.
"""

# Import streamlit
# Import requests
import requests
import streamlit as st

# FastAPI endpoint
API_URL = "http://localhost:8000/ask"

# App title
st.title("AWS Bedrock RAG Chatbot")

# Initialize session state
if "messages" not in st.session_state:

    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me anything about your PDF documents."}
    ]

# Display messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask your question"):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            # Call backend
            response = requests.post(API_URL, json={"question": prompt})

            # Extract answer
            answer = response.json()["answer"]

            # Display answer
            st.markdown(answer)

    # Store assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
