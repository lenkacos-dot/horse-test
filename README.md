# 🐎 Horse Test — Horse-Test

> **Hermes Agent Tuning Scoring System** | Pure Python standard library, zero external dependencies  
> Version: v4.0.0 | Platform: macOS / Windows / Linux

---

## Table of Contents

1. [What is Horse Test](#1-what-is-horse-test)
2. [Quick Start](#2-quick-start)
3. [Installation](#3-installation)
4. [Usage](#4-usage)
5. [Scoring Model](#5-scoring-model)
6. [Rank System](#6-rank-system)
7. [Report Output](#7-report-output)
8. [Cross-Platform Compatibility](#8-cross-platform-compatibility)
9. [FAQ](#9-faq)
10. [Project Structure](#10-project-structure)
11. [Version History](#11-version-history)

---

## 1. What is Horse Test

**Horse Test** is a tuning quality evaluation system designed for [Hermes Agent](https://hermes-agent.nousresearch.com).

> "Horse Test" = Training a fine steed = Tuning and optimizing your Hermes Agent

It automatically scans your `~/.hermes/` environment (skills, config files, Cron tasks, external tools, security rules, etc.), quantifies the Agent's configuration level across six dimensions, calculates the **HTS (Hermes Tuning Score)** composite score, and generates improvement suggestions.

### Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Quantified Evaluation** | Six-dimension scoring model + Weighted Geometric Mean algorithm, 0-1000 scale |
| 🔍 **Diagnose Weaknesses** | Auto-detect skill coverage gaps, config defects, security omissions |
| 📈 **Trend Tracking** | JSON history records, supports score trend comparison |
| 💡 **Improvement Suggestions** | Auto-generates actionable suggestions for low-scoring dimensions |
| 📄 **Word Report** | One-click generation of detailed Word report on desktop |
| 🌐 **Cross-Platform** | Runs on macOS / Windows / Linux |
| 🚫 **Zero Dependencies** | Pure Python standard library, no `pip install` required |

---

## 2. Quick Start

```bash
# 1. Clone or download the project
git clone https://github.com/your-username/horse-test.git ~/horse-test

# 2. Install to Hermes skill directory
cp -R ~/horse-test ~/.hermes/skills/horse-test/

# 3. Run the scoring
cd ~/.hermes/skills/horse-test
python3 horse_test.py
```

Or simply say this in a Hermes conversation:

> **"horse test"** or **"horse-test"**

---

## 3. Installation

### 3.1 Requirements

| Item | Requirement |
|------|-------------|
| **Python** | 3.8 or higher |
| **Hermes Agent** | Any version (not required for terminal-only use) |
| **python-docx** | *Optional* — for generating Word reports (`pip3 install python-docx`) |

**No pip dependencies required for terminal mode.** The core engine only uses standard libraries: `os` / `re` / `json` / `math` / `shutil` / `subprocess` / `pathlib`.

### 3.2 Installation Methods

#### Method A: Hermes Skill (Recommended)

```bash
# Create skill directory
mkdir -p ~/.hermes/skills/horse-test

# Copy all files
cp horse_test.py ~/.hermes/skills/horse-test/
cp SKILL.md ~/.hermes/skills/horse-test/
cp DESCRIPTION.md ~/.hermes/skills/horse-test/
```

Then say **"horse test"** in a Hermes conversation to trigger it.

#### Method B: Standalone Run

```bash
# Run directly
python3 horse_test.py
```

#### Method C: Run from Desktop Copy

```bash
cd ~/Desktop/horse-test-en
python3 horse_test.py
```

---

## 4. Usage

### 4.1 Terminal Run

```bash
python3 horse_test.py
```

Sample Output:

```
============================================================
  🐎 Horse Test Results — Hermes Agent Tuning Report  v4.0
============================================================
  User: alan        Date: 2026-06-30 14:57
  HTS Score: 794.1/1000  |  Rank: 🐉 Dragon Knight
============================================================

  📊 Six-Dimension Score Breakdown:
  ──────────────────────────────────────────────────────────
  🧠 Skills            ████████████████████████░░░░░░  81.0/100
  ⚙️ Config Tuning     ████████████████████████░░░░░░  80.0/100
  📝 Prompt Engineering ████████████████████░░░░░░░░░░  67.0/100
  🔌 Tool Ecosystem    ██████████████████████░░░░░░░░  74.0/100
  📊 Operations        █████████████████████░░░░░░░░░  70.0/100
  🛡️ Security & Privacy ███████████████████████░░░░░░░  78.0/100
  ──────────────────────────────────────────────────────────
  📐 Algorithm: Weighted Geometric Mean HTS = ∏(Sᵢ^Wᵢ)

  🏆 Current Rank: 🐉 Dragon Knight (Rank 5/6)
     5.9 points needed for next rank '👑Horse God'

  💡 Suggestions:
  1. 🟡 📝 Prompt Engineering (52/100) → Configure max_turns parameter
  2. 🟡 🛡️ Security & Privacy (54/100) → Add sensitive file isolation strategy
```

### 4.2 Word Report

Install python-docx and run:

```bash
pip3 install python-docx
python3 horse_test.py
```

Generates `Horse_Test_Report_v4_YYYYMMDD.docx` on the desktop, containing:
- Cover page (HTS + Rank + Date)
- Score overview table (six-dimension radar + composite score)
- Per-dimension score details table (31 sub-items with score/max/criteria)
- Improvement suggestions (sorted by priority)

### 4.3 History

Each evaluation is automatically saved to `~/.hermes/horse-test-history.json`:

```json
[
  {
    "date": "2026-06-30T14:57:00",
    "hts": 794.1,
    "dimensions": { "skills": 81, "config": 80, "prompt": 67, "tools": 74, "operations": 70, "security": 78 }
  }
]
```

Keeps the last 30 evaluations. The trend correction coefficient `β` automatically compares against the previous score.

### 4.4 Using as a Hermes Skill

After installing to `~/.hermes/skills/horse-test/`, trigger it by saying any of the following in any conversation:

| Command | Effect |
|---------|--------|
| `horse test` | Full scoring + report |
| `horse-test` | Same as above |
| `run horse test` | Same as above |

---

## 5. Scoring Model

### 5.1 Six-Dimension Scoring System

| # | Dimension | Weight | Sub-Items | Evaluation Content |
|---|-----------|--------|-----------|-------------------|
| 🧠 | **Skills** | **25%** | 5 | Skill count, frontmatter quality, description structure, domain coverage, community utilization |
| ⚙️ | **Config Tuning** | **15%** | 6 | Provider, Fallback, Profile, Token optimization, Memory, Network |
| 📝 | **Prompt Engineering** | **15%** | 5 | System Prompt quality, Skill descriptions, Context management, Multilingual, Instruction precision |
| 🔌 | **Tool Ecosystem** | **20%** | 5 | Plugins, Gateway, Cron tasks, External tools, API |
| 📊 | **Operations** | **10%** | 5 | Memory quality, Iterative optimization, Community engagement, Documentation, Automation |
| 🛡️ | **Security & Privacy** | **15%** | 5 | Privacy rules, Rule quality, Cross-Profile protection, Data isolation, Security awareness |

### 5.2 HTS Algorithm

**Weighted Geometric Mean:**

```
HTS_base = 1000 × S₁^W₁ × S₂^W₂ × ... × Sₙ^Wₙ

HTS_final = HTS_base × β × σ

Where:
  Sᵢ = Score of the i-th dimension (0.0 ~ 1.0)
  Wᵢ = Weight of the i-th dimension (∑Wᵢ = 1.0)
  β  = Trend correction coefficient (+5% increase, -5% decrease)
  σ  = Stability correction coefficient (reserved, currently = 1.0)
```

**Why Geometric Mean?**
- Geometric mean is more sensitive to low-scoring dimensions, preventing "one strength masking all weaknesses"
- Shortcomings in security/privacy shouldn't be ignored — geometric mean reflects this accurately

### 5.3 Scoring Objectivity

v4.0 no longer uses fixed scores or keyword existence checks. Instead:

| Sub-Item | v1.0 Method | v4.0 Method | Improvement |
|----------|-------------|-------------|-------------|
| `skill_desc` | Check for description/usage keywords | **Frontmatter field completeness + description structure analysis** | From "does it exist" to "how good is it" |
| `cfg_token` | Fixed 10 points | **Actual detection of max_tokens / context_window** | From "assumption" to "fact" |
| `sec_cross_profile` | Fixed 15 points | **Detection of actual config.yaml settings** | From "assumption" to "fact" |
| `sec_data_isolate` | Fixed 12 points | **4-dimensional deep analysis of .hermes.md** | From "assumption" to "fact" |

---

## 6. Rank System

| Rank | Score | Title | Characteristics |
|------|-------|-------|-----------------|
| 🐣 Rank 1 | 0-199 | Stable Boy | New to Hermes, basic setup complete |
| 🐴 Rank 2 | 200-349 | Rider | Mastered basic skills, daily use |
| 🏇 Rank 3 | 350-499 | Horse Trainer | Multi-Profile, custom skills |
| 🦄 Rank 4 | 500-649 | Master Trainer | Proficient with Cron/Gateway/Plugins |
| 🐉 Rank 5 | 650-799 | Dragon Knight | Custom skills, community contributions |
| 👑 Rank 6 | 800-1000 | Horse God | Ultimate tuning, automated workflows |

---

## 7. Report Output

### 7.1 Terminal Report

Real-time display of scoring results, including:
- Header info (username, date, HTS, rank)
- Six-dimension score bars (with progress bar visualization)
- Algorithm description (Base HTS / β correction / trend comparison)
- Rank info (current / distance to next rank)
- Improvement suggestions (up to 5, by priority)

### 7.2 Word Report

- Format: `~/Desktop/Horse_Test_Report_v4_YYYYMMDD.docx`
- Font: Arial (cross-platform compatible)
- Content: Cover → Score overview table → Per-dimension details table (31 sub-items) → Improvement suggestions
- Requirement: `python-docx` (`pip3 install python-docx`)

### 7.3 JSON History

- Format: `~/.hermes/horse-test-history.json`
- Retention: Last 30 evaluations
- Purpose: Trend tracking + β coefficient calculation

---

## 8. Cross-Platform Compatibility

| Feature | macOS | Windows | Linux |
|---------|-------|---------|-------|
| Scoring Engine | ✅ | ✅ | ✅ |
| Word Report | ✅ | ✅ | ✅ |
| Username Detection | `$USER` | `%USERNAME%` | `$USER` |
| Gateway Detection | `pgrep` | `tasklist` | `pgrep` |
| Script Detection | `.sh` | `.bat` / `.ps1` / `.cmd` | `.sh` |
| Path Format | `/Users/alan/` | `C:\Users\alan\` | `/home/alan/` |

Same codebase for all platforms, no modifications needed.

---

## 9. FAQ

### Q1: Why is my HTS much lower than arithmetic average?

Because scoring uses **Weighted Geometric Mean**, which penalizes low-scoring dimensions. If one dimension scores very low, HTS will be significantly pulled down even if other dimensions are perfect. This isn't a bug — geometric mean better reflects true capability.

### Q2: What dependencies do I need?

**Zero dependencies for terminal mode.** `python-docx` is only needed for generating Word reports and is optional. `PyYAML` is not required — v4.0 uses pure regex to parse frontmatter.

### Q3: How do I improve my skill description score?

Ensure each SKILL.md includes:
1. ✅ Complete YAML frontmatter (name / description / version / author / license / metadata)
2. ✅ Usage section (how to use)
3. ✅ Parameters section (parameter descriptions)
4. ✅ Examples section (example code)
5. ✅ Dependencies section (dependency info)

### Q4: How do I get full marks for Cross-Profile protection?

Configure `cross_profile` in `~/.hermes/config.yaml` to ensure data isolation between different Profiles.

### Q5: Word report generation fails?

```bash
pip3 install python-docx lxml
```

Then rerun `python3 horse_test.py`.

### Q6: Garbled text in Windows cmd?

Colored terminal output may not display correctly in Windows Command Prompt. This does not affect the scoring functionality; text information is still readable. Consider using Windows Terminal or VS Code terminal.

### Q7: FileNotFoundError: pgrep?

Windows systems don't have the `pgrep` command. v4.0 has built-in cross-platform support and will automatically switch to `tasklist`. If problems persist, ensure you've updated to the latest version.

---

## 10. Project Structure

```
horse-test/
├── horse_test.py             # Scoring engine (main file, 685 lines)
├── test_horse_test.py        # Unit tests (15 tests)
├── SKILL.md                  # Hermes skill definition
├── DESCRIPTION.md            # Auto-detect description (very short, saves tokens)
├── CHANGELOG.md              # Version history
├── usage-notes.md            # User tuning notes
└── README.md                 # This file
```

### Core File `horse_test.py` Internal Structure

| Section | Lines | Content |
|---------|-------|---------|
| Header | 1-30 | import + constants |
| Configuration | 31-60 | DIMENSIONS / TIERS |
| Utilities | 61-155 | Cross-platform tools + text quality analysis |
| HTS Algorithm | 156-180 | Weighted geometric mean + rank mapping |
| History | 181-200 | JSON persistence |
| Scanner | 201-370 | 8 scan methods |
| Scorer | 371-470 | 6 scoring methods |
| Suggestions | 471-510 | Improvement suggestions |
| Report Output | 511-610 | Terminal + Word + JSON |
| Main Entry | 611-626 | main() |

---

## 11. Version History

| Version | Date | Highlights |
|---------|------|------------|
| v4.0.0 | 2026-06-30 | Current version. Pure stdlib, frontmatter quality analysis, cross-platform compatibility, unit tests |
| v3.0.0 | 2026-06-30 | Community contribution. Modular architecture, enhanced scoring objectivity |
| v2.0.0 | 2026-06-30 | Scanner fixes. Cron/jobs.json reading, PATH expansion |
| v1.0.0 | 2026-06-30 | Initial version. Six-dimension scoring + HTS + rank system |

---

## License

MIT License

*Auto-maintained by Hermes Agent*
