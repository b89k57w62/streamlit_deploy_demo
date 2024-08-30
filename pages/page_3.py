import streamlit as st
import numpy as np
import pandas as pd
import pymysql


st.sidebar.write("Page 3")
conn = st.connection("my_database")


@st.cache_data
def get_profile_dataset(number_of_items: int = 20, seed: int = 0):
    query_set = conn.query(
        f"""
            SELECT c.first_name, c.last_name, COUNT(r.rental_id) as yearly_rentals from customer as c
            INNER JOIN rental as r on c.customer_id = r.customer_id
            WHERE YEAR(r.rental_date) = 2005
            GROUP BY c.customer_id
            LIMIT {number_of_items}
        """
    )
    df = pd.DataFrame(query_set, columns=["first_name", "last_name", "yearly_rentals"])
    np.random.seed(seed)
    df["daily_activity"] = [np.random.rand(25) for _ in range(len(df))]
    df["activity"] = [np.random.randint(2, 90, size=12) for _ in range(len(df))]

    return df


df = get_profile_dataset()
column_config = {
    "first_name": st.column_config.TextColumn(
        "First Name", help="The first name of the user", max_chars=100, width="medium"
    ),
    "last_name": st.column_config.TextColumn(
        "Last Name", help="The last name of the user", max_chars=100, width="medium"
    ),
    "yearly_rentals": st.column_config.NumberColumn(
        "Yearly Rentals",
        help="Total number of rentals made by the user in the year 2005",
        width="medium",
    ),
    "activity": st.column_config.LineChartColumn(
        "Activity (1 year)",
        help="The user's activity over the last 1 year",
        width="large",
        y_min=0,
        y_max=max(df["yearly_rentals"]),
    ),
    "daily_activity": st.column_config.BarChartColumn(
        "Activity (daily)",
        help="The user's activity in the last 25 days",
        width="medium",
        y_min=0,
        y_max=1,
    ),
}

select, compare = st.tabs(["Select members", "Compare selected"])

with select:
    st.header("All members")
    df = get_profile_dataset()
    event = st.dataframe(
        df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="multi-row",
    )
    st.header("Selected members")
    people = event.selection.rows
    filtered_df = df.iloc[people]

    st.dataframe(
        filtered_df,
        column_config=column_config,
        use_container_width=True,
    )

with compare:
    activity_df = {}
    for person in people:
        activity_df[df.iloc[person]["first_name"]] = df.iloc[person]["activity"]

    activity_df = pd.DataFrame(activity_df)

    daily_activity_df = {}
    for person in people:
        daily_activity_df[df.iloc[person]["first_name"]] = df.iloc[person][
            "daily_activity"
        ]

    daily_activity_df = pd.DataFrame(daily_activity_df)
    if len(people) > 0:
        st.header("Daily activity comparison")
        st.bar_chart(daily_activity_df)
        st.header("Yearly activity comparison")
        st.line_chart(activity_df)
    else:
        st.write("No members selected.")
