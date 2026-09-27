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
with st.expander("➕ 推荐一家店", expanded=False):
    name = st.text_input("店名：", key="shop_name")
    city = st.selectbox("城市：", ["马德里", "巴塞罗那", "瓦伦西亚", "塞维利亚", "其他"], key="shop_city")
    category = st.selectbox("类别：", ["中餐", "奶茶", "咖啡", "西餐", "甜品", "其他"], key="shop_cat")
    desc = st.text_area("推荐理由：", height=100, key="shop_desc")
    lat = st.number_input("纬度（latitude）：", value=40.4168, format="%.4f", key="shop_lat")
    lon = st.number_input("经度（longitude）：", value=-3.7038, format="%.4f", key="shop_lon")

    if st.button("发布推荐", type="primary", key="shop_pub"):
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
                "longitude": lon
            }).execute()
            st.success("✅ 推荐成功！")
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