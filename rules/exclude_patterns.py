"""
public-prep — 扫描排除规则

定义哪些目录/文件在扫描和 Clean Copy 时应该被排除。
"""

# ===== 目录排除 =====
# 这些目录在扫描和复制时都会被跳过
EXCLUDE_DIRS = [
    # 版本控制
    ".git",
    ".svn",
    ".hg",
    # 依赖目录
    "node_modules",
    ".venv",
    "venv",
    "env",
    "virtualenv",
    "vendor",
    # Python 缓存
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".hypothesis",
    # 构建输出
    "dist",
    "build",
    ".next",
    "out",
    ".nuxt",
    "target",  # Rust
    "bin",  # Go
    "obj",  # .NET
    # IDE
    ".vscode",
    ".idea",
    ".vs",
    # 其他
    ".git",
    ".terraform",
    ".serverless",
    "coverage",
    ".coverage",
]

# ===== 文件排除 =====
# 这些文件/文件类型在扫描和复制时会被跳过
EXCLUDE_FILES = [
    # 缓存/编译文件
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.o",
    "*.obj",
    "*.class",
    "*.so",
    "*.dll",
    "*.dylib",
    # 日志
    "*.log",
    # 压缩包
    "*.zip",
    "*.tar.gz",
    "*.tar",
    "*.rar",
    "*.7z",
    # 可执行文件
    "*.exe",
    "*.msi",
    "*.dmg",
    "*.app",
    # 图片（通常不含文本敏感信息）
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.ico",
    "*.svg",
    "*.webp",
    # 字体
    "*.ttf",
    "*.otf",
    "*.woff",
    "*.woff2",
    # 媒体
    "*.mp3",
    "*.mp4",
    "*.wav",
    "*.avi",
    "*.mov",
    "*.mkv",
    # 数据库
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    # IDE/OS 元数据
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    "*.swp",
    "*.swo",
    "*~",
]

# ===== 敏感文件清单 =====
# 这些文件在 Clean Copy 阶段需要被特别检查和删除
SENSITIVE_FILES = [
    # 环境变量
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    ".env.staging",
    # 密钥文件
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "*.jks",
    "*.cer",
    "*.crt",
    "*.der",
    # 凭证文件
    "credentials.json",
    "client_secret.json",
    "client_secret*.json",
    "service_account.json",
    "oauth*.json",
    # Token 文件
    "*token*",
    "*secret*",
    "*password*",
    # 配置文件（可能含敏感信息）
    "config.json",
    "config.yaml",
    "config.yml",
    # SSH
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    # GPG
    "*.gpg",
    "*.asc",
]

# ===== 扫描文件类型 =====
# 只扫描这些类型的文件（文本源码）
SCAN_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".less",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".ini",
    ".cfg",
    ".conf",
    ".env.example",
    ".java",
    ".go",
    ".rb",
    ".php",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".rs",
    ".swift",
    ".kt",
    ".scala",
    ".sh",
    ".bash",
    ".zsh",
    ".bat",
    ".cmd",
    ".ps1",
    ".psm1",
    ".sql",
    ".md",
    ".rst",
    ".txt",
    ".toml",
    ".tf",
    ".dockerfile",
    ".Dockerfile",
    "Makefile",
    "makefile",
    "GNUmakefile",
    ".env.example",
]
