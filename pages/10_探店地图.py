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
st.write("点击地图相应位置，分享探店体验~")

# 用 folium 建地图，让用户点击选点
from streamlit_folium import st_folium
import folium

m = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
clicked = st_folium(m, height=400, width=700, key="pick_map")

if clicked and clicked.get("last_clicked"):
    lat = clicked["last_clicked"]["lat"]
    lng = clicked["last_clicked"]["lng"]
    st.success(f"你选择了坐标：{lat:.4f}, {lng:.4f}")

    name = st.text_input("店名：", key="shop_name")
    city = st.selectbox("城市：", ["马德里", "巴塞罗那", "瓦伦西亚", "塞维利亚", "其他"], key="shop_city")
    category = st.selectbox("类别：", ["中餐", "奶茶", "咖啡", "西餐", "甜品", "其他"], key="shop_cat")
    desc = st.text_area("推荐理由：", height=100, key="shop_desc")
    is_recommend = st.radio("推荐还是避雷？", ["推荐", "避雷"], key="shop_rec") == "推荐"

    if st.button("发布", type="primary", key="shop_pub"):
        if not name.strip():
            st.warning("店名不能为空。")
        else:
            supabase.table("shops").insert({
                "user_email": user_email,
                "name": name,
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
    st.info("👆 请先在地图上点一下店铺的位置")
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
# ===== 店铺列表 =====
st.subheader("📍 店铺列表")
if df:
    for d in df:
        with st.expander(f"{d['name']} · {d['city']} · {d['category']}", expanded=False):
            st.write(d.get("description", ""))
            st.caption(f"坐标：{d['lat']}, {d['lon']}")
            
            # 导航按钮
            st.link_button(
                "🚗 用 Google Maps 导航",
                f"https://www.google.com/maps/dir/?api=1&destination={d['lat']},{d['lon']}"
            )
else:
    st.info("还没有人推荐店铺。")
    st.divider()
