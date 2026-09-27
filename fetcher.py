import os
import datetime
import feedparser
from openai import OpenAI
from supabase import create_client

# ===== 配置 =====
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
DEEPSEEK_API_KEY =os.environ.get("DEEPSEEK_API_KEY", "")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# ===== 你要抓取的 RSS 源 =====
RSS_FEEDS = [
    ("El País", "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"),
    ("El Mundo", "https://e00-elmundo.uecdn.es/elmundo/rss/portada.xml"),
    ("UCM 官网", "https://www.ucm.es/rss/noticias"),
]

def summarize(title, content):
    """用 DeepSeek 把一条新闻总结成 2-3 句中文"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个新闻摘要助手，请用中文把下面的新闻浓缩成2-3句话，简洁、清晰、信息量足。"},
                {"role": "user", "content": f"标题：{title}\n内容：{content[:1000]}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"（摘要生成失败：{e}）"

def fetch_and_save():
    for source, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # 每个源最多取5条
                title = entry.get("title", "")
                link = entry.get("link", "")
                content = entry.get("summary", "") or entry.get("description", "")
                
                # 用 AI 生成摘要
                summary = summarize(title, content)
                
                # 存进 Supabase
                supabase.table("daily_digest").insert({
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "source": source
                }).execute()
                
                print(f"✅ 已保存：{title}")
        except Exception as e:
            print(f"❌ 抓取 {source} 失败：{e}")

if __name__ == "__main__":
    fetch_and_save()