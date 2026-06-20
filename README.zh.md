# public-prep

> **把"本地能跑"变成"可以安心公开"——安全清洗、专业包装、一键就绪。**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

---

## 📌 为什么需要 public-prep？

你写了一个很酷的项目，在本地跑通了。想把它分享到 GitHub 上。

但心里开始打鼓：

> *"代码里有没有忘了删的 API Key？"*
> *"`config.py` 还硬编码着数据库密码吗？"*
> *"万一不小心把 `.env` 提交了怎么办？"*
> *"别人下载后知道怎么跑起来吗？"*
> *"需要 LICENSE 吗？.gitignore 怎么写？从哪里开始？"*

**public-prep** 就是你公开前的"安检仪"。自动扫描、清洗、打包你的本地项目，让你能放心发布。

---

## 🎯 适用人群

| 你是... | 你的处境... |
|:--------|:------------|
| 🧑‍💻 自学编程的开发者 | 做出了第一个像样的项目，想展示给别人看 |
| 🤖 AI 辅助编程 | 用 Claude/ChatGPT 写了个东西，但工程化方面拿不准 |
| 🔄 Side project 爱好者 | 有好几个项目想逐步开源 |
| 💼 转行者 / 求职者 | 需要一个拿得出手的 GitHub 主页 |
| 📦 第一次开源 | 完全不知道"安全公开"意味着什么 |

只要能跑 `python main.py`，就能用 public-prep。

---

## 🔥 解决了哪些问题？

| # | 问题 | 没有它的后果 |
|:--|:-----|:------------|
| 1 | **API Key 泄露** | `sk-xxx`、`ghp_xxx`、数据库密码硬编码在代码里——公开后几分钟就会被爬虫扫到 |
| 2 | **本地路径暴露** | `D:\Users\你的名字\Desktop\` 等路径泄露了你的隐私目录结构 |
| 3 | **项目包装缺失** | 没有 README、LICENSE、`.gitignore`——项目看起来像被遗弃的 |
| 4 | **依赖管理混乱** | 把 `node_modules`（3.6GB！）提交了，或者根本没有 `requirements.txt`——别人根本跑不起来 |
| 5 | **跨平台盲区** | `.bat` 脚本只有 Windows 能用，Mac/Linux 用户直接被挡在门外 |
| 6 | **没有安全习惯** | 不知道要检查什么、怎么检查——全靠运气 |
| 7 | **重复劳动** | 每个项目要公开都得折腾 2-5 小时，同样的检查反复做 |

---

## 🏗️ 工作流程——7 阶段管线

```
  ┌─────────────┐
  │ ① 项目预检   │  了解你的项目——类型、大小、Git 状态
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ② 深度扫描   │  查找 API Key、密码、Token、本地路径
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ③ 代码改造   │  把硬编码敏感信息替换为环境变量
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ④ 生成模板   │  自动创建 README、LICENSE、.gitignore、.env.example
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ⑤ Clean Copy│  创建干净的副本——无 .git、无密钥、无垃圾
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ⑥ Git 配置   │  配置公开身份、初始化仓库、首次提交
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ⑦ 最终验证   │  全量扫描 → 通过/不通过清单 → 准备推送
  └─────────────┘
```

### 各阶段详情

| 阶段 | 做什么 | 得到什么 |
|:-----|:-------|:---------|
| **① 项目预检** | 自动检测项目类型（Python/Node.js/HTML/混合）、大小、Git 状态、敏感文件初筛 | 项目概况报告——心里有数 |
| **② 深度扫描** | 正则 + gitleaks 双重引擎扫描 API Key、密码、Token、本地路径、隐私信息 | 逐行风险报告——无一遗漏 |
| **③ 代码改造辅助** | 定位硬编码密钥 → 给出环境变量替换建议。第1类自动替换，第2/3类逐条确认 | 精准改造，不误伤 |
| **④ 模板文件生成** | 自动生成 `.gitignore`（按项目类型）、`LICENSE`(MIT)、`README.md`（中英双语）、`.env.example`（从代码自动提取环境变量） | 开源三件套一步到位 |
| **⑤ Clean Copy** | 创建不含 Git 历史的干净副本，排除敏感文件/依赖目录/缓存，清理根目录残留 | 原仓库完好，公开版零风险 |
| **⑥ Git 配置** | 检测当前 Git 身份 → 引导设置 GitHub noreply 邮箱 → `git init` + 首次提交 | commit 历史不泄露个人邮箱 |
| **⑦ 最终验证** | 全量重扫 → 输出 ✅/❌ 检查清单 → 引导创建 GitHub 仓库 | 推送前最后一道闸门 |

---

## 🚀 快速开始

```bash
# 1. 克隆或下载 public-prep
git clone https://github.com/donglinfei-debug/public-prep.git
cd public-prep

