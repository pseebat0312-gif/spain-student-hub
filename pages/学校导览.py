import streamlit as st

st.set_page_config(page_title="学校导览", page_icon="🏛️")
st.title("🏛️ UCM 校园导览")
st.write("这里汇总了康普顿斯大学最常用的官方入口，方便快速访问。")

# --- 学术与教学 ---
st.subheader("📚 学术与教学")
col1, col2, col3, col4= st.columns(3)
with col1:
    st.link_button("UCM 官网", "https://www.ucm.es", use_container_width=True)
with col2:
    st.link_button("Campus Virtual", "https://www.ucm.es/campusvirtual", use_container_width=True)
with col3:
    st.link_button("学生邮箱", "https://www.ucm.es/correo", use_container_width=True)
with col4:
    st.link_button("学校提供的免费工具", "https://ssii.ucm.es/", use_container_width=True)

# --- 体育与生活 ---
st.subheader("🏃 体育与生活")
col4, col5, col6= st.columns(2)
with col4:
    st.link_button("官网体育主页", "https://www.ucm.es/deportesucm", use_container_width=True)
with col5:
    st.link_button("体育设施预约", "https://deportes.ucm.es/", use_container_width=True)
with col6:
    st.link_button("图书馆服务", "https://biblioteca.ucm.es/", use_container_width=True)

# --- 温馨提示 ---
st.divider()
st.info("💡 提示：在校外访问 Campus Virtual 时，需要先连接学校的 VPN。")