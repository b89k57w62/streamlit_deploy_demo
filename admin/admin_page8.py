import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


alt.themes.enable("opaque")
df = pd.read_csv("data/us-population-2010-2019-reshaped.csv")
with st.sidebar:
    yr_list = df.year.unique()[::-1]
    selected_yr = st.selectbox("Select a year", yr_list)
    df_selected_yr = df[df.year == selected_yr]
    df_selected_yr_sorted = df_selected_yr.sort_values(by="population", ascending=False)
    color_theme_list = ["blues", "cividis", "greens"]
    selected_color_theme = st.selectbox("Select a color theme", color_theme_list)


def make_heatmap(df, y, x, color, color_theme):
    heatmap = (
        alt.Chart(df)
        .mark_rect()
        .encode(
            y=alt.Y(
                y,
                axis=alt.Axis(
                    title="year",
                    titleFontSize=18,
                    titlePadding=15,
                    titleFontWeight=900,
                    labelAngle=0,
                ),
            ),
            x=alt.X(
                x,
                axis=alt.Axis(
                    title="", titleFontSize=18, titlePadding=15, titleFontWeight=900
                ),
            ),
            color=alt.Color(color, scale=alt.Scale(scheme=color_theme)),
            stroke=alt.value("black"),
            strokeWidth=alt.value(0.25),
        )
        .properties(width=900)
        .configure_axis(labelFontSize=12, titleFontSize=12)
    )
    return heatmap


def make_choropleth(df, id, col, color_theme):
    choropleth = px.choropleth(
        df,
        locations=id,
        color=col,
        locationmode="USA-states",
        range_color=(0, max(df_selected_yr.population)),
        scope="usa",
        labels={"population": "Population"},
    )
    # unnecessary to update layout, because hardcode
    return choropleth


def calculate_population_diff(df, yr):
    selected_yr_data = df[df.year == yr].reset_index()
    previous_yr_data = df[df.year == yr - 1].reset_index()
    selected_yr_data["population_diff"] = selected_yr_data.population.sub(
        previous_yr_data.population, fill_value=0
    )
    return pd.concat(
        [
            selected_yr_data.states,
            selected_yr_data.id,
            selected_yr_data.population,
            selected_yr_data.population_diff,
        ],
        axis=1,
    ).sort_values(by="population_diff", ascending=False)


