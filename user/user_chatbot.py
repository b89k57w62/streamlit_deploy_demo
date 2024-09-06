import streamlit as st
from openai import OpenAI

st.title("Chatbot-Demo")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

role = st.session_state.role

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Say something."):
    st.session_state.messages.append({"role": role, "content": prompt})
    st.chat_message(role).write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": message["role"], "content": message["content"]}
                for message in st.session_state.messages
            ],
            stream=True,  # will return generator
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
