import streamlit as st
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import streamlit_authenticator as stauth

load_dotenv()
db = os.getenv("DATABASE_URL")
engine = create_engine(db)


credentials_test = {"usernames": {}}
cookie_test = {
    "name": "my_cookie_register",
    "key": "some_key_register",
    "expiry_days": 30,
}

authenticator_register = stauth.Authenticate(
    credentials_test,
    cookie_test["name"],
    cookie_test["key"],
    cookie_test["expiry_days"],
)
new_user = authenticator_register.register_user(
    pre_authorization=False, key="register_key"
)

hashed_password = stauth.Hasher(["Qweasd1234@"]).generate()[0]
if new_user and all(new_user):
    column_names = ["email", "username", "name"]
    user_data = dict(zip(column_names, new_user))

    user_data["password"] = hashed_password
    user_data["role"] = st.session_state.role

    with engine.begin() as connection:
        existing_user_query = text(
            "SELECT * FROM members WHERE username = :username OR email = :email"
        )
        existing_user = connection.execute(
            existing_user_query,
            {"username": user_data["username"], "email": user_data["email"]},
        ).fetchone()
        if existing_user:
            st.error("existing")
        else:
            insert_query = text(
                "INSERT INTO members (username, email, password, role) VALUES (:username, :email, :password, :role)"
            )
            connection.execute(
                insert_query,
                {
                    "username": user_data["username"],
                    "email": user_data["email"],
                    "password": user_data["password"],
                    "role": user_data["role"],
                },
            )
            st.success("done")

