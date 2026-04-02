---
name: news-digest
description: |
  Use this skill when the user wants to fetch and summarize the latest AI technology news from multiple sources including Hacker News, arXiv, GitHub Trending, Anthropic, OpenAI, HuggingFace Daily Papers, Reddit, LangChain, GitHub Watch, OpenClaw, and ClawHub. Triggers on: "news digest", "latest AI news", "/news-digest", "tech news", "what's new in AI", "show me AI updates", "fetch news", "learning opportunities from news".
  Includes an intelligent learning layer (news-learner agent) that analyzes relevant items, compares them against existing platform capabilities, and recommends adoption strategies.
license: MIT
metadata:
  version: "1.0.0"
  author: cc-meta-project
  platforms: claude-code
  requires: "commands/news-digest.md + agents/news-learner.md"
---

# news-digest

Multi-source AI news fetching, summarization, and intelligent learning layer analysis.

## Install

```bash
# Option A: Claude Code plugin marketplace
/plugin marketplace add easyfan/news-digest

# Option B: npx (no clone needed)
npx news-digest

# Option C: clone and run install script
./install.sh              # macOS / Linux
.\install.ps1             # Windows

# Option D: manual copy
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

## Usage

```
/news-digest                          # full digest from all sources (with learning layer)
/news-digest --no-learn               # fast mode — news only
/news-digest llm agent                # filter by keyword
/news-digest --sources hn,arxiv,hf    # specific sources only
/news-digest --limit 10               # max 10 items per source
/news-digest mcp --sources anthropic,openai
```

## Sources

| Source ID | Name | Content |
|-----------|------|---------|
| `hn` | Hacker News | Front page posts |
| `arxiv` | arXiv cs.AI | AI papers |
| `hf` | HuggingFace Daily Papers | Curated AI papers |
| `github` | GitHub Trending | Trending repositories |
| `anthropic` | Anthropic News | Official updates |
| `openai` | OpenAI News | Official updates |
| `reddit` | Reddit AI communities | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | LangChain Blog | Blog RSS |
| `github_watch` | GitHub repo watch | Tracked repository releases |
| `openclaw` | OpenClaw Blog | OpenClaw updates |
| `clawhub` | ClawHub Skills | Latest skill updates |

## Requirements

- `curl` (system)
- `python3` (system — used for JSON/XML parsing)
- Claude Code CLI
