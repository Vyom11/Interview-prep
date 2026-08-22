"""
Streamlit frontend for the routing agent.
"""

import uuid

import requests
import streamlit as st

API_URL = "http://localhost:8000/chat"

st.title("Intelligent SQL + RAG Agent")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Ask about **database metrics** (sales, orders, customers) or "
                "**document content** (policies, PDFs), or both. I'll route your question automatically."
            ),
        }
    ]

with st.sidebar:
    st.caption(f"Session: `{st.session_state.session_id[:8]}…`")
    if st.button("New conversation"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Started a new conversation. How can I help?",
            }
        ]
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("route"):
            st.caption(f"Route: **{message['route']}**")

if prompt := st.chat_input("Ask your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Routing and thinking…"):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": prompt,
                        "session_id": st.session_state.session_id,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                answer = data.get("answer", "No answer returned.")
                route = data.get("route", "")
            except requests.RequestException as exc:
                answer = f"Backend error: {exc}"
                route = ""

        st.markdown(answer)
        if route:
            st.caption(f"Route: **{route}**")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "route": route}
    )
