import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

openai_api_key = st.secrets["OPENAI_API_KEY"]


def gen_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    st.info(model.invoke(input_text))


with st.form("my_form"):
    text = st.text_area("Enter text:")
    submit = st.form_submit_button("Submit")

gen_response(text)
