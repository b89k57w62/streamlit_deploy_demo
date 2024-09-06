import streamlit as st


class MemberDatabase:
    def __init__(self, db):
        self.conn = st.connection(db)

    def fetch_all(self):
        query = "SELECT * FROM members"
        data_set = self.conn.query(query)
        return data_set
