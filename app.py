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

user_index = st.Page("user/user_index.py", title="User Index", icon=":material/person:", default=(st.session_state.role == "User"))
user_updte = st.Page("user/user_update.py", title="User Update", icon="👤")

admin_page = st.Page("admin/admin_index.py", title="Admin Index", icon=":material/person_add:", default=(st.session_state.role == "Admin"))


account_pages = [logout_page, settings]
user_pages = [user_index, user_updte]
admin_pages = [admin_page]


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
# line-chart
chart_data = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)

st.write("script run time:", datetime.datetime.now())  # check refresh full script


# write_stream
def stream_data():
    for num in range(1, 11):
        yield str(num) + " "
        time.sleep(0.1)

    yield pd.DataFrame(np.random.randn(10, 5), columns=["a", "b", "c", "d", "e"])


if "show_data" not in st.session_state:  # like st.session_state={}
    st.session_state.show_data = False

if st.button("show/hide_data"):
    st.session_state.show_data = not st.session_state.show_data

if st.session_state.show_data:
    st.write_stream(stream_data)


@st.cache_data
def test_cache(a, b):
    time.sleep(2)
    return a + b


if st.button("check_cache"):
    st.write(test_cache(1, 2))

# another way to generate a table, difference between st.write()
# more arguments and more interative to control table
dataframe = pd.DataFrame(
    np.random.randn(10, 20), columns=("col %d" % i for i in range(20))
)
st.dataframe(dataframe.style.highlight_max(axis=0))  # axis=0 for column, 1 for row


# assigning keys to widgets and preserve the state
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
    key="contacted_method",
)
st.sidebar.write(st.session_state.contacted_method)



conn = st.connection("my_database")
df = conn.query("select * from actor where actor_id = 1")
st.dataframe(df)
