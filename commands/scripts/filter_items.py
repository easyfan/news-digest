#!/usr/bin/env python3
# filter_items.py — 去重 + 关键词过滤 + 相关性标记 → /tmp/nd_deduped.json + nd_relevant.json
# 用法：python3 filter_items.py
# 退出码：0=成功，1=输入文件缺失或格式无效
import json, os, difflib, sys
_S = os.environ.get('ND_SESSION', '')
def _p(n): return f'/tmp/nd_{_S}_{n}' if _S else f'/tmp/nd_{n}'

try:
    items = json.load(open(_p('items.json')))
    if not isinstance(items, list):
        raise ValueError('nd_items.json 不是 JSON 数组')
except Exception as e:
    print(f'[ERR] nd_items.json 读取失败：{e}', file=sys.stderr)
    sys.exit(1)

_p_data = json.load(open(_p('params.json')))
TOPICS  = _p_data.get('topics', [])
SOURCES = set(_p_data.get('sources', []))

SOURCE_RANK = {
    'anthropic': 5, 'openai': 4, 'arxiv': 3, 'hf': 3, 'github': 2,
    'hn': 1, 'reddit': 1, 'langchain': 2, 'github_watch': 2,
    'openclaw': 3, 'clawhub': 3,
}

# 读取项目 profile（detect_project_profile.py 写入）
try:
    _profile = json.load(open(_p('profile.json')))
except Exception:
    _profile = {'display': 'default', 'extra_keywords': [], 'preferred_sources': []}

# profile 的 preferred_sources 提升权重（+2）
for src in _profile.get('preferred_sources', []):
    if src in SOURCE_RANK:
        SOURCE_RANK[src] += 2

# 通用关键词 + profile 扩展词
BASE_KW = [
    'agent', 'skill', 'mcp', 'tool use', 'workflow', 'orchestration', 'multi-agent',
    'langchain', 'langgraph', 'crewai', 'autogen', 'n8n', 'dify', 'llamaindex', 'haystack',
    'cursor', 'copilot', 'opencode', 'openclaw', 'clawhub', 'swe-agent', 'open-swe', 'devin',
    'codex', 'computer use', 'agentic coding', 'coding agent', 'agent orchestration',
    'agent protocol', 'a2a', 'agent-to-agent', 'swarm', 'handoff', 'supervisor', 'subagent',
    'tool calling', 'function calling', 'prompt engineering', 'rag', 'fine-tun', 'evaluation',
    'evals', 'memory', 'planning', 'reasoning', 'llm', 'large language model', 'language model',
    'gpt', 'claude', 'gemini', 'llama', 'mistral', 'mixtral', 'phi', 'qwen', 'deepseek',
    'embedding', 'alignment', 'rlhf', 'reinforcement learning',
]
RELEVANT_KW = list(set(BASE_KW + _profile.get('extra_keywords', [])))

if _profile.get('display', 'default') != 'default':
    extra_count = len(_profile.get('extra_keywords', []))
    print(f'[过滤层] 已启用 profile "{_profile["display"]}" 关键词扩展（+{extra_count} 词，共 {len(RELEVANT_KW)} 词）')

# 1. 主题过滤
filtered = [i for i in items if any(t.lower() in (i['title']+i.get('snippet','')).lower() for t in TOPICS)] if TOPICS else list(items)

# 2. 去重（URL 精确 + 标题相似度 ≥ 0.8，保留高权威源）
deduped = []
seen_urls = set()
for item in filtered:
    url = item.get('url', '')
    if url in seen_urls:
        continue
    duplicate = False
    to_remove = []
    for kept in deduped:
        ratio = difflib.SequenceMatcher(None, item['title'].lower(), kept['title'].lower()).ratio()
        if ratio >= 0.8:
            if SOURCE_RANK.get(item['source'], 0) > SOURCE_RANK.get(kept['source'], 0):
                to_remove.append(kept)
            else:
                duplicate = True
                break
    if duplicate:
        continue
    for kept in to_remove:
        deduped.remove(kept)
        seen_urls.discard(kept.get('url', ''))
    deduped.append(item)
    seen_urls.add(url)

# 3. 相关性标记
for item in deduped:
    text = (item['title'] + ' ' + item.get('snippet', '')).lower()
    item['relevant'] = any(kw in text for kw in RELEVANT_KW)

# 4. 收集相关条目（最多 3 条，按权威度×热度排序）
relevant = sorted([i for i in deduped if i.get('relevant')],
                  key=lambda x: (SOURCE_RANK.get(x['source'], 0), x.get('metric', 0)), reverse=True)
relevant_items = relevant[:3]

json.dump(deduped,         open(_p('deduped.json'), 'w'))
json.dump(relevant_items,  open(_p('relevant.json'), 'w'))
print(f'[过滤结果] 原始 {len(items)} 条 → 去重后 {len(deduped)} 条 → 相关 {len(relevant_items)} 条')

# 全源失败诊断
ALL_SOURCES = {'hn','arxiv','github','anthropic','openai','hf','reddit','langchain','github_watch','openclaw','clawhub'}
enabled = SOURCES if SOURCES else ALL_SOURCES
sources_present = set(i.get('source','') for i in items)
failed = len(enabled - sources_present)
if failed > len(enabled) * 0.5:
    print(f'\n⚠️  [严重警告] 多数源抓取失败（{failed}/{len(enabled)} 个源无数据）！')
    print('   请检查网络连接，可运行 curl -s "https://hn.algolia.com/api/v1/search?tags=front_page" 测试。')
    print('   或用 --sources 指定可用源重试（如：/news-digest --sources hn,hf）\n')
elif failed > 3:
    print(f'[诊断] 部分源抓取失败（{failed}/{len(enabled)}），可用 --sources 指定可用源重试。')
