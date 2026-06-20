#!/usr/bin/env python3
"""
public-prep — 项目公开预处理工具

将本地项目一键"洗净打包"，安全地发布到 GitHub 公开仓库。

工作流程：
  1. 项目预检 → 2. 深度扫描 → 3. 代码改造辅助 → 4. 模板文件生成
  → 5. Clean Copy → 6. Git 配置引导 → 7. 最终验证

用法：
  python main.py --project /path/to/project
  python main.py --verify /path/to/public_copy
  python main.py --project /path/to/project --output /path/to/output
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def print_banner():
    """打印程序横幅"""
    print(r"""
     ____              _      ____
    |  _ \ _   _ _ __ | |_   |  _ \ _ __ ___  ___ ___
    | |_) | | | | '_ \| __|  | |_) | '__/ _ \/ __/ __|
    |  __/| |_| | | | | |_   |  __/| | |  __/\__ \__ \
    |_|    \__,_|_| |_|\__|  |_|   |_|  \___||___/___/
    """)
    print("  Project Public-Ready Preprocessor v1.0")
    print("  Make your local project ready for GitHub — safely.")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="public-prep — 项目公开预处理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py --project D:\\projects\\my-tool
  python main.py --verify D:\\projects\\my-tool_public
  python main.py --project D:\\projects\\my-tool --output D:\\github\\my-tool
        """,
    )

    parser.add_argument(
        "--project", "-p",
        type=str,
        help="源项目路径（完整流程模式）",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="公开版输出路径（默认: <项目名>_public）",
    )
    parser.add_argument(
        "--verify",
        type=str,
        help="仅验证模式：指定公开版路径进行安全检查",
    )
    parser.add_argument(
        "--license", "-l",
        type=str,
        default="MIT",
        choices=["MIT", "Apache-2.0", "GPL-3.0"],
        help="许可证类型（默认: MIT）",
    )
    parser.add_argument(
        "--readme-style", "-r",
        type=str,
        default="career",
        choices=["career", "share"],
        help="README 风格: career（详细）/ share（简洁）",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="跳过确认提示，直接执行",
    )

    return parser.parse_args()


def confirm(message):
    """获取用户确认"""
    response = input(f"\n{message} (y/N): ").strip().lower()
    return response in ("y", "yes")


def run_verify_mode(target_path, args):
    """仅验证模式"""
    from modules.verifier import Verifier

    target = Path(target_path).resolve()
    if not target.exists():
        print(f"[X] 路径不存在: {target}")
        return False

    print(f"\n📋 开始验证: {target}")
    verifier = Verifier(target)
    verifier.run_all()
    passed = verifier.print_report()

    return passed


