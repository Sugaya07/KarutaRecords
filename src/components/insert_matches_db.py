import gspread
import json
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

# 認証スコープ
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials_dict = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"]
}
credentials_json = json.dumps(credentials_dict)

def connect_sps(player1_id, player2_id, result, difference, round_num):
    # サービスアカウントの認証情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(credentials_json), scope)
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_content, scope)

    # Google Sheetsに接続
    gc = gspread.authorize(credentials)

    try:
        # 共有されたスプレッドシートのキー
        spreadsheet_key = '1UONHigFbVAq1YcS9MUfW4xKF7ILIslCUjGkM-4iPXko'

        # 共有されたスプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet("matches")

        # データの読み取り
        data = worksheet.col_values(1)

        # 直前のAセルの値を取得
        last_row = len(data)
        if last_row > 0 and data[last_row-1][0].isdigit():
            last_id = int(data[last_row-1][0])
        else:
            last_id = 0

        new_id = last_id + 1

        # 新しいデータの書き込み
        new_data = [[new_id, player1_id, player2_id, result, difference]]
        worksheet.append_rows(new_data)

        # 共有されたスプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet("rounds")

        # データの読み取り
        data = worksheet.col_values(1)
        # 直前のAセルの値を取得
        last_row = len(data)
        if last_row > 0 and data[last_row-1][0].isdigit():
            last_id = int(data[last_row-1][0])
        else:
            last_id = 0

        round_id = last_id + 1        
        # 新しいデータの書き込み
        new_data = [[round_id, new_id,round_num]]
        worksheet.append_rows(new_data)

    except Exception as e:
        print("エラーが発生しました:", e)
