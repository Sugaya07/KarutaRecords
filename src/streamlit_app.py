import streamlit as st
from components.show_user import user_show_data
from components.insert_user import user_management
from components.match_result_record import show_karuta_records
from components.show_data import karuta_show_result_by_player, karuta_show_result_by_round
from components.bracket import karuta_show_bracket

# Sidebarの選択肢を定義する
options = ["試合結果記録", "対戦表", "ユーザー管理", "記録閲覧"]
choice = st.sidebar.selectbox("Select an option", options)

# Mainコンテンツの表示を変える
if choice == "試合結果記録":
    show_karuta_records()
elif choice == "対戦表":
    karuta_show_bracket()
elif choice == "ユーザー管理":
    user_management()
    user_show_data()
else:
    karuta_show_result_by_round()
    karuta_show_result_by_player()