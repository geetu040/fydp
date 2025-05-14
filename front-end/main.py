import streamlit as st
import httpx
import time

BACKEND_API_URL = "http://20.102.45.30:8000/generate"

st.title("Data Orator: Seamless SQL Integration")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input and response handling
if prompt := st.chat_input("What is the latest iPhone model available?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with httpx.stream("POST", BACKEND_API_URL, json={"messages": st.session_state.messages}) as r:
            response = st.write_stream(r.iter_text())

    st.session_state.messages.append({"role": "assistant", "content": response})
