import streamlit as st
import pandas as pd
from components.utils.connect_sps import fetch_data_from_sheet

def karuta_show_bracket():
    bracket = fetch_data_from_sheet("bracket")
    st.dataframe(bracket)