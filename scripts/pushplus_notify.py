# encoding:utf-8
import os
import sys
import json
import requests
from datetime import datetime, timezone, timedelta

PUSHPLUS_API = "http://www.pushplus.plus/send"
BEIJING_TZ = timezone(timedelta(hours=8))


def send_notification(token, title, content, template="markdown"):
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
    }
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8")
    response = requests.post(PUSHPLUS_API, data=body, headers=headers, timeout=30)
    result = response.json()
    if result.get("code") == 200:
        print(f"推送成功: {title}")
    else:
        print(f"推送失败: {result.get('msg')}")
    return result


def main():
    token = os.environ.get("PUSHPLUS_TOKEN")
    if not token:
        print("错误: 未设置 PUSHPLUS_TOKEN")
        sys.exit(1)

    now = datetime.now(BEIJING_TZ)
    title = f"每日通知 - {now.strftime('%m月%d日')}"

    # ===== 在这里修改你的推送内容 =====
    content = f"""## 定时任务报告

**时间**: {now.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)

**状态**: ✅ 正常运行

---

> 此消息由 GitHub Actions 自动发送
"""

    send_notification(token, title, content)


if __name__ == "__main__":
    main()4. 拉到最下面，点 Commit changes → 再点 Commit changes 确认添加第 2 个文件：定时任务配置1. 回到仓库首页，再次点 Add file → Create new file2. 文件名填：.github/workflows/notify.yml（输入 .github/ 和 workflows/ 时会自动创建文件夹）3. 把下面的内容全部复制粘贴进去：name: PushPlus Notify

on:
  schedule:
    # 每天北京时间 08:00 执行
    # GitHub 用 UTC 时区，北京时间减 8 小时
    - cron: '0 0 * * *'

  # 允许手动运行（方便测试）
  workflow_dispatch:

jobs:
  send:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install requests

      - name: Send notification
        env:
          PUSHPLUS_TOKEN: ${{ secrets.PUSHPLUS_TOKEN }}
        run: python scripts/pushplus_notify.py
