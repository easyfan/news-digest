#!/usr/bin/env python3
# parse_items.py — 解析各源 /tmp/nd_*.{json,xml,html,md} → /tmp/nd_items.json
# 用法：python3 parse_items.py
# 退出码：0=成功，1=致命错误
import json, os, re, sys, glob, xml.etree.ElementTree as ET, datetime
_S = os.environ.get('ND_SESSION', '')
def _p(n): return f'/tmp/nd_{_S}_{n}' if _S else f'/tmp/nd_{n}'

_params = json.load(open(_p('params.json')))
LIMIT = _params.get('limit', 5)
SOURCES = set(_params.get('sources', []))  # 空集合 = 全部启用
items = []  # 统一格式: {title, url, source, snippet, metric}

def enabled(src): return not SOURCES or src in SOURCES

# ── hn ──────────────────────────────────────────────────
if enabled('hn'):
    try:
        data = json.load(open(_p('hn.json')))
        for h in data.get('hits', [])[:LIMIT]:
            items.append({'title': h.get('title',''), 'url': h.get('url') or f"https://news.ycombinator.com/item?id={h.get('objectID','')}",
                          'source': 'hn', 'snippet': '', 'metric': h.get('points', 0)})
    except Exception as e:
        print(f'[FETCH_FAILED] hn parse error: {e}', file=sys.stderr)

# ── arxiv ────────────────────────────────────────────────
if enabled('arxiv'):
    try:
        tree = ET.parse(_p('arxiv.xml'))
        channel = tree.find('./channel')
        skip_el = tree.find('.//skipDays')
        today_name = datetime.date.today().strftime('%A')
        is_skip_day = skip_el is not None and any(
            d.text and d.text.strip() == today_name for d in skip_el.findall('day'))
        if channel is None or is_skip_day:
            print('[SKIP-weekend] arXiv: 今日无新论文', file=sys.stderr)
        else:
            for item in list(channel.findall('item'))[:LIMIT]:
                items.append({'title': item.findtext('title','').strip(),
                              'url': item.findtext('link','').strip(),
                              'source': 'arxiv', 'snippet': item.findtext('description','').strip()[:200], 'metric': 0})
    except Exception as e:
        print(f'[FETCH_FAILED] arxiv parse error: {e}', file=sys.stderr)

# ── hf ──────────────────────────────────────────────────
if enabled('hf'):
    try:
        data = json.load(open(_p('hf.json')))
        if not data:
            print('[SKIP-no-content] HF Daily Papers: 今日暂无内容', file=sys.stderr)
        else:
            for p in data[:LIMIT]:
                paper = p.get('paper', {}); pid = paper.get('id', '')
                items.append({'title': paper.get('title',''), 'url': f'https://huggingface.co/papers/{pid}',
                              'source': 'hf', 'snippet': (paper.get('summary','') or '')[:200], 'metric': paper.get('upvotes', 0)})
    except Exception as e:
        print(f'[FETCH_FAILED] hf parse error: {e}', file=sys.stderr)

# ── github ───────────────────────────────────────────────
if enabled('github'):
    try:
        html = open(_p('github.html')).read(); seen = set()
        for m in re.finditer(r'<h2[^>]*>\s*<a[^>]+href="/([^"]+)"', html):
            slug = m.group(1).strip('/')
            if '/' in slug and slug not in seen:
                seen.add(slug)
                items.append({'title': slug, 'url': f'https://github.com/{slug}', 'source': 'github', 'snippet': '', 'metric': 0})
        if not seen:
            for m in re.finditer(r'data-hovercard-url="/([^/"]+/[^/"]+)/hovercard"', html):
                slug = m.group(1).strip('/')
                if '/' in slug and slug not in seen:
                    seen.add(slug)
                    items.append({'title': slug, 'url': f'https://github.com/{slug}', 'source': 'github', 'snippet': '', 'metric': 0})
        if not seen:
            print('[PARSE_WARN] github HTML 结构可能已变更，解析返回空列表', file=sys.stderr)
    except Exception as e:
        print(f'[FETCH_FAILED] github parse error: {e}', file=sys.stderr)

