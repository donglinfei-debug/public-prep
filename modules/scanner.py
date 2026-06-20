"""
public-prep — 深度扫描模块

双重检测引擎：
  1. 正则扫描（内置规则库，覆盖 20+ 种模式）
  2. gitleaks 扫描（可选，通过外部二进制调用）

使用方式：
  from modules.scanner import Scanner
  scanner = Scanner("/path/to/project")
  results = scanner.scan()
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from rules.scan_rules import SCAN_RULES, get_risk_label
from rules.exclude_patterns import EXCLUDE_DIRS, EXCLUDE_FILES, SCAN_EXTENSIONS


class ScanResult:
    """单条扫描结果"""

    def __init__(self, file_path, line_number, line_content, rule_name, risk, context_required):
        self.file_path = file_path
        self.line_number = line_number
        self.line_content = line_content
        self.rule_name = rule_name
        self.risk = risk
        self.context_required = context_required

    def __repr__(self):
        risk_icon = {"high": "[HIGH]", "medium": "[MED]", "low": "[LOW]"}.get(self.risk, "[?]")
        return f"{risk_icon} {self.rule_name} -> {self.file_path}:{self.line_number}"

    def to_dict(self):
        return {
            "file": str(self.file_path),
            "line": self.line_number,
            "content": self.line_content,
            "rule": self.rule_name,
            "risk": self.risk,
            "context_required": self.context_required,
        }


class Scanner:
    """项目敏感信息扫描器"""

    def __init__(self, project_path, use_gitleaks=True):
        self.project_path = Path(project_path).resolve()
        self.use_gitleaks = use_gitleaks
        self.results = []
        self.gitleaks_available = False

        if self.use_gitleaks:
            self.gitleaks_available = self._check_gitleaks()

    def _check_gitleaks(self):
        """检查 gitleaks 是否已安装"""
        try:
            result = subprocess.run(
                ["gitleaks", "--version"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _should_skip_file(self, file_path):
        """判断是否应该跳过此文件"""
        rel_path = file_path.relative_to(self.project_path) if file_path.is_relative_to(self.project_path) else file_path

        # 检查目录排除
        for part in rel_path.parts:
            if part in EXCLUDE_DIRS:
                return True

        # 检查文件扩展名排除
        ext = "".join(file_path.suffixes).lower()
        for pattern in EXCLUDE_FILES:
            if pattern.startswith("*"):
                if ext == pattern[1:].lower():
                    return True
            elif file_path.name == pattern:
                return True

        # 检查是否在扫描范围内
        if file_path.suffix.lower() not in SCAN_EXTENSIONS:
            # 还需要检查无扩展名文件如 Makefile、Dockerfile 等
            if file_path.name not in SCAN_EXTENSIONS:
                return True

        return False

    def _scan_regex(self):
        """正则模式扫描"""
        findings = []

        for root, dirs, files in os.walk(self.project_path):
            # 跳过排除目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                file_path = Path(root) / file
                if self._should_skip_file(file_path):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                except Exception:
                    continue

                for line_num, line in enumerate(lines, 1):
                    for rule in SCAN_RULES:
                        # 检查排除模式
                        skip = False
                        for ex_pattern in rule.get("exclude_patterns", []):
                            if ex_pattern in str(file_path):
                                skip = True
                                break
                        if skip:
                            continue

                        if re.search(rule["pattern"], line):
                            findings.append(ScanResult(
                                file_path=str(file_path),
                                line_number=line_num,
                                line_content=line,
                                rule_name=rule["name"],
                                risk=rule["risk"],
                                context_required=rule["context_required"],
                            ))

        return findings

    def _scan_gitleaks(self):
        """gitleaks 扫描（需要目标目录是 Git 仓库）"""
        if not self.gitleaks_available:
            return []

        findings = []
        try:
            result = subprocess.run(
                ["gitleaks", "detect", "--no-git", "-v"],
                capture_output=True, text=True, timeout=120,
                cwd=str(self.project_path)
            )

            # gitleaks 输出解析
            for line in result.stdout.split("\n"):
                if "leak" in line.lower() or "secret" in line.lower():
                    # 简单解析 gitleaks 输出行
                    findings.append(ScanResult(
                        file_path=str(self.project_path),
                        line_number=0,
                        line_content=line,
                        rule_name="gitleaks 检测",
                        risk="high",
                        context_required=True,
                    ))

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return findings

    def scan(self):
        """执行全量扫描，返回 ScanResult 列表"""
        all_findings = []

        # 1. 正则扫描
        regex_findings = self._scan_regex()
        all_findings.extend(regex_findings)

        # 2. gitleaks 扫描（可选）
        if self.use_gitleaks and self.gitleaks_available:
            gitleaks_findings = self._scan_gitleaks()
            all_findings.extend(gitleaks_findings)

        # 去重：同一文件同一行同一规则只保留一条
        seen = set()
        unique_findings = []
        for f in all_findings:
            key = (f.file_path, f.line_number, f.rule_name)
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)

        self.results = unique_findings
        return self.results

    def get_high_risk(self):
        """仅返回高风险发现"""
        return [r for r in self.results if r.risk == "high"]

    def get_medium_risk(self):
        """仅返回中风险发现"""
        return [r for r in self.results if r.risk == "medium"]

    def get_low_risk(self):
        """仅返回低风险发现"""
        return [r for r in self.results if r.risk == "low"]

    def get_auto_fixable(self):
        """返回可自动修复的发现"""
        return [r for r in self.results if not r.context_required]

    def get_manual_review(self):
        """返回需要人工确认的发现"""
        return [r for r in self.results if r.context_required]

    def print_report(self):
        """打印扫描报告"""
        if not self.results:
            print("== 未发现敏感信息 ==")
            return

        print(f"\n{'='*60}")
        print(f"🔍 扫描完成: 发现 {len(self.results)} 个问题")
        print(f"{'='*60}")

        # 按风险等级分组
        for risk_level in ["high", "medium", "low"]:
            items = [r for r in self.results if r.risk == risk_level]
            if not items:
                continue

            label = get_risk_label(risk_level)
            print(f"\n{label} 风险 ({len(items)} 个):")
            print("-" * 40)

            for item in items:
                print(f"  {item.rule_name}")
                print(f"    文件: {item.file_path}:{item.line_number}")
                print(f"    内容: {item.line_content[:100]}")
                if item.context_required:
                    print(f"    状态: [需要人工确认]")
                else:
                    print(f"    状态: [可自动处理]")
                print()

    def summary_stats(self):
        """返回统计摘要"""
        return {
            "total": len(self.results),
            "high": len(self.get_high_risk()),
            "medium": len(self.get_medium_risk()),
            "low": len(self.get_low_risk()),
            "auto_fixable": len(self.get_auto_fixable()),
            "manual_review": len(self.get_manual_review()),
        }
