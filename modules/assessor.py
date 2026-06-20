"""
public-prep — 项目预检模块

自动检测项目类型、大小、Git 状态、敏感文件初筛。
"""

import os
import subprocess
from pathlib import Path
from rules.exclude_patterns import EXCLUDE_DIRS


class Assessment:
    """项目预检结果"""

    def __init__(self, project_path):
        self.project_path = Path(project_path).resolve()
        self.project_name = self.project_path.name
        self.project_type = self._detect_type()
        self.size_mb = self._calc_size()
        self.is_git = self._check_git()
        self.remote_url = self._get_remote_url()
        self.file_count = self._count_files()
        self.sensitive_files = self._find_sensitive_files()

    def _detect_type(self):
        """检测项目类型"""
        types = []
        files = [f.name for f in self.project_path.iterdir() if f.is_file()]

        if "requirements.txt" in files or "setup.py" in files or "pyproject.toml" in files:
            types.append("Python")
        if "package.json" in files:
            types.append("Node.js")
        if any(f.endswith(".html") for f in files):
            types.append("HTML")
        if "go.mod" in files:
            types.append("Go")
        if "Cargo.toml" in files:
            types.append("Rust")
        if "pom.xml" in files or "build.gradle" in files:
            types.append("Java")
        if "CMakeLists.txt" in files or "Makefile" in files:
            types.append("C/C++")
        if "Gemfile" in files:
            types.append("Ruby")
        if "composer.json" in files:
            types.append("PHP")
        if "Dockerfile" in files or "docker-compose.yml" in files:
            types.append("Docker")

        # 递归扫描 src/ 目录中的文件类型
        py_files = list(self.project_path.rglob("*.py"))
        js_files = list(self.project_path.rglob("*.js"))
        ts_files = list(self.project_path.rglob("*.ts"))
        html_files = list(self.project_path.rglob("*.html"))

        if py_files and "Python" not in types:
            types.append("Python")
        if (js_files or ts_files) and "Node.js" not in types:
            types.append("JavaScript")

        if not types:
            return "未知 / 其他"
        return " + ".join(sorted(set(types)))

    def _calc_size(self):
        """计算项目大小（MB）"""
        total = 0
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                try:
                    total += (Path(root) / f).stat().st_size
                except OSError:
                    pass
        return round(total / (1024 * 1024), 1)

    def _check_git(self):
        """检查是否是 Git 仓库"""
        return (self.project_path / ".git").exists()

    def _get_remote_url(self):
        """获取远程仓库地址"""
        if not self._check_git():
            return None
        try:
            result = subprocess.run(
                ["git", "-C", str(self.project_path), "remote", "get-url", "origin"],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None

    def _count_files(self):
        """统计源码文件数"""
        count = 0
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            count += len(files)
        return count

    def _find_sensitive_files(self):
        """初筛敏感文件"""
        sensitive = []
        patterns = [".env", ".env.*", "*.pem", "*.key", "config.json",
                    "credentials.json", "token*", "*password*", "*secret*"]

        for pattern in patterns:
            for f in self.project_path.rglob(pattern):
                # 跳过排除目录
                if any(excl in f.parts for excl in EXCLUDE_DIRS):
                    continue
                sensitive.append(f)

        return sensitive

    def print_report(self):
        """打印预检报告"""
        print(f"\n{'='*60}")
        print(f"📋 项目预检报告: {self.project_name}")
        print(f"{'='*60}")
        print(f"  项目类型:     {self.project_type}")
        print(f"  项目大小:     {self.size_mb} MB")
        print(f"  文件数量:     {self.file_count} 个")
        print(f"  Git 仓库:     {'是' if self.is_git else '否'}")
        if self.remote_url:
            print(f"  远程地址:     {self.remote_url}")
        if self.sensitive_files:
            print(f"  ⚠️ 敏感文件:  {len(self.sensitive_files)} 个")
            for f in self.sensitive_files[:10]:
                print(f"    - {f.relative_to(self.project_path)}")
            if len(self.sensitive_files) > 10:
                print(f"    ... 还有 {len(self.sensitive_files) - 10} 个")
        else:
            print(f"  敏感文件:     无")
        print(f"{'='*60}\n")

    def to_dict(self):
        return {
            "project_name": self.project_name,
            "project_type": self.project_type,
            "size_mb": self.size_mb,
            "is_git": self.is_git,
            "remote_url": self.remote_url,
            "file_count": self.file_count,
            "sensitive_files_count": len(self.sensitive_files),
        }
