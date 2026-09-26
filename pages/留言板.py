import streamlit as st
from supabase import create_client

st.set_page_config(page_title="留言板", page_icon="✍️")
st.title("✍️ 留言板")
st.write("欢迎给作者留言！你的留言默认是私密的，只有作者能看见。作者如果觉得内容不错，可能会把它公开~")

# 连接数据库
supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# 检查登录
if not st.user.is_logged_in:
    st.warning("请先在首页登录，才能留言。")
    st.stop()

st.divider()

# ===== 写留言 =====
st.subheader("📝 写一条新留言")
message = st.text_area("你想对作者说什么？", height=150)

if st.button("发送留言", type="primary"):
    if not message.strip():
        st.warning("留言不能为空。")
    else:
        supabase.table("messages").insert({
            "user_email": st.user.email,
            "content": message
        }).execute()
        st.success("✅ 留言已发送！作者会尽快看。")
        st.rerun()

st.divider()

# ===== 我的留言记录 =====
st.subheader("📜 我的留言记录")
my_msgs = supabase.table("messages")\
    .select("*")\
    .eq("user_email", st.user.email)\
    .order("created_at", desc=True)\
    .execute()

if my_msgs.data:
    for msg in my_msgs.data:
        status = "🌍 已公开" if msg.get("is_public") else "🔒 私密"
        st.write(f"**{msg['created_at'][:19]}** | {status}")
        st.write(msg["content"])
        if msg.get("reply"):
            st.info(f"💬 作者回复：{msg['reply']}")
        st.divider()
else:
    st.info("你还没有发过留言。")

# ===== 公开留言区 =====
st.divider()
st.subheader("🌟 精选公开留言")
public_msgs = supabase.table("messages")\
    .select("*")\
    .eq("is_public", True)\
    .order("created_at", desc=True)\
    .execute()

if public_msgs.data:
    for msg in public_msgs.data:
        st.write(f"**{msg['created_at'][:19]}**")
        st.write(msg["content"])
        if msg.get("reply"):
            st.info(f"💬 作者回复：{msg['reply']}")
        st.divider()
else:
    st.info("还没有公开的留言，期待你的第一条！")