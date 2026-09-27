import streamlit as st
import datetime
import calendar
import pytz
from supabase import create_client
from streamlit_calendar import calendar as st_calendar
from styles import apply_sidebar_style
import smtplib
from email.mime.text import MIMEText
from crypto_utils import hash_password, verify_password
apply_sidebar_style()

def is_user_logged_in():
    """判断用户是否登录（Google 或 QQ 都算）"""
    return st.user.is_logged_in or ("qq_user_email" in st.session_state)

st.set_page_config(page_title="西班牙留学生工具站", page_icon="🇪🇸")
st.title("🇪🇸 西班牙留学生一站式工具站")
st.write("¡Bienvenidos! 请从左侧选择你要用的工具。")

st.divider()

# 每日更新入口
st.markdown("""
<div style="background: linear-gradient(135deg, #1a4d2e, #4a7c59); border-radius: 16px; padding: 24px; text-align: center; margin: 20px 0;">
    <h2 style="color: #ffffff; margin: 0;">📰 今日更新</h2>
    <p style="color: #d0e8d8; margin: 8px 0 0 0;">每天凌晨自动为你收集西班牙留学生最新资讯</p >
</div>
""", unsafe_allow_html=True)

if st.button("👉 点击查看今日更新", use_container_width=True):
    st.switch_page("pages/_每日更新.py")

    
# ===== 首页海报 =====
st.markdown("### 👋 刚到西班牙？先看看这个")

st.image("https://i.postimg.cc/CLQy7rxg/2.jpg", use_container_width=True)


if st.button("🚀 进入落地第一周攻略", type="primary", use_container_width=True, key="home_poster_btn"):
    st.switch_page("pages/_落地第一周.py")



@st.cache_resource
def get_supabase():
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

supabase = get_supabase()
ADMIN_EMAIL = "pseebat0312@gmail.com"

def safe_execute(query, default=None):
    try:
        return query.execute().data
    except Exception as e:
        st.error(f"数据库请求失败：{e}")
        return default if default is not None else []
    
# 从网址参数恢复 QQ 登录状态（防止刷新后丢失）
if "user" in st.query_params and "qq_user_email" not in st.session_state:
    st.session_state["qq_user_email"] = st.query_params["user"]

# ===== 侧边栏登录区 =====
with st.sidebar:
    if not is_user_logged_in():
        st.info("💡 登录后可使用全部功能")
        
        # 两个并排的登录方式
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔵 Google 登录", use_container_width=True):
                st.login()
        with col_b:
            if st.button("📧 QQ 邮箱", use_container_width=True):
                st.session_state["show_qq_login"] = True
        
        # QQ 邮箱登录区
        if st.session_state.get("show_qq_login", False):
            with st.expander("📧 QQ 邮箱登录", expanded=True):
                # ===== 登录 =====
                qq_email = st.text_input("邮箱：", key="qq_email_input")
                qq_password = st.text_input("密码：", type="password", key="qq_pwd_input")
                if st.button("登录", key="qq_login_btn", use_container_width=True):
                    if qq_email and qq_password:
                        user = safe_execute(
                            supabase.table("app_users").select("*").eq("email", qq_email)
                        )
                        if user and verify_password(qq_password, user[0]["password"]):
                            st.session_state["qq_user_email"] = qq_email
                            st.query_params["user"] = qq_email
                            st.success("✅ 登录成功")
                            st.rerun()
                        else:
                            st.error("❌ 邮箱或密码错误")
                    else:
                        st.warning("请输入邮箱和密码")
                
                st.divider()
                # ===== 注册（默认隐藏，点击才展开）=====
                if st.button("没有账号？点这里注册", key="show_reg_btn"):
                    st.session_state["show_reg"] = True
                
                if st.session_state.get("show_reg", False):
                    new_email = st.text_input("注册邮箱：", key="reg_email")
                    new_pwd = st.text_input("设置密码：", type="password", key="reg_pwd")
                    if st.button("注册", key="reg_btn", use_container_width=True):
                        if new_email and new_pwd:
                            try:
                                hashed = hash_password(new_pwd)
                                supabase.table("app_users").insert({
                                    "email": new_email,
                                    "password": hashed
                                }).execute()
                                st.success("✅ 注册成功，请返回上方登录")
                            except Exception as e:
                                st.error(f"注册失败（邮箱可能已被占用）：{e}")
                        else:
                            st.warning("邮箱和密码都不能为空")

    else:
        # ===== 已登录：显示用户信息 =====
        if st.user.is_logged_in:
            user_email = st.user.email
        else:
            user_email = st.session_state.get("qq_user_email", "")
        
        profile = safe_execute(
            supabase.table("user_profiles").select("nickname", "avatar_emoji").eq("email", user_email)
        )
        if profile:
            display_name = profile[0].get("nickname") or user_email
            display_emoji = profile[0].get("avatar_emoji") or "👤"
        else:
            display_name = user_email
            display_emoji = "👤"
        
        st.page_link("pages/9_个人中心.py", label=f"{display_emoji} {display_name}")
        
        if user_email == ADMIN_EMAIL:
            st.caption("🛡️ 管理员")
        
        if st.button("退出登录"):
            if st.user.is_logged_in:
                st.logout()
            st.session_state.pop("qq_user_email", None)
            st.query_params.clear()
            st.rerun()

