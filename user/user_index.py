import streamlit as st
import numpy as np
import pandas as pd
import datetime

st.header("line_chart demo")
st.write(f"You are logged in as {st.session_state.role}")


# line-chart
chart_data = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)

st.write("script run time:", datetime.datetime.now())  # check refresh full script
