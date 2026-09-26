import streamlit as st
from supabase import create_client

from styles import apply_sidebar_style
apply_sidebar_style()

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



# ---------- 个人资料 ----------
st.divider()
st.subheader("👤 个人资料设置")

profile = safe_execute(
    supabase.table("user_profiles")
    .select("*")
    .eq("email", st.user.email)
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
            "email": st.user.email,
            "nickname": new_nickname,
            "avatar_emoji": new_emoji,
        })
    )
    st.success("✅ 资料已保存")
    st.rerun()


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