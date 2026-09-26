import streamlit as st

st.set_page_config(page_title="学校快速导览", page_icon="🏛️")
st.title("🏛️ 大学校园快速导览")
st.write("请选择你的学校，查看对应的官方入口。")

school=st.selectbox(
    "选择你的学校：",
    ["UCM","UAM","UB","其他（即将添加）"]
)
st.divider()
if school =="UCM":
    st.subheader("📚 学术与教学")
    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.link_button("UCM 官网", "https://www.ucm.es", use_container_width=True)
    with col2:
        st.link_button("Campus Virtual", "https://www.ucm.es/campusvirtual", use_container_width=True)
    with col3:
        st.link_button("学生邮箱", "https://mail.google.com/", use_container_width=True)
    with col4:
        st.link_button("学校提供的免费工具", "https://ssii.ucm.es/", use_container_width=True)

    # --- 体育与生活 ---
    st.subheader("🏃 体育与生活")
    col4, col5, col6= st.columns(3)
    with col4:
        st.link_button("官网体育主页", "https://www.ucm.es/deportesucm", use_container_width=True)
    with col5:
        st.link_button("体育设施预约", "https://deportes.ucm.es/", use_container_width=True)
    with col6:
        st.link_button("图书馆服务", "https://biblioteca.ucm.es/", use_container_width=True)

    # --- 温馨提示 ---
    st.divider()
    st.info("💡 提示：在校外访问 Campus Virtual 时，需要先连接学校的 VPN。")

elif school == "马德里自治大学 (UAM)":
    st.info("UAM 的入口正在整理中，敬请期待！")

elif school == "巴塞罗那大学 (UB)":
    st.info("UB 的入口正在整理中，敬请期待！")

elif school == "庞培法布拉大学 (UPF)":
    st.info("UPF 的入口正在整理中，敬请期待！")

else:
    st.info("如果你希望添加你的学校，欢迎在留言板留言联系作者！")