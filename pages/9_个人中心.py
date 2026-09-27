import streamlit as st
from supabase import create_client

from styles import apply_sidebar_style
apply_sidebar_style()

import sys
sys.path.append("..")
from common import supabase, user_email, is_user_logged_in

# 统一获取当前登录用户的邮箱
if st.user.is_logged_in:
    user_email = st.user.email
else:
    user_email = st.session_state.get("qq_user_email", "")

if not user_email:
    st.warning("请先登录。")
    st.stop()

st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")

def safe_execute(query, default=None):
    """统一包裹 Supabase 查询，出错不崩页面"""
    try:
        return query.execute().data
    except Exception as e:
        st.error(f"数据库请求失败：{e}")
        return default if default is not None else []

  

def get_supabase():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = get_supabase()

import streamlit as st
from supabase import create_client
from crypto_utils import hash_password, verify_password

# 从网址参数恢复 QQ 登录状态（防止刷新后丢失）
if "user" in st.query_params and "qq_user_email" not in st.session_state:
    st.session_state["qq_user_email"] = st.query_params["user"]

# 判断是 Google 登录还是 QQ 登录
if st.user.is_logged_in:
    user_email = st.user.email
else:
    user_email = st.session_state.get("qq_user_email", "")

# 如果两种都没登录，直接停
if not user_email:
    st.warning("请先登录。")
    st.stop()


# ---------- 个人资料 ----------
st.divider()
st.subheader("👤 个人资料设置")

profile = safe_execute(
    supabase.table("user_profiles")
    .select("*")
    .eq("email", user_email)
)

if profile:
    current_nickname = profile[0].get("nickname", "")
    current_emoji = profile[0].get("avatar_emoji", "🐱")
else:
    current_nickname = ""
    current_emoji = "🐱"

new_nickname = st.text_input("昵称：", value=current_nickname)

emoji_options = [
    "🐱", "🐶", "🦊", "🐼", "🐸", "🦁", "🐯", "🐨",
    "🌸", "🌈", "⭐", "🌙", "☀️", "🍀", "🎵", "🍕",
]
new_emoji = st.selectbox(
    "选择一个头像：",
    emoji_options,
    index=emoji_options.index(current_emoji) if current_emoji in emoji_options else 0,
)

if st.button("💾 保存资料"):
    safe_execute(
        supabase.table("user_profiles").upsert({
            "email": user_email,
            "nickname": new_nickname,
            "avatar_emoji": new_emoji,
        })
    )
    st.success("✅ 资料已保存")
    st.rerun()


st.divider()
st.subheader("🔑 修改密码")

old_pwd = st.text_input("旧密码：", type="password", key="old_pwd")
new_pwd = st.text_input("新密码：", type="password", key="new_pwd")

if st.button("确认修改", key="change_pwd_btn"):
    if old_pwd and new_pwd:
        # 检查旧密码
        check = safe_execute(
            supabase.table("app_users").select("*").eq("email", user_email).eq("password", old_pwd)
        )
        if check:
            supabase.table("app_users").update({"password": new_pwd}).eq("email", user_email).execute()
            st.success("✅ 密码已修改")
        else:
            st.error("❌ 旧密码错误")
    else:
        st.warning("请填写完整")

# ---------- 会员状态 ----------
st.divider()
st.subheader("💎 会员状态")

col1, col2 = st.columns(2)
with col1:
    st.metric("当前等级", "免费用户")
with col2:
    st.metric("AI 分析次数", "0 / 3")

st.info("升级到会员，解锁无限次 AI 分析和历史记录保存功能。")
if st.button("升级到会员（即将开放）"):
    st.warning("付费功能正在开发中，敬请期待。")