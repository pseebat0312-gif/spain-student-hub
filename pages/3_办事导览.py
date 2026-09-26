import streamlit as st

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
        **1. 领取新 NIE 卡**：收到批准信后，需在指定时间内前往警察局按指纹并领取新卡。
        
        **2. 更新住家证明**：如果搬家了，需要重新办理住家证明。
        
        **3. 银行与保险更新**：确保银行账户和医疗保险持续有效，不要断。
        
        **4. 保存批准信**：批准信要留好，以后办返乡证或续签都会用到。
        """)
    
    st.subheader("🔗 申请通过后官方链接")
    col3, col4 = st.columns(2)
    with col3:
        st.link_button("警察局预约系统", "https://sede.administracionespublicas.gob.es/", use_container_width=True)
    with col4:
        st.link_button("返乡证办理指南", "https://www.ucm.es/tramitacion-renovacion-nie", use_container_width=True)

    # --- 温馨提示 ---
    st.divider()
    st.info("⚠️ 以下信息为整理汇总，具体要求请以西班牙移民局（Extranjería）官方发布为准。")

elif school == "办理返乡证":
    st.info("入口正在整理中，敬请期待！")

elif school == "办理住家证明":
    st.info("入口正在整理中，敬请期待！")

elif school == "租房":
    st.info("入口正在整理中，敬请期待！")

elif school == "找工作":
    st.info("入口正在整理中，敬请期待！")

else:
    st.info("如果你希望添加新的板块，欢迎在留言板留言联系作者！")