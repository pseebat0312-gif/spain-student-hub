import streamlit as st
from supabase import create_client

# ===== 页面配置 =====
st.set_page_config(page_title="西班牙留学生工具站", page_icon="🇪🇸")
st.title("🇪🇸 西班牙留学生一站式工具站")
st.write("¡Bienvenidos! 请从左侧选择你要用的工具。")

# ===== Supabase 客户端 =====
@st.cache_resource
def get_supabase():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = get_supabase()

ADMIN_EMAIL = "pseebat0312@gmail.com"


# ===== 工具函数 =====
def safe_execute(query, default=None):
    """统一包裹 Supabase 查询，出错不崩页面"""
    try:
        return query.execute().data
    except Exception as e:
        st.error(f"数据库请求失败：{e}")
        return default if default is not None else []


# ===== 侧边栏：登录区 =====
with st.sidebar:
    if not st.user.is_logged_in:
        st.info("💡 登录后可保存检测历史")
        if st.button("使用 Google 登录"):
            st.login()
    else:
        profile = safe_execute(
            supabase.table("user_profiles")
            .select("nickname", "avatar_emoji")
            .eq("email", st.user.email)
        )
        if profile:
            display_name = profile[0].get("nickname") or st.user.name
            display_emoji = profile[0].get("avatar_emoji") or "👤"
        else:
            display_name = st.user.name
            display_emoji = "👤"

        st.success(f"{display_emoji} {display_name}")
        if st.user.email == ADMIN_EMAIL:
            st.caption("🛡️ 管理员")
        if st.button("退出登录"):
            st.logout()


# ===== 未登录：到此为止 =====
if not st.user.is_logged_in:
    st.stop()


# ===== 已登录：专属空间 =====
st.divider()
st.subheader("📂 我的专属空间")
st.write(f"欢迎回来，{st.user.email}")


# ---------- 检测历史 ----------
if st.button("📜 查看我的检测历史"):
    only_fav = st.checkbox("⭐ 只看收藏", key="only_fav_checkbox")

    query = (
        supabase.table("detection_history")
        .select("*")
        .eq("user_email", st.user.email)
        .order("created_at", desc=True)
    )
    if only_fav:
        query = query.eq("is_favorite", True)

    records = safe_execute(query)

    if not records:
        st.info("你还没有检测记录。")
    else:
        st.write(f"共 {len(records)} 条记录：")
        for record in records:
            record_id = record["id"]
            is_fav = record.get("is_favorite", False)

            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:
                fav_mark = "⭐" if is_fav else ""
                st.write(
                    f"{fav_mark} **时间：** {record['created_at'][:19]} | "
                    f"**AI概率：** {record['ai_probability']:.2%}"
                )
                with st.expander("📄 查看全文"):
                    st.write(record.get("text_snippet", "（无内容）"))

            with col2:
                if st.button("⭐" if not is_fav else "✅", key=f"fav_{record_id}"):
                    safe_execute(
                        supabase.table("detection_history")
                        .update({"is_favorite": not is_fav})
                        .eq("id", record_id)
                    )
                    st.rerun()

            with col3:
                if st.button("🗑️", key=f"del_{record_id}"):
                    safe_execute(
                        supabase.table("detection_history")
                        .delete()
                        .eq("id", record_id)
                    )
                    st.success("已删除")
                    st.rerun()

            st.divider()


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