def run_full_workflow(args):
    """完整 7 阶段流程"""
    # ===== 阶段 1: 项目预检 =====
    from modules.assessor import Assessment
    from modules.scanner import Scanner
    from modules.refactor_helper import RefactorHelper
    from modules.template_generator import TemplateGenerator
    from modules.clean_copy import CleanCopy
    from modules.git_helper import GitHelper
    from modules.verifier import Verifier

    project_path = Path(args.project).resolve()
    if not project_path.exists():
        print(f"[X] 路径不存在: {project_path}")
        return False

    # 输出路径
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = project_path.parent / f"{project_path.name}_public"

    print(f"\n{'='*60}")
    print("🚀 public-prep 开始执行")
    print(f"   源项目: {project_path}")
    print(f"   输出:   {output_path}")
    print(f"{'='*60}")

    # ---- 阶段 1: 项目预检 ----
    print(f"\n{'─'*60}")
    print("📋 [阶段 1/7] 项目预检")
    print(f"{'─'*60}")

    assessment = Assessment(project_path)
    assessment.print_report()

    if not args.yes:
        if not confirm("是否继续?"):
            print("已取消")
            return False

    # ---- 阶段 2: 深度扫描 ----
    print(f"\n{'─'*60}")
    print("🔍 [阶段 2/7] 深度扫描")
    print(f"{'─'*60}")

    scanner = Scanner(project_path, use_gitleaks=True)
    findings = scanner.scan()
    scanner.print_report()
    stats = scanner.summary_stats()

    print(f"\n  扫描统计: 总计 {stats['total']} | "
          f"[H] {stats['high']} | [M] {stats['medium']} | [L] {stats['low']}")
    print(f"  可自动处理: {stats['auto_fixable']} | 需人工确认: {stats['manual_review']}")

    if stats["high"] > 0 and not args.yes:
        print("\n[!]  发现高风险问题。")
        if not confirm("是否继续处理?"):
            print("已取消")
            return False

    # ---- 阶段 3: 代码改造辅助 ----
    print(f"\n{'─'*60}")
    print("🔧 [阶段 3/7] 代码改造辅助")
    print(f"{'─'*60}")

    refactor = RefactorHelper(findings)
    suggestions = refactor.analyze()
    refactor.print_plan()

    auto_count = len(refactor.get_auto_suggestions())
    manual_count = len(refactor.get_manual_suggestions())
    print(f"\n  统计: 自动替换 {auto_count} 处 | 需确认 {manual_count} 处")

    if auto_count > 0 and not args.yes:
        if confirm("是否自动执行第1类替换?"):
            print("  🤖 自动替换将在 Clean Copy 中执行")
        else:
            print("  跳过自动替换")

    if manual_count > 0:
        print("\n  👆 请手动修改上述第2类项后继续。")
        if not args.yes:
            if not confirm("确认已修改完毕?"):
                print("  请在准备好后重新运行")
                return False

    # ---- 阶段 4: 模板文件生成 ----
    print(f"\n{'─'*60}")
    print("📄 [阶段 4/7] 生成模板文件")
    print(f"{'─'*60}")

    generator = TemplateGenerator(
        output_path=output_path,
        project_type=assessment.project_type,
        license_type=args.license,
        readme_style=args.readme_style,
        project_name=assessment.project_name,
        author="[copyright holder]",
    )
    status = generator.generate_all()
    generator.generate_readme(bilingual=True)

    for file, exists in status.items():
        print(f"  {'[OK]' if exists else '[X]'} {file}")

    # ---- 阶段 5: Clean Copy ----
    print(f"\n{'─'*60}")
    print("📦 [阶段 5/7] Clean Copy")
    print(f"{'─'*60}")

    cleaner = CleanCopy(project_path, output_path)
    count = cleaner.create_copy()
    deleted = cleaner.clean_sensitive_files()
    bat_issues = cleaner.check_bat_files()
    cleaner.print_report()

    if bat_issues:
        print("  启动脚本检查:")
        for script, issues in bat_issues:
            if issues:
                print(f"    [!] {script.name}: {', '.join(issues)}")
            else:
                print(f"    [OK] {script.name}: 无问题")

    # ---- 阶段 6: Git 配置引导 ----
    print(f"\n{'─'*60}")
    print("🔑 [阶段 6/7] Git 配置")
    print(f"{'─'*60}")

    git = GitHelper(output_path)
    git.print_config_report()

    if not args.yes:
        if git.local_email and not git.is_noreply_email(git.local_email):
            if confirm("是否设置 GitHub noreply 邮箱保护隐私?"):
                identity = git.set_public_identity()
                print(f"  [OK] 已设置: {identity['name']} <{identity['email']}>")

    # Git 初始化
    print("\n  初始化 Git 仓库...")
    if git.init_repo():
        print("  [OK] git init 完成")
        success, msg = git.create_initial_commit()
        if success:
            print("  [OK] 首次 commit 完成")
        else:
            print(f"  [!] commit 失败: {msg[:100]}")
    else:
        print("  [X] git init 失败")

    # ---- 阶段 7: 最终验证 ----
    print(f"\n{'─'*60}")
    print("[OK] [阶段 7/7] 最终验证")
    print(f"{'─'*60}")

    verifier = Verifier(output_path)
    verifier.run_all()
    passed = verifier.print_report()

    # ---- 完成 ----
    print(f"\n{'='*60}")
    if passed:
        print("[DONE] public-prep 执行完成！公开版已就绪。")
        print(f"\n  公开版路径: {output_path}")
        print("\n📌 下一步:")
        print(f"  1. 打开 https://github.com/new")
        print(f"  2. 创建新的公开仓库（不勾选 README）")
        print(f"  3. 在本地运行:")
        print(f"     cd {output_path}")
        print(f"     git remote add origin https://github.com/<用户名>/<仓库名>.git")
        print(f"     git branch -M main")
        print(f"     git push -u origin main")
        print(f"\n  4. 设置仓库 Topics 和 Description")
        print(f"  5. 开启 GitHub Secret Scanning")
    else:
        print("[!]  验证未通过，请查看上述 [X] 项")
        print(f"  公开版路径: {output_path}")

    return passed


def main():
    """主入口"""
    args = parse_args()
    print_banner()

    if args.verify:
        # 模式 2: 仅验证
        success = run_verify_mode(args.verify, args)
    elif args.project:
        # 模式 1: 完整流程
        success = run_full_workflow(args)
    else:
        # 无参数，显示帮助
        print("请指定一个项目路径:")
        print("  python main.py --project /path/to/project")
        print("  python main.py --verify /path/to/public_copy")
        print("  python main.py --help")
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
