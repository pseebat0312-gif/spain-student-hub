import streamlit as st
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()
from common import supabase, user_email, is_user_logged_in, render_sidebar, require_login

render_sidebar()
require_login()

import requests
from streamlit_folium import st_folium
import folium
from folium import Popup

st.title("🗺️ 留学生探店地图")

# ===== 发布新店 =====
with st.expander("➕ 推荐一家店", expanded=False):
    name = st.text_input("店名：", key="shop_name")
    address = st.text_input("地址（例如：Madrid, Calle Gran Vía 1）：", key="shop_address")
    city = st.selectbox("城市：", ["马德里", "巴塞罗那", "瓦伦西亚", "塞维利亚", "其他"], key="shop_city")
    category = st.selectbox("类别：", ["中餐", "奶茶", "咖啡", "西餐", "甜品", "其他"], key="shop_cat")
    desc = st.text_area("推荐理由：", height=100, key="shop_desc")
    is_recommend = st.radio("推荐还是避雷？", ["推荐", "避雷"], key="shop_rec") == "推荐"

    if st.button("发布", type="primary", key="shop_pub"):
        if not name.strip() or not address.strip():
            st.warning("店名和地址都不能为空。")
        else:
            url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
            headers = {"User-Agent": "spain-student-hub"}
            try:
                resp = requests.get(url, headers=headers, timeout=10).json()
                if resp:
                    lat = float(resp[0]["lat"])
                    lng = float(resp[0]["lon"])
                    supabase.table("shops").insert({
                        "user_email": user_email,
                        "name": name,
                        "address": address,
                        "city": city,
                        "category": category,
                        "description": desc,
                        "latitude": lat,
                        "longitude": lng,
                        "is_recommend": is_recommend
                    }).execute()
                    st.success("✅ 已保存！")
                    st.rerun()
                else:
                    st.error("找不到这个地址，请写得更详细。")
            except Exception as e:
                st.error(f"查询失败：{e}")

st.divider()

# ===== 地图 =====
all_shops = supabase.table("shops").select("*").execute().data or []
all_reviews = supabase.table("shop_reviews").select("*").execute().data or []

# 默认定位马德里，稍微放大
m = folium.Map(location=[40.4168, -3.7038], zoom_start=12, tiles="OpenStreetMap")

for s in all_shops:
    if not (s.get("latitude") and s.get("longitude")):
        continue

    # 统计推荐/避雷
    reviews = [r for r in all_reviews if r["shop_id"] == s["id"]]
    rec = sum(1 for r in reviews if r.get("rating") == "recommend")
    avoid = sum(1 for r in reviews if r.get("rating") == "avoid")

    # 颜色：推荐多绿色，避雷多红色
    color = "green" if rec >= avoid else "red"

    # 把评论拼成 HTML
    comment_html = ""
    for r in reviews:
        icon = "👍" if r.get("rating") == "recommend" else "👎"
        comment_html += f"<div style='font-size:12px;'>{icon} <b>{r['user_email']}</b>: {r['content']}</div>"

    popup_html = f"""
    <div style="font-family: sans-serif; width: 220px;">
        <h4 style="margin: 0 0 6px 0;">{s['name']}</h4>
        <div style="font-size: 12px; color: #666;">{s.get('city', '')} · {s.get('category', '')}</div>
        <div style="margin: 6px 0; font-size: 13px;">{s.get('description', '')}</div>
        <div style="font-size: 12px;">👍 {rec} · 👎 {avoid}</div>
        <hr style="margin: 6px 0;">
        {comment_html if comment_html else '<div style="font-size:12px;color:#999;">还没有评论</div>'}
    </div>
    """

    folium.Marker(
        location=[s["latitude"], s["longitude"]],
        tooltip=s["name"],
        popup=folium.Popup(popup_html, max_width=250),
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# 显示地图
st_folium(m, height=500, width=None, key="main_map")

st.divider()

# ===== 选中店铺的评论 + 发评论 =====
st.subheader("📝 写评论")

shop_names = [s["name"] for s in all_shops]
if shop_names:
    chosen = st.selectbox("选择店铺：", shop_names)
    shop = next((s for s in all_shops if s["name"] == chosen), None)
    if shop:
        rating = st.radio("推荐/避雷：", ["推荐", "避雷"], key="comment_rating")
        content = st.text_area("评论内容：", key="comment_content")
        if st.button("发布评论"):
            if content.strip():
                supabase.table("shop_reviews").insert({
                    "shop_id": shop["id"],
                    "user_email": user_email,
                    "rating": "recommend" if rating == "推荐" else "avoid",
                    "content": content
                }).execute()
                st.success("✅ 已发布")
                st.rerun()
else:
    st.info("还没有店铺，先去推荐一家吧。")