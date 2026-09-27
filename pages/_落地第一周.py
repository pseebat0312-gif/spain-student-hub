import streamlit as st

st.set_page_config(page_title="落地第一周", page_icon="🧳")
st.title("🧳 落地第一周攻略")
st.write("按顺序来，不慌。每一项都可以点开看详情。")

# ===== Day 1 · 落地当天 =====
st.subheader("📅 Day 1 · 落地当天")

with st.expander("📱 买手机卡", expanded=False):
    st.write("刚来西班牙，第一件事就是办一张本地手机卡。")
    st.write("**主流运营商对比：**")
    st.markdown("""
    - **Vodafone**：信号好，价格偏贵，适合对信号要求高的人
    - **Orange**：性价比高，流量多，很多留学生首选
    - **Yoigo**：最便宜，但信号一般，适合预算有限的人
    - **Lowi / Simyo**：虚拟运营商，价格更低，但客服一般
    """)
    st.info("💡 建议：刚落地先办一张预付费卡，等稳定了再换套餐。")

with st.expander("🚇 办交通卡", expanded=False):
    st.write("**马德里：** 去任何地铁站办 Multi Card，10 次票约 12 欧。")
    st.write("**巴塞罗那：** T-Casual 10 次票，约 11 欧。")
    st.info("💡 学生可以申请青年卡，交通费大幅打折。")

with st.expander("📲 下载必备 App", expanded=False):
    st.markdown("""
    - **Google Maps**：导航
    - **Cabify / Uber**：打车
    - **WhatsApp**：和本地人联系
    - **Wallapop**：二手交易
    - **Idealista**：租房
    """)

# ===== Day 2 · 学校注册 =====
st.subheader("📅 Day 2 · 学校注册")

with st.expander("🏛️ 去学校秘书处注册", expanded=False):
    st.write("带齐：护照、录取通知书、缴费证明、照片。")
    st.write("拿到学生卡后，就可以用学校图书馆、健身房等设施了。")

with st.expander("💻 激活 Campus Virtual", expanded=False):
    st.write("学校会给你一个邮箱和初始密码。")
    st.write("登录后，所有课件、作业、考试成绩都在里面。")
    st.info("💡 校外访问 Campus Virtual 需要先连学校 VPN。")

# ===== Day 3 · 住家证明 =====
st.subheader("📅 Day 3 · 住家证明")

with st.expander("🏠 办住家证明（Empadronamiento）", expanded=False):
    st.write("这是你在西班牙的“地址登记”，办续居留、医疗卡都要用。")
    st.write("**需要材料：** 护照、租房合同、房东身份证复印件。")
    st.write("**办理地点：** 你所在城市的市政府（Ayuntamiento）。")
    st.info("💡 住家证明有效期 3 个月，过期要重新办。")

# ===== Day 4-5 · 银行 + 医保 =====
st.subheader("📅 Day 4-5 · 银行 + 医保")

with st.expander("🏦 开银行账户", expanded=False):
    st.write("**Santander**：留学生友好，有专门的学生账户。")
    st.write("**BBVA**：APP 好用，转账方便。")
    st.write("**CaixaBank**：网点多，但月费偏高。")
    st.info("💡 开户需要：护照、NIE（或申请回执）、住家证明。")

with st.expander("🏥 办私立医保", expanded=False):
    st.write("**Adeslas**：覆盖广，价格中等。")
    st.write("**Sanitas**：服务好，价格偏高。")
    st.write("**Asisa**：性价比高，留学生常用。")
    st.info("💡 续居留时必须提供医保，建议提前办。")