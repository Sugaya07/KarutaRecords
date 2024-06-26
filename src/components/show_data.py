import streamlit as st
import pandas as pd
from components.utils.connect_sps import fetch_data_from_sheet

def karuta_show_result():
    st.subheader("結果表示")
    data = fetch_data_from_sheet("matches")

    if data: 
        df = pd.DataFrame(data, columns=['試合ID', '対戦者1', '対戦者2', '試合結果(勝者)', '枚数差'])

        st.dataframe(df)
    else:
        st.write("データがありません。")

    