# PDF-Audio-Video-to-Markdown with AI

> **Universal AI Skill** for Claude Code / Cursor / Antigravity / Windsurf and more
>
> Let AI handle everything - from setup to transcription!
>
> **通用 AI 技能** 适用于 Claude Code / Cursor / Antigravity / Windsurf 等
>
> 让 AI 处理一切 - 从环境配置到文件转录！

[![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-8A2BE2?logo=anthropic&logoColor=white)](https://claude.ai)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-00DC82?logo=cursor&logoColor=white)](https://cursor.com)
[![Antigravity](https://img.shields.io/badge/Antigravity-Compatible-FF6B6B)](https://antigravity.dev)
[![Windsurf](https://img.shields.io/badge/Windsurf-Compatible-0EA5E9)](https://windsurf.ai)

[![Python 3.10-3.12](https://img.shields.io/badge/Python-3.10--3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/evan966890/PDF-Audio-Video-to-Markdown-with-AI?style=social)](https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI)

---

**English** | **中文**

Intelligently convert PDF, Audio, Video & Images to Markdown text, especially optimized for **meeting recordings transcription**.

将 PDF / 音频 / 视频 / 图像 **智能转换** 为 Markdown 文本，特别适合 **会议录屏转文字** 场景。

---

## Table of Contents / 目录

- [Why This Tool / 为什么选择](#why-this-tool--为什么选择)
- [Features / 功能特性](#features--功能特性)
- [Privacy & Security / 隐私安全](#privacy--security--隐私安全)
- [System Requirements / 系统要求](#system-requirements--系统要求)
- [Quick Start / 快速开始](#quick-start--快速开始)
- [Usage / 使用方法](#usage--使用方法)
- [FAQ / 常见问题](#faq--常见问题)
- [Roadmap / 路线图](#roadmap--路线图)
- [Contributing / 贡献](#contributing--贡献)

---

## Why This Tool / 为什么选择

| Pain Point 痛点 | Solution 解决方案 |
|----------------|------------------|
| Meeting recordings unsearchable / 会议录屏无法搜索 | Auto-transcribe to searchable Markdown / 自动转写为可搜索 Markdown |
| Scanned PDF text not copyable / 扫描 PDF 无法复制文字 | Smart OCR auto-recognition / 智能 OCR 自动识别 |
| Large files cause memory overflow / 大文件导致内存溢出 | Auto-chunked processing (30s/chunk) / 自动分段处理 |
| Complex environment setup / 环境配置复杂 | One-click auto-install with retry / 一键自动安装，内置重试 |
| Different IDE needs different config / 不同 IDE 配置不同 | Universal Skill format / 通用 Skill 格式 |

---

## Features / 功能特性

### Core Features / 核心功能

| Feature 功能 | Description 描述 |
|-------------|------------------|
| **Multi-format** | PDF, Audio (MP3/WAV/M4A), Video (MP4/AVI/MKV), Images (PNG/JPG) |
| **Smart OCR** | Auto-detect scanned vs text PDF / 自动检测扫描版还是文字版 PDF |
| **Meeting Ready** | Optimized for meeting recordings / 针对会议录屏优化 |
| **Chunked Processing** | Auto-chunk large files to prevent OOM / 自动分段防止内存溢出 |
| **Auto Retry** | Built-in retry mechanism (3x per file) / 内置重试机制 |
| **Fully Offline** | All processing done locally / 完全本地处理 |
| **Zero Config** | Auto-install dependencies / 自动安装依赖 |
| **Portable** | Copy to any machine, no absolute paths / 可复制到任何机器 |

### Advanced Features (v2.0) / 高级功能

| Feature 功能 | Description 描述 |
|-------------|------------------|
| **Speaker Diarization** | Identify who said what (requires HuggingFace Token) / 说话人识别 |
| **YouTube Transcription** | Get subtitles or transcribe locally / YouTube 字幕获取或本地转录 |
| **Table Extraction** | Extract tables from PDF / 从 PDF 提取表格 |
| **Multi-format Output** | Export to SRT/VTT/JSON/TXT / 多格式导出 |
| **On-demand Dependencies** | Install features when needed / 按需安装功能依赖 |

---

## Privacy & Security / 隐私安全

> **100% Local Processing - Your Data Never Leaves Your Machine**
>
> **100% 本地处理 - 您的数据永远不会离开您的电脑**

| Guarantee 保障 | Description 说明 |
|---------------|-----------------|
| **No Cloud Upload** | All runs on your local machine / 完全在本地电脑运行 |
| **No Internet Required** | Works offline after setup / 配置后完全离线工作 |
| **No Data Collection** | Zero telemetry, no tracking / 无遥测，无追踪 |
| **Files Stay Local** | Never sent anywhere / 文件不会被发送 |
| **Open Source** | Full transparency / 完全开源透明 |

**Perfect for / 适用于：**
- Corporate confidential meetings / 企业机密会议
- Healthcare/Medical records / 医疗健康记录
- Legal documents / 法律文件
- Any sensitive content / 任何敏感内容

---

## System Requirements / 系统要求

| Component 组件 | Minimum 最低 | Recommended 推荐 |
|---------------|-------------|-----------------|
| **OS** | Windows 10 / macOS 10.15 / Ubuntu 18.04 | Windows 11 / macOS 12+ |
| **Python** | 3.10 (required / 必需) | 3.11 or 3.12 |
| **RAM** | 8 GB | 16 GB+ |
| **Storage** | 5 GB free (for models) | 10 GB+ SSD |
| **CPU** | 4 cores | 8+ cores |
| **GPU** | Not required / 非必需 | NVIDIA GPU (optional) |

---

## Quick Start / 快速开始

### 3 Steps / 三步开始

**Step 1: Clone to IDE Skills Folder / 克隆到 IDE 技能目录**

```bash
# Claude Code
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.claude/skills/PDF-Audio-Video-to-Markdown-with-AI

# Cursor
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.cursor/skills/PDF-Audio-Video-to-Markdown-with-AI

# Antigravity
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.antigravity/skills/PDF-Audio-Video-to-Markdown-with-AI

# Windsurf
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.windsurf/skills/PDF-Audio-Video-to-Markdown-with-AI
```

**Step 2: Ask AI to Setup / 让 AI 帮你配置**

Simply tell your AI assistant (no manual commands needed!):

只需用自然语言告诉你的 AI 助手（无需手动输入命令！）：

> **English**: "Please install all dependencies for the PDF-Audio-Video-to-Markdown-with-AI skill"
> 
> **中文**: "请帮我安装 PDF-Audio-Video-to-Markdown-with-AI 这个技能的所有依赖"

AI will automatically configure everything for you!

AI 会自动为你完成所有配置！

**Step 3: Use It / 开始使用**

Tell your AI what you want to process / 告诉 AI 你想处理什么：

> **English**: "Please transcribe the meeting.mp4 file"
>
> **中文**: "请把 meeting.mp4 转成文字"

**That's it! No manual commands needed!**

**就这么简单，无需手动输入任何命令！**

---

## Usage / 使用方法

### Natural Language (Recommended) / 自然语言（推荐）

Just tell AI what you want / 直接告诉 AI 你想做什么：

| English | 中文 |
|---------|------|
| "Transcribe this meeting recording" | "转录这个会议录音" |
| "Extract text from this PDF" | "提取这个 PDF 的文字" |
| "Convert video to text with speaker identification" | "把视频转文字，识别不同说话人" |
| "Get YouTube video subtitles" | "获取 YouTube 视频字幕" |
| "Batch process all files in folder" | "批量处理文件夹里的所有文件" |

### Command Line / 命令行

```bash
# Single file / 单个文件
python scripts/process_file.py <file_path> [output_dir]

# Batch processing / 批量处理
python scripts/process_all.py [input_dir] [output_dir]

# End-to-end test / 端到端测试
python scripts/run_e2e_test.py
```

---

## FAQ / 常见问题

**Python version error / Python 版本错误**

Install Python 3.10-3.12, or use `py -3.12` to specify version.

安装 Python 3.10-3.12，或使用 `py -3.12` 指定版本。

**Chinese garbled text on Windows / Windows 中文乱码**

```powershell
$env:PYTHONIOENCODING='utf-8'
python scripts/process_file.py ...
```

**Out of memory / 内存不足**

Large files are auto-chunked. If still failing, reduce chunk size in config.

大文件会自动分段。如仍失败，减小配置中的分段大小。

**FFmpeg not found**

Install FFmpeg: `winget install FFmpeg` (Windows), `brew install ffmpeg` (macOS), `sudo apt install ffmpeg` (Linux)

More FAQ: See `references/troubleshooting.md`

更多问题：参见 `references/troubleshooting.md`

---

## Roadmap / 路线图

- [x] PDF text extraction & OCR / PDF 文本提取和 OCR
- [x] Audio/Video transcription (FunASR) / 音视频转录
- [x] Smart routing & chunked processing / 智能路由和分段处理
- [x] Auto environment setup / 自动环境配置
- [x] Multi-IDE support / 多 IDE 支持
- [x] Speaker diarization / 说话人分离
- [x] YouTube transcription / YouTube 转录
- [x] Table extraction from PDF / PDF 表格提取
- [x] Multi-format output (SRT/VTT/JSON) / 多格式输出
- [x] On-demand dependency installation / 按需安装依赖
- [x] Bilingual documentation / 双语文档
- [ ] GPU acceleration support / GPU 加速支持
- [ ] Web UI interface / Web 界面
- [ ] Docker container / Docker 容器

**Have ideas? / 有想法？** [Open an issue](https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI/issues)!

---

## Contributing / 贡献

We welcome contributions! / 欢迎贡献！

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines / 参见贡献指南。

---

## License / 许可证

MIT License - see [LICENSE](LICENSE)

---

## Author / 作者

**evan966890** - evan966890@gmail.com

GitHub: https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI

---

**Star this repo if you find it useful! / 如果觉得有用，请点个 Star！**
