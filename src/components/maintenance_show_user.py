import streamlit as st
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# 認証スコープ
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# サービスアカウント用の認証情報ファイル（JSON形式）のパス
credentials_file = r"./karutarecords-36984d9fbf52.json"

def fetch_data_from_sheet():
    # サービスアカウントの認証情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # Google Sheetsに接続
    gc = gspread.authorize(credentials)

    try:
        # 共有されたスプレッドシートのキー
        spreadsheet_key = '1UONHigFbVAq1YcS9MUfW4xKF7ILIslCUjGkM-4iPXko'

        # 共有されたスプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet("players")

        # データの読み取り
        data = worksheet.get_all_values()
        
        # 2行目以降のデータを取得
        data_from_second_row = data[1:]
        return data_from_second_row

    except Exception as e:
        print("エラーが発生しました:", e)


def user_show_data():
    data = fetch_data_from_sheet()

    # データをデータフレームに変換
    df = pd.DataFrame(data, columns=['ID', '名前'])

    # データをテーブル形式で表示
    st.dataframe(df)