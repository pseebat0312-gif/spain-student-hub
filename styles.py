import streamlit as st

def apply_sidebar_style():
    st.markdown("""
    <style>
        /* ===== 全站背景：纯黑 ===== */
        .stApp, [data-testid="stAppViewContainer"] {
            background: #000000 !important;
        }
        
        /* ===== 全站字体：衬线体（serif） ===== */
        * {
            font-family: 'Georgia', 'Times New Roman', serif !important;
        }
        
        /* ===== 正文文字：白色 ===== */
        .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
            color: #ffffff !important;
        }
        
        /* ===== 标题：金色衬线 ===== */
        h1, h2, h3 {
            color: #f5e6a3 !important;
            font-family: 'Georgia', 'Times New Roman', serif !important;
            font-weight: 700 !important;
        }
        
        /* ===== 侧边栏 ===== */
        [data-testid="stSidebar"] {
            background-color: #0a0a0a !important;
            border-right: 2px solid #4a7c59 !important;
        }
        
        
        /* ===== 折叠框 ===== */
        div[data-testid="stExpander"] {
            border-radius: 12px !important;
            border: 1px solid #4a7c59 !important;
            background-color: #111111 !important;
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