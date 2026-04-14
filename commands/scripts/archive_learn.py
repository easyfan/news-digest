#!/usr/bin/env python3
# archive_learn.py — 将 nd_relevant.json[N-1] 追加归档到 tech-watch.md（w N 命令）
# 用法：python3 archive_learn.py <ITEM_IDX_0BASED> <TECH_WATCH_PATH>
# 退出码：0=成功（含已存在跳过），1=参数错误，2=条目越界
import json, datetime, sys

# 整数校验（防注入）
try:
    idx = int(sys.argv[1])
    assert idx >= 0
except (ValueError, AssertionError, IndexError):
    arg = sys.argv[1] if len(sys.argv) > 1 else '(空)'
    print(f'[ERR] ITEM_IDX 必须为非负整数，收到：{arg}', file=sys.stderr)
    sys.exit(1)

tech_watch = sys.argv[2] if len(sys.argv) > 2 else ''

items = json.load(open('/tmp/nd_relevant.json'))
if idx >= len(items):
    print(f'[ERR] 无效条目编号 {idx+1}，共 {len(items)} 条', file=sys.stderr)
    sys.exit(2)

item   = items[idx]
title  = item.get('title', '（无标题）')
source = item.get('source', '')
url    = item.get('url', '')

# URL 去重检查
try:
    existing = open(tech_watch).read()
    if url and url in existing:
        print(f'[SKIP-dup] URL 已存在，跳过重复归档：{url}')
        sys.exit(0)
except FileNotFoundError:
    # 首次创建文件：写入头部
    import os
    os.makedirs(os.path.dirname(tech_watch), exist_ok=True)
    with open(tech_watch, 'w') as f:
        f.write('# Tech Watch — 技术观察归档\n\n')
        f.write('记录历次 /news-digest 学习层中推荐等级为 [Learn] 的条目（持续关注，暂不行动）。\n')
        f.write('[Adopt] / [Priority Adopt] 条目在 /news-digest 会话中即时决策，不在此归档。\n')
        f.write('格式：日期 | 等级 | 标题 | 简要分析 + 备用时机。\n\n---\n\n')

today = datetime.date.today().isoformat()
with open(tech_watch, 'a') as f:
    f.write(f'## {today} | [Learn] | {title}\n\n')
    f.write(f'- **来源**：{source} | {url}\n')
    f.write('- **status**: pending\n\n---\n')

print(f'[归档] 条目已加入 tech-watch.md 观察队列：{title}')
