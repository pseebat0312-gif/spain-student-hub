import streamlit as st
from supabase import create_client

@st.cache_resource
def get_supabase():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = get_supabase()

# 统一获取当前登录用户的邮箱
if "qq_user_email" in st.session_state:
    user_email = st.session_state["qq_user_email"]
elif st.user.is_logged_in:
    user_email = st.user.email
else:
    user_email = ""

def is_user_logged_in():
    return bool(user_email)

def render_sidebar():
    """在每个页面顶部调用，渲染统一的侧边栏"""
    with st.sidebar:
        if not user_email:
            st.info("💡 登录后可使用全部功能")
            if st.button("🔵 Google 登录", use_container_width=True, key="google_login"):
                st.login()
            st.divider()
            if st.button("📧 QQ 邮箱登录", use_container_width=True, key="qq_login_entry"):
                st.session_state["show_qq_login"] = True
        else:
            # 显示用户信息
            profile = supabase.table("user_profiles")\
                .select("nickname", "avatar_emoji")\
                .eq("email", user_email)\
                .execute().data
            if profile:
                display_name = profile[0].get("nickname") or user_email
                display_emoji = profile[0].get("avatar_emoji") or "👤"
            else:
                display_name = user_email
                display_emoji = "👤"
            st.success(f"{display_emoji} {display_name}")
            if st.button("退出登录", use_container_width=True):
                st.logout()
                st.session_state.pop("qq_user_email", None)
                st.rerun()

def require_login():
    """每个需要登录的页面，顶部调用这个"""
    if not user_email:
        st.warning("🔒 请先登录")
        st.page_link("home.py", label="👉 点击前往登录", icon="🔑")
        st.stop()