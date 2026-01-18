# Contributing to PDF-Audio-video2Markdown

First off, thank you for considering contributing! 🎉

感谢你考虑为本项目做出贡献！

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)

---

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

---

## How Can I Contribute?

### 🐛 Reporting Bugs

1. Check [existing issues](https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI/issues) first
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment info (OS, Python version)
   - Error logs if applicable

### 💡 Suggesting Features

1. Open an issue with `[Feature Request]` prefix
2. Describe the use case
3. Explain why it would be useful

### 🔧 Code Contributions

Great areas to contribute:

| Area | Description |
|------|-------------|
| **Speaker Diarization** | Add "who said what" to transcriptions |
| **GPU Acceleration** | Optimize for CUDA/MPS |
| **New Formats** | Support more file types |
| **Performance** | Faster processing |
| **Documentation** | Improve docs, add examples |
| **Tests** | Add unit/integration tests |
| **Translations** | Translate docs to other languages |

---

## Development Setup

### Prerequisites

- Python 3.10-3.12
- Git
- FFmpeg (for audio/video)

### Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/PDF-Audio-video2Markdown.git
cd PDF-Audio-video2Markdown

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows

# 3. Install dependencies
python scripts/setup_environment.py

# 4. Create feature branch
git checkout -b feature/your-feature-name
```

### Testing Your Changes

```bash
# Run end-to-end test
python scripts/run_e2e_test.py

# Test single file
python scripts/process_file.py test_file.pdf ./output
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows the style guide
- [ ] Self-reviewed the changes
- [ ] Added/updated documentation if needed
- [ ] Tested the changes locally
- [ ] No new linter warnings

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guide
- [ ] Self-reviewed
- [ ] Documentation updated
- [ ] Tests pass
```

### After Submitting

1. Wait for review (usually within a few days)
2. Address any feedback
3. Once approved, it will be merged

---

## Style Guide

### Python

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small

```python
def process_file(path: Path, output_dir: Path) -> ProcessResult:
    """
    Process a single file and output Markdown.
    
    Args:
        path: Input file path
        output_dir: Output directory
        
    Returns:
        ProcessResult with status and output path
    """
    ...
```

### Commits

Use clear, descriptive commit messages:

```
feat: add speaker diarization support
fix: handle empty PDF pages gracefully
docs: update installation instructions
perf: optimize OCR for large images
```

Prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `perf:` - Performance
- `refactor:` - Code refactoring
- `test:` - Tests
- `chore:` - Maintenance

### Documentation

- Use Markdown
- Include code examples
- Keep it concise but complete
- Use bilingual format (English + Chinese) when possible

---

## Questions?

- Open an issue with `[Question]` prefix
- Or reach out via discussions

---

**Thank you for contributing! 感谢你的贡献！** 🙏
