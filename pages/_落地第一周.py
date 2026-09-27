import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()

import streamlit as st

st.set_page_config(page_title="落地第一周", page_icon="🧳", layout="wide")

st.page_link("home.py", label="⬅️ 返回首页", icon="🏠")

st.title("🧳 落地第一周攻略")
st.write("刚到西班牙，按顺序来，不慌。每一项一进来就能看到。")

st.divider()

# ===== 底部：互动推荐 =====
st.divider()
st.subheader("🎯 不知道选哪个？点这里让我推荐")

with st.expander("📱 手机卡推荐器", expanded=False):
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        stay = st.selectbox("停留时长：", ["少于1个月", "3-6个月", "1年以上"], key="stay")
    with col_b:
        budget = st.selectbox("月预算：", ["<10欧", "10-20欧", "20-30欧"], key="budget")
    with col_c:
        data_need = st.selectbox("流量需求：", ["<10GB", "10-30GB", ">30GB"], key="data")
    
    if st.button("🔍 推荐", key="recommend"):
        if stay == "少于1个月":
            st.success("推荐：Lycamobile / Lebara 预付费卡（机场或烟草店，10欧）")
        elif budget == "<10欧":
            st.success("推荐：Digi（€3/月3GB 起，最便宜）")
        elif data_need == ">30GB":
            st.success("推荐：O2 或 Lowi（€20/月50-60GB，信号好）")
        else:
            st.success("推荐：Orange Joven 或 Vodafone Yu（€15-19/月，学生优惠）")

# ===== 三列布局 =====
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
    st.write("- **青年卡（<26岁）**：€20/月，全区域无限坐")
    st.write("- 预约：tarjetatransportepublico.crtm.es")
    
    st.markdown("**巴塞罗那**")
    st.write("- **T-Jove（<25岁）**：€40/3个月，一区无限次")
    st.write("- **T-Casual**：€11.35/10次")
    st.write("- 购买：地铁站自动售票机")
    
    st.info("💡 26岁以下，一定要办青年卡，一个月20欧随便坐。")


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
    st.info("💡 续居留必须提供医保，建议提前办。")


