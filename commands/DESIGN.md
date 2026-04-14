---
name: DESIGN
description: news-digest DESIGN.md — data source config, architecture decisions, and channel roadmap. Not loaded into runtime context.
---
# news-digest DESIGN.md

本文档记录设计决策，不被 CC 自动加载到执行上下文。

---

## 数据源配置

| 源 ID | 名称 | 抓取方式 | 访问可靠性 | 备注 |
|-------|------|---------|-----------|------|
| `hn` | Hacker News | curl → HN Algolia API JSON | ✅ 稳定 | `https://hn.algolia.com/api/v1/search?tags=front_page` |
| `arxiv` | arXiv cs.AI | curl → RSS XML | ✅ 稳定（工作日）| 周末 `<skipDays>` 无新论文，标记 `[SKIP-weekend]` |
| `hf` | HF Daily Papers | curl → JSON API | ✅ 稳定 | `https://huggingface.co/api/daily_papers?limit={limit}` |
| `github` | GitHub Trending | curl → HTML + regex | ✅ 稳定 | 需 User-Agent 头 |
| `anthropic` | Anthropic News | curl → HTML | ✅ 稳定 | — |
| `openai` | OpenAI News | curl → Jina Reader → Markdown | ✅ 稳定 | `https://r.jina.ai/https://openai.com/news/` |
| `reddit` | Reddit AI 社区 | curl → `.json` API | ✅ 稳定 | 官方公开 API；抓 MachineLearning + LocalLLaMA + agents |
| `langchain` | LangChain Blog | curl → RSS XML | ✅ 稳定 | 需 `-L` 跟重定向 |
| `github_watch` | 指定仓库动态 | curl → GitHub Atom RSS | ✅ 稳定 | 无需 Token，公开仓库直接可用 |
| `openclaw` | OpenClaw Blog | curl → RSS XML | ✅ 稳定 | `https://openclaw.ai/rss.xml` |
| `clawhub` | ClawHub Skills | curl → JSON API（多词聚合）| ✅ 稳定 | 多词搜索取最近更新 skill；`/api/v1/skills` list 已废弃 |
| `devto` | DEV Community | curl → JSON API | ✅ 稳定 | `https://dev.to/api/articles?tag=ai&per_page=N&top=1` |

> **抓取方式**：所有源均使用 `curl` 保存到 `/tmp/` 后解析（不用 WebFetch），确保网络受限环境兼容性。
> 微信需认证，不列入默认源。Reddit 用官方 `.json` API，无需登录。

---

## 扩展渠道（规划中）

当前仅支持 `cli` 输出。传入其他 `--channel` 值自动回退至 `cli`，不报错。

| Channel | Handler | 状态 |
|---------|---------|------|
| `cli` | 直接输出到终端 | ✅ done |
| `slack` | POST 到 Slack Incoming Webhook（需 `SLACK_WEBHOOK_URL`） | planned |
| `email` | 发送 HTML 邮件（需配置 SMTP） | planned |
| `file` | 保存到 `~/news-digest-{date}.md` | planned |
| `gist` | 发布到 GitHub Gist（需 `gh` CLI 登录） | planned |

> 新增渠道只需在 Step 3 分支添加对应 handler，核心抓取/过滤逻辑（scripts/）不变。

---

## 设计决策

### 为何用 curl + /tmp/ 而非 WebFetch

WebFetch 在部分网络受限环境（VPN、防火墙）下不稳定，curl 可配置代理且错误信息更清晰。`/tmp/` 用于 curl 下载的临时数据，`agent_scratch/` 用于 agent 间持久化传递。

### SOURCE_RANK 权威度评分

anthropic=5, openai=4, arxiv=3, hf=3, openclaw=3, clawhub=3, github=2, langchain=2, github_watch=2, hn=1, reddit=1。Profile 的 preferred_sources 额外 +2。设计原则：官方信源 > 学术/社区 > 社交聚合。

### 去重相似度阈值 0.8

基于实测，标题相似度 ≥ 0.8 覆盖了 "同一新闻多源转载" 的主要情形，低于 0.8 误伤率较高。去重时保留权威度更高的源版本。

### relevant_items 上限 3 条

学习层分析每条约 20-30 秒，3 条上限将总时长控制在 60-90 秒（可用 --no-learn 跳过）。排序依据：`(SOURCE_RANK, metric)` 降序。

### 项目 profile 机制

通过 `detect_project_profile.py` 检测项目目录名，匹配内置 profile（cc_manager, thinking_of_memory）或用户自定义 `~/.claude/news-digest-profiles.json`。Profile 影响：`preferred_sources` 权重提升 +2、`extra_keywords` 扩展相关性判断、`learner_instruction` 指导 news-learner 分析方向。
