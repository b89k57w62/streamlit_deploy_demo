import streamlit as st
import pandas as pd
import altair as alt


@st.cache_data
def load_data():
    return pd.read_csv(
        "data/us-population-2010-2019-reshaped.csv",
        index_col=0,
    )


population_data = load_data()
st.header("bar chart")
st.bar_chart(population_data, x="states", y="population")
st.divider()

st.header("interactive bar chart")
selected_year = st.selectbox(
    "Select a year.", population_data.year.unique()[::-1]  # no need to convert to list
)
if selected_year:
    population_selected_year = population_data[population_data.year == selected_year]
    st.bar_chart(population_selected_year, x="states", y="population")

st.divider()

st.header("line chart")
line_chart_data = population_data.copy()
line_chart_data["year"] = line_chart_data["year"].astype(str)  # format 2,019 to 2019
c = (
    alt.Chart(line_chart_data)
    .mark_line()
    .encode(x=alt.X("year"), y=alt.Y("population"), color="states")
)
st.altair_chart(c, use_container_width=True)
st.divider()

st.header("interactive line chart")
states = st.multiselect("Pick states", population_data.states.unique(), "California")
date_range = st.slider("Pick date", 2010, 2019, (2010, 2019))
if states:
    chart_data = population_data[population_data["states"].isin(states)]
    chart_data = chart_data[chart_data["year"].between(date_range[0], date_range[1])]
    chart_data["year"] = chart_data["year"].astype(str)
    c = (
        alt.Chart(chart_data)
        .mark_line()
        .encode(x=alt.X("year"), y=alt.Y("population"), color="states")
    )
st.altair_chart(c, use_container_width=True)
st.divider()

df = pd.DataFrame(
    [
        {"Product": "Apple", "rating": 5},
        {"Product": "AWS", "rating": 3},
        {"Product": "Google", "rating": 4},
    ]
)

edit_df = st.data_editor(
    df,
    column_config={
        "rating": st.column_config.NumberColumn(
            help="max=5, min=1", min_value=1, max_value=5
        )
    },
)

fav_product = edit_df.loc[edit_df["rating"].idxmax()]["Product"]
st.write(f"fav product: {fav_product}")
