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
st.subheader("📅 点击日期查看详情")

# 拉取当前用户所有日程
if st.user.is_logged_in:
    schedules = safe_execute(
        supabase.table("schedules")
        .select("*")
        .eq("user_email", st.user.email)
    )
else:
    schedules = []

events = []

# 用户日程（绿色）
for s in (schedules or []):
    events.append({
        "title": s["title"],
        "start": f"{s['event_date']}T{s.get('event_time', '09:00')}:00",
        "end": f"{s['event_date']}T{s.get('event_time', '10:00')}:00",
        "color": "#4a7c59"
    })

# 节日数据（简称 + 全名）
festivals = {
    # 中国节日（红色）
    f"{today.year}-01-01": {"short": "🎉 元旦", "full": "元旦（中国 / Año Nuevo）", "color": "#e74c3c"},
    f"{today.year}-01-29": {"short": "🧧 春节", "full": "春节（中国 / Año Nuevo Chino）", "color": "#e74c3c"},
    f"{today.year}-04-04": {"short": "🌿 清明", "full": "清明节（中国 / Qingming）", "color": "#e74c3c"},
    f"{today.year}-05-01": {"short": "💼 劳动节", "full": "劳动节（中国+西班牙 / Día del Trabajo）", "color": "#e74c3c"},
    f"{today.year}-06-10": {"short": "🐉 端午", "full": "端午节（中国 / Festival del Barco Dragón）", "color": "#e74c3c"},
    f"{today.year}-09-17": {"short": "🌕 中秋", "full": "中秋节（中国 / Festival del Medio Otoño）", "color": "#e74c3c"},
    f"{today.year}-10-01": {"short": "🇨🇳 中国国庆", "full": "中国国庆（China / Día Nacional de China）", "color": "#e74c3c"},
    
    # 西班牙节日（蓝色）
    f"{today.year}-01-06": {"short": "👑 三王节", "full": "三王节（西班牙 / Día de Reyes）", "color": "#3498db"},
    f"{today.year}-03-19": {"short": "👨 父亲节", "full": "父亲节（西班牙 / Día del Padre）", "color": "#3498db"},
    f"{today.year}-04-18": {"short": "✝️ 圣周", "full": "圣周（西班牙 / Semana Santa）", "color": "#3498db"},
    f"{today.year}-05-04": {"short": "👩 母亲节", "full": "母亲节（西班牙 / Día de la Madre）", "color": "#3498db"},
    f"{today.year}-06-24": {"short": "🔥 圣胡安", "full": "圣胡安节（西班牙 / Noche de San Juan）", "color": "#3498db"},
    f"{today.year}-08-15": {"short": "⛪ 圣母升天", "full": "圣母升天节（西班牙 / Asunción de la Virgen）", "color": "#3498db"},
    f"{today.year}-10-12": {"short": "🇪🇸 西班牙国庆", "full": "西班牙国庆（España / Fiesta Nacional）", "color": "#3498db"},
    f"{today.year}-11-01": {"short": "👻 万圣节", "full": "万圣节（西班牙 / Día de Todos los Santos）", "color": "#3498db"},
    f"{today.year}-12-06": {"short": "📜 宪法日", "full": "宪法日（西班牙 / Día de la Constitución）", "color": "#3498db"},
    f"{today.year}-12-08": {"short": "⛪ 圣母无染", "full": "圣母无染原罪节（西班牙 / Inmaculada Concepción）", "color": "#3498db"},
    f"{today.year}-12-25": {"short": "🎄 圣诞", "full": "圣诞节（西班牙 / Navidad）", "color": "#3498db"},
}

# 把节日加进日历
for date_str, info in festivals.items():
    events.append({
        "title": info["short"],
        "start": date_str,
        "allDay": True,
        "color": info["color"]
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
    "eventDisplay": "block",
    "dayMaxEvents": 2,
}

cal_result = calendar(events=events, options=calendar_options, key="my_calendar")

# ===== 未登录：到此为止 =====
if not st.user.is_logged_in:
    st.stop()


# 如果用户点了某天，就存起来
if cal_result and cal_result.get("dateClick"):
    raw_date = cal_result["dateClick"]["date"][:10]
    parsed = datetime.datetime.strptime(raw_date, "%Y-%m-%d") + datetime.timedelta(hours=12)
    clicked_date = parsed.strftime("%Y-%m-%d")
    st.session_state["clicked_date"] = clicked_date


# ===== 4. 当天详情 =====
if "clicked_date" in st.session_state and st.session_state["clicked_date"]:
    clicked_date = st.session_state["clicked_date"]
    st.divider()
    st.subheader(f"📌 {clicked_date} 的详情")
    
    # 当天节日
    if clicked_date in festivals:
        info = festivals[clicked_date]
        st.success(f"🎊 **{info['full']}**")
        st.caption("📖 节日介绍即将添加...")
    
    # 当天用户日程
    if st.user.is_logged_in:
        day_schedules = safe_execute(
            supabase.table("schedules")
            .select("*")
            .eq("user_email", st.user.email)
            .eq("event_date", clicked_date)
            .order("event_time", desc=False)
        )
        
        if day_schedules:
            st.write("**你的日程：**")
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
            st.info("这一天还没有你的日程。")
        
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
    else:
        st.info("🔒 登录后可以添加和管理你的日程。")
        