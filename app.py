import time
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pymysql

pymysql.install_as_MySQLdb()

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Admin", "User"]


def login():
    st.header("Log in")
    role = st.selectbox("Choose role", ROLES)
    if st.button("Login"):
        st.session_state.role = role
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()


logout_page = st.Page(logout, title="Logout", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

user_index = st.Page(
    "user/user_index.py",
    title="User Index",
    icon=":material/person:",
    default=(st.session_state.role == "User"),
)
user_updte = st.Page("user/user_update.py", title="User Update", icon="👤")
user_chatbot = st.Page("user/user_chatbot.py", title="User Chatbot", icon="🤨")

admin_page = st.Page(
    "admin/admin_index.py",
    title="Admin Index",
    icon=":material/person_add:",
    default=(st.session_state.role == "Admin"),
)
admin_page2 = st.Page("admin/admin_page2.py", title="Tooltips demo")
admin_page3 = st.Page("admin/admin_page3.py", title="Tab demo")
admin_page4 = st.Page(
    "admin/admin_page4.py", title="Trigger a full-script rerun from inside a fragment"
)
admin_page5 = st.Page("admin/admin_page5.py", title="tab demo3")
admin_page6 = st.Page("admin/admin_page6.py", title="tab demo4")

account_pages = [logout_page, settings]
user_pages = [user_index, user_updte, user_chatbot]
admin_pages = [
    admin_page,
    admin_page2,
    admin_page3,
    admin_page4,
    admin_page5,
    admin_page6,
]


st.title("Request manager")

page_dict = {}
if st.session_state.role in ["User", "Admin"]:
    page_dict["User"] = user_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
