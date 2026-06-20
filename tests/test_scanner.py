"""Scanner 模块单元测试"""

import sys
import os
import tempfile
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.scanner import Scanner, ScanResult
from rules.scan_rules import SCAN_RULES, get_rules_by_risk


def test_scan_rules_loaded():
    """验证扫描规则库已加载"""
    assert len(SCAN_RULES) > 0
    high_rules = get_rules_by_risk("high")
    medium_rules = get_rules_by_risk("medium")
    low_rules = get_rules_by_risk("low")
    assert len(high_rules) > 0
    assert len(medium_rules) > 0
    print(f"  [PASS] 规则库: {len(SCAN_RULES)} 条 ({len(high_rules)} 高/{len(medium_rules)} 中/{len(low_rules)} 低)")


def test_scan_detects_api_key():
    """验证扫描能检测到 API Key"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "config.py"
        test_file.write_text(
            'API_KEY = "sk-proj-wkjOJeyw1234567890"\n'
            'print("hello")\n',
            encoding="utf-8",
        )

        scanner = Scanner(tmpdir, use_gitleaks=False)
        results = scanner.scan()
        api_hits = [r for r in results if "API" in r.rule_name]
        assert len(api_hits) >= 1, f"未检测到 API Key, 结果: {results}"
        print(f"  [PASS] API Key 检测: {api_hits[0].rule_name} 在行 {api_hits[0].line_number}")


def test_scan_detects_local_path():
    """验证扫描能检测到本地路径"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "utils.py"
        test_file.write_text(
            'BASE_PATH = "D:\\\\Users\\\\test\\\\Desktop\\\\data"\n',
            encoding="utf-8",
        )

        scanner = Scanner(tmpdir, use_gitleaks=False)
        results = scanner.scan()
        path_hits = [r for r in results if "Path" in r.rule_name or "路径" in r.rule_name]
        assert len(path_hits) >= 1, f"未检测到本地路径, 结果: {results}"
        print(f"  [PASS] 本地路径检测: {path_hits[0].rule_name} 在行 {path_hits[0].line_number}")


def test_scan_detects_password():
    """验证扫描能检测到硬编码密码"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "db.py"
        test_file.write_text(
            'DATABASE_URL = "mysql://root:password123@localhost:3306/mydb"\n',
            encoding="utf-8",
        )

        scanner = Scanner(tmpdir, use_gitleaks=False)
        results = scanner.scan()
        db_hits = [r for r in results if "Database" in r.rule_name or "Password" in r.rule_name]
        assert len(db_hits) >= 1, f"未检测到数据库密码, 结果: {results}"
        print(f"  [PASS] 数据库密码检测: {db_hits[0].rule_name} 在行 {db_hits[0].line_number}")


def test_scan_preserves_indentation():
    """验证扫描结果保留原始缩进"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "config.py"
        test_file.write_text(
            '    API_KEY = "sk-test-key-indent-abcdefgh"\n',
            encoding="utf-8",
        )

        scanner = Scanner(tmpdir, use_gitleaks=False)
        results = scanner.scan()
        assert len(results) > 0
        # 验证缩进保留
        assert results[0].line_content.startswith("    "), \
            f"缩进丢失: {repr(results[0].line_content[:20])}"
        print(f"  [PASS] 缩进保留: {repr(results[0].line_content[:20])}")


def test_scan_skips_excluded_dirs():
    """验证排除目录不被扫描"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # 在排除目录中放一个含密钥的文件
        excluded_dir = Path(tmpdir) / "node_modules"
        excluded_dir.mkdir()
        (excluded_dir / "secret.js").write_text(
            'const key = "sk-proj-excluded-key";\n',
            encoding="utf-8",
        )

        scanner = Scanner(tmpdir, use_gitleaks=False)
        results = scanner.scan()
        assert len(results) == 0, f"排除目录仍被扫描: {results}"
        print(f"  [PASS] 排除目录跳过: node_modules 未被扫描")


def test_verifier_checklist():
    """验证 Verifier 检查项完整性"""
    from modules.verifier import Verifier

    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建一个"干净"的公开版
        (Path(tmpdir) / "README.md").write_text("# Test", encoding="utf-8")
        (Path(tmpdir) / "LICENSE").write_text("MIT", encoding="utf-8")
        (Path(tmpdir) / ".gitignore").write_text(".env\n__pycache__\n", encoding="utf-8")
        (Path(tmpdir) / ".env.example").write_text("# Copy to .env\nAPI_KEY=your_key\n", encoding="utf-8")

        verifier = Verifier(tmpdir)
        checklist, findings = verifier.run_all()

        assert checklist.get("gitignore_exists") is True
        assert checklist.get("license_exists") is True
        assert checklist.get("readme_exists") is True
        assert checklist.get("env_removed") is True
        print(f"  [PASS] Verifier 检查项全部通过")


def test_assessment():
    """验证 Assessment 预检功能"""
    from modules.assessor import Assessment

    with tempfile.TemporaryDirectory() as tmpdir:
        # 模拟一个 Python 项目
        (Path(tmpdir) / "requirements.txt").write_text("flask\n", encoding="utf-8")
        (Path(tmpdir) / "main.py").write_text("print('hello')\n", encoding="utf-8")

        a = Assessment(tmpdir)
        assert "Python" in a.project_type
        assert a.is_git is False
        assert a.file_count > 0
        print(f"  [PASS] Assessment: 类型={a.project_type}, 文件数={a.file_count}")


def test_clean_copy():
    """验证 Clean Copy 排除功能"""
    from modules.clean_copy import CleanCopy

    with tempfile.TemporaryDirectory() as tmpdir:
        src = Path(tmpdir) / "src_proj"
        dst = Path(tmpdir) / "dst_proj"
        src.mkdir()

        # 创建正常文件 + 应排除文件
        (src / "main.py").write_text("print('hi')\n", encoding="utf-8")
        (src / ".env").write_text("SECRET=xxx\n", encoding="utf-8")
        (src / "requirements.txt").write_text("flask\n", encoding="utf-8")
        # 创建应排除的子目录
        (src / "__pycache__").mkdir()
        (src / "__pycache__" / "cache.pyc").write_text("", encoding="utf-8")

        cc = CleanCopy(src, dst)
        count = cc.create_copy()
        deleted = cc.clean_sensitive_files()

        # 正常文件应被复制
        assert (dst / "main.py").exists(), "main.py 未被复制"
        assert (dst / "requirements.txt").exists(), "requirements.txt 未被复制"
        # 敏感文件应被删除
        assert not (dst / ".env").exists(), ".env 未被删除"
        # 排除目录不应被复制
        assert not (dst / "__pycache__").exists(), "__pycache__ 被复制"
        print(f"  [PASS] Clean Copy: 复制 {count} 个, 删除 {len(deleted)} 个敏感文件")


if __name__ == "__main__":
    tests = [
        test_scan_rules_loaded,
        test_scan_detects_api_key,
        test_scan_detects_local_path,
        test_scan_detects_password,
        test_scan_preserves_indentation,
        test_scan_skips_excluded_dirs,
        test_verifier_checklist,
        test_assessment,
        test_clean_copy,
    ]

    passed = 0
    failed = 0
    print(f"运行 {len(tests)} 个测试...\n")
    for test in tests:
        try:
            test()
            print(f"  [PASS] {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1
    print(f"\n{'='*40}")
    print(f"结果: {passed} 通过, {failed} 失败")