# 2. 指向你的项目
python main.py --project /path/to/your/project

# 3. 按照交互引导操作
```

### 命令行参数

| 参数 | 简写 | 说明 |
|:-----|:-----|:------|
| `--project` | `-p` | 你的本地项目路径（完整流程必填） |
| `--output` | `-o` | 公开版输出目录（默认: `<项目名>_public`） |
| `--verify` | `-v` | 仅验证模式——扫描指定目录的安全性 |
| `--license` | `-l` | 许可证类型: `MIT`（默认）、`Apache-2.0`、`GPL-3.0` |
| `--readme-style` | `-r` | README 风格: `career`（详细）或 `share`（简洁） |
| `--help` | `-h` | 显示完整帮助 |

### 使用示例

```bash
# 完整流程——预检、扫描、改造、模板、复制、验证
python main.py --project ~/projects/my-tool

# 快速验证——仅扫描密钥
python main.py --verify ~/projects/my-tool_public

# 自定义输出位置
python main.py --project ~/projects/my-tool --output ~/github/my-tool
```

---

## 🧩 输出结构

运行完成后，你的 `public-release/` 目录结构如下：

```
D:\claude-workspace\
├── 15-subtitle-tool\            ← 原项目（完好无损）
│
└── public-release\              ← 所有公开版集中存放
    ├── _REPO_MAPPING.md         ← 映射关系：原项目 ↔ 公开版 ↔ GitHub
    └── subtitle-tool\           ← 干净的公开版，准备推送
        ├── README.md
        ├── README.zh.md
        ├── LICENSE
        ├── .gitignore
        ├── .env.example
        └── src/
```

---

## 📦 环境要求

- **Python 3.8+**（仅依赖标准库，无需第三方包）
- **gitleaks**（可选，推荐）— 安装：`winget install gitleaks` 或 `scoop install gitleaks`

---

## 🔒 安全理念

public-prep 采用**纵深防御**策略：

1. **双引擎扫描** — 正则覆盖已知格式，gitleaks 兜底其余
2. **不自动推送** — 工具从不自动推送到 GitHub，最终决定权在你
3. **原仓库不动** — 所有变换都在副本上进行
4. **分批确认** — 有歧义的发现会列出清单让你逐条确认，不会盲目替换

安全不是一次性工作，而是习惯。public-prep 让这个习惯变得容易坚持。

---

## 🔍 需求可追溯清单

本项目附带一份 `REQUIREMENTS_CHECKLIST.md`，将源操作指南文档逐条提取为可验证的清单。

**使用方式：**
- 执行前：读取清单，理解所有要求
- 执行中：逐条完成，逐条标记
- 执行后：用清单对照验证，确保无遗漏

这不仅是一个检查工具，更是一个**质量保证机制**——确保从"源文档要求"到"最终交付物"之间不走样。

---

## 🤝 贡献指南

欢迎提交 Issue 和 PR。

---

## 📄 许可证

[MIT](LICENSE) © 2026 [Ryan Dong](https://github.com/donglinfei-debug)

---

## 📬 联系方式

- **Email**: donglinfei@gmail.com（商务/招聘）
- **GitHub**: [@donglinfei-debug](https://github.com/donglinfei-debug)

---

*为那些想安心分享自己作品的人而构建。*
