#!/usr/bin/env python3
# parse_arguments.py — 解析 $ARGUMENTS 字符串 → /tmp/nd_params.json
# 用法：python3 parse_arguments.py "$ARGUMENTS"
# 退出码：0=成功，1=失败
import json, os, re, sys
_S = os.environ.get('ND_SESSION', '')
def _p(n): return f'/tmp/nd_{_S}_{n}' if _S else f'/tmp/nd_{n}'

args = sys.argv[1] if len(sys.argv) > 1 else ''

# 解析 --limit
limit = 5
m = re.search(r'--limit\s+(\d+)', args)
if m:
    limit = int(m.group(1))

# 解析 --sources（大小写不敏感，自动转小写）
VALID_SOURCES = {'hn','arxiv','github','anthropic','openai','hf','reddit','langchain','github_watch','openclaw','clawhub','devto'}
sources = []
m = re.search(r'--sources\s+(\S+)', args)
if m:
    raw = [s.strip().lower() for s in m.group(1).split(',') if s.strip()]
    invalid = [s for s in raw if s not in VALID_SOURCES]
    if invalid:
        print(f"[WARN] 未知源：{', '.join(invalid)}，有效源：{', '.join(sorted(VALID_SOURCES))}。已忽略无效值。")
    sources = [s for s in raw if s in VALID_SOURCES]

# 解析 --no-learn
no_learn = '--no-learn' in args

# 解析 topics
cleaned = re.sub(r'--(?:limit|sources|channel)\s+\S+', '', args)
cleaned = re.sub(r'--no-learn', '', cleaned)
topics = [w for w in cleaned.split() if w and not w.startswith('-')]

json.dump({'topics': topics, 'limit': limit, 'sources': sources, 'no_learn': no_learn},
          open(_p('params.json'), 'w'))
print(f"PARAMS: topics={topics} limit={limit} sources={sources} no_learn={no_learn}")

# --channel 回退提示
ch = re.search(r'--channel\s+(\S+)', args)
if ch:
    print(f"[--channel] 渠道 '{ch.group(1)}' 当前仅支持 cli 输出，已自动回退。")
