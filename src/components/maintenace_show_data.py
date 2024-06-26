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

def fetch_karuta_data():
    # サービスアカウントの認証情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # Google Sheetsに接続
    gc = gspread.authorize(credentials)

    try:
        # 共有されたスプレッドシートのキー
        spreadsheet_key = '1UONHigFbVAq1YcS9MUfW4xKF7ILIslCUjGkM-4iPXko'

        # 共有されたスプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet("matches")

        # データの読み取り
        data = worksheet.get_all_values()
        
        # 2行目以降のデータを取得
        data_from_second_row = data[1:]

        return data_from_second_row

    except Exception as e:
        print("エラーが発生しました:", e)
        return []

def karuta_show_result():
    # Google Sheetsからデータを取得
    st.subheader("結果表示")
    data = fetch_karuta_data()

    if data:  # データが存在する場合
        # データをデータフレームに変換
        df = pd.DataFrame(data, columns=['試合ID', '対戦者1', '対戦者2', '試合結果(勝者)', '枚数差'])

        # データをテーブル形式で表示
        st.dataframe(df)
    else:
        st.write("データがありません。")

    