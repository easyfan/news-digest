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

多源 AI 技术新闻抓取 + 摘要 + 智能学习层分析。

## 安装

```bash
# 方式一：Claude Code 原生插件（发布后可用）
/plugin marketplace add easyfan/news-digest

# 方式二：npx（无需克隆仓库）
npx news-digest

# 方式三：克隆后运行安装脚本
./install.sh              # macOS / Linux
.\install.ps1             # Windows

# 方式四：手动复制
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

## 用法

```
/news-digest                          # 全源默认摘要（含学习层）
/news-digest --no-learn               # 快速模式，仅摘要
/news-digest llm agent                # 只看 LLM/Agent 相关
/news-digest --sources hn,arxiv,hf    # 指定来源
/news-digest --limit 10               # 每源最多 10 条
/news-digest mcp --sources anthropic,openai
```

## 数据源

| 源 ID | 名称 | 说明 |
|-------|------|------|
| `hn` | Hacker News | 前端热帖 |
| `arxiv` | arXiv cs.AI | AI 论文 |
| `hf` | HuggingFace Daily Papers | 精选 AI 论文 |
| `github` | GitHub Trending | 热门仓库 |
| `anthropic` | Anthropic News | 官方动态 |
| `openai` | OpenAI News | 官方动态 |
| `reddit` | Reddit AI 社区 | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | LangChain Blog | 博客 RSS |
| `github_watch` | GitHub 仓库动态 | 指定仓库 releases |
| `openclaw` | OpenClaw Blog | OpenClaw 动态 |
| `clawhub` | ClawHub Skills | 最新 skill 更新 |

## 依赖

- `curl`（系统自带）
- `python3`（系统自带，用于 JSON/XML 解析）
- Claude Code CLI
