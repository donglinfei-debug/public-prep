<div align="center">

# 🔧 public-prep

**From "it works on my machine" to "ready to share with the world" — security sanitization, professional packaging, one command.**

[![GitHub Stars](https://img.shields.io/github/stars/donglinfei-debug/public-prep?style=flat-square&logo=github)](https://github.com/donglinfei-debug/public-prep/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/donglinfei-debug/public-prep?style=flat-square&logo=github)](https://github.com/donglinfei-debug/public-prep/issues)
[![GitHub Forks](https://img.shields.io/github/forks/donglinfei-debug/public-prep?style=flat-square&logo=github)](https://github.com/donglinfei-debug/public-prep/forks)
[![License](https://img.shields.io/github/license/donglinfei-debug/public-prep?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=flat-square)]()

🌏 **Language / 语言**：[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)

</div>

---

Your pre-flight checklist before publishing a project to GitHub, **automated**. Scans for secrets, removes local paths, generates `.env.example`/`.gitignore`/`LICENSE`/`README`, and creates a clean copy ready to push.


## 📌 Why This?

You built something cool. It runs on your machine. Now you want to share it on GitHub.

But then doubt creeps in:

> *"Did I leave any API keys in the code?"*
> *"Is my config.py still hardcoding the database password?"*
> *"What if I accidentally commit .env?"*
> *"Will other people even know how to run this?"*
> *"Do I need a LICENSE? A .gitignore? How do I even start?"*

**public-prep** is your automated pre-flight checklist. It scans for secrets, removes local paths, generates the missing files (.env.example, .gitignore, LICENSE, README), and creates a clean copy ready to push — so you can publish with confidence, not doubt.

## 🏗️ Architecture

```mermaid
flowchart TB
    subgraph Input["📥 Input"]
        PROJ[Local Project Directory]
    end

    subgraph Pipeline["⚙️ Pipeline (main.py)"]
        SCN[scanner.py<br/>Secret Scan · Path Leak · Gitleaks]
        ASS[assessor.py<br/>Risk Assessment · Report Generation]
        TPL[template_generator.py<br/>.env.example · .gitignore · LICENSE · README]
        RFA[refactor_helper.py<br/>Hardcoded Secrets → Env Vars]
        CCP[clean_copy.py<br/>Exclude · Copy · Sanitize]
        GIT[git_helper.py<br/>Git Init · Config · Commit]
        VRF[verifier.py<br/>Final Check · Validation]
    end

    subgraph Output["📦 Output"]
        PUB[Clean Public Copy → GitHub]
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

## ✨ Features

- **🔍 Secret Scanner** — API keys, tokens, passwords, database connection strings
- **📁 Path Leak Detection** — Finds local paths (D:\, C:\Users\) in code
- **🔧 Auto Refactor** — Replaces hardcoded secrets with `os.environ.get()` suggestions
- **📝 Template Generator** — `.env.example`, `.gitignore`, MIT `LICENSE`, `README`
- **🧹 Clean Copy** — Excludes sensitive/temp files, creates a release-ready directory
- **✅ Final Verifier** — Re-scans the clean copy before you publish

## 📦 Requirements

| Requirement | Version |
|:------------|:--------|
| **Python** | 3.8+ |
| **OS** | Windows / macOS / Linux |

## 🚀 Quick Start

```bash
# Scan a project
python main.py --project D:\projects\my-tool

# Full pipeline: scan → refactor → generate → copy → verify
python main.py --project D:\projects\my-tool --output D:\github\my-tool
```

## 📁 Structure

```
public-prep/
├── main.py                    # CLI entry point
├── modules/
│   ├── scanner.py             # Secret & path leak detection
│   ├── assessor.py            # Risk assessment
│   ├── refactor_helper.py     # Hardcoded → env var conversion
│   ├── template_generator.py  # .env / .gitignore / LICENSE / README
│   ├── clean_copy.py          # Filtered project copy
│   ├── git_helper.py          # Git init & commit
│   └── verifier.py            # Final validation
├── rules/
│   ├── scan_rules.py          # Scan pattern definitions
│   └── exclude_patterns.py    # Exclusion rules
├── templates/
│   ├── LICENSE_MIT.txt
│   ├── env_example.txt
│   └── gitignore/ / readme/
├── README.md / README.zh.md
└── REQUIREMENTS_CHECKLIST.md
```



## ❓ FAQ

**What kinds of secrets can it detect?**
API keys (sk-*, AKIA*), GitHub tokens (ghp_*), database connection strings, private keys, passwords, and custom patterns you define in scan_rules.py.

**Does it modify my source code?**
It detects issues and suggests fixes, but it only creates a clean copy — your original project is never modified.

**Can I add custom scan rules?**
Yes. Add patterns to rules/scan_rules.py. The scanner uses regex-based matching, so any pattern you can express as a regex can be added.

**Does this run on macOS/Linux?**
Yes. Python 3.8+ cross-platform. The CLI works on Windows, macOS, and Linux.

## 📄 License

MIT © 2026 Ryan Dong

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=donglinfei-debug/public-prep&type=Date)](https://star-history.com/#donglinfei-debug/public-prep&Date)



## 👤 About the Author

**Ryan Dong** — AI Product Manager & Full-Stack Developer

I bridge the gap between AI capabilities and production-ready software. My work spans the full stack: from designing AI-powered product features and integrating LLM APIs, to building modular backend services and shipping clean, documented code.

| Role | Focus |
|:-----|:------|
| 🧠 **AI Product Manager** | Product strategy, AI feature design, prompt engineering, model selection |
| 💻 **Full-Stack Developer** | Python, FastAPI, Google Apps Script, automation pipelines, API integration |

This repository is part of a personal toolbox — a growing collection of practical, reusable modules that solve real automation problems. Each project is designed to be independently useful and easily integrated into larger systems.

📬 **donglinfei@gmail.com** — open to business discussions, collaborations, and recruiting inquiries.

## 📬 Contact

Ryan Dong — donglinfei@gmail.com
