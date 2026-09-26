import streamlit as st
import sys
sys.path.append("..")
from styles import apply_sidebar_style
apply_sidebar_style()
st.set_page_config(page_title="西班牙办事快速导览", page_icon="🏛️")
st.title("🏛️ 西班牙办事快速导览")
st.write("请选择你要办的材料，查看对应的官方入口。")

school=st.selectbox(
    "选择你的需求：",
    ["请选择","续居留","办理返乡证","办理住家证明","租房","找工作","其他（即将添加）"]
)
st.divider()
if school=="请选择":
    st.info("👆 请从上方下拉菜单中选择您的需求。")

if school == "续居留":
    # ===== 前期申请 =====
    st.subheader("📚 前期申请")
    
    with st.expander("⏰ 办理时间与流程（点击展开）", expanded=False):
        st.markdown("""
        - **最佳时间**：NIE 过期前的 **60 天** 内开始办理。
        - **最晚时间**：过期后 **90 天** 内仍可提交，但可能面临行政处罚。
        - **办理方式**：马德里地区可以通过 **Mercurio 平台** 在线提交（需电子证书），也可以线下前往 **Oficina de Extranjería**。
        """)
    
    with st.expander("📋 必备材料清单（点击展开）", expanded=False):
        st.markdown("""
        **1. 官方申请表**：EX-00 表格（两联），完整填写并签名。
        
        **2. 护照**：有效期内的护照全本复印件。
        
        **3. 资金证明**：西班牙本地银行流水，建议余额覆盖整个续签期（约 IPREM 100%，每月 600 欧）。
        
        **4. 医疗保险**：覆盖整个学习期间的私立医疗保险证明。
        
        **5. 学业证明**：上一学年的成绩单 + 下一学年的注册单（注册学分需满足全日制要求）。
        
        **6. 缴费单**：Tasa 790-052，约 16.48 欧元。
        """)
    
    st.subheader("🔗 前期申请官方链接")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("UCM 续居留指导页", "https://www.ucm.es/tramitacion-renovacion-nie", use_container_width=True)
    with col2:
        st.link_button("EX-00 表格下载", "https://extranjeros.inclusion.gob.es/", use_container_width=True)
    
    st.divider()
    
    # ===== 申请通过后 =====
    st.subheader("✅ 申请通过后")
    
    with st.expander("📌 后续流程与注意事项（点击展开）", expanded=False):
        st.markdown("""
        **1. 领取新 NIE 卡**：收到批准信后，需在指定时间内前往警察局按指纹(Toma de huellas)并领取新卡。
        
        **2. 更新住家证明**：如果搬家了，需要重新办理住家证明。
        
        **3. 银行与保险更新**：确保银行账户和医疗保险持续有效，不要断。
        
        **4. 保存批准信**：批准信要留好，以后办返乡证或续签都会用到。
        """)
    
    st.subheader("🔗 申请通过后官方链接")
    col1, = st.columns(1)
    with col1:
        st.link_button("警察局预约系统", "https://sede.administracionespublicas.gob.es/", use_container_width=True)
    
    # --- 温馨提示 ---
    st.divider()
    st.info("⚠️ 以下信息为整理汇总，具体要求请以西班牙移民局（Extranjería）官方发布为准。")

