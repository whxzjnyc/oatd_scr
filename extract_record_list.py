import os
import re
from bs4 import BeautifulSoup

html_dir = "oatd_pages"
records = set()

# 用于校验 record 参数是否合法
valid_pattern = re.compile(r"record=([^&]+)")

for fname in os.listdir(html_dir):
    if not fname.endswith(".html"):
        continue

    path = os.path.join(html_dir, fname)

    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 只从主结果区提取
    for result in soup.select("div.result"):
        a = result.find(
            "a",
            string=lambda s: s and "Record Details" in s
        )
        if not a or not a.get("href"):
            continue

        href = a["href"]

        # 必须是 record=xxx 的形式
        if not valid_pattern.search(href):
            continue

        url = "https://oatd.org/oatd/" + href
        records.add(url)

# 保存
with open("record_details.txt", "w", encoding="utf-8") as f:
    for r in sorted(records):
        f.write(r + "\n")

print(f"✅ 共提取 {len(records)} 条 record details")