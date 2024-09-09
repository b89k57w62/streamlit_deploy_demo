import streamlit as st
import streamlit_authenticator as stauth
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
db = os.getenv("DATABASE_URL")



class CustomAuthenticator(stauth.Authenticate): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine(db)

    def login(self, form_name, location="main"):
        if location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == "main":
            login_form = st.form(key="login_form", clear_on_submit=True)
        elif location == "sidebar":
            login_form = st.sidebar.form(key="login_form", clear_on_submit=True)

        login_form.subheader("Login")
        username_input = login_form.text_input("Username")
        password_input = login_form.text_input("Password", type="password")

        if login_form.form_submit_button("Login"):
            user = self._fetch_user_from_db(username_input)
            if user:
                if self._check_password(user["password"], password_input):
                    st.session_state["name"] = user["name"]
                    st.session_state["authentication_status"] = True
                    st.session_state["username"] = username_input
                    return user["name"], True, username_input
                else:
                    st.session_state["authentication_status"] = False
                    return None, False, None
            else:
                st.error("User not found")
                return None, False, None
        return None, None, None

    def _fetch_user_from_db(self, username):
        query = text(
            "SELECT username, password, name, role FROM members WHERE username = :username"
        )
        with self.engine.connect() as connection:
            result = connection.execute(query, {"username": username})
            user = result.fetchone()
            if user:
                column_names = result.keys()
                user_dict = dict(zip(column_names, user))
                return user_dict
            return None

    def _check_password(self, hashed_password, input_password):
        from bcrypt import checkpw

        return checkpw(input_password.encode("utf-8"), hashed_password.encode("utf-8"))


