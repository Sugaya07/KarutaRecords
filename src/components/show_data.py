import streamlit as st
import pandas as pd
from components.utils.connect_sps import fetch_data_from_sheet

def karuta_show_result_by_player():
    players = fetch_data_from_sheet("players")
    player_names = [player[-1] if isinstance(player, list) else player for player in players]
    selected_player = st.selectbox("結果を見たい人の名前を選択してください", player_names)

    data = fetch_data_from_sheet("matches")
    if not data: 
        pass
    df = pd.DataFrame(data, columns=['試合ID', '日付', '対戦者1', '対戦者2', '試合結果(勝者)', '枚数差']).drop(columns=['試合ID'])
    filtered_df = df[(df['対戦者1'].str.contains(selected_player)) | (df['対戦者2'].str.contains(selected_player))]
    def swap_columns(row):
        if row['対戦者2'] == selected_player:
            return pd.Series({'対戦者1': row['対戦者2'], '対戦者2': row['対戦者1']}, index=['対戦者1', '対戦者2'])
        else:
            return pd.Series({'対戦者1': row['対戦者1'], '対戦者2': row['対戦者2']}, index=['対戦者1', '対戦者2'])
    filtered_df[['対戦者1', '対戦者2']] = filtered_df.apply(swap_columns, axis=1)
    print(filtered_df)
    filtered_df['結果'] = filtered_df.apply(
        lambda x: '○' if x['対戦者1'] == x['試合結果(勝者)'] else 'x',
        axis=1
    )
    filtered_df['枚数差'] = filtered_df['結果'] + filtered_df['枚数差'].astype(str)
    filtered_df = filtered_df.drop(columns=['対戦者1', '結果', '試合結果(勝者)'])
    filtered_df = filtered_df.rename(columns={'対戦者2': '対戦者'})
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.write(f"No match results found for {selected_player}.")


def karuta_show_result_by_round():
    matches_data = fetch_data_from_sheet("matches")
    rounds_data = fetch_data_from_sheet("rounds")
    if not matches_data or rounds_data : 
        pass
    
    matches_df = pd.DataFrame(matches_data, columns=['match_id', '日付', '対戦者1', '対戦者2', '試合結果(勝者)', '枚数差'])
    rounds_df = pd.DataFrame(rounds_data, columns=['round_id', 'match_id', 'round_num'])

    date_list = matches_df['日付'].unique()
    sorted_dates = sorted(date_list)
    
    selected_date = st.selectbox("何日の記録を見たいですか", sorted_dates)
    selected_round = st.selectbox("何回戦の記録を見たいですか", list(range(1,8)))

    merged_df = pd.merge(matches_df, rounds_df, on='match_id')
    filtered_df = merged_df[(merged_df['日付'] == selected_date)
                             & (merged_df['round_num'] == str (selected_round))]
    filtered_df = filtered_df.drop(columns=['match_id', 'round_id', 'round_num', '日付'])
    st.dataframe(filtered_df)
