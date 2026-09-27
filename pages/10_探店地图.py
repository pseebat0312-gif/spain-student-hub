import streamlit as st
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

from common import supabase, user_email, is_user_logged_in

if not user_email:
    st.warning("请先登录。")
    st.stop()

st.title("🗺️ 留学生探店地图")
st.write("分享你发现的好店，看看大家都在哪里打卡。")

# ===== 发布新店 =====
from streamlit_folium import st_folium
import folium

st.subheader("➕ 推荐一家店")

# 用 folium 建一张地图
m = folium.Map(location=[40.4168, -3.7038], zoom_start=6)

# 让用户点击地图
clicked = st_folium(m, height=400, width=700, key="pick_map")

# 如果用户点了地图，就会返回坐标
if clicked and clicked.get("last_clicked"):
    lat = clicked["last_clicked"]["lat"]
    lng = clicked["last_clicked"]["lng"]
    st.success(f"你选择了坐标：{lat:.4f}, {lng:.4f}")
    
    name = st.text_input("店名：")
    city = st.text_input("城市：")
    desc = st.text_area("推荐理由：")
    st.link_button(
            "🚗 用 Google Maps 导航",
            f"https://www.google.com/maps/dir/?api=1&destination={d['lat']},{d['lon']}"
        )
    
    if st.button("发布"):
        supabase.table("shops").insert({
            "user_email": user_email,
            "name": name,
            "city": city,
            "description": desc,
            "latitude": lat,
            "longitude": lng,
            "is_recommend": True
        }).execute()
        st.rerun()
st.divider()

# ===== 拉取所有店铺 =====
shops = supabase.table("shops").select("*").execute().data or []

df = []
for s in shops:
    if s.get("latitude") and s.get("longitude"):
        df.append({
            "name": s["name"],
            "city": s.get("city", ""),
            "category": s.get("category", ""),
            "description": s.get("description", ""),
            "lat": s["latitude"],
            "lon": s["longitude"],
        })

# ===== 地图 =====
st.subheader("🗺️ 地图")
if df:
    map_data = [{"lat": d["lat"], "lon": d["lon"]} for d in df]
    st.map(map_data, zoom=5)
else:
    st.info("还没有人添加坐标，去发布第一条吧。")

st.divider()

# ===== 店铺列表 =====
st.subheader("📍 店铺列表")
if df:
    for d in df:
        st.write(f"**{d['name']}** · {d['city']} · {d['category']}")
        st.caption(d.get("description", ""))
        st.caption(f"坐标：{d['lat']}, {d['lon']}")
        st.divider()
else:
    st.info("还没有人推荐店铺。")