"""
public-prep — 代码改造辅助模块

定位硬编码敏感信息，给出环境变量替换建议。
分类处理：
  第1类（明确密钥模式）→ 自动替换
  第2/3类（文件级/歧义项）→ 列清单逐条确认
"""

import re
from pathlib import Path


class RefactorSuggestion:
    """单条改造建议"""

    def __init__(self, file_path, line_number, original, suggestion, rule_name, category):
        self.file_path = file_path
        self.line_number = line_number
        self.original = original.strip()
        self.suggestion = suggestion
        self.rule_name = rule_name
        self.category = category  # 1: 自动, 2: 需确认, 3: 文件级

    def __repr__(self):
        return f"[类别{self.category}] {self.file_path}:{self.line_number}"


class RefactorHelper:
    """代码改造辅助"""

    def __init__(self, scanner_results, env_var_names=None):
        """
        Args:
            scanner_results: Scanner 的扫描结果列表
            env_var_names: 已有环境变量名列表（用于避免冲突）
        """
        self.scanner_results = scanner_results
        self.env_var_names = env_var_names or []
        self.suggestions = []

    def _generate_env_var_name(self, original_line, rule_name):
        """根据原始内容生成环境变量名"""
        # 提取常见的变量名模式
        patterns = [
            r"(?:api_key|apikey|api[_-]?key)\s*[=:]\s*['\"]([^'\"]+)['\"]",
            r"(?:secret|secret_key)\s*[=:]\s*['\"]([^'\"]+)['\"]",
            r"(?:password|passwd|pwd)\s*[=:]\s*['\"]([^'\"]+)['\"]",
            r"(?:token|access_token)\s*[=:]\s*['\"]([^'\"]+)['\"]",
            r"(?:database_url|db_url|mongodb_uri)\s*[=:]\s*['\"]([^'\"]+)['\"]",
        ]

        for pattern in patterns:
            match = re.search(pattern, original_line, re.IGNORECASE)
            if match:
                key = match.group(1).upper()
                # 根据规则名称推断
                if "API Key" in rule_name or "OpenAI" in rule_name:
                    return "API_KEY"
                elif "Token" in rule_name:
                    return "TOKEN"
                elif "Password" in rule_name or "Database" in rule_name:
                    return "DATABASE_URL"
                elif "Secret" in rule_name:
                    return "SECRET_KEY"
                elif "AWS" in rule_name:
                    return "AWS_ACCESS_KEY_ID"
                elif "JWT" in rule_name:
                    return "JWT_SECRET"

        # 默认根据规则名生成
        name_map = {
            "OpenAI API Key": "OPENAI_API_KEY",
            "GitHub Token": "GITHUB_TOKEN",
            "AWS Access Key": "AWS_ACCESS_KEY_ID",
            "Database URL": "DATABASE_URL",
            "Bearer Token": "BEARER_TOKEN",
            "Hardcoded Password": "PASSWORD",
            "Slack Token": "SLACK_TOKEN",
            "JWT Token": "JWT_SECRET",
            "Alibaba Cloud AccessKey": "ALIBABA_CLOUD_ACCESS_KEY_ID",
            "Tencent Cloud SecretId": "TENCENT_CLOUD_SECRET_ID",
        }

        for key, value in name_map.items():
            if key in rule_name:
                return value

        return "SECRET_VALUE"

    def _generate_replacement_line(self, original_line, env_var_name):
        """生成替换后的代码行"""
        # 处理 Python: value = "sk-xxx" → value = os.environ.get("ENV_VAR", "")
        py_match = re.match(r"^(\s*[a-zA-Z_]\w*\s*[=:])\s*['\"].+['\"]\s*(.*)$", original_line)
        if py_match:
            return f"{py_match.group(1)} os.environ.get(\"{env_var_name}\", \"\"){py_match.group(2)}"

        # 处理 JS: value: "xxx" → value: process.env.ENV_VAR || ''
        js_match = re.match(r"^(\s*[a-zA-Z_]\w*\s*:\s*)['\"].+['\"]\s*(.*)$", original_line)
        if js_match:
            return f"{js_match.group(1)} process.env.{env_var_name} || ''{js_match.group(2)}"

        # 处理 JS: value = "xxx" → value = process.env.ENV_VAR || ''
        js_match2 = re.match(r"^(\s*[a-zA-Z_]\w*\s*=\s*)['\"].+['\"]\s*(.*)$", original_line)
        if js_match2:
            return f"{js_match2.group(1)} process.env.{env_var_name} || ''{js_match2.group(2)}"

        # 处理 JSON/YAML 格式
        json_match = re.match(r"^(\s*['\"]?[a-zA-Z_]\w*['\"]?\s*:\s*)['\"].+['\"]\s*(.*)$", original_line)
        if json_match:
            return f"{json_match.group(1)}\"${{{env_var_name}}}\"{json_match.group(2)}"

        # Fallback: 直接替换字符串内容
        return original_line

    def analyze(self):
        """分析扫描结果，生成改造建议"""
        for result in self.scanner_results:
            # 生成建议的环境变量名
            env_var = self._generate_env_var_name(result.line_content, result.rule_name)
            # 生成替换后的代码
            replacement = self._generate_replacement_line(result.line_content, env_var)

            # 分类
            if not result.context_required:
                category = 1  # 明确模式，可自动替换
            else:
                category = 2  # 需要人工确认

            self.suggestions.append(RefactorSuggestion(
                file_path=result.file_path,
                line_number=result.line_number,
                original=result.line_content,
                suggestion=replacement,
                rule_name=result.rule_name,
                category=category,
            ))

        return self.suggestions

    def get_auto_suggestions(self):
        """获取可自动处理的建议（类别1）"""
        return [s for s in self.suggestions if s.category == 1]

    def get_manual_suggestions(self):
        """获取需要人工确认的建议（类别2）"""
        return [s for s in self.suggestions if s.category == 2]

    def print_plan(self):
        """打印改造计划"""
        auto_items = self.get_auto_suggestions()
        manual_items = self.get_manual_suggestions()

        print(f"\n{'='*60}")
        print("🔧 代码改造计划")
        print(f"{'='*60}")

        if auto_items:
            print(f"\n🤖 第1类 - 自动替换 ({len(auto_items)} 处):")
            print("-" * 40)
            for item in auto_items:
                print(f"  [{item.rule_name}]")
                print(f"  文件: {item.file_path}:{item.line_number}")
                print(f"  原始: {item.original[:80]}")
                print(f"  替换: {item.suggestion[:80]}")
                print()

        if manual_items:
            print(f"\n👤 第2类 - 需人工确认 ({len(manual_items)} 处):")
            print("-" * 40)
            for item in manual_items:
                print(f"  [{item.rule_name}]")
                print(f"  文件: {item.file_path}:{item.line_number}")
                print(f"  内容: {item.original[:80]}")
                print(f"  建议: {item.suggestion[:80]}")
                print()
