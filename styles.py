import streamlit as st

def apply_sidebar_style():
    st.markdown("""
    <style>
        /* ===== 全站背景：纯黑 ===== */
        .stApp, [data-testid="stAppViewContainer"] {
            background: #000000 !important;
        }

        /* ===== 正文文字：白色 ===== */
        .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
            color: #ffffff !important;
        }

        /* ===== 标题：浅绿 ===== */
        h1, h2, h3 {
            color: #a0d8b3 !important;
        }

        /* ===== 侧边栏：深绿背景 ===== */
        [data-testid="stSidebar"] {
            background-color: #1a1a2e !important;
            border-right: 3px solid #4a7c59 !important;
        }
        
        /* ===== 侧边栏链接：白色、悬停滑动 ===== */
        [data-testid="stSidebar"] a {
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
            border: 1px solid #4a7c59 !important;
            border-radius: 10px !important;
            padding: 8px 12px !important;
            margin-bottom: 5px !important;
            display: block !important;
            text-decoration: none !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stSidebar"] a:hover {
            background-color: #4a7c59 !important;
            color: #ffffff !important;
            transform: translateX(5px) !important;
        }

        /* ===== 所有按钮：圆润、悬停放大 ===== */
        div[data-testid="stButton"] > button {
            border-radius: 12px !important;
            box-shadow: 0 4px 12px rgba(74, 124, 89, 0.2) !important;
            transition: all 0.3s ease !important;
            background-color: #4a7c59 !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 8px 20px rgba(74, 124, 89, 0.4) !important;
            background-color: #5a8f6b !important;
        }

        /* ===== 折叠框 ===== */
        div[data-testid="stExpander"] {
            border-radius: 12px !important;
            border: 1px solid #4a7c59 !important;
            background-color: #111111 !important;
        }

        /* ===== 输入框 ===== */
        div[data-testid="stTextInput"] input {
            border-radius: 10px !important;
            border: 2px solid #4a7c59 !important;
            background-color: #1a1a1a !important;
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)