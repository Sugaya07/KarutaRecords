import gspread
import pandas as pd
import streamlit as st
import json
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
# credentials_dict = json.loads(credentials_content)

def fetch_data_from_sheet(table_name: str):
    # サービスアカウントの認証情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(credentials_json), scope)

    # Google Sheetsに接続
    gc = gspread.authorize(credentials)

    try:
        # 共有されたスプレッドシートのキー
        spreadsheet_key = '1UONHigFbVAq1YcS9MUfW4xKF7ILIslCUjGkM-4iPXko'

        # 共有されたスプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet(table_name)

        # データの読み取り
        data = worksheet.get_all_values()
        
        # 2行目以降のデータを取得
        data_from_second_row = data[1:]

        return data_from_second_row

    except Exception as e:
        print("エラーが発生しました:", e)
        return pd.DataFrame()
