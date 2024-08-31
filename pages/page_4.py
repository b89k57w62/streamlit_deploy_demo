import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import time


@st.cache_data
def get_data():
    conn = st.connection("my_database")
    query_set = conn.query(
        """
            SELECT category, total_sales FROM sales_by_film_category
        """
    )
    category = query_set["category"].tolist()
    total_sales = query_set["total_sales"].tolist()
    average_daily_sales = [round(sale / 30, 2) for sale in total_sales]
    products = dict(zip(category, average_daily_sales))

    data = pd.DataFrame({})
    sales_dates = np.arange(date(2023, 1, 1), date(2024, 1, 1), timedelta(days=1))
    for category, sales in products.items():
        data[category] = np.random.normal(sales, 20, len(sales_dates))
    data.index = sales_dates
    data.index = data.index.date  # format data
    return data


@st.fragment
def show_daily_sales(data):
    with st.container(height=100):
        selected_date = st.date_input(
            "Pick a day ",
            value=date(2023, 1, 1),
            min_value=date(2023, 1, 1),
            max_value=date(2023, 12, 31),
            key="selected_date",
        )
    if "previous_date" not in st.session_state:
        st.session_state.previous_date = selected_date
    previous_date = st.session_state.previous_date
    st.session_state.previous_date = selected_date
    is_new_month = selected_date.replace(day=1) != previous_date.replace(day=1)
    if is_new_month:
        st.rerun()
    with st.container(height=510):
        st.header(f"Best sellers, {selected_date:%m/%d/%y}")
        top_three = data.loc[selected_date].sort_values(ascending=False)[0:3]
        cols = st.columns([1, 4])
        cols[0].dataframe(top_three)
        cols[1].bar_chart(top_three)

    with st.container(height=510):
        st.header(f"Worst sellers, {selected_date:%m/%d/%y}")
        bottom_three = data.loc[selected_date].sort_values()[0:3]
        cols = st.columns([1, 4])
        cols[0].dataframe(bottom_three)
        cols[1].bar_chart(bottom_three)


def show_monthly_sales(data):
    selected_date = st.session_state.selected_date
    this_month = selected_date.replace(day=1)
    next_month = (selected_date.replace(day=28) + timedelta(days=4)).replace(day=1)

    st.container(height=100, border=False)
    with st.container(height=510):
        st.header(f"Daily sales for all products, {this_month:%B %Y}")
        monthly_sales = data[(data.index < next_month) & (data.index >= this_month)]
        st.write(monthly_sales)
    with st.container(height=510):
        st.header(f"Total sales for all products, {this_month:%B %Y}")
        st.bar_chart(monthly_sales.sum())


st.set_page_config(layout="wide")
st.title("Daily vs monthly sales, by product")

data = get_data()
daily, monthly = st.columns(2)
with daily:
    show_daily_sales(data)
with monthly:
    show_monthly_sales(data)
