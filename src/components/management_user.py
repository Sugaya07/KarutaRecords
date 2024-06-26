import streamlit as st
import sqlite3
from components.insert_players_db import connect_sps

def user_management():
    # データベース接続
    conn = sqlite3.connect('karuta_record.db')
    c = conn.cursor()

    # データを表示する関数
    def show_data():
        c.execute('SELECT * FROM players')
        data = c.fetchall()
        for match in data:
            st.write(f"名前: {match[0]}")
            st.write("------")

    # データを追加する関数
    def add_data(user_name):
        if user_name:  # Check if all fields are filled
            c.execute('INSERT INTO players (name) VALUES (?)', (user_name,))
            conn.commit()
            st.write("Success!")
        else:
            st.write("すべての項目に入力してください。")

    c.execute('''CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')


    # ユーザーインターフェース
    st.title("ユーザー管理データベース")

    st.subheader("ユーザー追加")
    user_name = st.text_input('名前', '')
    if st.button('Add User'):
        add_data(user_name)
        connect_sps(user_name) 
        
    # データベース接続を閉じる
    conn.close()
