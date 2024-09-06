import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


@st.cache_data
def load_data():
    data = pd.read_csv("data/train.csv")  # Titanic Dataset
    return data


data = load_data()
gb = GridOptionsBuilder()
shouldDisplayPivoted = st.checkbox("Pivot data on Pclass")
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)


gb.configure_column(
    field="PassengerId",
    header_name="PassengerId",
    width=100,
    type=["numericColumn"],
)

gb.configure_column(
    field="Pclass",
    header_name="Pclass",
    flex=1,
    type=["numericColumn"],
    rowGroup=shouldDisplayPivoted,
)
gb.configure_column(
    field="Survived",
    header_name="Survived",
    flex=1,
    type=["numericColumn"],
)
if shouldDisplayPivoted == True:
    gb.configure_column(
        field="Survived",
        header_name="Survived",
        flex=1,
        type=["numericColumn"],
        aggFunc="avg",
        valueFormatter="(x*100).toFixed(2) + '%'",
    )
gb.configure_column(
    field="Name",
    header_name="Name",
    flex=1,
    type=["textColumn"],
)
gb.configure_column(
    field="Sex",
    header_name="Sex",
    flex=1,
    type=["textColumn"],
)
gb.configure_column(
    field="Age",
    header_name="Age",
    flex=1,
    type=["numericColumn"],
)
gb.configure_column(
    field="SibSp",
    header_name="Siblings/Spouses Aboard",
    flex=1,
    type=["numericColumn"],
)
gb.configure_column(
    field="Parch",
    header_name="Parents/Children Aboard",
    flex=1,
    type=["numericColumn"],
)
gb.configure_column(
    field="Ticket",
    header_name="Ticket Number",
    flex=1,
)
gb.configure_column(
    field="Fare", header_name="Fare", flex=1, type=["numericColumn"], aggFunc="sum"
)
gb.configure_column(
    field="Cabin",
    header_name="Cabin",
    flex=1,
)
gb.configure_column(
    field="Embarked",
    header_name="Port of Embarkation",
    flex=1,
)


gb.configure_grid_options(pivotMode=shouldDisplayPivoted)
go = gb.build()

AgGrid(data, gridOptions=go, height=400)
