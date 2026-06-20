# public-prep — 需求可追溯清单

> 源文档：`GitHub公开仓库预处理完整操作指南.md`
> 用途：逐条对照检查完成情况，确保无遗漏
> 使用方式：每完成一条，将 `[ ]` 改为 `[x]`

---

## 板块 A：核心策略

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| A-01 | 采用 Clean Copy 双仓库策略（保留旧仓库，创建独立公开副本） | 工具输出不含 .git 历史的干净副本，旧仓库不受影响 | [ ] |
| A-02 | 8 步工作流已全部实现（预检→扫描→改造→模板→Copy→Git→推送→维护） | main.py 包含 7 阶段流程编排 | [ ] |

---

## 板块 B：项目预检（Assessment）

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| B-01 | 自动检测项目类型（Python/Node.js/HTML/混合） | assessor.py 能返回项目类型字符串 | [ ] |
| B-02 | 自动统计项目大小（MB） | assessor.py 返回 size_mb | [ ] |
| B-03 | 自动检测是否 Git 仓库 + 远程地址 | assessor.py 返回 is_git + remote_url | [ ] |
| B-04 | 自动初筛敏感文件（.env, *.pem, *.key, config.json 等） | assessor.py 返回敏感文件列表 | [ ] |
| B-05 | 输出项目概况报告 | assessor.py 有 print_report() 方法 | [ ] |

---

## 板块 C：深度扫描

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| C-01 | 扫描 API Key 模式（sk-, ghp_, AKIA, Bearer） | 正则规则覆盖 5 种 API Key 模式 | [ ] |
| C-02 | 扫描密码字段（password, passwd, pwd） | 正则规则覆盖密码赋值模式 | [ ] |
| C-03 | 扫描本地路径（D:\, C:\Users\） | 正则规则覆盖 Windows/Unix 路径 | [ ] |
| C-04 | 扫描数据库连接串（mysql://, postgres:// 等含密码） | 正则规则覆盖 4 种数据库 URL 模式 | [ ] |
| C-05 | 扫描个人隐私（邮箱、内网 IP） | 正则规则覆盖邮箱和私有 IP | [ ] |
| C-06 | 扫描私钥/证书内容（-----BEGIN... PRIVATE KEY-----） | 正则覆盖 RSA/EC/OpenSSH 私钥 | [ ] |
| C-07 | 支持 gitleaks 自动扫描（可选增强） | scanner.py 检测 gitleaks 并调用 | [ ] |
| C-08 | 无 gitleaks 时降级为正则扫描 | scanner.py 自动检测并降级 | [ ] |
| C-09 | 扫描结果按风险分级（高/中/低） | scanner.py 有 get_high/medium/low_risk() | [ ] |
| C-10 | 输出逐行扫描报告（文件+行号+内容+风险） | scanner.py print_report() 格式完整 | [ ] |

---

## 板块 D：代码改造辅助

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| D-01 | 定位硬编码敏感信息 → 建议环境变量替换 | refactor_helper.py 生成替换建议 | [ ] |
| D-02 | 分类处理：第1类自动替换，第2/3类逐条确认 | refactor_helper.py 区分 category 1/2 | [ ] |
| D-03 | Python 代码替换模式（os.environ.get） | refactor_helper.py 正则匹配 Python 赋值 | [ ] |
| D-04 | Node.js 代码替换模式（process.env） | refactor_helper.py 正则匹配 JS 赋值 | [ ] |
| D-05 | 创建 .env.example（占位符，不含真实值） | template_generator.py 生成 .env.example | [ ] |
| D-06 | 启动脚本(.bat/.sh)检查和清理引导 | clean_copy.py check_bat_files() | [ ] |
| D-07 | 前端外部 CSS 变量解耦引导 | 扫描检查 CSS var(--) 引用 | [ ] |

---

