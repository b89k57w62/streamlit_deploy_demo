import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_recent_data(last_timestamp):
    now = datetime.now()
    # initialize last_tmestamp, never return more than 60 secs
    if now - last_timestamp > timedelta(seconds=60):
        last_timestamp = now - timedelta(seconds=60)
    sample_time = timedelta(seconds=0.5)
    next_timestamp = sample_time + last_timestamp
    timestamps = np.arange(next_timestamp, now, sample_time)
    sample_values = np.random.randn(len(timestamps), 2)
    data = pd.DataFrame(sample_values, index=timestamps, columns=["a", "b"])
    return data


def toggle_stream():
    st.session_state.stream = not st.session_state.stream


if "data" not in st.session_state:
    st.session_state.data = get_recent_data(datetime.now() - timedelta(seconds=60))

if "stream" not in st.session_state:
    st.session_state.stream = False

st.title("Start and stop a streaming fragment")

st.sidebar.slider(
    "Check for updates every (secs)", 0.5, 5.0, value=1.0, key="run_every"
)

st.sidebar.button("Start", disabled=st.session_state.stream, on_click=toggle_stream)

st.sidebar.button("Stop", disabled=not st.session_state.stream, on_click=toggle_stream)

if st.session_state.stream == True:
    run_every = st.session_state.run_every
else:
    run_every = None


@st.fragment(run_every=run_every)
def show_latest_data():
    last_timestamp = st.session_state.data.index[-1]

    st.session_state.data = pd.concat(
        [st.session_state.data, get_recent_data(last_timestamp)]
    )
    st.session_state.data = st.session_state.data[-100:]
    st.line_chart(st.session_state.data)


show_latest_data()
