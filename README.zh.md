<div align="center">

# 🔧 public-prep

**把"本地能跑"变成"可以安心公开"——安全清洗、专业包装、一键就绪。**

[![GitHub Stars](https://img.shields.io/github/stars/donglinfei-debug/public-prep?style=flat-square&logo=github)](https://github.com/donglinfei-debug/public-prep/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/donglinfei-debug/public-prep?style=flat-square&logo=github)](https://github.com/donglinfei-debug/public-prep/issues)
[![GitHub Forks](https://img.shields.io/github/forks/donglinfei-debug/public-prep?style=flat-square&logo=github)](https://github.com/donglinfei-debug/public-prep/forks)
[![License](https://img.shields.io/github/license/donglinfei-debug/public-prep?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat-square)]()

🌏 **语言 / Language**：[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)

</div>

---

项目公开前的一站式预处理工具。自动扫描密钥泄露、清理本地路径、生成 `.env.example` / `.gitignore` / LICENSE / README，创建干净的发布副本。

## 🏗️ 架构示意

```mermaid
flowchart TB
    subgraph Input["📥 输入"]
        PROJ[本地项目目录]
    end

    subgraph Pipeline["⚙️ 处理管线 (main.py)"]
        SCN[scanner.py<br/>密钥扫描 · 路径泄露 · Gitleaks]
        ASS[assessor.py<br/>风险评估 · 报告生成]
        TPL[template_generator.py<br/>.env.example · .gitignore · LICENSE · README]
        RFA[refactor_helper.py<br/>硬编码密钥 → 环境变量]
        CCP[clean_copy.py<br/>排除 · 复制 · 清洗]
        GIT[git_helper.py<br/>Git 初始化 · 配置 · 提交]
        VRF[verifier.py<br/>最终校验]
    end

    subgraph Output["📦 输出"]
        PUB[干净副本 → GitHub]
    end

    PROJ --> SCN --> ASS
    ASS --> RFA --> TPL
    TPL --> CCP --> GIT --> VRF
    VRF --> PUB

    style PROJ fill:#6366f1,color:#fff,stroke:none
    style SCN fill:#0ea5e9,color:#fff,stroke:none
    style ASS fill:#0ea5e9,color:#fff,stroke:none
    style TPL fill:#0ea5e9,color:#fff,stroke:none
    style RFA fill:#0ea5e9,color:#fff,stroke:none
    style CCP fill:#0ea5e9,color:#fff,stroke:none
    style GIT fill:#0ea5e9,color:#fff,stroke:none
    style VRF fill:#0ea5e9,color:#fff,stroke:none
    style PUB fill:#10b981,color:#fff,stroke:none
```

## ✨ 功能特性

- **🔍 密钥扫描** — API Key、Token、密码、数据库连接串
- **📁 路径泄露检测** — 发现代码中的本地路径（D:\、C:\Users\）
- **🔧 自动重构** — 硬编码密钥替换为 `os.environ.get()` 建议
- **📝 模板生成** — `.env.example`、`.gitignore`、MIT License、README
- **🧹 干净拷贝** — 排除敏感/临时文件，生成可发布的目录
- **✅ 最终验证** — 重新扫描发布副本，确保安全

## 📦 系统要求

| 要求 | 版本 |
|:-----|:------|
| **Python** | 3.8+ |
| **操作系统** | Windows / macOS / Linux |

## 🚀 快速开始

```bash
# 扫描项目
python main.py --project D:\projects\my-tool

# 全流程：扫描 → 重构 → 生成 → 拷贝 → 验证
python main.py --project D:\projects\my-tool --output D:\github\my-tool
```

## 📁 文件结构

```
public-prep/
├── main.py                    # CLI 入口
├── modules/
│   ├── scanner.py             # 密钥与路径泄露检测
│   ├── assessor.py            # 风险评估
│   ├── refactor_helper.py     # 硬编码 → 环境变量
│   ├── template_generator.py  # 模板生成
│   ├── clean_copy.py          # 过滤拷贝
│   ├── git_helper.py          # Git 初始化和提交
│   └── verifier.py            # 最终验证
├── rules/
├── templates/
├── README.md / README.zh.md
└── REQUIREMENTS_CHECKLIST.md
```

## 📄 许可证

MIT © 2026 Ryan Dong

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=donglinfei-debug/public-prep&type=Date)](https://star-history.com/#donglinfei-debug/public-prep&Date)

## 📬 联系方式

Ryan Dong — donglinfei@gmail.com
