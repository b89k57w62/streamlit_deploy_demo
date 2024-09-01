import streamlit as st

st.header("User Index")
st.write(f"You are logged in as {st.session_state.role}")