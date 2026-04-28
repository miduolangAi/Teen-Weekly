import feedparser
import os
from datetime import datetime

# 1. 定义 RSS 源 (这里使用 GitHub Blog 作为测试，非常稳定)
RSS_URLS = [
    "https://github.blog/changelog/feed/"
]

# 2. 解析 RSS 并提取内容
def fetch_rss():
    items = []
    for url in RSS_URLS:
        print(f"正在抓取: {url}")
        feed = feedparser.parse(url)

        # 检查是否抓取成功
        if feed.bozo != 0:
            print(f"⚠️ 抓取失败或解析错误: {url}")
            print(f"错误详情: {feed.bozo_exception}")
            continue

        # 循环提取前 5 条新闻
        for entry in feed.entries[:5]:
            items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "未知时间")
            })

    return items

# 3. 写入 Markdown 文件
def save_to_markdown(items):
    if not items:
        print("❌ 没有获取到任何内容，不生成文件。")
        return

    # 确保 issues 文件夹存在
    os.makedirs("issues", exist_ok=True)

    # 定义文件名：issues/2026-04-28-news.md
    filename = f"issues/{datetime.now().strftime('%Y-%m-%d')}-news.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 📰 每日快讯 {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("以下内容由 Python 脚本自动抓取生成：\n\n---\n\n")

        for i, item in enumerate(items, 1):
            f.write(f"### {i}. {item['title']}\n")
            f.write(f"- [🔗 点击阅读]({item['link']})\n")
            f.write(f"- *发布时间: {item['published']}*\n\n")
            f.write("---\n\n")

    print(f"✅ 成功生成文件: {filename}")

# 主程序入口
if __name__ == "__main__":
    data = fetch_rss()
    save_to_markdown(data)
