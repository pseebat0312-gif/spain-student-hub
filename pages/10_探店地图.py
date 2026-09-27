import streamlit as st
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

from common import supabase, user_email, is_user_logged_in
import requests

if not user_email:
    st.warning("请先登录。")
    st.stop()

st.title("🗺️ 留学生探店地图")
st.write("分享你发现的好店，看看大家都在哪里打卡。")

# ===== 发布新店 =====
st.subheader("➕ 推荐一家店")
st.write("输入地址后，系统会自动定位。")

name = st.text_input("店名：", key="shop_name")
address = st.text_input("地址（城市 + 街道，例如：Madrid, Calle Gran Vía 1）：", key="shop_address")
city = st.selectbox("城市：", ["马德里", "巴塞罗那", "瓦伦西亚", "塞维利亚", "其他"], key="shop_city")
category = st.selectbox("类别：", ["中餐", "奶茶", "咖啡", "西餐", "甜品", "其他"], key="shop_cat")
desc = st.text_area("推荐理由：", height=100, key="shop_desc")
is_recommend = st.radio("推荐还是避雷？", ["推荐", "避雷"], key="shop_rec") == "推荐"

if st.button("发布", type="primary", key="shop_pub"):
    if not name.strip() or not address.strip():
        st.warning("店名和地址都不能为空。")
    else:
        # 用 Nominatim 把地址转成经纬度
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
                st.success(f"✅ 已保存！位置：{lat:.4f}, {lng:.4f}")
                st.rerun()
            else:
                st.error("找不到这个地址，请写得更详细一些。")
        except Exception as e:
            st.error(f"查询地址失败：{e}")

st.divider()

# ===== 我发布的店铺 =====
st.subheader("📍 我发布的店铺")

my_shops = supabase.table("shops")\
    .select("*")\
    .eq("user_email", user_email)\
    .order("created_at", desc=True)\
    .execute().data or []

if my_shops:
    for s in my_shops:
        with st.expander(f"{s['name']} · {s.get('city', '')} · {s.get('category', '')}", expanded=False):
            st.write(f"**地址：** {s.get('address', '未填')}")
            st.write(f"**推荐理由：** {s.get('description', '')}")
            st.caption(f"坐标：{s['latitude']}, {s['longitude']}")

            st.link_button(
                "🚗 用 Google Maps 导航",
                f"https://www.google.com/maps/dir/?api=1&destination={s['latitude']},{s['longitude']}"
            )

            if st.button("🗑️ 删除", key=f"del_shop_{s['id']}"):
                supabase.table("shops").delete().eq("id", s["id"]).execute()
                st.rerun()
else:
    st.info("你还没有发布任何店铺。")

st.divider()

# ===== 所有人的店铺地图 =====
st.subheader("🗺️ 所有人的推荐")

all_shops = supabase.table("shops").select("*").execute().data or []

df = []
for s in all_shops:
    if s.get("latitude") and s.get("longitude"):
        df.append({
            "name": s["name"],
            "lat": s["latitude"],
            "lon": s["longitude"],
        })

if df:
    map_data = [{"lat": d["lat"], "lon": d["lon"]} for d in df]
    st.map(map_data, zoom=5)
else:
    st.info("还没有人添加店铺。")