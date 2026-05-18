---
description: 从多平台（HN/arXiv/GitHub 等）抓取 AI 技术新闻并生成摘要，支持关键词过滤和智能学习层分析；学习层会写入 tech-watch.md 并调用 news-learner subagent（额外 60-80 秒），可用 --no-learn 跳过
argument-hint: "[topics...] [--sources SOURCE,...] [--limit N] [--no-learn] [--channel cli]"
allowed-tools: ["Bash", "Agent"]
---
Follow the instructions in ~/.claude/skills/news-digest/SKILL.md with the arguments: $ARGUMENTS
