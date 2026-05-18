#!/usr/bin/env python3
# write_tech_watch.py — 将 [Learn] 条目追加归档到 tech-watch.md（带 URL 去重）
# 用法：python3 write_tech_watch.py <tech_watch_path> <item_url> <item_entry_text>
# 退出码：0=写入成功或已跳过，1=参数错误
import sys, os, pathlib

if len(sys.argv) < 4:
    print('usage: write_tech_watch.py <tech_watch_path> <item_url> <item_entry>', file=sys.stderr)
    sys.exit(1)

tech_watch_path = sys.argv[1]
item_url        = sys.argv[2]
item_entry      = sys.argv[3]

if os.path.exists(tech_watch_path):
    existing = pathlib.Path(tech_watch_path).read_text(encoding='utf-8')
    if item_url and item_url in existing:
        print(f'[去重] 已跳过（URL 已存在）: {item_url}')
        sys.exit(0)
else:
    pathlib.Path(tech_watch_path).parent.mkdir(parents=True, exist_ok=True)
    header = (
        '# Tech Watch — 技术观察归档\n\n'
        '记录历次 /news-digest 学习层中推荐等级为 [Learn] 的条目（持续关注，暂不行动）。\n'
        '[Adopt] / [Priority Adopt] 条目在 /news-digest 会话中即时决策，不在此归档。\n'
        '格式：日期 | 等级 | 标题 | 简要分析 + 备用时机。\n\n---\n\n'
    )
    pathlib.Path(tech_watch_path).write_text(header, encoding='utf-8')

with open(tech_watch_path, 'a', encoding='utf-8') as f:
    f.write(item_entry + '\n')
print(f'[归档] 已写入 tech-watch.md: {item_url}')