## 板块 E：模板文件生成

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| E-01 | .gitignore 包含环境变量排除规则 | templates/gitignore/base.txt 含 .env 规则 | [ ] |
| E-02 | .gitignore 包含密钥/证书排除 | templates/gitignore/base.txt 含 *.pem/*.key | [ ] |
| E-03 | .gitignore 按项目类型补充（Python/Node.js） | templates/gitignore/python.txt + node.txt | [ ] |
| E-04 | LICENSE 文件（MIT，含年份和版权人占位符） | templates/LICENSE_MIT.txt 存在 | [ ] |
| E-05 | .env.example 模板（占位符描述，不含真实值） | templates/env_example.txt 存在且内容安全 | [ ] |
| E-05b | 项目根目录 .env.example 存在（仅对非工具类项目必选） | 项目根目录存在 .env.example 或说明不适用 | [ ] |
| E-06 | README 模板——详细版（求职版） | templates/readme/README_career.md 存在 | [ ] |
| E-07 | README 模板——简洁版（分享版） | templates/readme/README_share.md 存在 | [ ] |
| E-08 | README 中文模板支持 | template_generator.py bilingual 模式有兜底 | [ ] |

---

## 板块 F：Clean Copy

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| F-01 | 创建不含 .git 历史的干净副本 | clean_copy.py create_copy() 排除 .git | [ ] |
| F-02 | 排除 node_modules/venv/__pycache__/dist 等目录 | exclude_patterns.py 目录排除列表完整 | [ ] |
| F-03 | 删除 .env 及敏感文件 | clean_copy.py clean_sensitive_files() | [ ] |
| F-04 | 检查根目录是否有残留旧版本源码文件 | clean_copy.py 检查 root vs subdir 同名文件 | [ ] |
| F-05 | 检查启动脚本中的敏感信息 | clean_copy.py check_bat_files() | [ ] |
| F-06 | 输出 Clean Copy 报告 | clean_copy.py print_report() | [ ] |

---

## 板块 G：Git 配置

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| G-01 | 检查当前 Git 身份配置 | git_helper.py check_current_config() | [ ] |
| G-02 | 检测是否使用 GitHub noreply 邮箱 | git_helper.py is_noreply_email() | [ ] |
| G-03 | 支持设置公开仓库专用身份 | git_helper.py set_public_identity() | [ ] |
| G-04 | 身份隔离引导（公开/私人不同身份） | git_helper.py print_config_report() 提示 | [ ] |
| G-05 | git init + 首次 commit | git_helper.py init_repo() + create_initial_commit() | [ ] |
| G-06 | amend 修复已用私人邮箱提交的 commit | git_helper.py 有 amend 引导说明 | [ ] |

---

## 板块 H：品牌与国际化

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| H-01 | 提供中英双语 README（README.md + README.zh.md） | 项目根目录两个文件均存在 | [ ] |
| H-02 | README 内容含：痛点描述、核心亮点、快速开始、配置说明、项目结构 | README.md 覆盖所有板块 | [ ] |
| H-03 | README 内容含：系统架构/技术栈、测试、FAQ、Roadmap、联系方式 | README.md 覆盖所有板块 | [ ] |
| H-04 | 仓库 Topics 标签已设置（核心+功能+品牌） | GitHub API 返回 topics 非空 | [ ] |
| H-05 | 仓库 Description 已设置（一句话说明） | GitHub API 返回 description 非空 | [ ] |
| H-06 | 仓库命名规范：小写、连字符分隔、不超过 40 字符 | 仓库名 public-prep 符合 | [ ] |
| H-07 | README 首段自然包含核心关键词 | README.md 第一段含 "security sanitization" 等 | [ ] |
| H-08 | 截图素材管理流程有说明 | README 或 SKILL.md 提及截图工作流 | [ ] |

---

## 板块 I：最终验证（闸门③）

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| I-01 | .env 已从公开版中删除 | 核验脚本检查 .env 不存在 | [ ] |
| I-02 | .env.example 不含真实值 | 核验脚本检查 .env.example 内容安全 | [ ] |
| I-03 | .gitignore 存在且包含 .env 规则 | 核验脚本检查 .gitignore 内容 | [ ] |
| I-04 | LICENSE 文件存在 | 核验脚本检查 LICENSE 存在 | [ ] |
| I-05 | README.md 存在 | 核验脚本检查 README.md 存在 | [ ] |
| I-06 | README.zh.md 存在（与 H-01 同一条） | 核验脚本检查 README.zh.md 存在 | [ ] |
| I-07 | 无高风险 API Key 残留 | 扫描结果 high_risk_count == 0 | [ ] |
| I-08 | 无硬编码密码 | 扫描结果无 password 匹配 | [ ] |
| I-09 | 无本地路径泄露 | 扫描结果无路径匹配 | [ ] |
| I-10 | 安全验证结果汇总 → 通过/未通过 | 核验脚本输出总体结论 | [ ] |

---

## 板块 J：GitHub 发布

| ID | 要求 | 完成标准 | 状态 |
|:---|:-----|:---------|:----:|
| J-01 | 公开仓库已成功创建 | GitHub 仓库存在且可见性 public | [ ] |
| J-02 | 代码已推送至 main 分支 | git log 确认已推送 | [ ] |
| J-03 | Git 作者使用 GitHub noreply 邮箱 | git config user.email 含 users.noreply.github.com | [ ] |
| J-04 | Secret Scanning 已开启 | API 返回 secret_scanning.status == enabled | [ ] |
| J-05 | Push Protection 已开启 | API 返回 push_protection.status == enabled | [ ] |
| J-06 | 旧仓库完好无损（未被误删或修改） | 确认原项目存在 | [ ] |

---

## 使用说明

1. **执行前**：逐条阅读，确认理解每条要求
2. **执行中**：完成一条标记一条 `[x]`
3. **执行后**：运行配套核验脚本，自动对照此清单输出结果
4. **复盘**：如果发现清单本身有遗漏，补充到对应板块
