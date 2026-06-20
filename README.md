# public-prep

> **From "it works on my machine" to "ready to share with the world" — security sanitization, professional packaging, one command.**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

---

## 📌 Why public-prep?

You built something cool. It runs on your machine. Now you want to share it on GitHub.

But then doubt creeps in:

> *"Did I leave any API keys in the code?"*
> *"Is my `config.py` still hardcoding the database password?"*
> *"What if I accidentally commit `.env`?"*
> *"Will other people even know how to run this?"*
> *"Do I need a LICENSE? A .gitignore? How do I even start?"*

**public-prep** is your pre-flight checklist, automated. It scans, sanitizes, and packages your local project so you can publish it without second-guessing.

---

## 🎯 Who is this for?

| You are... | And you... |
|:-----------|:-----------|
| 🧑‍💻 A self-taught developer | Built your first real project, want to show it off |
| 🤖 AI-assisted coder | Used Claude/ChatGPT to build something, but unsure about the engineering side |
| 🔄 Side project creator | Have multiple projects you want to open-source gradually |
| 💼 Career-switcher | Need a polished GitHub profile for job applications |
| 📦 First-time open-sourcer | Have no idea what "safe to publish" even means |

If you can run `python main.py`, you can use public-prep.

---

## 🔥 What problems does it solve?

| # | Problem | What happens without it |
|:--|:--------|:------------------------|
| 1 | **API key leakage** | `sk-xxx`, `ghp_xxx`, database passwords hardcoded in source — bots scan public repos in minutes |
| 2 | **Local path exposure** | `D:\Users\YourName\Desktop\` in configs reveals your private directory structure |
| 3 | **Missing project packaging** | No README, no LICENSE, no `.gitignore` — the project looks abandoned |
| 4 | **Dependency chaos** | `node_modules` (3.6GB!) committed, or no `requirements.txt` — nobody can run it but you |
| 5 | **Cross-platform blindspot** | `.bat` scripts only work on Windows; Mac/Linux users are locked out |
| 6 | **No security habit** | Don't know what to check, or how to check — relying on luck |
| 7 | **Repetitive manual labor** | 2-5 hours per project, same boring checks every time |

---

## 🏗️ How it works — the 7-stage pipeline

```
  ┌─────────────┐
  │ ① Assessment │  Know your project — type, size, Git status
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ② Deep Scan  │  Find secrets: API keys, passwords, tokens, local paths
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ③ Refactor   │  Replace hardcoded secrets with environment variables
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ④ Templates  │  Generate README, LICENSE, .gitignore, .env.example
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ⑤ Clean Copy │  Create a safe copy — no .git, no secrets, no junk
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ⑥ Git Setup  │  Configure public identity, init repo, first commit
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │ ⑦ Verify     │  Final full scan → pass/fail checklist → ready to push
  └─────────────┘
```

### Stage details

| Stage | What it does | What you get |
|:------|:-------------|:-------------|
| **① Assessment** | Auto-detect project type (Python / Node.js / HTML / Mixed), measure size, check Git status, scan for suspicious files | A project overview report — know what you're dealing with |
| **② Deep Scan** | Regex + gitleaks dual-engine scan for API keys, passwords, tokens, local paths, private info | A line-by-line risk report — nothing slips through |
| **③ Refactor Helper** | Locate hardcoded secrets → suggest environment-variable replacements. Batch mode: auto-fix clear patterns, confirm ambiguous ones | Precise fixes, no false positives |
| **④ Template Generator** | Auto-generate `.gitignore` (typed), `LICENSE` (MIT), `README.md` (bilingual), `.env.example` (extracted from your code) | Open-source essentials, ready in seconds |
| **⑤ Clean Copy** | Create a `.git`-free clean copy, strip sensitive files/dependency dirs/cache, check for stale root-level files | Original repo untouched, public copy zero-risk |
| **⑥ Git Setup** | Detect current Git identity → guide to set GitHub noreply email → `git init` + first commit | No personal email in commit history |
| **⑦ Verify** | Re-scan everything → output ✅/❌ checklist → guide you to create the GitHub repo | Last gate before publish — push with confidence |

---

## 🚀 Quick Start

```bash
# 1. Clone or download public-prep
git clone https://github.com/donglinfei-debug/public-prep.git
cd public-prep

# 2. Point it at your project
python main.py --project /path/to/your/project

# 3. Follow the interactive guide
```

### Command-line options

| Option | Short | Description |
|:-------|:------|:------------|
| `--project` | `-p` | Path to your local project (required for full workflow) |
| `--output` | `-o` | Output directory for the public copy (default: `<project>_public`) |
| `--verify` | `-v` | Verification-only mode — scan a directory for secrets |
| `--license` | `-l` | License type: `MIT` (default), `Apache-2.0`, `GPL-3.0` |
| `--readme-style` | `-r` | README style: `career` (detailed) or `share` (concise) |
| `--help` | `-h` | Show full help |

### Examples

```bash
# Full workflow — assess, scan, refactor, template, copy, verify
python main.py --project ~/projects/my-tool

# Quick verification — just scan for secrets
python main.py --verify ~/projects/my-tool_public

# Custom output location
python main.py --project ~/projects/my-tool --output ~/github/my-tool
```

---

## 🧩 Output Structure

After running, your `public-release/` directory looks like:

```
D:\claude-workspace\
├── 15-subtitle-tool\           ← Your original project (untouched)
│
└── public-release\             ← All public copies live here
    ├── _REPO_MAPPING.md        ← Mapping: original ↔ public ↔ GitHub
    └── subtitle-tool\          ← Clean public copy, ready to push
        ├── README.md
        ├── LICENSE
        ├── .gitignore
        ├── .env.example
        └── src/
```

---

## 📦 Requirements

- **Python 3.8+** (no third-party packages required)
- **gitleaks** (optional, recommended) — install via `winget install gitleaks` or `scoop install gitleaks`

---

## 🔒 Security Philosophy

public-prep follows a **defense-in-depth** approach:

1. **Dual-engine scanning** — regex patterns catch known formats, gitleaks catches everything else
2. **No auto-push** — the tool never pushes to GitHub for you; you always review the final result
3. **Original repo untouched** — all transformations happen on a clean copy
4. **Batched confirmation** — ambiguous findings are presented for your review, not blindly fixed

Security isn't a one-time task — it's a habit. public-prep makes that habit easy to repeat.

---

## 🤝 Contributing

Issues and PRs welcome! See the [open issues](https://github.com/donglinfei-debug/public-prep/issues) for roadmap items.

---

## 📄 License

[MIT](LICENSE) © 2026 [Ryan Dong](https://github.com/donglinfei-debug)

---

## 📬 Contact

- **Email**: donglinfei@gmail.com
- **GitHub**: [@donglinfei-debug](https://github.com/donglinfei-debug)

---

*Built with ❤️ for developers who want to share their work without anxiety.*

---

> 如果你 fork 此项目，请将 `donglinfei-debug` 替换为你自己的 GitHub 用户名。
