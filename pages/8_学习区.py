import streamlit as st
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")

st.set_page_config(page_title="西语学习资料", page_icon="📚")
st.title("📚 西班牙语学习资料汇总")
st.write("从零基础到 DELE 考试，这里整理了最实用的免费资源。")

# ===== A1-A2 入门 =====
with st.expander("🟢 A1-A2 入门（零基础 / 日常对话）", expanded=False):
    st.markdown("**📖 免费学习网站**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("SpanishDict", "https://www.spanishdict.com/", use_container_width=True)
    with col2:
        st.link_button("Duolingo", "https://www.duolingo.com/", use_container_width=True)
    
    st.markdown("**🎥 YouTube 频道**")
    col3, col4 = st.columns(2)
    with col3:
        st.link_button("Butterfly Spanish", "https://www.youtube.com/@ButterflySpanish", use_container_width=True)
    with col4:
        st.link_button("Spanish with Paul", "https://www.youtube.com/@SpanishWithPaul", use_container_width=True)
    
    st.markdown("**🎧 播客**")
    col5, col6 = st.columns(2)
    with col5:
        st.link_button("Coffee Break Spanish", "https://coffeebreaklanguages.com/coffeebreakspanish/", use_container_width=True)
    with col6:
        st.link_button("Notes in Spanish", "https://www.notesinspanish.com/", use_container_width=True)

# ===== B1-B2 进阶 =====
with st.expander("🟡 B1-B2 进阶（看懂新闻 / 写简单文章）", expanded=False):
    st.markdown("**📖 免费学习网站**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("RTVE 新闻","https://www.rtve.es/", use_container_width=True)
    with col2:
        st.link_button("El País 简易版", "https://elpais.com/", use_container_width=True)
    
    st.markdown("**🎥 YouTube 频道**")
    col3, col4 = st.columns(2)
    with col3:
        st.link_button("Spanish Pod 101", "https://www.youtube.com/@SpanishPod101", use_container_width=True)
    with col4:
        st.link_button("Easy Spanish", "https://www.youtube.com/@EasySpanish", use_container_width=True)
    
    st.markdown("**🎧 播客**")
    col5, col6 = st.columns(2)
    with col5:
        st.link_button("Hoy Hablamos", "https://hoyhablamos.com/", use_container_width=True)
    with col6:
        st.link_button("Español con Juan", "https://www.spanishwithjuan.com/", use_container_width=True)

# ===== C1-C2 高级 =====
with st.expander("🔴 C1-C2 高级（接近母语 / 学术写作）", expanded=False):
    st.markdown("**📖 学习资源**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("RAE 皇家语言学院", "https://www.rae.es/", use_container_width=True)
    with col2:
        st.link_button("Fundéu 语言建议", "https://www.fundeu.es/", use_container_width=True)
    
    st.markdown("**🎥 YouTube 频道**")
    col3, col4 = st.columns(2)
    with col3:
        st.link_button("Español con María", "https://www.youtube.com/@EspanolconMaria", use_container_width=True)
    with col4:
        st.link_button("Linguriosa", "https://www.youtube.com/@Linguriosa", use_container_width=True)

# ===== DELE / SIELE 考试专项 =====
with st.expander("🎯 DELE / SIELE 考试专项", expanded=False):
    st.markdown("**📖 官方资源**")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("DELE 官网", "https://examenes.cervantes.es/es/dele", use_container_width=True)
    with col2:
        st.link_button("SIELE 官网", "https://siele.org/", use_container_width=True)
    
    st.markdown("**📝 备考资料**")
    col3, col4 = st.columns(2)
    with col3:
        st.link_button("塞万提斯学院", "https://www.cervantes.es/", use_container_width=True)
    with col4:
        st.link_button("DELE 模拟题", "https://examenes.cervantes.es/es/dele/preparar-prueba", use_container_width=True)

st.divider()
st.caption("💡 提示：以上资源均免费，建议根据自己的水平选择对应的板块。")