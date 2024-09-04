import streamlit as st
import pymysql

pymysql.install_as_MySQLdb()
st.set_page_config(layout="wide")
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
user_langchain = st.Page(
    "user/user_langchain.py", title="Build an LLM app using LangChain", icon="🤖"
)

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
admin_page5 = st.Page(
    "admin/admin_page5.py", title="Create a fragment across multiple containers"
)
admin_page6 = st.Page(
    "admin/admin_page6.py", title="Start and stop a streaming fragment"
)
admin_page7 = st.Page(
    "admin/admin_page7.py", title="Streamlit 101: The fundamentals of a Python data app"
)
admin_page8 = st.Page(
    "admin/admin_page8.py", title="Building a dashboard in Python using Streamlit"
)
admin_page9 = st.Page(
    "admin/admin_page9.py", title="Build an image background remover in Streamlit"
)
account_pages = [logout_page, settings]
user_pages = [user_index, user_updte, user_chatbot, user_langchain]
admin_pages = [
    admin_page,
    admin_page2,
    admin_page3,
    admin_page4,
    admin_page5,
    admin_page6,
    admin_page7,
    admin_page8,
    admin_page9,
]


st.title("Request manager")
st.divider()
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
