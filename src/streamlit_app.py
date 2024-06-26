import streamlit as st
from components.maintenance_show_user import user_show_data
from components.management_user import user_management
from components.maintenance_show_karuta_records import show_karuta_records
from components.maintenace_show_data import karuta_show_result
# from components.insert_players_db import connect_sps

# Sidebarの選択肢を定義する
options = ["試合結果記録ページ", "ユーザー管理ページ", "記録閲覧"]
choice = st.sidebar.selectbox("Select an option", options)

# Mainコンテンツの表示を変える
if choice == "試合結果記録ページ":
    show_karuta_records()
elif choice == "ユーザー管理ページ":
    user_name = user_management()
    user_show_data()
else:
    karuta_show_result()
