import streamlit as st
from supabase import create_client

st.set_page_config(page_title="二手市场", page_icon="🛒")
st.title("🛒 留学生二手市场")
st.write("发布你的二手物品，或者看看别人在卖什么。")

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

if not st.user.is_logged_in:
    st.warning("请先在首页登录，才能发布或查看联系方式。")
    st.stop()

st.divider()

# ===== 发布新物品 =====
with st.expander("➕ 发布我要卖的东西", expanded=False):
    title = st.text_input("物品名称：")
    desc = st.text_area("物品描述：", height=100)
    price = st.text_input("价格（欧元）：")
    contact = st.text_input("联系方式（微信 / WhatsApp）：")
    
    if st.button("发布", type="primary"):
        if not title.strip() or not contact.strip():
            st.warning("名称和联系方式不能为空。")
        else:
            supabase.table("marketplace").insert({
                "user_email": st.user.email,
                "title": title,
                "description": desc,
                "price": price,
                "contact": contact
            }).execute()
            st.success("✅ 发布成功！")
            st.rerun()

st.divider()

# ===== 浏览所有物品 =====
st.subheader("📦 最新发布")
items = supabase.table("marketplace")\
    .select("*")\
    .order("created_at", desc=True)\
    .execute()

if items.data:
    for item in items.data:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"**{item['title']}** | 💶 {item['price']}")
            st.caption(item.get("description", ""))
            st.write(f"📞 联系方式：{item['contact']}")
        with col2:
            if item["user_email"] == st.user.email:
                if st.button("🗑️ 删除", key=f"del_item_{item['id']}"):
                    supabase.table("marketplace")\
                        .delete()\
                        .eq("id", item["id"])\
                        .execute()
                    st.rerun()
        st.divider()
else:
    st.info("还没有人发布物品，你可以做第一个！")