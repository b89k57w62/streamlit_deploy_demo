import streamlit as st
import os
from database import CustomAuthenticator, CustomAuthenticationController
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import streamlit_authenticator as stauth

load_dotenv()
db = os.getenv("DATABASE_URL")
engine = create_engine(db)
st.write("User Login Page")


def generate_credentials():
    query = text("SELECT username, password, name FROM members")
    with engine.connect() as connection:
        result = connection.execute(query)
        users = result.fetchall()
        column_names = result.keys()
    credentials = {
        "usernames": {
            dict(zip(column_names, user))["username"]: {
                "name": dict(zip(column_names, user))["name"],
                "password": dict(zip(column_names, user))["password"],
            }
            for user in users
        }
    }
    return credentials


credentials = generate_credentials()

authenticator = CustomAuthenticator(
    credentials, "test_inherit", "abcdef", cookie_expiry_days=0
)

if st.session_state.role == "User":
    name, authentication_status, username = authenticator.login("Login")
    if authentication_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.write(f"Welcome, {name}")
    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")
