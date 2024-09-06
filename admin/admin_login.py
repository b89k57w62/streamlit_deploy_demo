import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
from database import MemberDatabase


db = MemberDatabase("my_database")
users = db.fetch_all()
st.write("Admin Login Page")

credentials = {
    "usernames": {
        row["username"]: {"name": row["name"], "password": row["password"]}
        for _, row in users.iterrows()
    }
}

authenticator = stauth.Authenticate(credentials, "Demo", "abcd", cookie_expiry_days=0)

name, authentication_status, username = authenticator.login()

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.write(f"Admin, {name}")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")
