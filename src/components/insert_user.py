import streamlit as st
from components.insert_players_db import connect_sps

def user_management():
    st.title("ユーザー管理データベース")

    st.subheader("ユーザー追加")
    user_name = st.text_input('名前', '')
    if st.button('Add User'):
        connect_sps(user_name) 