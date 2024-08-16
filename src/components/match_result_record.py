import streamlit as st
import pandas as pd
from components.insert_matches_db import connect_sps
from components.utils.connect_sps import fetch_data_from_sheet

def show_karuta_records():
    player_list = fetch_data_from_sheet("players")
    player_df = pd.DataFrame(player_list, columns=['player_id', 'name'])

    # データが存在しない場合の処理
    if player_df.empty:
        st.write("プレイヤーデータの取得に失敗しました。")
        return

    # 選手データの辞書を作成
    player_options = {row['name']: row['player_id'] for _, row in player_df.iterrows()}
    
    # ユーザーインターフェース
    st.title("カルタ試合記録データベース")

    st.subheader("対戦結果記録")

    round_num = st.number_input("試合数", min_value=1)
    player1_name = st.selectbox("対戦者1", list(player_options.keys()))
    player2_name = st.selectbox("対戦者2", [name for name in player_options.keys() if name != player1_name])
    result_name = st.selectbox("試合結果(勝者)", [player1_name, player2_name])
    difference = st.number_input("枚数差",min_value=1)

    if st.button('Add data'):
        connect_sps(player1_name, player2_name, result_name, difference, round_num)
        st.write("データを追加しました。ページを再読み込みしてください。")