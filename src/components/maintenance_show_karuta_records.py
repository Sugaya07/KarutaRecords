import streamlit as st
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from components.insert_matches_db import connect_sps

# 認証スコープ
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# サービスアカウント用の認証情報ファイル（JSON形式）のパス
credentials_file = r"./karutarecords-36984d9fbf52.json"

def fetch_player_data():
    
    # サービスアカウントの認証情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # Google Sheetsに接続
    gc = gspread.authorize(credentials)

    try:
        # 共有されたスプレッドシートのキー
        spreadsheet_key = '1UONHigFbVAq1YcS9MUfW4xKF7ILIslCUjGkM-4iPXko'

        # "players"シートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet("players")

        # データの読み取り
        data = worksheet.get_all_values()
        
        # 2行目以降のデータを取得
        player_data = data[1:]

        # データをデータフレームに変換
        df = pd.DataFrame(player_data, columns=['player_id', 'name'])
        return df

    except Exception as e:
        print("エラーが発生しました:", e)
        return pd.DataFrame()

def show_karuta_records():
    # Google Sheetsからデータを取得
    player_df = fetch_player_data()

    # データが存在しない場合の処理
    if player_df.empty:
        st.write("プレイヤーデータの取得に失敗しました。")
        return

    # 選手データの辞書を作成 key:name, value: id
    player_options = {row['name']: row['player_id'] for _, row in player_df.iterrows()}
    
    # ユーザーインターフェース
    st.title("カルタ試合記録データベース")

    st.subheader("データ追加")

    round_num = st.selectbox("試合数", list(range(1, 8)))
    player1_name = st.selectbox("対戦者1", list(player_options.keys()))
    player2_name = st.selectbox("対戦者2", list(player_options.keys()))
    result_name = st.selectbox("試合結果(勝者)", list(player_options.keys()))
    difference = st.selectbox("枚数差", list(range(1, 26)))

    if st.button('Add data'):
        connect_sps(player1_name, player2_name, result_name, difference, round_num)
        st.write("データを追加しました。ページを再読み込みしてください。")