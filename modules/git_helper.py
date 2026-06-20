"""
public-prep — Git 配置和初始化模块

检测当前 Git 身份，引导设置公开仓库专用身份（GitHub noreply 邮箱），
git init + 首次 commit。
"""

import subprocess
from pathlib import Path


class GitHelper:
    """Git 配置助手"""

    def __init__(self, repo_path):
        self.repo_path = Path(repo_path).resolve()
        self.global_name = self._get_global_config("user.name")
        self.global_email = self._get_global_config("user.email")
        self.local_name = None
        self.local_email = None

    def _run_git(self, args):
        """运行 git 命令"""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_path)] + args,
                capture_output=True, text=True, timeout=30
            )
            return result.stdout.strip(), result.returncode
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return "", -1

    def _get_global_config(self, key):
        """获取全局 Git 配置"""
        try:
            result = subprocess.run(
                ["git", "config", "--global", key],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None

    def check_current_config(self):
        """检查当前仓库的 Git 配置"""
        out, _ = self._run_git(["config", "user.name"])
        self.local_name = out or None
        out, _ = self._run_git(["config", "user.email"])
        self.local_email = out or None
        return {
            "local_name": self.local_name,
            "local_email": self.local_email,
            "global_name": self.global_name,
            "global_email": self.global_email,
        }

    def is_noreply_email(self, email):
        """检查是否是 GitHub noreply 邮箱"""
        return email and "users.noreply.github.com" in email

    def set_public_identity(self, username="donglinfei-debug", display_name="Ryan Dong"):
        """设置公开仓库专用身份"""
        noreply_email = f"{username}@users.noreply.github.com"

        self._run_git(["config", "user.name", display_name])
        self._run_git(["config", "user.email", noreply_email])

        self.local_name = display_name
        self.local_email = noreply_email

        return {"name": display_name, "email": noreply_email}

    def init_repo(self):
        """初始化 Git 仓库"""
        out, code = self._run_git(["init"])
        return code == 0

    def create_initial_commit(self, message="Initial commit"):
        """创建首次 commit"""
        # 先 add
        self._run_git(["add", "-A"])
        # 再 commit
        out, code = self._run_git(["commit", "-m", message])
        return code == 0, out

    def print_config_report(self):
        """打印 Git 配置报告"""
        config = self.check_current_config()

        print(f"\n{'='*60}")
        print("🔑 Git 配置检查")
        print(f"{'='*60}")

        print(f"\n  全局配置:")
        print(f"    用户名: {config['global_name'] or '❌ 未设置'}")
        print(f"    邮箱:   {config['global_email'] or '❌ 未设置'}")

        print(f"\n  当前仓库:")
        print(f"    用户名: {config['local_name'] or '（继承全局）'}")
        print(f"    邮箱:   {config['local_email'] or '（继承全局）'}")

        if config['local_email'] and self.is_noreply_email(config['local_email']):
            print(f"\n  ✅ 使用 GitHub noreply 邮箱，隐私受保护")
        elif config['global_email'] and self.is_noreply_email(config['global_email']):
            print(f"\n  ✅ 全局已配置 GitHub noreply 邮箱")
        else:
            print(f"\n  ⚠️  建议设置 GitHub noreply 邮箱保护隐私")
            print(f"     格式: <用户名>@users.noreply.github.com")

        print(f"{'='*60}\n")
