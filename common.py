import streamlit as st
from supabase import create_client

# 连接 Supabase
@st.cache_resource
def get_supabase():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = get_supabase()

# 统一获取当前登录用户的邮箱
if st.user.is_logged_in:
    user_email = st.user.email
else:
    user_email = st.session_state.get("qq_user_email", "")

# 判断是否登录
def is_user_logged_in():
    return bool(user_email)

import streamlit as st

def remember_page():
    if "last_page" not in st.session_state:
        st.session_state["last_page"] = "home.py"
    current = st.session_state.get("current_page", "home.py")
    if current != st.session_state["last_page"]:
        st.session_state["last_page"] = current

def go_back():
    if st.button("⬅️ 返回上一步"):
        st.switch_page(st.session_state.get("last_page", "home.py"))