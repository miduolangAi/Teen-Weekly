name: Science News RSS Fetcher
on:
  workflow_dispatch:  # 手动触发
  schedule:
    - cron: '0 12 * * *'  # 每天UTC时间12点自动运行

permissions:  # 完整权限配置
  contents: write
  pull-requests: write

jobs:
  fetch-science-news:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4  # 检出代码

      - name: Fetch RSS Feed
        uses: suisei-cn/rss-action@v2
        with:
          url: https://www.sciencenews.org/feed  # 官方RSS源
          output: ./science-news/raw.json  # JSON输出路径
          timeout: 10000  # 超时设置(毫秒)

      - name: Validate JSON
        run: |
          jq empty ./science-news/raw.json || exit 1  # 验证JSON格式

      - name: Create PR
        if: ${{ success() }}
        uses: peter-evans/create-pull-request@v5
        with:
          branch: update-science-news
          title: "Update: Science News Data ${{ date 'YYYY-MM-DD' }}"
          commit-message: "Auto-update science news feed"
