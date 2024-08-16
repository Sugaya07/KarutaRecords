import streamlit as st
from components.show_user import user_show_data
from components.insert_user import user_management
from components.match_result_record import show_karuta_records
from components.show_data import karuta_show_result_by_player, karuta_show_result_by_round

# Sidebarの選択肢を定義する
options = ["試合結果記録ページ", "ユーザー管理ページ", "記録閲覧"]
choice = st.sidebar.selectbox("Select an option", options)

# Mainコンテンツの表示を変える
if choice == "試合結果記録ページ":
    show_karuta_records()
elif choice == "ユーザー管理ページ":
    user_management()
    user_show_data()
else:
    karuta_show_result_by_player()
    karuta_show_result_by_round()
