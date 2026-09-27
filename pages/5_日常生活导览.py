import streamlit as st
from supabase import create_client
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")

st.set_page_config(page_title="日常导览", page_icon="🎭")
st.title("🎭 日常导览")

st.write("这里汇总了西班牙本地生活相关的官方入口，方便你查最新信息。")

tab1, tab2, tab3 = st.tabs(["🎵 音乐与演出", "⚽ 体育与运动", "✈️ 旅游与探索"])

# ===== 音乐与演出 =====
with tab1:
    st.subheader("🎵 音乐与演出")
    
    st.write("**演出与购票平台**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("Ticketmaster", "https://www.ticketmaster.es/", use_container_width=True)
    with col2:
        st.link_button("Entradas.com", "https://www.entradas.com/", use_container_width=True)
    with col3:
        st.link_button("Fever", "https://feverup.com/es/madrid", use_container_width=True)
    
    st.divider()
    
    st.write("**官方文化活动日历**")
    col4, col5 = st.columns(2)
    with col4:
        st.link_button("马德里官方活动日历", "https://www.esmadrid.com/agenda", use_container_width=True)
    with col5:
        st.link_button("马德里市政府文化日历", "https://www.madrid.es/portales/munimadrid/es/Inicio/Cultura-ocio-y-deporte/", use_container_width=True)

# ===== 体育与运动 =====
with tab2:
    st.subheader("⚽ 体育与运动")
    
    st.write("**足球赛事门票**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button("皇家马德里", "https://www.realmadrid.com/entradas", use_container_width=True)
    with col2:
        st.link_button("马德里竞技", "https://www.atleticodemadrid.com/entradas", use_container_width=True)
    with col3:
        st.link_button("西甲官方票务", "https://www.laliga.com/", use_container_width=True)
    
    st.divider()
    
    st.write("**体育设施与活动**")
    col4, col5 = st.columns(2)
    with col4:
        st.link_button("马德里体育设施预约", "https://www.madrid.es/portales/munimadrid/es/Inicio/El-Ayuntamiento/Deporte/", use_container_width=True)
    with col5:
        st.link_button("马德里官方体育日历", "https://www.esmadrid.com/deportes", use_container_width=True)

# ===== 旅游与探索 =====
with tab3:
    st.subheader("✈️ 旅游与探索")
    
    st.write("**官方旅游信息与导览**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("马德里官方旅游网站", "https://www.esmadrid.com/", use_container_width=True)
    with col2:
        st.link_button("免费导览路线", "https://www.esmadrid.com/visitas-guiadas", use_container_width=True)
    
    st.divider()
    
    st.write("**短途旅行与周边游**")
    col3, col4 = st.columns(2)
    with col3:
        st.link_button("西班牙国家旅游局", "https://www.spain.info/es/", use_container_width=True)
    with col4:
        st.link_button("马德里周边游指南", "https://www.esmadrid.com/rutas", use_container_width=True)

st.divider()
st.caption("💡 提示：以上链接均为官方平台，活动信息和票务信息会实时更新。")