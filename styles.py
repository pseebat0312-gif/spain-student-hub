import streamlit as st

def apply_sidebar_style():
    st.markdown("""
    <style>
        /* ============================================
           1. 全局背景：深色
           ============================================ */
        .stApp, [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #000000 0%, #0a1f12 100%) !important;
            background-attachment: fixed !important;
        }
        .stApp, .stApp p, .stApp div, .stApp span, .stApp label {
            color: #ffffff !important;
        }

        /* ============================================
           2. 标题：带光晕动画
           ============================================ */
        h1 {
            color: #a0d8b3 !important;
            animation: glow 3s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 5px #4a7c59; }
            to { text-shadow: 0 0 20px #a0d8b3, 0 0 30px #4a7c59; }
        }
        h2, h3 {
            color: #a0d8b3 !important;
        }

        /* ============================================
           3. 页面加载动画：淡入 + 上滑
           ============================================ */
        .main .block-container {
            animation: fadeInUp 0.8s ease-out;
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ============================================
           4. 侧边栏：悬停滑动
           ============================================ */
        [data-testid="stSidebar"] {
            background-color: #1a1a2e !important;
            border-right: 3px solid #4a7c59 !important;
        }
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
            transform: translateX(8px) !important;
        }

        /* ============================================
           5. 按钮：悬停放大 + 上浮 + 阴影
           ============================================ */
        div[data-testid="stButton"] > button {
            border-radius: 12px !important;
            background-color: #4a7c59 !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
            box-shadow: 0 4px 12px rgba(74, 124, 89, 0.2) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stButton"] > button:hover {
            transform: translateY(-4px) scale(1.03) !important;
            box-shadow: 0 12px 24px rgba(74, 124, 89, 0.5) !important;
            background-color: #5a8f6b !important;
        }
        div[data-testid="stButton"] > button:active {
            transform: translateY(-1px) scale(1.01) !important;
        }

        /* ============================================
           6. 折叠框：悬停时轻微上浮
           ============================================ */
        div[data-testid="stExpander"] {
            border-radius: 12px !important;
            border: 1px solid #4a7c59 !important;
            background-color: #111111 !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stExpander"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(74, 124, 89, 0.3) !important;
        }

        /* ============================================
           7. 输入框：聚焦时发光
           ============================================ */
        div[data-testid="stTextInput"] input {
            border-radius: 10px !important;
            border: 2px solid #4a7c59 !important;
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #a0d8b3 !important;
            box-shadow: 0 0 12px rgba(160, 216, 179, 0.5) !important;
        }

        /* ============================================
           8. 图片：悬停时放大
           ============================================ */
        img {
            border-radius: 12px !important;
            transition: transform 0.3s ease !important;
        }
        img:hover {
            transform: scale(1.02) !important;
        }

        /* ============================================
           9. 提示框：淡入
           ============================================ */
        div[data-testid="stAlert"] {
            border-radius: 10px !important;
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* ============================================
           10. 加载进度条：流光效果
           ============================================ */
        div[data-testid="stProgress"] > div > div > div {
            background: linear-gradient(90deg, #4a7c59, #a0d8b3, #4a7c59) !important;
            background-size: 200% 100% !important;
            animation: shimmer 2s infinite !important;
        }
        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    """, unsafe_allow_html=True)