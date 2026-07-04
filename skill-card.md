# 🐎 养马测试 — 技能卡片

**Hermes Agent 调教评分引擎**

| 属性 | 值 |
|------|-----|
| 版本 | v4.0.0 |
| 类型 | 诊断/评估 |
| 依赖 | 纯 Python 标准库 |
| 平台 | macOS / Windows / Linux |

## 触发方式

对话中说 **养马测试** 或 **horse-test**

## 六维评分

| 维度 | 权重 |
|------|------|
| 🧠 技能体系 | 25% |
| ⚙️ 配置调优 | 15% |
| 📝 Prompt工程 | 15% |
| 🔌 工具生态 | 20% |
| 📊 运营水平 | 10% |
| 🛡️ 安全隐私 | 15% |

## CLI 命令

```bash
python3 horse_test.py            # 完整报告
python3 horse_test.py --quiet    # 一行结果
python3 horse_test.py --json     # JSON 输出
python3 horse_test.py --no-word  # 跳过 Word
python3 horse_test.py --hermes-home /path/to/agent  # 自定义路径
```

## 段位体系

🥚 马蛋(0) → 🐴 小马(200) → 🏃 快马(350) → 🦄 千里马(500) → 🐉 龙马(650) → 👑 马神(800)
