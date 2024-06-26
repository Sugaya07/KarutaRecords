import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証スコープ
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# サービスアカウント用の認証情報ファイル（JSON形式）のパス
credentials_file = r"./karutarecords-36984d9fbf52.json"

def connect_sps(player1_id, player2_id, result, difference, round_num):
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
        print("スプレッドシートのデータ:")
        print(data)

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
        print("新しいデータが追加されました。")

        # 共有されたスプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).worksheet("rounds")

        # データの読み取り
        data = worksheet.get_all_values()
        print("スプレッドシートのデータ:")
        print(data)
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
        print("新しいデータが追加されました。")

    except Exception as e:
        print("エラーが発生しました:", e)
