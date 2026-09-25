import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="简易翻译器", page_icon="🌐")
st.title("🌐 简易翻译器")
st.write("支持中文、英文、西班牙语互译。")

# 语言选择
languages = {
    "中文": "zh-CN",
    "English": "en",
    "Español": "es"
}

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("源语言：", list(languages.keys()))
with col2:
    target_lang = st.selectbox("目标语言：", list(languages.keys()), index=1)

# 输入文本
text_input = st.text_area("输入要翻译的文本：", height=150)

# 翻译按钮
if st.button("🔄 翻译", type="primary"):
    if not text_input.strip():
        st.warning("请输入要翻译的文本。")
    elif source_lang == target_lang:
        st.info("源语言和目标语言相同，不需要翻译。")
    else:
        try:
            translated = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text_input)
            st.divider()
            st.subheader("翻译结果：")
            st.success(translated)
        except Exception as e:
            st.error(f"翻译失败：{e}")