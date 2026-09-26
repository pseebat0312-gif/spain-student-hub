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

        st.success(f"{display_emoji} {display_name}")
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

import datetime
import calendar
import pytz

# ===== 顶部时钟 =====
import datetime
import calendar
import pytz

# ===== 顶部时钟（实时跳动） =====
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


# ===== 会动的日历 =====
st.divider()
st.subheader("📅 中西文化日历")

spain_tz = pytz.timezone("Europe/Madrid")
today = datetime.datetime.now(spain_tz).date()
year = today.year
month = today.month

# 节日数据
festivals = {
    (1, 1): "🎉 元旦",
    (1, 6): "👑 三王节",
    (1, 29): "🧧 春节",
    (2, 14): "💘 情人节",
    (3, 8): "👩 妇女节",
    (3, 19): "👨 父亲节",
    (4, 23): "📚 读书日",
    (5, 1): "💼 劳动节",
    (6, 24): "🔥 圣胡安节",
    (8, 15): "⛪ 圣母升天节",
    (9, 11): "🏴 加泰日",
    (10, 1): "🇨🇳 中国国庆",
    (10, 12): "🇪🇸 西班牙国庆",
    (11, 1): "👻 万圣节",
    (12, 6): "📜 宪法日",
    (12, 8): "⛪ 圣母节",
    (12, 25): "🎄 圣诞节",
}

cal = calendar.monthcalendar(year, month)
weekdays = ["一", "二", "三", "四", "五", "六", "日"]

# 用 CSS 强制每列等宽
html = """
<style>
    .calendar-table {
        width: 100%;
        table-layout: fixed;
        border-collapse: separate;
        border-spacing: 6px;
    }
    .calendar-table th {
        padding: 10px;
        color: #4a7c59;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
    }
    .calendar-table td {
        padding: 10px 5px;
        text-align: center;
        border-radius: 10px;
        height: 80px;
        vertical-align: top;
        font-size: 14px;
    }
    .today-cell {
        background: #4a7c59;
        color: white !important;
        box-shadow: 0 0 12px #4a7c59;
    }
    .normal-cell {
        background: #2a2a40;
        color: #ddd;
    }
    .festival-text {
        font-size: 10px;
        margin-top: 4px;
        color: #a0d8b3;
    }
    .today-cell .festival-text {
        color: #fff;
    }
    .day-icon {
        font-size: 18px;
        display: block;
    }
</style>
<table class="calendar-table">
"""

html += "<tr>"
for wd in weekdays:
    html += f"<th>{wd}</th>"
html += "</tr>"

for week in cal:
    html += "<tr>"
    for day in week:
        if day == 0:
            html += "<td></td>"
        else:
            is_today = (day == today.day)
            festival = festivals.get((month, day), "")
            cls = "today-cell" if is_today else "normal-cell"
            icon = "🧍" if is_today else ""
            html += f'<td class="{cls}">'
            html += f'<span class="day-icon">{icon}</span>'
            html += f'<div style="font-weight:bold;">{day}</div>'
            if festival:
                html += f'<div class="festival-text">{festival}</div>'
            html += "</td>"
    html += "</tr>"

html += "</table>"
st.markdown(html, unsafe_allow_html=True)


# ===== 用户日程 =====
st.divider()
st.subheader("📝 我的日程")

if st.user.is_logged_in:
    with st.expander("➕ 添加新日程", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            event_date = st.date_input("日期：", value=today)
        with col2:
            event_title = st.text_input("事项：")
        
        if st.button("保存日程", type="primary"):
            if event_title.strip():
                supabase.table("schedules").insert({
                    "user_email": st.user.email,
                    "event_date": str(event_date),
                    "title": event_title
                }).execute()
                st.success("✅ 日程已保存")
                st.rerun()
            else:
                st.warning("请输入事项内容。")
    
    schedules = supabase.table("schedules")\
        .select("*")\
        .eq("user_email", st.user.email)\
        .order("event_date", desc=False)\
        .execute()
    
    if schedules.data:
        for s in schedules.data:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.write(f"📌 **{s['event_date']}**：{s['title']}")
            with col2:
                if st.button("🗑️", key=f"del_schedule_{s['id']}"):
                    supabase.table("schedules")\
                        .delete()\
                        .eq("id", s["id"])\
                        .execute()
                    st.rerun()
    else:
        st.info("你还没有添加日程。")
else:
    st.info("登录后可以添加你的个人日程。")


# ---------- 个人资料 ----------
st.divider()
st.subheader("👤 个人资料设置")

profile = safe_execute(
    supabase.table("user_profiles")
    .select("*")
    .eq("email", st.user.email)
)

if profile:
    current_nickname = profile[0].get("nickname", "")
    current_emoji = profile[0].get("avatar_emoji", "🐱")
else:
    current_nickname = ""
    current_emoji = "🐱"

new_nickname = st.text_input("昵称：", value=current_nickname)

emoji_options = [
    "🐱", "🐶", "🦊", "🐼", "🐸", "🦁", "🐯", "🐨",
    "🌸", "🌈", "⭐", "🌙", "☀️", "🍀", "🎵", "🍕",
]
new_emoji = st.selectbox(
    "选择一个头像：",
    emoji_options,
    index=emoji_options.index(current_emoji) if current_emoji in emoji_options else 0,
)

if st.button("💾 保存资料"):
    safe_execute(
        supabase.table("user_profiles").upsert({
            "email": st.user.email,
            "nickname": new_nickname,
            "avatar_emoji": new_emoji,
        })
    )
    st.success("✅ 资料已保存")
    st.rerun()


# ---------- 会员状态 ----------
st.divider()
st.subheader("💎 会员状态")

col1, col2 = st.columns(2)
with col1:
    st.metric("当前等级", "免费用户")
with col2:
    st.metric("AI 分析次数", "0 / 3")

st.info("升级到会员，解锁无限次 AI 分析和历史记录保存功能。")
if st.button("升级到会员（即将开放）"):
    st.warning("付费功能正在开发中，敬请期待。")