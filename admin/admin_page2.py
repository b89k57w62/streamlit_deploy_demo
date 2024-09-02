import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data


st.sidebar.write("Page 2")
st.header("tooltips demo")


@st.cache_data
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source


stock_data = get_data()

hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)

lines = (
    alt.Chart(stock_data, title="stock pirces")
    .mark_line()  # creat a line with data points
    .encode(
        x="date",
        y="price",
        color="symbol",
    )
)

points = lines.transform_filter(hover).mark_circle(size=65)

tooltips = (
    alt.Chart(stock_data)
    .mark_rule()
    .encode(
        x="yearmonthdate(date)",
        y="price",
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("date", title="Date"),
            alt.Tooltip("price", title="Price USD"),
        ],
    )
    .add_selection(hover)
)
# layers are added sequentially, each subsequent layer on top of the previous one
data_layer = lines + points + tooltips

st.altair_chart(data_layer, use_container_width=True)
