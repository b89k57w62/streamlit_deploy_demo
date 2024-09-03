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


def make_donut(response, text, color):
    if color == "green":
        chart_color = ["#27AE60", "#12783D"]
    if color == "red":
        chart_color = ["#E74C3C", "#781F16"]

    source = pd.DataFrame({"Topic": ["", text], "% value": [100 - response, response]})
    source_bg = pd.DataFrame(
        {"Topic": ["", text], "% value": [100, 0]}
    )
    plot = (
        alt.Chart(source)
        .mark_arc(innerRadius=45, outerRadius=25)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic", scale=alt.Scale(domain=[text, ""], range=chart_color)
            ),
        )
        .properties(width=130, height=130)
    )
    plot_text = plot.mark_text(
        align="center",
        color="#29b5e8",
        font="Lato",
        fontSize=18,
        fontWeight=700,
        fontStyle="italic",
    ).encode(text=alt.value(f"{response} %"))
    plot_bg = (
        alt.Chart(source_bg)
        .mark_arc(innerRadius=45, outerRadius=20)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic", scale=alt.Scale(domain=[text, ""], range=chart_color)
            ),
        )
        .properties(width=130, height=130)
    )
    return plot_bg + plot + plot_text


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

col = st.columns((1.5, 4.5, 2), gap="medium")

with col[0]:
    st.write("Gains/losses")
    df_population_diff = calculate_population_diff(df, selected_yr)

    if selected_yr > 2010:
        state_name = df_population_diff.states.iloc[0]
        state_population = int(df_population_diff.population.iloc[0])
        state_delta = int(df_population_diff.population_diff.iloc[0])
    else:
        state_name = "-"
        state_population = "-"
        state_delta = ""
    
    st.metric(label=state_name, value=state_population, delta=state_delta)

    if selected_yr > 2010:
        state_name = df_population_diff.states.iloc[-1]
        state_population = int(df_population_diff.population.iloc[-1])
        state_delta = int(df_population_diff.population_diff.iloc[-1])
    else:
        state_name = "-"
        state_population = "-"
        state_delta = ""
    
    st.metric(label=state_name, value=state_population, delta=state_delta)

    st.write("States Migration")
    
    if selected_yr > 2000:
        df_gt_50000 = df_population_diff[df_population_diff.population_diff > 50000]
        df_lt_50000 = df_population_diff[df_population_diff.population_diff < -50000]
        states_migration_gt = round(len(df_gt_50000) / df_population_diff.states.nunique() * 100)
        states_migration_lt = round(len(df_lt_50000) / df_population_diff.states.nunique() * 100)
        dount_chart_gt = make_donut(states_migration_gt, "Inbound Migration", "green")
        dount_chart_lt = make_donut(states_migration_lt, "Outbound Migration", "red")
    else:
        states_migration_gt = 0
        states_migration_lt = 0
        dount_chart_gt = make_donut(states_migration_gt, "Inbound Migration", "green")
        dount_chart_lt = make_donut(states_migration_lt, "Outbound Migration", "red")
    
    migration_col = st.columns((0.2, 1, 0.2))
    with migration_col[1]:
        st.write("Inbound")
        st.altair_chart(dount_chart_gt)
        st.write("Outbound")
        st.altair_chart(dount_chart_lt)