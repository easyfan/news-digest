#!/usr/bin/env bash
# fetch_sources.sh — 并行抓取所有启用的新闻源到 /tmp/nd_*.{json,xml,html,md}
# 用法：bash fetch_sources.sh（读取 /tmp/nd_params.json 中的 sources/limit）
# 退出码：0=成功（各源失败用 fallback 文件标记，不影响整体退出码）
set -euo pipefail

ND_SESSION="${ND_SESSION:-}"
ndtmp() { [ -n "$ND_SESSION" ] && echo "/tmp/nd_${ND_SESSION}_${1}" || echo "/tmp/nd_${1}"; }

LIMIT=$(python3 -c "import json; print(json.load(open('$(ndtmp params.json)')).get('limit', 5))")
SOURCES=$(python3 -c "import json; src=json.load(open('$(ndtmp params.json)')).get('sources',[]); print(' '.join(src) if src else '')")

enabled() { [[ -z "$SOURCES" || " $SOURCES " =~ " $1 " ]]; }

enabled hn && \
  (curl -s --max-time 15 \
    "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=${LIMIT}" \
    -o "$(ndtmp hn.json)" || echo '{"hits":[]}' > "$(ndtmp hn.json)") &

enabled arxiv && \
  (curl -s --max-time 15 \
    "https://export.arxiv.org/rss/cs.AI" \
    -o "$(ndtmp arxiv.xml)" || echo '<rss><channel></channel></rss>' > "$(ndtmp arxiv.xml)") &

enabled hf && \
  (curl -s --max-time 15 \
    "https://huggingface.co/api/daily_papers?limit=${LIMIT}" \
    -o "$(ndtmp hf.json)" || echo '[]' > "$(ndtmp hf.json)") &

enabled github && \
  (curl -s --max-time 15 -A "Mozilla/5.0" \
    "https://github.com/trending" \
    -o "$(ndtmp github.html)" || echo '' > "$(ndtmp github.html)") &

enabled anthropic && \
  (curl -s --max-time 15 \
    "https://www.anthropic.com/news" \
    -o "$(ndtmp anthropic.html)" || echo '' > "$(ndtmp anthropic.html)") &

enabled openai && \
  (curl -s --max-time 20 \
    "https://r.jina.ai/https://openai.com/news/" \
    -o "$(ndtmp openai.md)" || echo '' > "$(ndtmp openai.md)") &

if enabled reddit; then
  for sub in MachineLearning LocalLLaMA agents; do
    (curl -s --max-time 15 -A "news-digest/1.0" \
      "https://www.reddit.com/r/${sub}/hot.json?limit=${LIMIT}" \
      -o "$(ndtmp reddit_${sub}.json)" || echo '{"data":{"children":[]}}' > "$(ndtmp reddit_${sub}.json)") &
  done
fi

enabled langchain && \
  (curl -sL --max-time 15 \
    "https://blog.langchain.com/rss/" \
    -o "$(ndtmp langchain.xml)" || echo '<rss><channel></channel></rss>' > "$(ndtmp langchain.xml)") &

enabled openclaw && \
  (curl -sL --max-time 15 \
    "https://openclaw.ai/rss.xml" \
    -o "$(ndtmp openclaw.xml)" || echo '<rss><channel></channel></rss>' > "$(ndtmp openclaw.xml)") &

if enabled clawhub; then
  rm -f "$(ndtmp clawhub_)*.json" 2>/dev/null || true
  for q in agent mcp code git workflow security web; do
    (curl -sL --max-time 10 \
      "https://clawhub.ai/api/v1/search?q=${q}&limit=20" \
      -o "$(ndtmp clawhub_${q}.json)" || echo '{"results":[]}' > "$(ndtmp clawhub_${q}.json)") &
  done
fi

if enabled github_watch; then
  WATCHED_REPOS=("openclaw/openclaw" "openclaw/clawhub" "anomalyco/opencode")
  python3 -c "import json,sys; json.dump(sys.argv[1:], open('$(ndtmp watched_repos.json)','w'))" "${WATCHED_REPOS[@]}"
  rm -f "$(ndtmp ghwatch_)*.xml" 2>/dev/null || true
  for repo in "${WATCHED_REPOS[@]}"; do
    (slug=$(echo "$repo" | tr '/' '_')
     curl -s --max-time 15 -A "Mozilla/5.0" \
       "https://github.com/${repo}/releases.atom" \
       -o "$(ndtmp ghwatch_${slug}.xml)" || echo '<feed></feed>' > "$(ndtmp ghwatch_${slug}.xml)") &
  done
fi

enabled devto && \
  (curl -s --max-time 15 \
    "https://dev.to/api/articles?tag=ai&per_page=${LIMIT}&top=1" \
    -o "$(ndtmp devto.json)" || echo '[]' > "$(ndtmp devto.json)") &

wait
echo "FETCH_DONE"
