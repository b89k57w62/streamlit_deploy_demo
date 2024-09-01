import streamlit as st

st.header("Admin Index")
st.write(f"You are logged in as {st.session_state.role}")