import streamlit as st
import datetime
import calendar
import pytz
from supabase import create_client
from streamlit_calendar import calendar as st_calendar
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



# ===== 已登录：专属空间 =====
st.divider()
st.subheader("📂 我的专属空间")
if st.user.is_logged_in:
    st.write(f"欢迎回来，{st.user.email}")
else:
    st.info("🔒 登录后可以管理你的专属空间")

# ===== 1. 实时时钟 =====
st.divider()
st.subheader("🕐 现在时间")

clock_html = """
<div style="display:flex; gap:20px; flex-wrap:wrap;">
  <div style="flex:1; background:#1a1a2e; padding:15px; border-radius:12px; border:2px solid #4a7c59; text-align:center; color:white;">
    <div style="font-size:16px; color:#a0d8b3;">🇪🇸 西班牙时间</div>
    <div id="spain-clock" style="font-size:22px; font-weight:bold; margin-top:8px;">--:--:--</div>
  </div>
  <div style="flex:1; background:#1a1a2e; padding:15px; border-radius:12px; border:2px solid #4a7c59; text-align:center; color:white;">
    <div style="font-size:16px; color:#a0d8b3;">🇨🇳 中国时间</div>
    <div id="china-clock" style="font-size:22px; font-weight:bold; margin-top:8px;">--:--:--</div>
  </div>
</div>
<script>
function updateClocks() {
  const now = new Date();
  const spain = new Date(now.toLocaleString("en-US", {timeZone: "Europe/Madrid"}));
  const china = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Shanghai"}));
  const pad = (n) => String(n).padStart(2, '0');
  const fmt = (d) => `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
  document.getElementById('spain-clock').innerText = fmt(spain);
  document.getElementById('china-clock').innerText = fmt(china);
}
setInterval(updateClocks, 1000);
updateClocks();
</script>
"""
st.components.v1.html(clock_html, height=130)

# ===== 2. 今年进度条 =====
spain_tz = pytz.timezone("Europe/Madrid")
now = datetime.datetime.now(spain_tz)
today = now.date()
year = today.year

days_in_year = 366 if calendar.isleap(year) else 365
day_of_year = today.timetuple().tm_yday
days_left = days_in_year - day_of_year
progress = day_of_year / days_in_year

st.divider()
st.subheader("📊 今年进度")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("今天是", f"{today.month}月{today.day}日")
with col2:
    st.metric("今年已过", f"{day_of_year} 天")
with col3:
    st.metric("今年还剩", f"{days_left} 天")
st.progress(progress)

# ===== 3. 可点击的日历 =====
st.divider()
st.subheader("📅 点击日期查看日程")

schedules = safe_execute(
    supabase.table("schedules")
    .select("*")
    .eq("user_email", st.user.email)
)

events = []
for s in (schedules or []):
    events.append({
        "title": s["title"],
        "start": f"{s['event_date']}T{s.get('event_time', '09:00')}:00",
        "end": f"{s['event_date']}T{s.get('event_time', '10:00')}:00",
    })

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

cal_result = st_calendar(events=events, options=calendar_options, key="my_calendar")

# 如果用户点了某天，就存起来
if cal_result and cal_result.get("dateClick"):
    raw_date = cal_result["dateClick"]["date"][:10]
    # 直接加一整天
    parsed = datetime.datetime.strptime(raw_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    clicked_date = parsed.strftime("%Y-%m-%d")
    st.session_state["clicked_date"] = clicked_date


# ===== 未登录：到此为止 =====
if not st.user.is_logged_in:
    st.stop()

    
# ===== 4. 当天日程详情 =====
if "clicked_date" in st.session_state and st.session_state["clicked_date"]:
    clicked_date = st.session_state["clicked_date"]
    st.divider()
    st.subheader(f"📌 {clicked_date} 的日程")

    day_schedules = safe_execute(
        supabase.table("schedules")
        .select("*")
        .eq("user_email", st.user.email)
        .eq("event_date", clicked_date)
        .order("event_time", desc=False)
    )

    if day_schedules:
        for s in day_schedules:
            col1, col2 = st.columns([6, 1])
            with col1:
                time_str = s.get("event_time", "全天")
                st.write(f"⏰ **{time_str}** — {s['title']}")
            with col2:
                if st.button("🗑️", key=f"del_day_{s['id']}"):
                    supabase.table("schedules")\
                        .delete()\
                        .eq("id", s["id"])\
                        .execute()
                    st.rerun()
    else:
        st.info("这一天还没有日程。")

    with st.expander("➕ 在这一天添加日程", expanded=False):
        event_time = st.time_input("时间：", value=datetime.time(9, 0), key=f"time_{clicked_date}")
        event_title = st.text_input("事项：", key=f"title_{clicked_date}")
        if st.button("保存", key=f"save_{clicked_date}"):
            if event_title.strip():
                supabase.table("schedules").insert({
                    "user_email": st.user.email,
                    "event_date": clicked_date,
                    "event_time": str(event_time),
                    "title": event_title
                }).execute()
                st.success("✅ 已添加")
                st.rerun()

# ===== 5. 我的所有日程列表 =====
st.divider()
st.subheader("📝 我所有的日程")

all_schedules = safe_execute(
    supabase.table("schedules")
    .select("*")
    .eq("user_email", st.user.email)
    .order("event_date", desc=False)
)

if all_schedules:
    for s in all_schedules:
        col1, col2 = st.columns([6, 1])
        with col1:
            time_str = s.get("event_time", "全天")
            st.write(f"📌 **{s['event_date']} {time_str}**：{s['title']}")
        with col2:
            if st.button("🗑️", key=f"del_all_{s['id']}"):
                supabase.table("schedules")\
                    .delete()\
                    .eq("id", s["id"])\
                    .execute()
                st.rerun()
else:
    st.info("你还没有添加日程。")