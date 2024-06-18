import streamlit as st
import sqlite3
import pandas as pd

# Sidebarの選択肢を定義する
options = ["試合結果記録ページ", "ユーザー管理ページ", "記録閲覧"]
choice = st.sidebar.selectbox("Select an option", options)

# 1から25までのリストを作成
karuta_difference = list(range(1, 30))

def karuta_show_data():
    # データベース接続
    conn = sqlite3.connect('karuta_record.db')
    c = conn.cursor()

    # データを表示する関数
    def show_data():
        c.execute('SELECT * FROM matches')
        data = c.fetchall()
        for match in data:
            st.write(f"試合ID: {match[0]}")
            st.write(f"対戦者1: {match[1]}")
            st.write(f"対戦者2: {match[2]}")
            st.write(f"試合結果(勝者): {match[3]}")
            st.write(f"枚数差: {match[4]}")
            st.write("------")
    st.subheader("データ表示")
    show_data()


def showdata():
    # データベース接続
    conn = sqlite3.connect('karuta_record.db')
    c = conn.cursor()

    # データを追加する関数
    def add_data(player1_id,player2_id, result, difference):
        if player1_id and player2_id and result and difference:  # Check if all fields are filled
            c.execute('INSERT INTO matches (player1_id, player2_id, result, difference) VALUES (?, ?, ?, ?)', (player1_id, player2_id, result, difference))
            conn.commit()
            st.write("データを追加しました。ページを再読み込みしてください。")
        else:
            st.write("すべての項目に入力してください。")

    # データベースにテーブルを作成する
    c.execute('''CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player1_id INTEGER NOT NULL,
        player2_id INTEGER NOT NULL,
        result TEXT NOT NULL,
        difference INTEGER NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS rounds (
        round_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER NOT NULL,
        round_num INTEGER NOT NULL,
        winner_id INTEGER NOT NULL,
        FOREIGN KEY (match_id) REFERENCES matches(match_id),
        FOREIGN KEY (winner_id) REFERENCES players(player_id)
    )''')

    # ユーザーインターフェース
    st.title("カルタ試合記録データベース")

    st.subheader("データ追加")
    # 選手IDと名前を取得
    c.execute('SELECT player_id, name FROM players')
    player_data = c.fetchall()

    # 選手データの辞書を作成
    player_options = {name : player_id for player_id, name in player_data}
    
    player1_id = st.selectbox("対戦者1", list(player_options.keys()))
    player2_id = st.selectbox("対戦者2", list(player_options.keys()))
    result = st.selectbox("試合結果(勝者)", [player1_id, player2_id])
    difference = st.selectbox("枚数差", karuta_difference)
    if st.button('Add data'):
        add_data(player1_id, player2_id, result, difference)


def user_management():
    # データベース接続
    conn = sqlite3.connect('karuta_record.db')
    c = conn.cursor()

    # データを表示する関数
    def show_data():
        c.execute('SELECT * FROM players')
        data = c.fetchall()
        for match in data:
            st.write(f"ユーザーID: {match[0]}")
            st.write(f"名前: {match[1]}")
            st.write("------")

    data = c.fetchall()
    for match in data:
        st.write(f"名前: {match[0]}")
        st.write("------")

    # データを追加する関数
    def add_data(user_name):
        if user_name:  # Check if all fields are filled
            c.execute('INSERT INTO players (name) VALUES (?)', (user_name,))
            conn.commit()
            st.write("データを追加しました。ページを再読み込みしてください。")
        else:
            st.write("すべての項目に入力してください。")

    c.execute('''CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')

    # ユーザーインターフェース
    st.title("ユーザー管理データベース")

    st.subheader("データ表示")
    show_data()

    st.subheader("ユーザー追加")
    # テキスト入力ボックス
    user_name = st.text_input('名前', 'Input some text here.')
    if st.button('Add data'):
        add_data(user_name)


# データを表示する関数


def user_show_data():
    # データベース接続
    conn = sqlite3.connect('karuta_record.db')
    c = conn.cursor()

    # データベースからデータを取得
    c.execute('SELECT * FROM players')
    data = c.fetchall()

    # データをデータフレームに変換
    df = pd.DataFrame(data, columns=['ユーザーID', '名前'])

    # データをテーブル形式で表示
    st.dataframe(df)

    # データベース接続を閉じる
    conn.close()
# Mainコンテンツの表示を変える
if choice == "試合結果記録ページ":
    showdata()
elif choice == "ユーザー管理ページ":
    user_management()
    user_show_data()
else:
    karuta_show_data()