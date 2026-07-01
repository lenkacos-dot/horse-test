---
name: horse-test
description: "Horse Test v4.0 — Hermes Agent Tuning Scoring System. Six-dimension scoring model + Weighted Geometric Mean HTS algorithm, pure stdlib with no external dependencies."
version: 4.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [eval, scoring, diagnostics, tuning, horse, benchmark]
    related_skills: [token-saver]
    toolsets: [terminal, file, search]
---

# Horse Test — Hermes Agent Tuning Scoring System v4.0

## Overview

Automatically scans your ~/.hermes/ environment, calculates HTS (Hermes Tuning Score) using a six-dimension scoring model, and generates improvement suggestions.

## v4.0 Key Features

- **Six-Dimension Scoring**: Skills(25%) / Config Tuning(15%) / Prompt Engineering(15%) / Tool Ecosystem(20%) / Operations(10%) / Security & Privacy(15%)
- **Enhanced Objectivity**: Frontmatter field completeness analysis + description text structure evaluation + actual config detection (no keyword existence checks)
- **Zero External Dependencies**: Pure Python stdlib (os/re/json/math), no pip packages required
- **Cross-Platform Word**: Arial font, macOS/Linux/Windows compatible
- **Scoring Report**: Terminal + Word document + JSON history

## Usage

Say **horse test** or **horse-test** in conversation, or run directly:
```bash
cd ~/.hermes/skills/horse-test
python3 horse_test.py
```
