---
name: horse-test
description: "养马测试 v4.0 — Hermes Agent 调教评分系统。六维评分模型 + 加权几何平均 HTS 算法，纯 stdlib 无外部依赖。"
version: 4.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [eval, scoring, diagnostics, tuning, horse, benchmark]
    related_skills: [token-saver]
    toolsets: [terminal, file, search]
---

# 养马测试软件 — Hermes Agent 调教评分系统 v4.0

## 概述

自动扫描 ~/.hermes/ 环境，通过六维评分模型计算 HTS（Hermes Tuning Score）并生成改进建议。

## v4.0 核心特性

- **六维评分**：技能体系(25%) / 配置调优(15%) / Prompt工程(15%) / 工具生态(20%) / 运营水平(10%) / 安全隐私(15%)
- **增强客观性**：frontmatter 字段完整度分析 + 描述文本结构化评估 + 实际配置检测（不依赖关键词存在性检查）
- **零外部依赖**：纯 Python stdlib（os/re/json/math），无需安装 pip 包
- **跨平台 Word**：Arial 字体，macOS/Linux/Windows 兼容
- **评分报告**：终端 + Word 文档 + JSON 历史记录

## 使用方法

对话中说 **养马测试** 或 **horse-test**，或直接运行：
```bash
cd ~/.hermes/skills/horse-test
python3 horse_test.py
```
