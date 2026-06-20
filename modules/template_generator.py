"""
public-prep — 模板文件生成模块

自动创建 README、LICENSE、.gitignore、.env.example。
模板文件存放在 templates/ 目录下，根据项目类型组合。
"""

from pathlib import Path
import shutil


class TemplateGenerator:
    """模板文件生成器"""

    def __init__(self, output_path, project_type, license_type="MIT",
                 readme_style="career", project_name="", description="",
                 author="", year="2026"):
        self.output_path = Path(output_path)
        self.project_type = project_type
        self.license_type = license_type
        self.readme_style = readme_style
        self.project_name = project_name or self.output_path.name
        self.description = description
        self.author = author or "[copyright holder]"
        self.year = year

        # 模板目录（相对于本文件）
        self.template_dir = Path(__file__).parent.parent / "templates"

    def generate_all(self):
        """生成所有模板文件"""
        self.generate_gitignore()
        self.generate_license()
        self.generate_env_example()

        # README 在最终验证阶段由主流程调用
        return self._report()

    def generate_gitignore(self):
        """生成 .gitignore"""
        gitignore_dir = self.template_dir / "gitignore"
        output_file = self.output_path / ".gitignore"

        content = []

        # 通用模板
        base_file = gitignore_dir / "base.txt"
        if base_file.exists():
            content.append(base_file.read_text(encoding="utf-8"))

        # 按项目类型补充
        type_map = {
            "Python": "python.txt",
            "Node.js": "node.txt",
            "JavaScript": "node.txt",
        }

        for ptype in self.project_type.split(" + "):
            if ptype in type_map:
                extra_file = gitignore_dir / type_map[ptype]
                if extra_file.exists():
                    content.append("\n")
                    content.append(extra_file.read_text(encoding="utf-8"))

        output_file.write_text("\n".join(content), encoding="utf-8")

    def generate_license(self):
        """生成 LICENSE 文件"""
        license_file = self.template_dir / "LICENSE_MIT.txt"
        output_file = self.output_path / "LICENSE"

        if license_file.exists():
            content = license_file.read_text(encoding="utf-8")
            content = content.replace("[year]", self.year)
            content = content.replace("[copyright holder]", self.author)
            output_file.write_text(content, encoding="utf-8")

    def generate_env_example(self):
        """生成 .env.example"""
        env_file = self.template_dir / "env_example.txt"
        output_file = self.output_path / ".env.example"

        if env_file.exists():
            shutil.copy2(env_file, output_file)

    def generate_readme(self, bilingual=False):
        """生成 README.md（英文版）和可选的 README.zh.md（中文版）"""
        style = self.readme_style  # "career" or "share"
        template_file = self.template_dir / "readme" / f"README_{style}.md"
        output_file = self.output_path / "README.md"

        if template_file.exists():
            content = template_file.read_text(encoding="utf-8")
            content = content.replace("Project Name", self.project_name)
            content = content.replace("[year]", self.year)
            content = content.replace("[copyright holder]", self.author)
            output_file.write_text(content, encoding="utf-8")

        # 中文版
        if bilingual:
            zh_template = self.template_dir / "readme" / f"README_{style}.zh.md"
            zh_output = self.output_path / "README.zh.md"
            if zh_template.exists():
                content = zh_template.read_text(encoding="utf-8")
                zh_output.write_text(content, encoding="utf-8")
            else:
                # 无中文模板时，基于英文版生成一个说明占位
                zh_content = (
                    f"# {self.project_name}\n\n"
                    f"> 中文版 README — 如需补充中文说明，请编辑此文件。\n\n"
                    f"## 项目简介\n\n{self.description}\n\n"
                    f"## 快速开始\n\n请参考 [README.md](README.md) 的英文说明。\n\n"
                    f"## 许可证\n\n[MIT](LICENSE) © {self.year} {self.author}\n"
                )
                zh_output.write_text(zh_content, encoding="utf-8")

    def _report(self):
        """报告生成状态"""
        files = [".gitignore", "LICENSE", ".env.example", "README.md"]
        status = {}
        for f in files:
            status[f] = (self.output_path / f).exists()
        return status