# ── anthropic ────────────────────────────────────────────
if enabled('anthropic'):
    try:
        html = open(_p('anthropic.html')).read()
        for block in re.finditer(r'<a href="(/news/[^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL):
            title_m = re.search(r'<h[34][^>]*>([^<]+)</h[34]>', block.group(2))
            if not title_m: continue
            title = title_m.group(1).strip()
            if title:
                items.append({'title': title, 'url': 'https://www.anthropic.com' + block.group(1), 'source': 'anthropic', 'snippet': '', 'metric': 0})
            if sum(1 for i in items if i['source']=='anthropic') >= LIMIT: break
    except Exception as e:
        print(f'[FETCH_FAILED] anthropic parse error: {e}', file=sys.stderr)

# ── openai ───────────────────────────────────────────────
if enabled('openai'):
    try:
        content = open(_p('openai.md')).read()
        if not content.strip():
            print('[FETCH_FAILED] openai: 内容为空', file=sys.stderr)
        else:
            count = 0
            for m in re.finditer(r'\[([^\]]{5,200})\]\((https://openai\.com/(?:index|research|blog)/[^)]+)\)', content):
                title = re.sub(r'\s+(?:Safety|Company|Product|Engineering|Research|Stories|Events|News|Announcements)\s+\w+\s+\d+,?\s*\d*$', '', m.group(1)).strip()
                if title and m.group(2):
                    items.append({'title': title, 'url': m.group(2), 'source': 'openai', 'snippet': '', 'metric': 0})
                    count += 1
                if count >= LIMIT: break
            if count == 0:
                print('[FETCH_FAILED] openai: 0 items parsed', file=sys.stderr)
    except Exception as e:
        print(f'[FETCH_FAILED] openai parse error: {e}', file=sys.stderr)

# ── reddit ───────────────────────────────────────────────
if enabled('reddit'):
    reddit_items = []
    for sub in ['MachineLearning', 'LocalLLaMA', 'agents']:
        try:
            data = json.load(open(_p(f'reddit_{sub}.json')))
            for child in data.get('data', {}).get('children', []):
                d = child.get('data', {})
                if d.get('stickied'): continue
                reddit_items.append({'title': d.get('title',''), 'url': d.get('url',''),
                                     'source': 'reddit', 'snippet': f"r/{d.get('subreddit','')}", 'metric': d.get('score', 0)})
        except Exception as e:
            print(f'[FETCH_FAILED] reddit/{sub} parse error: {e}', file=sys.stderr)
    reddit_items.sort(key=lambda x: x['metric'], reverse=True)
    items.extend(reddit_items[:LIMIT])

# ── langchain ────────────────────────────────────────────
if enabled('langchain'):
    try:
        tree = ET.parse(_p('langchain.xml')); channel = tree.find('./channel')
        if channel is None:
            print('[FETCH_FAILED] langchain: no channel', file=sys.stderr)
        else:
            for item in list(channel.findall('item'))[:LIMIT]:
                items.append({'title': item.findtext('title','').strip(), 'url': item.findtext('link','').strip(),
                              'source': 'langchain', 'snippet': item.findtext('description','').strip()[:200], 'metric': 0})
    except Exception as e:
        print(f'[FETCH_FAILED] langchain parse error: {e}', file=sys.stderr)

# ── openclaw ─────────────────────────────────────────────
if enabled('openclaw'):
    try:
        tree = ET.parse(_p('openclaw.xml')); channel = tree.find('./channel')
        if channel is None:
            print('[FETCH_FAILED] openclaw: no channel', file=sys.stderr)
        else:
            for item in list(channel.findall('item'))[:LIMIT]:
                items.append({'title': item.findtext('title','').strip(), 'url': item.findtext('link','').strip(),
                              'source': 'openclaw', 'snippet': item.findtext('description','').strip()[:200], 'metric': 0})
    except Exception as e:
        print(f'[FETCH_FAILED] openclaw parse error: {e}', file=sys.stderr)

# ── clawhub ──────────────────────────────────────────────
if enabled('clawhub'):
    try:
        skill_map = {}
        for fpath in sorted(glob.glob(_p('clawhub_') + '*.json')):
            try:
                data = json.load(open(fpath))
                for r in data.get('results', []):
                    slug = r.get('slug', '')
                    if slug and (slug not in skill_map or r.get('updatedAt', 0) > skill_map[slug].get('updatedAt', 0)):
                        skill_map[slug] = r
            except Exception: pass
        skills = sorted(skill_map.values(), key=lambda x: x.get('updatedAt', 0), reverse=True)[:LIMIT]
        if not skills:
            print('[SKIP-no-content] ClawHub: 暂无 skill 数据', file=sys.stderr)
        for s in skills:
            items.append({'title': s.get('displayName', s.get('slug','')), 'url': f"https://clawhub.ai/skills/{s.get('slug','')}",
                          'source': 'clawhub', 'snippet': (s.get('summary','') or '')[:200], 'metric': 0})
    except Exception as e:
        print(f'[FETCH_FAILED] clawhub parse error: {e}', file=sys.stderr)

# ── devto ────────────────────────────────────────────────
if enabled('devto'):
    try:
        data = json.load(open(_p('devto.json')))
        if not data:
            print('[SKIP-no-content] DEV.to: 暂无内容', file=sys.stderr)
        else:
            for a in data[:LIMIT]:
                title = a.get('title','').strip(); url = a.get('url','').strip()
                if title and url:
                    items.append({'title': title, 'url': url, 'source': 'devto',
                                  'snippet': (a.get('description') or '')[:200].strip(), 'metric': a.get('positive_reactions_count', 0)})
    except Exception as e:
        print(f'[FETCH_FAILED] devto parse error: {e}', file=sys.stderr)

# ── github_watch ─────────────────────────────────────────
if enabled('github_watch'):
    try:
        WATCHED_REPOS = json.load(open(_p('watched_repos.json')))
    except Exception:
        WATCHED_REPOS = []
    for repo in WATCHED_REPOS:
        slug = repo.replace('/', '_')
        try:
            tree = ET.parse(_p(f'ghwatch_{slug}.xml'))
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = tree.findall('.//atom:entry', ns)
            if not entries:
                print(f'[SKIP-no-release] github_watch/{repo}: 暂无新 release', file=sys.stderr)
                continue
            for entry in entries[:LIMIT]:
                title = (entry.findtext('atom:title', '', ns) or '').strip()
                link_el = entry.find('atom:link', ns)
                url = link_el.get('href', '') if link_el is not None else f'https://github.com/{repo}'
                updated = (entry.findtext('atom:updated', '', ns) or '')[:10]
                items.append({'title': f'[{repo}] {title}', 'url': url,
                              'source': 'github_watch', 'snippet': f'release · {updated}', 'metric': 0})
        except Exception as e:
            print(f'[FETCH_FAILED] github_watch/{repo} parse error: {e}', file=sys.stderr)

json.dump(items, open(_p('items.json'), 'w'))
print(f'ITEMS_COUNT={len(items)}')
