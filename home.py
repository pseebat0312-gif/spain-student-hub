import streamlit as st
from supabase import create_client

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

if "fav_status" not in st.session_state:
    st.session_state.fav_status = {}

@st.cache_data(ttl=5)
def get_history(user_email):
    return supabase.table("detection_history")\
        .select("*")\
        .eq("user_email", user_email)\
        .order("created_at", desc=True)\
        .execute().data

if "local_fav" not in st.session_state:
    st.session_state.local_fav=[]

ADMIN_EMAIL = "pseebat0312@gmail.com"

st.set_page_config(page_title="西班牙留学生工具站", page_icon="🇪🇸")
st.title("🇪🇸 西班牙留学生一站式工具站")
st.write("¡bienvenidos! 请从左侧选择你要用的工具。")

# ===== 侧边栏登录区 =====
with st.sidebar:
    if not st.user.is_logged_in:
        st.info("💡 登录后可保存检测历史")
        if st.button("使用 Google 登录"):
            st.login()
    else:
        profile = supabase.table("user_profiles")\
                .select("nickname", "avatar_emoji")\
                .eq("email", st.user.email)\
                .execute()
            
        if profile.data and profile.data[0]:
                display_name = profile.data[0].get("nickname") or st.user.name
                display_emoji = profile.data[0].get("avatar_emoji") or "👤"
        else:
                display_name = st.user.name
                display_emoji = "👤"
            
        st.success(f"{display_emoji} {display_name}")
        if st.button("退出登录"):
            st.logout()

# ===== 登录后才显示的功能 =====
if st.user.is_logged_in:
    st.divider()
    st.subheader("📂 我的专属空间")
    st.write(f"欢迎回来，{st.user.email}")
    
    # 查看历史记录
    if st.button("📜 查看我的检测历史"):
        # 查询条件
        query = supabase.table("detection_history")\
            .select("*")\
            .eq("user_email", st.user.email)\
            .order("created_at", desc=True)

        # 只看收藏的开关
        if "only_fav" not in st.session_state:
            st.session_state.only_fav = False

        only_fav = st.checkbox("⭐ 只看收藏", value=st.session_state.only_fav, key="only_fav_checkbox")
        st.session_state.only_fav = only_fav

        if only_fav:
            query = query.eq("is_favorite", True)

        # 执行查询
        response = query.execute()

        if response.data:
            st.write(f"共 {len(response.data)} 条记录：")
            for record in response.data:
                record_id = record["id"]
                
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    fav = "⭐" if record.get("is_favorite") else ""
                    st.write(f"{fav} **时间：** {record['created_at'][:19]} | **AI概率：** {record['ai_probability']:.2%}")
                    with st.expander("📄 查看全文"):
                        st.write(record['text_snippet'])
                
                with col2:
                        is_fav = record.get("is_favorite", False)
                
                # 按钮：点一下就把这条记录的 id 加到本地列表里
                        if st.button("⭐" if not is_fav else "✅", key=f"fav_{record_id}"):
                            st.session_state.local_fav.append(record_id)
                            st.success("已收藏！")
                
                # 如果这条记录被点过，就显示已收藏
                        if record_id in st.session_state.local_fav:
                            st.write("❤️ 已收藏")
                        else:
                            st.write("🤍 未收藏")
            
                with col3:
                    if st.button("🗑️", key=f"del_{record_id}"):
                        supabase.table("detection_history")\
                            .delete()\
                            .eq("id", record_id)\
                            .execute()
                        st.success("已删除")
                        st.rerun()
                
                st.divider()
        else:
            st.info("你还没有检测记录。")
# ===== 个人资料设置 =====
st.divider()
st.subheader("👤 个人资料设置")

# 读取当前用户的资料
response = supabase.table("user_profiles")\
    .select("*")\
    .eq("email", st.user.email)\
    .execute()

if response.data:
    current_nickname = response.data[0].get("nickname", "")
    current_emoji = response.data[0].get("avatar_emoji", "🐱")
else:
    current_nickname = ""
    current_emoji = "🐱"

# 昵称输入
new_nickname = st.text_input("昵称：", value=current_nickname)

# Emoji 头像选择
emoji_options = ["🐱", "🐶", "🦊", "🐼", "🐸", "🦁", "🐯", "🐨", 
                 "🌸", "🌈", "⭐", "🌙", "☀️", "🍀", "🎵", "🍕"]
new_emoji = st.selectbox(
    "选择一个头像：",
    emoji_options,
    index=emoji_options.index(current_emoji) if current_emoji in emoji_options else 0
)

# 保存按钮
if st.button("💾 保存资料"):
    supabase.table("user_profiles").upsert({
        "email": st.user.email,
        "nickname": new_nickname,
        "avatar_emoji": new_emoji
    }).execute()
    st.success("✅ 资料已保存")
    st.rerun()

    # === 会员状态区 ===
    col1, col2 = st.columns(2)
    with col1:
        st.metric("当前等级", "免费用户")
    with col2:
        st.metric("AI分析次数", "0 / 3")
    
    st.info("升级到会员，解锁无限次 AI 分析和历史记录保存功能。")
    if st.button("升级到会员（即将开放）"):
        st.warning("付费功能正在开发中，敬请期待。")