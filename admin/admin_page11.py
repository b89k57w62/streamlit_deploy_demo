import streamlit as st
import pandas as pd

sheet_id = "1nctiWcQFaB5UlIs6z8d1O6ZgMHFDMAoo3twVxYnBUws"
sheet_name = "charlas"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"  # call API return sheets with csv
df = pd.read_csv(url, dtype=str).fillna("")
st.title("Create a search engine with Streamlit and Google Sheets")

keyword_search = st.text_input("Serach something", value="", placeholder="Demo")
m1 = df["Autor"].str.contains(
    keyword_search, case=False
)  # need to str method to use contains method, due to pd
m2 = df["Título"].str.contains(keyword_search, case=False)
df_searched = df[m1 | m2]

N_cards_per_row = 3
if keyword_search:
    for n_row, row in df_searched.reset_index().iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        with cols[i]:
            st.caption(f"{row["Evento"]} - {row["Lugar"]} - {row["Fecha"]}")
            st.markdown(f"**{row["Autor"]}**")
            st.markdown(f"**{row["Título"]}**")
            st.markdown(f"**{row["Video"]}**")
