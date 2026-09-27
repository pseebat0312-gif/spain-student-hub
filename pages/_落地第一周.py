import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

import streamlit as st
# 统一获取当前登录用户的邮箱
if st.user.is_logged_in:
    user_email = st.user.email
else:
    user_email = st.session_state.get("qq_user_email", "")

if not user_email:
    st.warning("请先登录。")
    st.stop()
st.set_page_config(page_title="落地第一周", page_icon="🧳", layout="wide")
st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")
st.title("🧳 落地第一周攻略")
st.write("刚到西班牙，按顺序来，不慌。每一项一进来就能看到。")

st.divider()

# ===== 推荐器（最上面） =====
st.subheader("🎯 不知道选哪个？先点这里")
with st.expander("📱 手机卡推荐器", expanded=True):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        stay = st.selectbox("停留时长：", ["少于1个月", "3-6个月", "1年以上"], key="stay")
    with col_b:
        budget = st.selectbox("月预算：", ["<10欧", "10-20欧", "20-30欧"], key="budget")
    with col_c:
        data_need = st.selectbox("流量需求：", ["<10GB", "10-30GB", ">30GB"], key="data")

    if st.button("🔍 推荐", key="recommend"):
        if stay == "少于1个月":
            st.success("推荐：Lycamobile 或 Lebara 预付费卡（机场/烟草店，10欧）")
            st.link_button("📱 去 Lycamobile 官网", "https://www.lycamobile.es", use_container_width=True)
            st.link_button("📱 去 Lebara 官网", "https://www.lebara.es", use_container_width=True)
        elif budget == "<10欧":
            st.success("推荐：Digi（€3/月3GB 起，最便宜）")
            st.link_button("📱 去 Digi 官网", "https://www.digi.es", use_container_width=True)
        elif data_need == ">30GB":
            st.success("推荐：O2 或 Lowi（€20/月50-60GB，信号好）")
            st.link_button("📱 去 O2 官网", "https://www.o2online.es", use_container_width=True)
            st.link_button("📱 去 Lowi 官网", "https://www.lowi.es", use_container_width=True)
        else:
            st.success("推荐：Orange Joven 或 Vodafone Yu（€15-19/月，学生优惠）")
            st.link_button("📱 去 Orange 官网", "https://www.orange.es", use_container_width=True)
            st.link_button("📱 去 Vodafone 官网", "https://www.vodafone.es", use_container_width=True)

st.divider()

# ===== 三列 =====
col1, col2, col3 = st.columns(3)

# ===== 第一列：手机卡 =====
with col1:
    st.subheader("📱 手机卡")
    st.write("刚来先办预付费卡，凭护照就行。")
    
    st.markdown("**📊 主流运营商对比**")
    st.markdown("""
    | 运营商 | 月租 | 流量 | 适合 |
    |--------|------|------|------|
    | Digi | €3-10 | 3-50GB | 预算极低 |
    | Lycamobile | €10 | 10GB | 短期停留 |
    | Lowi | €15-20 | 25-50GB | 性价比高 |
    | O2 | €16-22 | 30-60GB | 信号最好 |
    | Orange | €15起 | 15-30GB | 学生优惠 |
    | Vodafone | €19起 | 25GB | 信号稳定 |
    | Movistar | €25+ | 25GB | 最贵最好 |
    """)
    
    st.markdown("**🔗 点这里直接去官网**")
    st.link_button("📱 Digi 官网", "https://www.digi.es", use_container_width=True)
    st.link_button("📱 Lycamobile 官网", "https://www.lycamobile.es", use_container_width=True)
    st.link_button("📱 Lowi 官网", "https://www.lowi.es", use_container_width=True)
    st.link_button("📱 O2 官网", "https://www.o2online.es", use_container_width=True)
    st.link_button("📱 Orange 官网", "https://www.orange.es", use_container_width=True)
    st.link_button("📱 Vodafone 官网", "https://www.vodafone.es", use_container_width=True)
    st.link_button("📱 Movistar 官网", "https://www.movistar.es", use_container_width=True)
    
    st.markdown("**🏪 在哪办？**")
    st.write("- 机场/烟草店：适合短期")
    st.write("- 市区营业厅：需要 NIE")
    st.write("- 网上申请：寄到家")
    
    st.info("💡 刚落地先买 Lycamobile 或 Lebara，10欧能用一个月。拿到 NIE 再换合约卡。")


# ===== 第二列：交通卡 =====
with col2:
    st.subheader("🚇 交通卡")
    
    st.markdown("**马德里**")
    st.write("- **Tarjeta Multi**：地铁站自动售票机买，卡 €2.50")
    st.write("- **Metrobús 10次票**：€12，地铁+公交")
    st.write("- **青年卡（<26岁）**：€10/月，全区域无限坐")
    
    st.markdown("**🔗 官网链接**")
    st.link_button("🚇 CRTM 马德里交通官网", "https://www.crtm.es", use_container_width=True)
    st.link_button("🚇 青年卡在线申请", "https://tarjetatransportepublico.crtm.es", use_container_width=True)
    st.link_button("🚇 TMB 巴塞罗那交通官网", "https://www.tmb.cat", use_container_width=True)
    
    st.markdown("**🎫 充值步骤（地铁站自动售票机）**")
    st.markdown("""
    1. 点屏幕上的 **「Recargar」**（充值）
    2. 把交通卡插入机器卡槽
    3. 选择 **「Abono Joven」**（青年卡，10欧）或 **「10 viajes」**（10次票，12欧）
    4. 用现金或银行卡付款
    5. 取回卡片，完成
    """)
    
    st.info("💡 26岁以下，一定要办青年卡，一个月10欧随便坐。")


# ===== 第三列：银行 + 医保 =====
with col3:
    st.subheader("🏦 银行 + 🏥 医保")
    
    st.markdown("**🏦 银行对比**")
    st.markdown("""
    | 银行 | 类型 | 特点 |
    |------|------|------|
    | Santander | 实体 | 学生免管理费 |
    | BBVA | 实体 | APP好用 |
    | CaixaBank | 实体 | 网点最多 |
    | N26 | 数字 | 易开户，⚠️续居留不认 |
    """)
    
    st.markdown("**🔗 银行官网**")
    st.link_button("🏦 Santander 官网", "https://www.santander.es", use_container_width=True)
    st.link_button("🏦 BBVA 官网", "https://www.bbva.es", use_container_width=True)
    st.link_button("🏦 CaixaBank 官网", "https://www.caixabank.es", use_container_width=True)
    st.link_button("🏦 N26 官网", "https://n26.com", use_container_width=True)
    
    st.write("**开户需要：** 护照 + NIE + 住家证明 + 注册单")
    st.warning("⚠️ N26/Revolut 续居留可能被拒，建议办实体银行。")
    
    st.markdown("**🏥 医保对比**")
    st.markdown("""
    | 医保 | 价格 | 特点 |
    |------|------|------|
    | Adeslas | 中等 | 覆盖广 |
    | Sanitas | 偏高 | 服务好 |
    | Asisa | 性价比高 | 留学生常用 |
    """)
    
    st.markdown("**🔗 医保官网**")
    st.link_button("🏥 Adeslas 官网", "https://www.adeslas.es", use_container_width=True)
    st.link_button("🏥 Sanitas 官网", "https://www.sanitas.es", use_container_width=True)
    st.link_button("🏥 Asisa 官网", "https://www.asisa.es", use_container_width=True)
    
    st.info("💡 续居留必须提供医保，建议提前办。")