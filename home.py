import streamlit as st

st.set_page_config(page_title="西班牙留学生工具站", page_icon="🇪🇸")
st.title("🇪🇸 西班牙留学生一站式工具站")
st.write("¡bienvenidos! 请从左侧选择你要用的工具。")

# ===== 侧边栏登录区 =====
with st.sidebar:
    if not st.user.is_logged_in:
        st.info("💡 登录后可保存检测历史")
        if st.button("使用 Google 登录"):
            st.login()
    else:
        st.success(f"👤 {st.user.name}")
        if st.button("退出登录"):
            st.logout()

# ===== 登录后才显示的功能 =====
if st.user.is_logged_in:
    st.divider()
    st.subheader("📂 我的专属空间")
    st.write(f"欢迎回来，{st.user.email}")
    st.write("（未来这里会显示检测历史、个性化设置等）")