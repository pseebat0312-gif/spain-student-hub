import streamlit as st

def apply_sidebar_style():
    st.markdown("""
    <style>
        /* ===== 全站背景：淡绿渐变 ===== */
        .stApp {
            background: linear-gradient(135deg, #f0f9f4 0%, #ffffff 50%, #e8f5ec 100%);
        }

        /* ===== 侧边栏 ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a4d2e, #2f5d3a) !important;
            border-right: 3px solid #4a7c59 !important;
        }
        [data-testid="stSidebar"] a {
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            padding: 8px 12px !important;
            margin-bottom: 5px !important;
            display: block !important;
            text-decoration: none !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stSidebar"] a:hover {
            background-color: #4a7c59 !important;
            transform: translateX(8px) !important;
        }

        /* ===== 所有按钮：圆润、有阴影、悬停放大 ===== */
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

        /* ===== 折叠框：圆角、淡绿边框 ===== */
        div[data-testid="stExpander"] {
            border-radius: 12px !important;
            border: 1px solid #c8e6d0 !important;
            background-color: #ffffff !important;
            box-shadow: 0 2px 8px rgba(74, 124, 89, 0.08) !important;
        }

        /* ===== 标题 ===== */
        h1 {
            color: #1a4d2e !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }
        h2, h3 {
            color: #2f5d3a !important;
            font-weight: 700 !important;
        }

        /* ===== 输入框 ===== */
        div[data-testid="stTextInput"] input {
            border-radius: 10px !important;
            border: 2px solid #c8e6d0 !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #4a7c59 !important;
            box-shadow: 0 0 0 3px rgba(74, 124, 89, 0.15) !important;
        }

        /* ===== 图片：圆角 ===== */
        img {
            border-radius: 12px !important;
        }

        /* ===== 提示框 ===== */
        div[data-testid="stAlert"] {
            border-radius: 10px !important;
        }
    </style>
    """, unsafe_allow_html=True)