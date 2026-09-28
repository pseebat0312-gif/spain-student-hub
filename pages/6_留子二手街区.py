import streamlit as st
from supabase import create_client
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()
from common import supabase, user_email, is_user_logged_in, render_sidebar, require_login

render_sidebar()
require_login()

# 统一获取当前登录用户的邮箱
if st.user.is_logged_in:
    user_email = st.user.email
else:
    user_email = st.session_state.get("qq_user_email", "")

if not user_email:
    st.warning("请先登录。")
    st.stop()
st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")

st.set_page_config(page_title="二手市场", page_icon="🛒")
st.title("🛒 留学生二手市场")
st.write("此平台仅作为沟通媒介，不涉及交易，请通过买家提供的联系方式进行后续交易。")

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

if not user_email:
    st.warning("请先在首页登录，才能发布或查看联系方式。")
    st.stop()

# ===== 发布新物品 =====
with st.expander("➕ 发布我要卖的东西", expanded=False):
    title = st.text_input("物品名称：")
    desc = st.text_area("物品描述：", height=100)
    price = st.text_input("价格（欧元）：")
    contact = st.text_input("联系方式（微信 / WhatsApp）：")
    image_url = st.text_input("图片链接（可选，建议用图床链接）：")
    
    if st.button("发布", type="primary"):
        if not title.strip() or not contact.strip():
            st.warning("名称和联系方式不能为空。")
        else:
            supabase.table("marketplace").insert({
                "user_email": st.user.email,
                "title": title,
                "description": desc,
                "price": price,
                "contact": contact,
                "image_url": image_url
            }).execute()
            st.success("✅ 发布成功！")
            st.rerun()

st.divider()

# ===== 排序 =====
sort_by = st.selectbox("排序方式：", ["最新发布", "价格从低到高", "最多浏览", "只看收藏"])

query = supabase.table("marketplace").select("*").eq("status", "available")

if sort_by == "最新发布":
    query = query.order("created_at", desc=True)
elif sort_by == "价格从低到高":
    query = query.order("price", desc=False)
elif sort_by == "最多浏览":
    query = query.order("views", desc=True)
elif sort_by == "只看收藏":
    query = query.eq("is_favorite", True)

items = query.execute()

# ===== 列表 =====
st.subheader("📦 物品列表")
if items.data:
    for item in items.data:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f"**{item['title']}** | 💶 {item['price']} | 👀 {item.get('views', 0)} 次浏览")
            st.caption(item.get("description", ""))
            if item.get("image_url"):
                st.image(item["image_url"], width=200)
            st.write(f"📞 联系方式：{item['contact']}")
        with col2:
            if st.button("⭐", key=f"fav_item_{item['id']}"):
                supabase.table("marketplace")\
                    .update({"is_favorite": not item.get("is_favorite", False)})\
                    .eq("id", item["id"])\
                    .execute()
                st.rerun()
            if st.button("👀 详情", key=f"view_item_{item['id']}"):
                supabase.table("marketplace")\
                    .update({"views": item.get("views", 0) + 1})\
                    .eq("id", item["id"])\
                    .execute()
                st.session_state[f"detail_{item['id']}"] = True
                st.rerun()
            if item["user_email"] == user_email:
                if st.button("🗑️", key=f"del_item_{item['id']}"):
                    supabase.table("marketplace")\
                        .delete()\
                        .eq("id", item["id"])\
                        .execute()
                    st.rerun()
        
        # 详情展开
        if st.session_state.get(f"detail_{item['id']}", False):
            with st.expander(f"📄 {item['title']} 的详细信息", expanded=True):
                st.write(item.get("description", "无描述"))
                if item.get("image_url"):
                    st.image(item["image_url"], width=400)
                st.write(f"📞 {item['contact']}")
        st.divider()
else:
    st.info("还没有人发布物品，你可以做第一个！")