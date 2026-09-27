import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

import streamlit as st
import pydeck as pdk
from supabase import create_client

st.set_page_config(page_title="探店地图", page_icon="🗺️", layout="wide")
st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")

st.title("🗺️ 留学生探店地图")
st.write("分享你发现的好店，看看大家都在哪里打卡。")

supabase = create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# ===== 发布新店 =====
with st.expander("➕ 推荐一家店", expanded=False):
    name = st.text_input("店名：")
    city = st.selectbox("城市：", ["马德里", "巴塞罗那", "瓦伦西亚", "塞维利亚", "其他"])
    category = st.selectbox("类别：", ["中餐", "奶茶", "咖啡", "西餐", "甜品", "其他"])
    address = st.text_input("地址：")
    desc = st.text_area("推荐理由：", height=100)
    lat = st.number_input("纬度（latitude）：", value=40.4168, format="%.4f")
    lon = st.number_input("经度（longitude）：", value=-3.7038, format="%.4f")

    if st.button("发布推荐", type="primary"):
        if not name.strip():
            st.warning("店名不能为空。")
        else:
            supabase.table("shops").insert({
                "user_email": st.user.email if st.user.is_logged_in else st.session_state.get("qq_user_email", ""),
                "name": name,
                "city": city,
                "category": category,
                "address": address,
                "description": desc,
                "latitude": lat,
                "longitude": lon
            }).execute()
            st.success("✅ 推荐成功！")
            st.rerun()

# ===== 拉取所有店铺 =====
shops = supabase.table("shops").select("*").execute().data or []

# ===== 地图展示 =====
if shops:
    df = []
    for s in shops:
        if s.get("latitude") and s.get("longitude"):
            df.append({
                "name": s["name"],
                "city": s.get("city", ""),
                "category": s.get("category", ""),
                "description": s.get("description", ""),
                "lat": s["latitude"],
                "lon": s["longitude"]
            })

    if df:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position="[lon, lat]",
            get_color="[74, 124, 89, 200]",
            get_radius=500,
            pickable=True,
            auto_highlight=True,
        )

        view_state = pdk.ViewState(
            latitude=40.4168,
            longitude=-3.7038,
            zoom=5,
            pitch=0,
        )

        tooltip = {
            "html": "<b>{name}</b><br/>{city} · {category}<br/>{description}",
            "style": {"backgroundColor": "#1a4d2e", "color": "white"}
        }

        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/dark-v10"
        ))
    else:
        st.info("还没有人添加坐标，去发布第一条吧。")
else:
    st.info("还没有人推荐店铺。")