if is_user_logged_in():
    # 记录本次登录（用 session_state 防止每次刷新都写一条）
    if "logged_in_once" not in st.session_state:
        supabase.table("login_logs").insert({
            "user_email": user_email
        }).execute()
        st.session_state["logged_in_once"] = True

# ===== 时钟 =====
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

# ===== 今年进度（紧凑版） =====
spain_tz = pytz.timezone("Europe/Madrid")
now = datetime.datetime.now(spain_tz)
today = now.date()
year = today.year

days_in_year = 366 if calendar.isleap(year) else 365
day_of_year = today.timetuple().tm_yday
days_left = days_in_year - day_of_year
progress = day_of_year / days_in_year

# ===== 今年进度（紧凑版） =====
st.caption(f"📊 **{today.month}月{today.day}日** · 今年已过 {day_of_year} 天 · 还剩 **{days_left}** 天")
st.progress(progress)

# ===== 专属空间 =====
st.divider()
st.subheader("📂 我的专属空间")
if is_user_logged_in():
    st.write(f"欢迎回来，{user_email}")
else:
    st.info("🔒 登录后可以管理你的专属空间")




# ===== 倒计时卡片 =====
st.divider()
st.subheader("⏳ 我的倒计时")

if is_user_logged_in():
    # 拉取用户的倒计时
    countdowns = safe_execute(
        supabase.table("countdowns")
        .select("*")
        .eq("user_email", user_email)
        .order("event_date", desc=False)
    )
    
    if countdowns:
        for c in countdowns:
            event_dt = datetime.datetime.strptime(str(c["event_date"]), "%Y-%m-%d").date()
            days_left_countdown = (event_dt - today).days
            
            col1, col2 = st.columns([6, 1])
            with col1:
                if days_left_countdown > 0:
                    st.markdown(f"🎯 **{c['event_name']}** —— 还有 **{days_left_countdown}** 天")
                elif days_left_countdown == 0:
                    st.markdown(f"🎉 **{c['event_name']}** —— 就是今天！")
                else:
                    st.caption(f"✅ {c['event_name']}（已过去 {-days_left_countdown} 天）")
            with col2:
                if st.button("🗑️", key=f"del_countdown_{c['id']}"):
                    supabase.table("countdowns")\
                        .delete()\
                        .eq("id", c["id"])\
                        .execute()
                    st.rerun()
    else:
        st.caption("还没有倒计时，添加一个吧！")
    
    # 添加倒计时
    with st.expander("➕ 添加倒计时", expanded=False):
        cd_name = st.text_input("事件名称：", key="cd_name")
        cd_date = st.date_input("日期：", value=today + datetime.timedelta(days=30), key="cd_date")
        if st.button("添加", key="add_countdown"):
            if cd_name.strip():
                supabase.table("countdowns").insert({
                    "user_email": st.user.email,
                    "event_name": cd_name,
                    "event_date": str(cd_date)
                }).execute()
                st.success("✅ 已添加")
                st.rerun()
            else:
                st.warning("请输入事件名称。")
else:
    st.info("🔒 登录后可以添加你的倒计时。")

