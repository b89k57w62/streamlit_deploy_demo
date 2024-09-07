import streamlit as st
import streamlit_authenticator as stauth
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from streamlit_authenticator.controllers import AuthenticationController
from typing import Optional, List, Callable

load_dotenv()
db = os.getenv("DATABASE_URL")
engine = create_engine(db)


class CustomAuthenticator(stauth.Authenticate):  # views
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


class CustomAuthenticationController(AuthenticationController):
    def __init__(self, credentials: dict, *args, **kwargs):
        super().__init__(credentials, *args, **kwargs)
        self.engine = create_engine(db)

    def register_user(self, new_name: str, *args, **kwargs):
        email, username, name = super().register_user(new_name, *args, **kwargs)

        if email and username and name:
            try:
                hashed_password = self.authentication_model.credentials["usernames"][
                    username
                ]["password"]

                role = st.session_state.get("role", "User")
                st.write(
                    f"Attempting to insert: username={username}, email={email}, name={name}, password={hashed_password}, role={role}"
                )
                with self.engine.connect() as connection:
                    query = text(
                        """
                        INSERT INTO members (username, email, name, password, role)
                        VALUES (:username, :email, :name, :password, :role)
                    """
                    )
                    connection.execute(
                        query,
                        {
                            "username": username,
                            "email": email,
                            "name": name,
                            "password": hashed_password,
                            "role": role,
                        },
                    )
                    st.success(
                        f"User {name} successfully registered and saved to database."
                    )
            except Exception as e:
                st.error(f"An error occurred while saving user to the database: {e}")
        return email, username, name
