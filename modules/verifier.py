"""
public-prep — 最终验证模块

对公开版全量重扫描，输出 ✅/❌ 检查清单。
"""

from pathlib import Path
from modules.scanner import Scanner
from rules.exclude_patterns import SENSITIVE_FILES


class Verifier:
    """最终验证器"""

    def __init__(self, target_path):
        self.target_path = Path(target_path).resolve()
        self.scanner = Scanner(target_path, use_gitleaks=True)
        self.checklist = {}

    def verify_env_file(self):
        """检查 .env 是否在公开版中残留"""
        env_file = self.target_path / ".env"
        if env_file.exists():
            self.checklist["env_removed"] = False
            return False
        self.checklist["env_removed"] = True
        return True

    def verify_env_example(self):
        """检查 .env.example 是否存在"""
        env_example = self.target_path / ".env.example"
        if env_example.exists():
            content = env_example.read_text(encoding="utf-8", errors="ignore")
            # 检查是否不含真实值
            has_real_values = False
            for line in content.split("\n"):
                if "=" in line and not line.strip().startswith("#"):
                    value = line.split("=", 1)[1].strip()
                    if value and "your" not in value.lower() and "这里" not in value:
                        has_real_values = True
                        break
            self.checklist["env_example_clean"] = not has_real_values
            return not has_real_values
        self.checklist["env_example_exists"] = False
        return False

    def verify_gitignore(self):
        """检查 .gitignore 是否存在"""
        gi = self.target_path / ".gitignore"
        exists = gi.exists()
        self.checklist["gitignore_exists"] = exists
        if exists:
            content = gi.read_text(encoding="utf-8", errors="ignore")
            has_env = ".env" in content
            self.checklist["gitignore_has_env"] = has_env
            return has_env
        return False

    def verify_license(self):
        """检查 LICENSE 是否存在"""
        lic = self.target_path / "LICENSE"
        exists = lic.exists()
        self.checklist["license_exists"] = exists
        return exists

    def verify_readme(self):
        """检查 README.md 是否存在"""
        readme = self.target_path / "README.md"
        exists = readme.exists()
        self.checklist["readme_exists"] = exists
        return exists

    def verify_scan(self):
        """执行全量扫描验证"""
        findings = self.scanner.scan()

        # 高风险问题
        high_risk = [f for f in findings if f.risk == "high"]
        medium_risk = [f for f in findings if f.risk == "medium"]

        self.checklist["high_risk_count"] = len(high_risk)
        self.checklist["medium_risk_count"] = len(medium_risk)
        self.checklist["total_findings"] = len(findings)
        self.checklist["scan_passed"] = len(high_risk) == 0

        return findings

    def run_all(self):
        """执行全部验证"""
        self.verify_env_file()
        self.verify_env_example()
        self.verify_gitignore()
        self.verify_license()
        self.verify_readme()
        findings = self.verify_scan()

        return self.checklist, findings

    def print_report(self):
        """打印验证报告"""
        if not self.checklist:
            self.run_all()

        print(f"\n{'='*60}")
        print("✅ 最终验证报告")
        print(f"{'='*60}")

        print(f"\n📋 检查清单:")
        checks = [
            ("env_removed",       ".env 文件已删除"),
            ("env_example_clean", ".env.example 不含真实值"),
            ("gitignore_exists",  ".gitignore 存在"),
            ("gitignore_has_env", ".gitignore 包含 .env"),
            ("license_exists",    "LICENSE 存在"),
            ("readme_exists",     "README.md 存在"),
        ]

        for key, label in checks:
            if key in self.checklist:
                status = "✅" if self.checklist[key] else "❌"
                print(f"  {status} {label}")

        print(f"\n🔍 安全扫描:")
        if "scan_passed" in self.checklist:
            if self.checklist["scan_passed"]:
                print(f"  ✅ 无高风险问题")
            else:
                print(f"  ❌ {self.checklist['high_risk_count']} 个高风险问题")
            print(f"  📊 总计: {self.checklist.get('total_findings', 0)} 个发现")
            print(f"     高风险: {self.checklist.get('high_risk_count', 0)}")
            print(f"     中风险: {self.checklist.get('medium_risk_count', 0)}")

        # 总体结论
        passed = all([
            self.checklist.get("env_removed", False),
            self.checklist.get("scan_passed", False),
            self.checklist.get("gitignore_exists", False),
        ])

        print(f"\n{'='*60}")
        if passed:
            print("🎉 验证通过！可以推送到 GitHub 公开仓库")
        else:
            print("⚠️  验证未通过，请查看上述 ❌ 项并修复")
        print(f"{'='*60}\n")

        return passed
