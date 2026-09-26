import streamlit as st
from supabase import create_client
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()


st.set_page_config(page_title="日常生活导览", page_icon="🎭")
st.title("🎭 日常生活导览")
st.write("看剧、看球、抢演唱会门票，或者周末不知道去哪？这里帮你整理好了。")

# ===== 常用购票平台 =====
st.subheader("🎫 常用购票平台")
col1, col2, col3 = st.columns(3)
with col1:
    st.link_button("Ticketmaster", "https://www.ticketmaster.es/", use_container_width=True)
with col2:
    st.link_button("Fever", "https://feverup.com/es/madrid", use_container_width=True)
with col3:
    st.link_button("Entradas.com", "https://www.entradas.com/", use_container_width=True)

col4, col5 = st.columns(2)
with col4:
    st.link_button("El Corte Inglés 演出", "https://www.elcorteingles.es/entradas/", use_container_width=True)
with col5:
    st.link_button("Atrápalo", "https://www.atrapalo.com/", use_container_width=True)

st.divider()

# ===== 近期活动推荐 =====
st.subheader("📅 近期值得关注的活动")

# --- 音乐与演唱会 ---
with st.expander("🎵 音乐与演唱会", expanded=False):
    st.markdown("""
    **Hispanidad 2026（10月2日-12日，马德里）**
    - 西班牙语文化节，超过 150 场活动，大部分免费。
    - **Sebastián Yatra** 免费演唱会：10月10日，Plaza de España。
    - **Marta Sánchez** 演唱会：10月11日，Plaza de España。
    - **Trueno** 演唱会：10月21日，Movistar Arena。
    - **Placebo** 30周年巡演：10月1日，Movistar Arena。
    """)

# --- 戏剧与音乐剧 ---
with st.expander("🎭 戏剧与音乐剧", expanded=False):
    st.markdown("""
    **《La Casa de Bernarda Alba》（10月2日-12月11日，Teatro Serrano）**
    - 西班牙经典戏剧，票价约 18.50 欧元起。
    
    **《Querido Evan Hansen》（10月23日-11月27日，Teatro Rialto）**
    - 百老汇获奖音乐剧，票价约 18.52 欧元起。
    
    **《El Imitador》（9月8日-10月30日，Gran Teatro Pavón）**
    - 70 种嗓音、一个故事，票价约 23.50 欧元起。
    """)

# --- 体育赛事 ---
with st.expander("⚽ 体育赛事", expanded=False):
    st.markdown("""
    **足球比赛（LaLiga）**
    - 购票方式：各俱乐部官网直接购票，或通过 Ticketmaster 等平台。
    - 示例：Málaga vs Espanyol（10月11日，Estadio La Rosaleda），票价约 30 欧元起。
    
    **其他体育赛事**
    - 可关注马德里自治区体育活动的官方页面，获取最新的赛事信息。
    """)

st.divider()

st.info("💡 提示：热门演唱会和球赛的门票通常很快售罄，建议提前关注官方开票时间。")