import streamlit as st

def apply_sidebar_style():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1a1a2e !important;
            border-right: 3px solid #4a7c59 !important;
        }
        
        [data-testid="stSidebar"] a {
            color: #ffffff !important;
            font-weight: bold !important;
            font-size: 18px !important;
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
        
    /* 侧边栏“个人中心”链接：整框抹茶绿 */
    [data-testid="stSidebar"] [data-testid="stPageLink"] {
        background-color: #4a7c59 !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        border: none !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        color: #ffffff !important;
        font-weight: bold !important;
        text-decoration: none !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
        background-color: #6b9e7a !important;
    }
    </style>
    """, unsafe_allow_html=True)