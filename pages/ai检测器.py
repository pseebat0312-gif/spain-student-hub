import streamlit as st
from supabase import create_client
supabase=create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])




# 检查用户是否登录
if not st.user.is_logged_in:
    st.warning("请先在首页登录，才能保存检测历史。")
    st.stop()  # 停止往下执行


import sys
sys.path.append("..")
from miexperiencia import check_my_experience
import streamlit as st
import math
import re

st.set_page_config(page_title="AI 文本检测器", page_icon="🔍")
st.title("🔍 AI 文本检测器")
st.write("粘贴一段文本，判断它是人类写的还是 AI 生成的。")

def calculate_burstiness(text):
    sentences = re.split(r'[.!?。！？\n]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
    if len(sentences) < 2:
        return 0.5
    lengths = [len(s) for s in sentences]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    return min(std_dev / (avg + 1), 1.0)

def calculate_lexical_diversity(text):
    words = re.findall(r'\w+', text.lower())
    if len(words) == 0:
        return 0.0
    unique_words = set(words)
    return len(unique_words) / len(words)

def simple_ai_score(text):
    burstiness = calculate_burstiness(text)
    diversity = calculate_lexical_diversity(text)
    
    # 突发性越低、词汇越单调，AI 概率越高
    ai_score = 0.0
    if burstiness < 0.55:
        ai_score += (0.55 - burstiness) * 2.5
    if diversity < 0.65:
        ai_score += (0.65 - diversity) * 2.5
    
    ai_score = min(max(ai_score, 0.0), 1.0)
    return ai_score, burstiness, diversity

language = st.selectbox("选择语言：", ["español","English","中文"])

text_input = st.text_area("输入文本：", height=200, placeholder="在这里粘贴要检测的文本...")

if st.button("检测", type="primary"):
    if not text_input.strip():
        st.warning("请输入一些文本。")
    else:
        ai_prob, burst, diver = simple_ai_score(text_input)
        
        if ai_prob > 0.6:
            st.error(f"🤖 **AI 生成**（可能性：{ai_prob:.2%}）")
        elif ai_prob > 0.35:
            st.warning(f"⚠️ **可能是 AI 生成**（可能性：{ai_prob:.2%}）")
        else:
            st.success(f"✍️ **人类书写**（可能性：{(1-ai_prob):.2%}）")

        my_issues = check_my_experience(text_input, language)
        if my_issues:
            st.divider()
            st.subheader("💡 **专属修改建议（基于beta自己的经验库）**：")
            for issue in my_issues:
                st.markdown(f"- {issue}")
        else:
            st.caption("💡 **根据beta的经验库**：未发现明显问题。")
        
        st.divider()
        st.caption("📊 底层分析数据（供参考）")
        col1, col2 = st.columns(2)
        col1.metric("句子波动性 (Burstiness)", f"{burst:.3f}")
        col2.metric("词汇多样性 (Diversity)", f"{diver:.3f}")
        st.caption("提示：突发性越低、词汇越单调，越可能是 AI。人类写作通常有长短句交错和更丰富的用词。")

        if st.user.is_logged_in:
            supabase.table("detection_history").insert({
                "user_email": st.user.email,
                "text_snippet": text_input[:100],
                "ai_probability": ai_prob
            }).execute()
            st.success("✅ 本次检测已保存")

st.divider()
st.caption("当前版本基于数学统计法，不依赖外部模型，秒级出结果。")