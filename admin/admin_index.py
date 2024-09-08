import streamlit as st
import time
import numpy as np
import pandas as pd

st.header("st.write_stream, st.session_state demo")
st.write(f"You are logged in as {st.session_state.role}")


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
    time.sleep(5)
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
