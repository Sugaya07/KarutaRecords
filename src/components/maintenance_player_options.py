# def get_player_options():
#     conn = sqlite3.connect('karuta_record.db')
#     c = conn.cursor()
#     c.execute('SELECT player_id, name FROM players')
#     player_data = c.fetchall()
#     player_options = {name: player_id for player_id, name in player_data}
#     conn.close()
#     return player_options

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証スコープ
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# サービスアカウント用の認証情報ファイル（JSON形式）のパス
credentials_file = r"./karutarecords-36984d9fbf52.json"

def get_player_options():
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

        # プレイヤーデータの辞書を作成
        player_options = {row[1]: int(row[0]) for row in player_data}
        return player_options

    except Exception as e:
        print("エラーが発生しました:", e)
        return {}

# テスト用にStreamlitで表示
st.title("Player Options from Google Sheets")
player_options = get_player_options()
st.write(player_options)

# def karuta_show_data():
#     # データベース接続
#     conn = sqlite3.connect('karuta_record.db')
#     c = conn.cursor()

#     # データを表示する関数
#     def show_data():
#         c.execute('SELECT * FROM matches')
#         data = c.fetchall()
#         for match in data:
#             st.write(f"試合ID: {match[0]}")
#             st.write(f"対戦者1: {match[1]}")
#             st.write(f"対戦者2: {match[2]}")
#             st.write(f"試合結果(勝者): {match[3]}")
#             st.write(f"枚数差: {match[4]}")
#             st.write("------")
#     st.subheader("データ表示")
#     show_data()
