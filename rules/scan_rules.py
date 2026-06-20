"""
public-prep — 敏感信息检测规则库

每条规则定义：
  - name: 规则名称
  - pattern: 正则表达式
  - risk: 风险等级 (high / medium / low)
  - context_required: 是否需要上下文判断（True=需人工确认，False=可自动处理）
  - description: 说明
  - exclude_ext: 排除的文件扩展名
  - exclude_patterns: 排除的文件路径模式
"""

SCAN_RULES = [
    # ===== 极高风险 =====
    {
        "name": "OpenAI API Key",
        "pattern": r"sk-[a-zA-Z0-9_-]{20,}",
        "risk": "high",
        "context_required": False,
        "description": "OpenAI / 各类 AI API 密钥前缀",
        "exclude_ext": [],
        "exclude_patterns": [".env.example", "README.md", "SKILL.md"],
    },
    {
        "name": "GitHub Token",
        "pattern": r"ghp_[a-zA-Z0-9]{20,}|gho_[a-zA-Z0-9]{20,}|ghu_[a-zA-Z0-9]{20,}|ghs_[a-zA-Z0-9]{20,}",
        "risk": "high",
        "context_required": False,
        "description": "GitHub Personal Access Token",
        "exclude_ext": [],
        "exclude_patterns": [".env.example", "README.md"],
    },
    {
        "name": "AWS Access Key",
        "pattern": r"AKIA[0-9A-Z]{16}",
        "risk": "high",
        "context_required": False,
        "description": "AWS Access Key ID",
        "exclude_ext": [],
        "exclude_patterns": [".env.example"],
    },
    {
        "name": "Database URL with Password",
        "pattern": r"(mysql|postgres|mongodb|redis)://[^:]+:[^@]+@",
        "risk": "high",
        "context_required": False,
        "description": "数据库连接串（含密码）",
        "exclude_ext": [],
        "exclude_patterns": [".env.example", "README.md"],
    },
    {
        "name": "Bearer Token in Code",
        "pattern": r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}",
        "risk": "high",
        "context_required": True,
        "description": "Bearer 认证令牌（可能是示例或真实值）",
        "exclude_ext": [],
        "exclude_patterns": [".env.example"],
    },
    # ===== 中风险 =====
    {
        "name": "Hardcoded Password",
        "pattern": r"(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]+['\"]",
        "risk": "medium",
        "context_required": True,
        "description": "硬编码密码字段（可能是默认值或真实密码）",
        "exclude_ext": [],
        "exclude_patterns": [".env.example", "package.json", "requirements.txt"],
    },
    {
        "name": "Local Windows Path",
        "pattern": r"[A-Z]:\\[A-Za-z0-9_\-\.\\]+",
        "risk": "medium",
        "context_required": True,
        "description": "Windows 本地绝对路径",
        "exclude_ext": [".png", ".jpg", ".gif", ".ico", ".pyc"],
        "exclude_patterns": [".gitignore", "*.log"],
    },
    {
        "name": "Local Unix Path",
        "pattern": r"/(home|Users|tmp|var|etc)/[a-zA-Z0-9_\-]+",
        "risk": "medium",
        "context_required": True,
        "description": "Unix/Linux 本地绝对路径",
        "exclude_ext": [".png", ".jpg", ".gif"],
        "exclude_patterns": [],
    },
    {
        "name": "Private Email Address",
        "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "risk": "medium",
        "context_required": True,
        "description": "邮箱地址（可能是联系人信息或隐私泄露）",
        "exclude_ext": [],
        "exclude_patterns": [".env.example", "package.json", "README.md"],
    },
    {
        "name": "Private IP Address",
        "pattern": r"(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})",
        "risk": "medium",
        "context_required": True,
        "description": "内网 IP 地址",
        "exclude_ext": [],
        "exclude_patterns": [],
    },
    {
        "name": "Secret Key / Private Key",
        "pattern": r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
        "risk": "high",
        "context_required": False,
        "description": "私钥文件内容",
        "exclude_ext": [],
        "exclude_patterns": [],
    },
    {
        "name": "JWT Token",
        "pattern": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "risk": "high",
        "context_required": True,
        "description": "JWT Token（可能是真实或示例）",
        "exclude_ext": [],
        "exclude_patterns": [".env.example"],
    },
    {
        "name": "Slack Token",
        "pattern": r"xox[baprs]-[a-zA-Z0-9-]{10,}",
        "risk": "high",
        "context_required": False,
        "description": "Slack API Token",
        "exclude_ext": [],
        "exclude_patterns": [],
    },
    {
        "name": "Google OAuth / Service Account",
        "pattern": r"\"client_secret\":\s*\"[a-zA-Z0-9_-]+\"",
        "risk": "high",
        "context_required": False,
        "description": "Google OAuth 客户端密钥",
        "exclude_ext": [],
        "exclude_patterns": [],
    },
    {
        "name": "SSH Private Key",
        "pattern": r"-----BEGIN OPENSSH PRIVATE KEY-----",
        "risk": "high",
        "context_required": False,
        "description": "OpenSSH 私钥",
        "exclude_ext": [],
        "exclude_patterns": [],
    },
    {
        "name": "Alibaba Cloud AccessKey",
        "pattern": r"LTAI[a-zA-Z0-9]{12,}",
        "risk": "high",
        "context_required": False,
        "description": "阿里云 AccessKey ID",
        "exclude_ext": [],
        "exclude_patterns": [".env.example"],
    },
    {
        "name": "Tencent Cloud SecretId",
        "pattern": r"AKID[a-zA-Z0-9]{10,}",
        "risk": "high",
        "context_required": False,
        "description": "腾讯云 SecretId",
        "exclude_ext": [],
        "exclude_patterns": [".env.example"],
    },
    # ===== 低风险 =====
    {
        "name": "Debug Print Statement",
        "pattern": r"(^|[^#\"'])print\s*\(|console\.log\s*\(",
        "risk": "low",
        "context_required": True,
        "description": "调试输出语句（建议清理）",
        "exclude_ext": [],
        "exclude_patterns": ["*.pyc", "node_modules/"],
    },
    {
        "name": "TODO / FIXME / HACK",
        "pattern": r"(TODO|FIXME|HACK|XXX|WORKAROUND)[:\s]",
        "risk": "low",
        "context_required": True,
        "description": "未完成的待办事项",
        "exclude_ext": [".pyc", ".o", ".exe"],
        "exclude_patterns": [],
    },
]


def get_rules_by_risk(risk_level=None):
    """按风险等级获取规则"""
    if risk_level is None:
        return SCAN_RULES
    return [r for r in SCAN_RULES if r["risk"] == risk_level]


def get_auto_fix_rules():
    """获取可自动修复的规则（context_required=False）"""
    return [r for r in SCAN_RULES if not r["context_required"]]


def get_manual_review_rules():
    """获取需要人工确认的规则（context_required=True）"""
    return [r for r in SCAN_RULES if r["context_required"]]


def get_risk_label(risk_level):
    """获取风险等级的显示标签"""
    labels = {
        "high": "[HIGH]",
        "medium": "[MED]",
        "low": "[LOW]",
    }
    return labels.get(risk_level, risk_level)
