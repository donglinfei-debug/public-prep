"""
public-prep — Clean Copy 创建模块

创建不含 .git 历史的干净副本，自动排除敏感文件/依赖目录/缓存。
在副本中执行残留敏感文件清理。
"""

import os
import re
import shutil
from pathlib import Path
from rules.exclude_patterns import EXCLUDE_DIRS, EXCLUDE_FILES, SENSITIVE_FILES


class CleanCopy:
    """Clean Copy 创建器"""

    def __init__(self, source_path, output_path):
        self.source_path = Path(source_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.copied_count = 0
        self.deleted_files = []

    def _should_exclude(self, item_path, rel_path):
        """判断是否排除此文件/目录"""
        # 检查目录排除
        for part in rel_path.parts:
            if part in EXCLUDE_DIRS:
                return True

        # 检查文件排除模式
        name = item_path.name
        for pattern in EXCLUDE_FILES:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True

        return False

    def create_copy(self):
        """创建干净副本"""
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.copied_count = 0

        for root, dirs, files in os.walk(self.source_path):
            # 计算相对路径
            rel_path = Path(root).relative_to(self.source_path)

            # 跳过排除目录（修改 dirs 列表以控制 os.walk 的递归）
            dirs[:] = [d for d in dirs if not self._should_exclude(
                Path(root) / d, rel_path / d)]

            # 跳过 .git 目录
            dirs[:] = [d for d in dirs if d != ".git"]

            # 创建目标目录
            target_dir = self.output_path / rel_path
            target_dir.mkdir(parents=True, exist_ok=True)

            # 复制文件
            for file in files:
                src_file = Path(root) / file
                rel_file_path = rel_path / file

                if self._should_exclude(src_file, rel_file_path):
                    continue

                dst_file = target_dir / file
                try:
                    shutil.copy2(src_file, dst_file)
                    self.copied_count += 1
                except (OSError, shutil.Error):
                    pass

        return self.copied_count

    def clean_sensitive_files(self):
        """在副本中删除敏感文件"""
        self.deleted_files = []

        for root, dirs, files in os.walk(self.output_path):
            for file in files:
                file_path = Path(root) / file
                # 检查敏感文件模式
                for pattern in SENSITIVE_FILES:
                    if pattern.startswith("*") and pattern.endswith("*"):
                        # 包含模式: *token*
                        if pattern[1:-1].lower() in file.lower():
                            self._delete_file(file_path)
                    elif pattern.startswith("*"):
                        # 扩展名模式: *.pem
                        if file.lower().endswith(pattern[1:].lower()):
                            self._delete_file(file_path)
                    elif file.lower() == pattern.lower():
                        # 精确匹配: .env
                        self._delete_file(file_path)

        # 检查根目录是否有残留源码文件（常见于旧版残留）
        root_files = [f for f in self.output_path.iterdir() if f.is_file() and f.suffix in (".py", ".js", ".ts")]
        if root_files:
            # 检查是否有 backend/ 或 src/ 子目录含同名文件
            subdirs = ["backend", "src", "app", "core"]
            for sd in subdirs:
                sub_path = self.output_path / sd
                if sub_path.exists() and sub_path.is_dir():
                    for rf in root_files:
                        if (sub_path / rf.name).exists():
                            self._delete_file(rf)
                            break

        return self.deleted_files

    def _delete_file(self, file_path):
        """安全删除文件"""
        try:
            file_path.unlink()
            self.deleted_files.append(str(file_path))
        except OSError:
            pass

    def check_bat_files(self):
        """检查 .bat/.sh 启动脚本中的敏感信息"""
        findings = []
        for bat_file in self.output_path.rglob("*.bat"):
            content = bat_file.read_text(encoding="utf-8", errors="ignore")
            issues = []
            if re.search(r"[A-Z]:\\", content):
                issues.append("含本地绝对路径")
            if re.search(r"(password|token|secret|api_key)", content, re.IGNORECASE):
                issues.append("含疑似敏感信息")
            if issues:
                findings.append((bat_file, issues))
            else:
                findings.append((bat_file, []))

        # 同样检查 .sh 和 .ps1
        for ext in ["*.sh", "*.ps1"]:
            for script_file in self.output_path.rglob(ext):
                content = script_file.read_text(encoding="utf-8", errors="ignore")
                issues = []
                if re.search(r"[A-Z]:\\", content):
                    issues.append("含本地绝对路径")
                if re.search(r"(password|token|secret|api_key)", content, re.IGNORECASE):
                    issues.append("含疑似敏感信息")
                if issues:
                    findings.append((script_file, issues))

        return findings

    def print_report(self):
        """打印 Clean Copy 报告"""
        print(f"\n{'='*60}")
        print("📦 Clean Copy 报告")
        print(f"{'='*60}")
        print(f"  源路径:   {self.source_path}")
        print(f"  目标路径: {self.output_path}")
        print(f"  已复制:   {self.copied_count} 个文件")
        if self.deleted_files:
            print(f"  🗑️ 已删除: {len(self.deleted_files)} 个敏感文件")
            for f in self.deleted_files[:10]:
                rel = Path(f).relative_to(self.output_path)
                print(f"    - {rel}")
            if len(self.deleted_files) > 10:
                print(f"    ... 还有 {len(self.deleted_files) - 10} 个")
        else:
            print(f"  敏感文件: 无")
        print(f"{'='*60}\n")