# ===== 节日数据（放在循环外面） =====
festivals = {
    f"{year}-01-01": {"short": "元旦", "full": "元旦（中国 / Ano Nuevo）", "color": "#e74c3c"},
    f"{year}-01-29": {"short": "春节", "full": "春节（中国 / Ano Nuevo Chino）", "color": "#e74c3c"},
    f"{year}-04-04": {"short": "清明", "full": "清明节（中国 / Qingming）", "color": "#e74c3c"},
    f"{year}-05-01": {"short": "劳动节", "full": "劳动节（中国+西班牙 / Dia del Trabajo）", "color": "#e74c3c"},
    f"{year}-06-10": {"short": "端午", "full": "端午节（中国 / Festival del Barco Dragon）", "color": "#e74c3c"},
    f"{year}-09-17": {"short": "中秋", "full": "中秋节（中国 / Festival del Medio Otono）", "color": "#e74c3c"},
    f"{year}-10-01": {"short": "中国国庆", "full": "中国国庆（China / Dia Nacional）", "color": "#e74c3c"},
    f"{year}-01-06": {"short": "三王节", "full": "三王节（西班牙 / Dia de Reyes）", "color": "#3498db"},
    f"{year}-03-19": {"short": "父亲节", "full": "父亲节（西班牙 / Dia del Padre）", "color": "#3498db"},
    f"{year}-04-18": {"short": "圣周", "full": "圣周（西班牙 / Semana Santa）", "color": "#3498db"},
    f"{year}-05-04": {"short": "母亲节", "full": "母亲节（西班牙 / Dia de la Madre）", "color": "#3498db"},
    f"{year}-06-24": {"short": "圣胡安", "full": "圣胡安节（西班牙 / Noche de San Juan）", "color": "#3498db"},
    f"{year}-08-15": {"short": "圣母升天", "full": "圣母升天节（西班牙 / Asuncion de la Virgen）", "color": "#3498db"},
    f"{year}-10-12": {"short": "西班牙国庆", "full": "西班牙国庆（Espana / Fiesta Nacional）", "color": "#3498db"},
    f"{year}-11-01": {"short": "万圣节", "full": "万圣节（西班牙 / Dia de Todos los Santos）", "color": "#3498db"},
    f"{year}-12-06": {"short": "宪法日", "full": "宪法日（西班牙 / Dia de la Constitucion）", "color": "#3498db"},
    f"{year}-12-08": {"short": "圣母无染", "full": "圣母无染原罪节（ Concepcion）", "color": "#3498db"},
    f"{year}-12-25": {"short": "圣诞", "full": "圣诞节（西班牙 / Navidad）", "color": "#3498db"},
}

# ===== 距离下一个节日的倒数 =====
today_str = today.strftime("%Y-%m-%d")
future_dates = sorted([d for d in festivals.keys() if d > today_str])
if future_dates:
    next_date = future_dates[0]
    next_info = festivals[next_date]
    days_to_next = (datetime.datetime.strptime(next_date, "%Y-%m-%d").date() - today).days
    st.caption(f"⏳ 距离 **{next_info['full']}** 还有 **{days_to_next}** 天")

# ===== 日历 =====
st.divider()
st.subheader("📅 点击日期查看详情")

if is_user_logged_in():
    schedules = safe_execute(
        supabase.table("schedules").select("*").eq("user_email", user_email)
    )
else:
    schedules = []

events = []

# 用户日程
for s in (schedules or []):
    events.append({
        "title": s["title"],
        "start": f"{s['event_date']}T{s.get('event_time', '09:00')}:00",
        "end": f"{s['event_date']}T{s.get('event_time', '10:00')}:00",
        "color": "#4a7c59"
    })

# 节日
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

cal_result = st_calendar(events=events, options=calendar_options, key="my_calendar")

# 记录点击的日期
if cal_result and cal_result.get("dateClick"):
    raw_date = cal_result["dateClick"]["date"][:10]
    parsed = datetime.datetime.strptime(raw_date, "%Y-%m-%d") + datetime.timedelta(days=1)
    clicked_date = parsed.strftime("%Y-%m-%d")
    st.session_state["clicked_date"] = clicked_date

# ===== 未登录：到此为止 =====
if not is_user_logged_in():
    st.stop()

# ===== 当天详情 =====
if "clicked_date" in st.session_state and st.session_state["clicked_date"]:
    clicked_date = st.session_state["clicked_date"]
    st.divider()
    st.subheader(f"📌 {clicked_date} 的详情")

    if clicked_date in festivals:
        info = festivals[clicked_date]
        st.success(f"🎊 **{info['full']}**")
        st.caption("📖 节日介绍即将添加...")
    else:
        st.caption("这一天没有节日记录。")

    day_schedules = safe_execute(
        supabase.table("schedules").select("*").eq("user_email", user_email).eq("event_date", clicked_date).order("event_time", desc=False)
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
                    supabase.table("schedules").delete().eq("id", s["id"]).execute()
                    st.rerun()
    else:
        st.info("这一天还没有你的日程。")

    with st.expander("➕ 在这一天添加日程", expanded=False):
        event_time = st.time_input("时间：", value=datetime.time(9, 0), key=f"time_{clicked_date}")
        event_title = st.text_input("事项：", key=f"title_{clicked_date}")
        if st.button("保存", key=f"save_{clicked_date}"):
            if event_title.strip():
                supabase.table("schedules").insert({
                    "user_email": user_email,
                    "event_date": clicked_date,
                    "event_time": str(event_time),
                    "title": event_title
                }).execute()
                st.success("✅ 已添加")
                st.rerun()