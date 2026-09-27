import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

import streamlit as st
from supabase import create_client


st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")


st.set_page_config(page_title="留学生社区", page_icon="💬")
st.title("💬 留学生互助社区")
st.write("分享你的经验、踩过的坑，或者向其他人求助。")

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

if not st.user.is_logged_in:
    st.warning("请先在首页登录，才能发帖和回复。")
    st.stop()

# ===== 发新帖 =====
with st.expander("➕ 发布新帖子", expanded=False):
    title = st.text_input("标题：")
    content = st.text_area("内容：", height=150)
    category = st.selectbox("分类：", ["经验分享", "踩坑求助", "学习交流", "生活日常", "其他"])
    
    if st.button("发布", type="primary"):
        if not title.strip() or not content.strip():
            st.warning("标题和内容不能为空。")
        else:
            supabase.table("posts").insert({
                "user_email": st.user.email,
                "title": title,
                "content": content,
                "category": category
            }).execute()
            st.success("✅ 发布成功！")
            st.rerun()

st.divider()

# ===== 帖子列表 =====
sort_by = st.selectbox("排序方式：", ["最新发布", "最多回复"])

if sort_by == "最新发布":
    posts_data = supabase.table("posts").select("*").order("created_at", desc=True).execute().data
else:
    all_posts = supabase.table("posts").select("*").execute().data
    posts_data = sorted(
        all_posts,
        key=lambda p: len(supabase.table("replies").select("*").eq("post_id", p["id"]).execute().data),
        reverse=True
    )

if posts_data:
    for post in posts_data:
        with st.expander(f"📌 [{post['category']}] {post['title']}({post['created_at'][:10]})", expanded=False):
            st.write(post["content"])
            st.caption(f"发布者：{post['user_email']}")
            
            st.divider()
            
            # 显示回复
            replies = supabase.table("replies")\
                .select("*")\
                .eq("post_id", post["id"])\
                .order("created_at", desc=False)\
                .execute()
            
            if replies.data:
                for reply in replies.data:
                    st.write(f"💬 **{reply['user_email']}**：{reply['content']}")
            else:
                st.caption("还没有回复，来抢沙发吧！")
            
            # 发回复
            reply_text = st.text_input("回复内容：", key=f"reply_text_{post['id']}")
            if st.button("发送回复", key=f"send_reply_{post['id']}_{len(replies.data)}"):
                if reply_text.strip():
                    supabase.table("replies").insert({
                        "post_id": post["id"],
                        "user_email": st.user.email,
                        "content": reply_text
                    }).execute()
                    st.rerun()
else:
    st.info("还没有帖子，你可以发第一个！")