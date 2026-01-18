# Contributing to PDF-Audio-Video-to-Markdown-with-AI
# 为 PDF-Audio-Video-to-Markdown-with-AI 贡献

First off, thank you for considering contributing!

首先，感谢你考虑为本项目做出贡献！

## Table of Contents / 目录

- [Code of Conduct / 行为准则](#code-of-conduct--行为准则)
- [How Can I Contribute? / 如何贡献](#how-can-i-contribute--如何贡献)
- [Development Setup / 开发环境配置](#development-setup--开发环境配置)
- [Pull Request Process / PR 流程](#pull-request-process--pr-流程)
- [Style Guide / 代码风格](#style-guide--代码风格)

---

## Code of Conduct / 行为准则

This project follows a simple code of conduct:

本项目遵循简单的行为准则：

- Be respectful and inclusive / 尊重他人，包容差异
- Focus on constructive feedback / 提供建设性反馈
- Help others learn and grow / 帮助他人学习成长

---

## How Can I Contribute? / 如何贡献

### Reporting Bugs / 报告问题

1. Check [existing issues](https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI/issues) first
   
   先检查 [已有问题](https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI/issues)

2. Create a new issue with / 创建新问题时请包含:
   - Clear title / 清晰的标题
   - Steps to reproduce / 复现步骤
   - Expected vs actual behavior / 期望与实际行为
   - Environment info (OS, Python version) / 环境信息（操作系统、Python版本）
   - Error logs if applicable / 错误日志（如有）

### Suggesting Features / 建议新功能

1. Open an issue with `[Feature Request]` prefix
   
   创建带 `[Feature Request]` 前缀的问题

2. Describe the use case / 描述使用场景

3. Explain why it would be useful / 解释其价值

### Code Contributions / 代码贡献

Great areas to contribute / 欢迎贡献的领域:

| Area 领域 | Description 描述 |
|-----------|------------------|
| **Speaker Diarization** | Add "who said what" / 说话人识别 |
| **GPU Acceleration** | Optimize for CUDA/MPS / GPU加速优化 |
| **New Formats** | Support more file types / 支持更多格式 |
| **Performance** | Faster processing / 性能优化 |
| **Documentation** | Improve docs, add examples / 完善文档 |
| **Tests** | Add unit/integration tests / 添加测试 |
| **Translations** | Translate to other languages / 翻译文档 |

---

## Development Setup / 开发环境配置

### Prerequisites / 前置条件

- Python 3.10-3.12
- Git
- FFmpeg (for audio/video / 音视频处理需要)

### Setup Steps / 配置步骤

```bash
# 1. Fork and clone / Fork 并克隆
git clone https://github.com/YOUR_USERNAME/PDF-Audio-Video-to-Markdown-with-AI.git
cd PDF-Audio-Video-to-Markdown-with-AI

# 2. Create virtual environment / 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or / 或者
.\venv\Scripts\activate   # Windows

# 3. Install dependencies / 安装依赖
python scripts/setup_environment.py

# 4. Create feature branch / 创建功能分支
git checkout -b feature/your-feature-name
```

### Testing Your Changes / 测试改动

```bash
# Run end-to-end test / 运行端到端测试
python scripts/run_e2e_test.py

# Test single file / 测试单个文件
python scripts/process_file.py test_file.pdf ./output
```

---

## Pull Request Process / PR 流程

### Before Submitting / 提交前检查

- [ ] Code follows the style guide / 代码符合风格指南
- [ ] Self-reviewed the changes / 已自查改动
- [ ] Added/updated documentation if needed / 已更新文档（如需要）
- [ ] Tested the changes locally / 已本地测试
- [ ] No new linter warnings / 无新的代码警告

### PR Template / PR 模板

```markdown
## Description / 描述
Brief description of changes / 简要描述改动

## Type of Change / 改动类型
- [ ] Bug fix / 问题修复
- [ ] New feature / 新功能
- [ ] Documentation update / 文档更新
- [ ] Performance improvement / 性能优化

## Testing / 测试
How was this tested? / 如何测试的？

## Checklist / 检查清单
- [ ] Code follows style guide / 代码符合规范
- [ ] Self-reviewed / 已自查
- [ ] Documentation updated / 已更新文档
- [ ] Tests pass / 测试通过
```

### After Submitting / 提交后

1. Wait for review (usually within a few days) / 等待审核（通常几天内）
2. Address any feedback / 处理反馈意见
3. Once approved, it will be merged / 批准后将被合并

---

## Style Guide / 代码风格

### Python

- Follow PEP 8 / 遵循 PEP 8
- Use type hints where possible / 尽可能使用类型注解
- Add docstrings to functions / 为函数添加文档字符串
- Keep functions focused and small / 保持函数简洁专注

```python
def process_file(path: Path, output_dir: Path) -> ProcessResult:
    """
    Process a single file and output Markdown.
    处理单个文件并输出 Markdown。
    
    Args:
        path: Input file path / 输入文件路径
        output_dir: Output directory / 输出目录
        
    Returns:
        ProcessResult with status and output path
        包含状态和输出路径的 ProcessResult
    """
    ...
```

### Commits / 提交信息

Use clear, descriptive commit messages / 使用清晰描述性的提交信息:

```
feat: add speaker diarization support
fix: handle empty PDF pages gracefully
docs: update installation instructions
perf: optimize OCR for large images
```

Prefixes / 前缀:
- `feat:` - New feature / 新功能
- `fix:` - Bug fix / 问题修复
- `docs:` - Documentation / 文档
- `perf:` - Performance / 性能
- `refactor:` - Code refactoring / 代码重构
- `test:` - Tests / 测试
- `chore:` - Maintenance / 维护

### Documentation / 文档

- Use Markdown / 使用 Markdown
- Include code examples / 包含代码示例
- Keep it concise but complete / 简洁但完整
- **Use bilingual format (English + Chinese)** / **使用双语格式（中英文）**

---

## Questions? / 有问题？

- Open an issue with `[Question]` prefix / 创建带 `[Question]` 前缀的问题
- Or reach out via discussions / 或在 discussions 中讨论

---

**Thank you for contributing!**

**感谢你的贡献！**
