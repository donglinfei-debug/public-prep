---
name: public-prep
description: |
  项目公开预处理 — 安全扫描、代码改造、Clean Copy、模板生成、验证。
  当用户说"公开项目"、"准备公开仓库"、"发布到GitHub"、"安全检查后公开"时触发。
---

# /public-prep — 项目公开预处理工具

将本地项目一键"洗净打包"，安全地发布到 GitHub 公开仓库。

## 触发方式

| 方式 | 示例 |
|:-----|:------|
| 🌐 自然语言 | "帮我准备公开这个项目" / "把这个项目清洗一下放到 GitHub" |
| `/` 斜杠命令 | `/public-prep --project D:\projects\my-tool` |

## 使用场景

- 你有一个本地能跑的项目，想公开到 GitHub 但不确定是否安全
- 你有多个 side project，想逐步公开但不想每次手动重复 2-5 小时
- 你需要一个专业的 README/LICENCE/.gitignore 模板
- 你想确保 commit 历史中不泄露个人邮箱和隐私信息

## 工作模式

### 模式 1：完整流程（首次公开）
```bash
/public-prep --project D:\projects\my-tool
# → 预检 → 深度扫描 → 代码改造 → 模板生成 → Clean Copy → Git配置 → 验证
```

### 模式 2：仅验证（检查公开版是否安全）
```bash
/public-prep --verify D:\projects\my-tool_public
# → 全量扫描敏感信息 → 输出 ✅/❌ 检查清单
```

### 模式 3：自定义输出
```bash
/public-prep --project D:\projects\my-tool --output D:\github\my-tool --license MIT
```

## 参数说明

| 参数 | 简写 | 必填 | 说明 |
|:-----|:-----|:-----|:------|
| `--project` | `-p` | ✅ | 源项目路径（完整流程必填） |
| `--output` | `-o` | ❌ | 公开版输出路径（默认：`<项目名>_public`） |
| `--verify` | `-v` | ❌ | 仅验证模式（扫指定目录安全状态） |
| `--license` | `-l` | ❌ | 许可证类型：MIT / Apache-2.0 / GPL-3.0（默认 MIT） |
| `--readme-style` | `-r` | ❌ | README 风格：career（详细）/ share（简洁）（默认 career） |

## 工作流程

```
用户输入 /public-prep --project <路径>
         │
         ▼
┌─────────────────────┐
│ 1. 项目预检          │  自动检测项目类型、大小、Git 状态
│  (assessment)        │  输出：项目概况报告
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 2. 深度扫描          │  扫描 API Key / 密码 / Token / 路径 / 隐私
│  (scan)              │  输出：敏感信息清单（文件路径+行号）
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 3. 代码改造辅助      │  定位硬编码 → 给出环境变量替换建议
│  (refactor)          │  输出：需手动修改的清单 + 替换建议
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 4. 模板文件生成       │  自动创建 README / LICENSE / .gitignore / .env.example
│  (templates)         │  根据项目类型定制
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 5. Clean Copy 创建   │  创建干净副本 + 删除敏感文件/依赖目录
│  (clean-copy)        │  输出：副本路径
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 6. Git 初始化配置     │  git init + 设置公开身份（noreply 邮箱）+ 首次 commit
│  (git-setup)         │  输出：GitHub 新建仓库指引
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ 7. 最终验证          │  对公开版全量重扫描 → 输出 ✅/❌ 检查清单
│  (verify)            │  引导打开 GitHub → New repository → push
└─────────────────────┘
```

## 依赖

- **Python 3.8+**（核心逻辑仅依赖标准库，无需 pip install）
- **gitleaks**（可选）— 专业密钥扫描。安装：`winget install gitleaks` 或 `scoop install gitleaks`
  - 未安装时自动降级为正则扫描，不影响主流程

## 输出产物

```
项目_公开版/
├── README.md              ← 英文版项目说明
├── README.zh.md           ← 中文版项目说明
├── LICENSE                ← MIT 许可证
├── .gitignore             ← 按项目类型定制的忽略规则
├── .env.example           ← 环境变量模板（不含真实值）
├── requirements.txt       ← 依赖声明（Python项目）
└── src/                   ← 源码（已脱敏）
```

## 原理说明

public-prep 基于"Clean Copy 双仓库策略"——保留原私人仓库，创建独立的公开副本。所有清洗操作在副本上进行，原始仓库不受影响。

核心检测引擎采用**正则 + gitleaks 双重方案**：
- 正则可检测 7 大类 20+ 种敏感信息模式（API Key / 密码 / Token / 本地路径等）
- gitleaks（如已安装）提供更深层的 Git-aware 扫描
- 二者互补，覆盖单一工具的盲区