elif school == "办理返乡证":
    st.subheader("✈️ 办理返乡证（Autorización de Regreso）")
    st.write("如果你需要离开西班牙，但 TIE 正在续签或暂缺，需要先办理返乡证才能回得来。")

    with st.expander("📌 办理前提与适用情况", expanded=False):
        st.markdown("""
        *   **TIE 续签期间**：已提交续签申请，但还没拿到新卡。
        *   **等待制卡期间**：已按指纹，卡还在制作中。
        *   **证件丢失或被盗**：TIE 卡丢失或被盗，并已报警。
        *   **首次办理居留**：初次居留申请获批，但还没拿到卡。
        """)

    with st.expander("📋 必备材料清单（点击展开）", expanded=False):
        st.markdown("""
        **1. 官方申请表**：EX-13 表格，完整填写并签名。
        **2. 护照**：有效期内的护照原件及全本复印件。
        **3. 居留相关材料**：续签回执单或正在办理中的证明。
        **4. 缴费单**：Tasa 790-012，费用约 16.32 欧元。
        **5. 行程证明**：机票或火车票等旅行凭证。
        **6. 紧急情况证明**（如适用）：如工作、家庭、健康等证明。
        """)

    with st.expander("⏰ 办理步骤与注意事项", expanded=False):
        st.markdown("""
        **1. 预约**：在 ICPP 系统选择“POLICIA - AUTORIZACIÓN DE REGRESO”预约。
        **2. 准备材料**：带齐上述所有材料，**原件和复印件都要带**。
        **3. 现场办理**：按预约时间前往警察局，提交材料并缴费。
        **4. 领取**：**办理周期约 7 天**，批准后需本人亲自前往领取。
        **5. 注意有效期**：返乡证有效期 90 天，只能用于一次入境。
        """)

    st.subheader("🔗 官方预约与表格下载")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("（如果进不去请直接搜索Sede policia autorizazion de regreso）")
        st.link_button("预约返乡证（ICPP）", "https://sede.administracionespublicas.gob.es/icpplus/", use_container_width=True)
    with col2:
        st.link_button("EX-13 表格下载", "https://extranjeros.inclusion.gob.es/", use_container_width=True)

    st.divider()
    st.info("⚠️ 提示：返乡证批准后需本人领取，请提前规划好时间，不要赶在出发前才去办理。")

elif school == "办理住家证明":
    st.subheader("🏠 办理住家证明（Certificado de Empadronamiento）")
    st.write("住家证明是你在西班牙的“地址登记”，办理续居留、医疗卡、银行开户时都会用到。")

    with st.expander("📌 办理前提与适用情况", expanded=False):
        st.markdown("""
        *   **刚到西班牙**：第一次租房后，需要去市政府登记。
        *   **搬家之后**：换了地址，需要更新住家证明。
        *   **办理其他手续**：续居留、办医疗卡、办银行卡时，可能需要提供。
        """)

    with st.expander("📋 必备材料清单（点击展开）", expanded=False):
        st.markdown("""
        **1. 护照或 NIE**：原件及复印件。
        **2. 租房合同**：你和房东签的正式合同。
        **3. 房东的身份证复印件**：房东的 DNI 或 NIE。
        **4. 最近的水电费单**：证明你确实住在这里。
        **5. 申请表**：部分城市需要提前在网上填表。
        """)

    with st.expander("⏰ 办理步骤与注意事项", expanded=False):
        st.markdown("""
        **1. 预约**：去你所在城市的市政府官网（Ayuntamiento）预约 cita。
        **2. 带齐材料**：带齐上述所有材料，**原件和复印件都要带**。
        **3. 现场办理**：按预约时间前往，提交材料。
        **4. 领取**：通常当场就能拿到，或者几天后去取。
        **5. 注意有效期**：住家证明通常有效期 **3 个月**，过期需要重新办理。
        """)

    st.subheader("🔗 官方预约与表格下载")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("马德里市政府预约", "https://www.madrid.es/", use_container_width=True)
    with col2:
        st.link_button("巴塞罗那市政府预约", "https://www.barcelona.cat/", use_container_width=True)

    st.divider()
    st.info("⚠️ 提示：不同城市的办理流程略有不同，建议直接搜索“Empadronamiento + 你的城市名”获取最新信息。")


elif school == "租房":
    st.info("入口正在整理中，敬请期待！")

elif school == "找工作":
    st.info("入口正在整理中，敬请期待！")

else:
    st.info("如果你希望添加新的板块，欢迎在留言板留言联系作者！")