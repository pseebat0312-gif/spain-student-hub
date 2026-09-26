import streamlit as st
from supabase import create_client

from styles import apply_sidebar_style
apply_sidebar_style()

# ===== 页面配置 =====
st.set_page_config(page_title="西班牙留学生工具站", page_icon="🇪🇸")
st.title("🇪🇸 西班牙留学生一站式工具站")
st.write("¡Bienvenidos! 请从左侧选择你要用的工具。")

# ===== Supabase 客户端 =====
@st.cache_resource
def get_supabase():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = get_supabase()

ADMIN_EMAIL = "pseebat0312@gmail.com"


# ===== 工具函数 =====
def safe_execute(query, default=None):
    """统一包裹 Supabase 查询，出错不崩页面"""
    try:
        return query.execute().data
    except Exception as e:
        st.error(f"数据库请求失败：{e}")
        return default if default is not None else []


# ===== 侧边栏：登录区 =====
with st.sidebar:
    if not st.user.is_logged_in:
        st.info("💡 登录后可使用全部功能")
        if st.button("使用 Google 登录"):
            st.login()
    else:
        profile = safe_execute(
            supabase.table("user_profiles")
            .select("nickname", "avatar_emoji")
            .eq("email", st.user.email)
        )
        if profile:
            display_name = profile[0].get("nickname") or st.user.name
            display_emoji = profile[0].get("avatar_emoji") or "👤"
        else:
            display_name = st.user.name
            display_emoji = "👤"

        st.page_link("pages/9_个人中心.py", label=f"{display_emoji} {display_name}")
        if st.user.email == ADMIN_EMAIL:
            st.caption("🛡️ 管理员")
        if st.button("退出登录"):
            st.logout()


# ===== 未登录：到此为止 =====
if not st.user.is_logged_in:
    st.stop()


# ===== 已登录：专属空间 =====
st.divider()
st.subheader("📂 我的专属空间")
st.write(f"欢迎回来，{st.user.email}")

from streamlit_calendar import calendar
import datetime
import pytz

# ===== 可点击的日历 =====
st.divider()
st.subheader("📅 点击日期查看日程")

spain_tz = pytz.timezone("Europe/Madrid")
today = datetime.datetime.now(spain_tz).date()

# 拉取当前用户所有日程
if st.user.is_logged_in:
    schedules = supabase.table("schedules")\
        .select("*")\
        .eq("user_email", st.user.email)\
        .execute()
    
    # 把日程转成 calendar 组件需要的格式
    events = []
    for s in (schedules.data or []):
        events.append({
            "title": s["title"],
            "start": f"{s['event_date']}T{s.get('event_time', '09:00')}:00",
            "end": f"{s['event_date']}T{s.get('event_time', '10:00')}:00",
        })
else:
    events = []

# 显示日历
calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "zh-cn",
    "height": 500,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,listMonth"
    },
}

cal_result = calendar(
    events=events,
    options=calendar_options,
    key="my_calendar"
)

# 如果用户点了某天，就把那天存起来
if cal_result and cal_result.get("dateClick"):
    clicked_date = cal_result["dateClick"]["date"][:10]  # 取 YYYY-MM-DD
    st.session_state["clicked_date"] = clicked_date

# ===== 弹出当天日程 =====
if "clicked_date" in st.session_state and st.session_state["clicked_date"]:
    clicked_date = st.session_state["clicked_date"]
    st.divider()
    st.subheader(f"📌 {clicked_date} 的日程")
    
    if st.user.is_logged_in:
        day_schedules = supabase.table("schedules")\
            .select("*")\
            .eq("user_email", st.user.email)\
            .eq("event_date", clicked_date)\
            .order("event_time", desc=False)\
            .execute()
        
        if day_schedules.data:
            for s in day_schedules.data:
                col1, col2 = st.columns([6, 1])
                with col1:
                    time_str = s.get("event_time", "全天")
                    st.write(f"⏰ **{time_str}** — {s['title']}")
                with col2:
                    if st.button("🗑️", key=f"del_{s['id']}"):
                        supabase.table("schedules")\
                            .delete()\
                            .eq("id", s["id"])\
                            .execute()
                        st.rerun()
        else:
            st.info("这一天还没有日程。")
        
        # 快速在这一天添加日程
        with st.expander("➕ 在这一天添加日程", expanded=False):
            event_time = st.time_input("时间：", value=datetime.time(9, 0))
            event_title = st.text_input("事项：", key=f"add_title_{clicked_date}")
            
            if st.button("保存", key=f"add_btn_{clicked_date}"):
                if event_title.strip():
                    supabase.table("schedules").insert({
                        "user_email": st.user.email,
                        "event_date": clicked_date,
                        "event_time": str(event_time),
                        "title": event_title
                    }).execute()
                    st.success("✅ 已添加")
                    st.rerun()
    else:
        st.info("登录后可以查看和添加日程。")