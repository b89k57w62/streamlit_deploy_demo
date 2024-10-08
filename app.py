import streamlit as st


st.set_page_config(layout="wide")


if "role" not in st.session_state:
    st.session_state.role = None

ROLES = ["Admin", "User"]


def choose_role():
    st.header("Choose the role")
    role = st.selectbox("Choose role", ROLES, index=1)
    if st.button("Submit"):
        st.session_state.role = role
        st.rerun()


def back():
    st.session_state.role = None
    st.rerun()


back_page = st.Page(back, title="Back", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
user_login = st.Page(
    "user/user_login.py",
    title="User Login",
    icon="🅰️",
    default=(st.session_state.role == "User"),
)
user_index = st.Page(
    "user/user_index.py",
    title="User Index",
    icon=":material/person:",
    # default=(st.session_state.role == "User"),
)
user_updte = st.Page("user/user_update.py", title="User Update", icon="👤")
user_chatbot = st.Page("user/user_chatbot.py", title="User Chatbot", icon="🤨")
user_langchain = st.Page(
    "user/user_langchain.py", title="Build an LLM app using LangChain", icon="🤖"
)
admin_login = st.Page(
    "admin/admin_login.py",
    title="Admin Login",
    icon="🅱️",
    default=(st.session_state.role == "Admin"),
)
admin_register = st.Page(
    "admin/admin_register.py",
    title="Admin register",
    icon="❗️",
)
admin_page = st.Page(
    "admin/admin_index.py",
    title="Admin Index",
    icon=":material/person_add:",
    # default=(st.session_state.role == "Admin"),
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
admin_page10 = st.Page(
    "admin/admin_page10.py",
    title="Building a PivotTable report with Streamlit and AG Grid",
)
admin_page11 = st.Page(
    "admin/admin_page11.py",
    title="Create a search engine with Streamlit and Google Sheets",
)
account_pages = [back_page, settings]
user_pages = [user_login, user_index, user_chatbot, user_langchain]
admin_pages = [
    admin_login,
    admin_register,
    admin_page,
    admin_page2,
    admin_page3,
    admin_page4,
    admin_page5,
    admin_page6,
    admin_page7,
    admin_page8,
    admin_page9,
    admin_page10,
    admin_page11,
]


st.title("Streamlit Demo")
st.divider()
page_dict = {}
if st.session_state.role in ["User", "Admin"]:
    page_dict["User"] = user_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(choose_role)])

pg.run()
