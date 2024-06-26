import gspread
import streamlit as st
import json
from oauth2client.service_account import ServiceAccountCredentials
from components.utils.connect_sps import fetch_data_from_sheet

# 認証スコープ
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# サービスアカウント用の認証情報ファイル（JSON形式）のパス
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

def connect_sps(user_name):
    # サービスアカウントの認証情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(credentials_json), scope)
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_content, scope)

    # Google Sheetsに接続
    gc = gspread.authorize(credentials)

    try:
        # 共有されたスプレッドシートのキー
        spreadsheet_key = '1UONHigFbVAq1YcS9MUfW4xKF7ILIslCUjGkM-4iPXko'

        # 共有されたスプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet("players")

        # シートの実際の行数を取得
        data = worksheet.col_values(1)

        # 直前のAセルの値を取得
        last_row = len(data)
        if last_row > 0 and data[last_row-1][0].isdigit():
            last_id = int(data[last_row-1][0])
        else:
            last_id = 0

        new_id = last_id + 1

        # 新しいデータの書き込み
        new_data = [[new_id, user_name]]
        worksheet.append_rows(new_data)

    except Exception as e:
        print("エラーが発生しました:", e)
