#!/usr/bin/env bash
# fetch_full_content.sh — 对 nd_relevant.json 中每条条目抓取全文（最多 3 条）
# 用法：bash fetch_full_content.sh
# 输出：item_0~item_2 的 /tmp/nd_learn_{i}.html，退出码：0=全部处理完毕（含部分失败）
# 退出码：0=成功，1=nd_relevant.json 不存在
set -euo pipefail

if [ ! -f /tmp/nd_relevant.json ]; then
    echo "[ERR] /tmp/nd_relevant.json 不存在" >&2
    exit 1
fi

python3 - << 'FETCH_EOF'
import json, subprocess, sys

items = json.load(open('/tmp/nd_relevant.json'))
for i, item in enumerate(items[:3]):
    url = item.get('url', '')
    out = f'/tmp/nd_learn_{i}.html'
    result = subprocess.run(
        ['curl', '-s', '-A', 'Mozilla/5.0', '--max-time', '10', '-o', out, url],
        capture_output=True
    )
    try:
        size = len(open(out, 'rb').read())
    except Exception:
        size = 0
    status = 'ok' if result.returncode == 0 and size >= 500 else 'summary_only'
    print(f'item_{i}: url={url} size={size} status={status}')
FETCH_EOF
