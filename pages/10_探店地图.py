import pydeck as pdk
import streamlit as st
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()
import sys
sys.path.append("..")
from common import supabase, user_email, is_user_logged_in
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()
# 统一获取当前登录用户的邮箱
if st.user.is_logged_in:
    user_email = st.user.email
else:
    user_email = st.session_state.get("qq_user_email", "")

if not user_email:
    st.warning("请先登录。")
    st.stop()

# ===== 地图 =====
# ===== 构造地图数据 =====
shops=supabase.table("shops").select("*").execute().data or []

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

if df:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[lon, lat]",
        get_color="[231, 76, 60, 200]",
        get_radius=300,
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
        map_style=f"mapbox://styles/mapbox/streets-v12?access_token={st.secrets['mapbox']['token']}"
    ))
else:
    st.info("还没有人添加坐标。")