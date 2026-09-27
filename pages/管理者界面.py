import streamlit as st
from supabase import create_client

st.set_page_config(page_title="管理后台", page_icon="🛠️")
st.title("🛠️ 管理后台")

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

ADMIN_EMAIL = "pseebat0312@gmail.com"

if not st.user.is_logged_in:
    st.warning("请先登录。")
    st.stop()

if st.user.email != ADMIN_EMAIL:
    st.error("抱歉，你没有权限访问此页面。")
    st.stop()

st.success(f"欢迎管理员：{st.user.email}")

# ===== 四个标签页 =====
tab1, tab2, tab3, tab4 = st.tabs(["👥 用户", "🔍 检测记录", "✍️ 留言", "💬 社区"])

# ===== 1. 用户与登录记录 =====
with tab1:
    st.subheader("👥 用户登录记录")
    
    logs = supabase.table("login_logs")\
        .select("*")\
        .order("login_time", desc=True)\
        .execute()
    
    if logs.data:
        # 按用户分组
        users = {}
        for log in logs.data:
            email = log["user_email"]
            if email not in users:
                users[email] = []
            users[email].append(log["login_time"][:19])
        
        st.write(f"共 {len(users)} 个用户，累计 {len(logs.data)} 次登录记录")
        
        for email, times in users.items():
            with st.expander(f"📧 {email}（{len(times)} 次登录）", expanded=False):
                st.write("**最近登录时间：**")
                for t in times[:10]:
                    st.write(f"- {t}")
                if len(times) > 10:
                    st.caption(f"还有 {len(times) - 10} 条更早的记录...")
    else:
        st.info("暂无登录记录。")
    
    st.divider()
    st.subheader("👤 用户资料")
    profiles = supabase.table("user_profiles").select("*").execute()
    if profiles.data:
        for p in profiles.data:
            with st.expander(f"{p.get('avatar_emoji', '👤')} {p.get('nickname', '未命名')}（{p['email']}）"):
                st.write(f"昵称：{p.get('nickname', '未设置')}")
                st.write(f"头像：{p.get('avatar_emoji', '未设置')}")
                st.write(f"更新时间：{p.get('updated_at', '未知')}")
    else:
        st.info("暂无用户资料。")


# ===== 2. 检测记录 =====
with tab2:
    st.subheader("🔍 所有用户的检测记录")
    
    records = supabase.table("detection_history")\
        .select("*")\
        .order("created_at", desc=True)\
        .execute()
    
    if records.data:
        st.write(f"共 {len(records.data)} 条检测记录")
        
        # 按用户分组
        by_user = {}
        for r in records.data:
            email = r["user_email"]
            if email not in by_user:
                by_user[email] = []
            by_user[email].append(r)
        
        for email, items in by_user.items():
            with st.expander(f"📧 {email}（{len(items)} 条记录）", expanded=False):
                for r in items:
                    st.write(f"**{r['created_at'][:19]}** | AI概率：{r['ai_probability']:.2%}")
                    st.caption(f"文本：{r.get('text_snippet', '')[:100]}...")
                    if st.button("🗑️ 删除", key=f"del_rec_{r['id']}"):
                        supabase.table("detection_history")\
                            .delete()\
                            .eq("id", r["id"])\
                            .execute()
                        st.rerun()
                    st.divider()
    else:
        st.info("暂无检测记录。")


# ===== 3. 留言 =====
with tab3:
    st.subheader("✍️ 所有留言")
    
    msgs = supabase.table("messages")\
        .select("*")\
        .order("created_at", desc=True)\
        .execute()
    
    if msgs.data:
        st.write(f"共 {len(msgs.data)} 条留言")
        
        for m in msgs.data:
            status = "🌍 已公开" if m.get("is_public") else "🔒 私密"
            with st.expander(f"{status} | {m['user_email']} | {m['created_at'][:19]}", expanded=False):
                st.write(f"**内容：** {m['content']}")
                
                # 回复
                reply_text = st.text_area("回复：", value=m.get("reply", ""), key=f"reply_{m['id']}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("💾 保存回复", key=f"save_reply_{m['id']}"):
                        supabase.table("messages")\
                            .update({"reply": reply_text})\
                            .eq("id", m["id"])\
                            .execute()
                        st.success("已保存")
                        st.rerun()
                with col2:
                    if st.button("🌍 公开" if not m.get("is_public") else "🔒 取消", key=f"pub_{m['id']}"):
                        supabase.table("messages")\
                            .update({"is_public": not m.get("is_public")})\
                            .eq("id", m["id"])\
                            .execute()
                        st.rerun()
                with col3:
                    if st.button("🗑️ 删除", key=f"del_msg_{m['id']}"):
                        supabase.table("messages")\
                            .delete()\
                            .eq("id", m["id"])\
                            .execute()
                        st.rerun()
    else:
        st.info("暂无留言。")


# ===== 4. 社区 =====
with tab4:
    st.subheader("💬 社区帖子")
    
    posts = supabase.table("posts")\
        .select("*")\
        .order("created_at", desc=True)\
        .execute()
    
    if posts.data:
        st.write(f"共 {len(posts.data)} 条帖子")
        
        for p in posts.data:
            with st.expander(f"[{p.get('category', '未分类')}] {p['title']} | {p['user_email']}", expanded=False):
                st.write(p["content"])
                st.caption(f"发布时间：{p['created_at'][:19]}")
                
                # 查看回复
                replies = supabase.table("replies")\
                    .select("*")\
                    .eq("post_id", p["id"])\
                    .order("created_at", desc=False)\
                    .execute()
                
                if replies.data:
                    st.write("**回复：**")
                    for r in replies.data:
                        col1, col2 = st.columns([6, 1])
                        with col1:
                            st.write(f"💬 **{r['user_email']}**：{r['content']}")
                        with col2:
                            if st.button("🗑️", key=f"del_reply_{r['id']}"):
                                supabase.table("replies")\
                                    .delete()\
                                    .eq("id", r["id"])\
                                    .execute()
                                st.rerun()
                else:
                    st.caption("暂无回复。")
                
                # 删除帖子
                if st.button("🗑️ 删除帖子", key=f"del_post_{p['id']}"):
                    supabase.table("posts")\
                        .delete()\
                        .eq("id", p["id"])\
                        .execute()
                    st.rerun()
    else:
        st.info("暂无帖子。")