import feedparser
import json
import os
from datetime import datetime

# 1. 定义 RSS 源（已更换为稳定源）
RSS_URLS = [
    "https://github.blog/changelog/feed/"
]

# 2. 解析 RSS 并提取内容
def fetch_rss():
    items = []
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        # 调试：打印一下状态，看看是不是成功了
        if feed.bozo == 1:
            print(f"Error parsing {url}: {feed.bozo_exception}")
            continue

        for entry in feed.entries[:5]:
            items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", str(datetime.now()))
            })
    return items

# 3. 写入 Markdown 文件
def save_to_markdown(items):
    if not items:
        print("No items found, exiting.")
        return

    filename = f"issues/{datetime.now().strftime('%Y-%m-%d')}-news.md"

    # 确保 issues 文件夹存在
    os.makedirs("issues", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 每日快讯 {datetime.now().strftime('%Y-%m-%d')}\n\n")
        for i, item in enumerate(items, 1):
            f.write(f"### {i}. {item['title']}\n")
            f.write(f"- [阅读链接]({item['link']})\n")
            f.write(f"- *发布时间: {item['published']}*\n\n")

    print(f"✅ 成功保存文件: {filename}")

if __name__ == "__main__":
    data = fetch_rss()
    save_to_markdown(data)
