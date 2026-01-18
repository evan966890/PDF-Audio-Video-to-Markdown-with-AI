---
name: pdf-audio-video-to-markdown-with-ai
description: >
  Universal AI Skill to convert PDF, audio, video, and images to Markdown text.
  Use this skill when: transcribing meeting recordings, extracting PDF text,
  OCR scanned documents, converting audio/video to text, processing conference recordings,
  batch document conversion, extracting text from screenshots.
  触发关键词: 转录, 会议录屏, PDF转文字, 音频转文字, 视频转文字, OCR, 文档处理,
  transcribe, meeting recording, PDF to text, audio to text, video to text, document processing.
  Works with Claude Code, Cursor, Antigravity, Windsurf, and any IDE supporting skill format.
  Let AI handle everything - from environment setup to file transcription!
---

# PDF-Audio-Video-to-Markdown with AI

🤖 **Universal AI Skill** | 通用 AI 技能 | Let AI do the work!

Convert PDF / Audio / Video / Images to Markdown text intelligently.

将 PDF / 音频 / 视频 / 图像 智能转换为 Markdown 文本。

## Overview | 概述

PDF-Audio-video2Markdown is a **fully portable** multimodal document processing skill, optimized for:

- 🎬 **Meeting recordings** → Searchable text (会议录屏转文字)
- 📄 **PDF documents** → Extracted/OCR text (PDF 文档提取)
- 🎵 **Audio files** → Transcription (音频转录)
- 🖼️ **Images** → OCR text (图像文字识别)

**Version**: 1.0.0  
**Python**: 3.10-3.12 (required)  
**Compatibility**: Claude Code, Cursor, Antigravity, Windsurf, and more

## Quick Start | 快速开始

### Step 1: Clone to IDE Skills Folder | 克隆到 IDE 技能目录

```bash
# Claude Code
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.claude/skills/PDF-Audio-Video-to-Markdown-with-AI

# Cursor
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.cursor/skills/PDF-Audio-Video-to-Markdown-with-AI
```

### Step 2: Ask AI to Setup | 让 AI 帮你配置

Just tell your AI assistant in natural language (no manual commands!):

只需用自然语言告诉 AI（无需手动命令！）：

> 🗣️ "Please install all dependencies for the PDF-Audio-Video-to-Markdown-with-AI skill"
>
> 🗣️ "请帮我安装 PDF-Audio-Video-to-Markdown-with-AI 这个技能的所有依赖"

### Step 3: Use It | 开始使用

Tell AI what to process:

告诉 AI 要处理什么：

> 🗣️ "Please transcribe meeting.mp4 to text"
>
> 🗣️ "请把 meeting.mp4 转成文字"

## Supported Formats | 支持格式

| Type | Formats |
|------|---------|
| Video | MP4, AVI, MKV, MOV |
| Audio | MP3, WAV, M4A, FLAC |
| PDF | PDF (text layer / scanned - auto-detect) |
| Image | PNG, JPG, JPEG, TIFF |

## Key Features | 核心特性

- ✅ **Smart OCR**: Auto-detect text vs scanned PDF
- ✅ **Chunked Processing**: Large files split into 30s segments
- ✅ **Auto Retry**: 3 retries per file, 10 for E2E tests
- ✅ **100% Local**: All processing on your machine, data never uploaded
- ✅ **Zero Config**: Auto-install dependencies
- ✅ **Portable**: No absolute paths, copy anywhere

## 🔒 Privacy | 隐私保障

**100% Local Processing** - Your data never leaves your machine!

**100% 本地处理** - 您的数据永远不会离开您的电脑！

- No cloud upload 无云端上传
- No internet required after setup 配置后无需联网
- No data collection 无数据收集
- Open source & auditable 开源可审计

## 💻 Requirements | 系统要求

| Component | Minimum |
|-----------|---------|
| Python | 3.10-3.12 |
| RAM | 8 GB |
| Storage | 5 GB free |
| OS | Windows 10+ / macOS 10.15+ / Linux |

## Reference Docs | 参考文档

- `references/routing_strategies.md` - Processing logic details
- `references/troubleshooting.md` - Common issues & solutions

## IDE Installation | IDE 安装

| IDE | Path |
|-----|------|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Cursor | `~/.cursor/skills/` or `.cursor/skills/` |
| Antigravity | `~/.antigravity/skills/` |
| Windsurf | `~/.windsurf/skills/` |

## Author | 作者

**evan966890** - evan966890@gmail.com
