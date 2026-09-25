import streamlit as st
from supabase import create_client

st.set_page_config(page_title="管理员后台", page_icon="📊")
st.title("📊 管理员后台")

# 连接数据库
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# 检查是否登录
if not st.user.is_logged_in:
    st.warning("请先登录。")
    st.stop()

# 检查是否是管理员
ADMIN_EMAIL = "pseebat0312@gmail.com"  # 换成你自己的邮箱
if st.user.email != ADMIN_EMAIL:
    st.error("抱歉，你没有权限访问此页面。")
    st.stop()

# ===== 管理员专属功能 =====
st.success(f"欢迎管理员：{st.user.email}")

# 查看所有用户的检测记录
if st.button("📋 查看全部用户记录"):
    response = supabase.table("detection_history")\
        .select("*")\
        .order("created_at", desc=True)\
        .execute()
    
    if response.data:
        st.write(f"共 {len(response.data)} 条记录：")
        
        # 按用户分组
        users = {}
        for record in response.data:
            email = record["user_email"]
            if email not in users:
                users[email] = []
            users[email].append(record)
        
        # 展示每个用户的数据
        for email, records in users.items():
            with st.expander(f"👤 {email}（{len(records)} 条记录）"):
                for r in records:
                    st.write(f"**时间：** {r['created_at'][:19]} | **AI概率：** {r['ai_probability']:.2%}")
                    st.caption(f"文本：{r['text_snippet']}...")
                    st.divider()
    else:
        st.info("暂无记录。")