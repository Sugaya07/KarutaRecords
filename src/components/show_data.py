import streamlit as st
import pandas as pd
from components.utils.connect_sps import fetch_data_from_sheet

def karuta_show_result_by_player():
    players = fetch_data_from_sheet("players")
    player_names = [player[-1] if isinstance(player, list) else player for player in players]
    selected_player = st.selectbox("プレイヤーを選択", player_names)

    data = fetch_data_from_sheet("matches")
    if data: 
        df = pd.DataFrame(data, columns=['試合ID', '対戦者1', '対戦者2', '試合結果(勝者)', '枚数差']).drop(columns=['試合ID'])
        filtered_df = df[(df['対戦者1'].str.contains(selected_player)) | (df['対戦者2'].str.contains(selected_player))]
        if not filtered_df.empty:
            st.dataframe(filtered_df)
        else:
            st.write(f"No match results found for {selected_player}.")

