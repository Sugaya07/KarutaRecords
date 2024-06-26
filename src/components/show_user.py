import streamlit as st
import pandas as pd
from components.utils.connect_sps import fetch_data_from_sheet

def user_show_data():
    data = fetch_data_from_sheet("players")
    df = pd.DataFrame(data, columns=['ID', '名前'])
    st.dataframe(df)