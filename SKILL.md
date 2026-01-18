---
name: pdf-audio-video-to-markdown-with-ai
description: >
  Universal AI Skill to convert PDF, audio, video, and images to Markdown text.
  Features: speaker diarization, YouTube transcription, table extraction, multi-format output.
  Use this skill when: transcribing meeting recordings, extracting PDF text,
  OCR scanned documents, converting audio/video to text, processing conference recordings,
  batch document conversion, extracting tables, YouTube subtitles, speaker identification.
  触发关键词: 转录, 会议录屏, PDF转文字, 音频转文字, 视频转文字, OCR, 文档处理,
  说话人分离, YouTube字幕, 表格提取, SRT字幕, 批量处理,
  transcribe, meeting recording, PDF to text, audio to text, video to text, 
  document processing, speaker diarization, YouTube transcript, table extraction.
  Works with Claude Code, Cursor, Antigravity, Windsurf, and any IDE supporting skill format.
  Let AI handle everything - from environment setup to file transcription!
---

# PDF-Audio-Video-to-Markdown with AI

🤖 **Universal AI Skill** | 通用 AI 技能 | Let AI do the work!

Convert PDF / Audio / Video / Images to Markdown text intelligently.

将 PDF / 音频 / 视频 / 图像 智能转换为 Markdown 文本。

---

## 🌐 语言交互指南 / Language Interaction Guide

**重要：AI 应根据用户使用的语言自动回复！**

**Important: AI should respond in the user's language automatically!**

### 语言检测规则 / Language Detection Rules

1. **用户说中文** → AI 用中文回复
   - 示例: "请帮我转录这个音频" → AI 用中文回答并执行

2. **User speaks English** → AI responds in English
   - Example: "Please transcribe this audio" → AI responds and executes in English

3. **混合语言 / Mixed language** → 优先使用用户问题中主要使用的语言
   - Use the dominant language in user's message

### AI 回复示例 / AI Response Examples

**中文用户 Chinese User:**
```
用户: 帮我把这个会议录音转成文字
AI: 好的，我来帮您处理会议录音。
    1. 首先检查依赖状态...
    2. 检测到文件类型为音频
    3. 开始转录...
```

**English User:**
```
User: Transcribe this meeting recording for me
AI: Sure, I'll process the meeting recording.
    1. Checking dependencies first...
    2. Detected file type: audio
    3. Starting transcription...
```

---

## ⚠️ AI 执行流程 / AI Execution Flow

**执行任何功能前，AI 必须先检查依赖状态！**

**Before executing any feature, AI must check dependency status first!**

### Step 1: 检查依赖 / Check Dependencies
```bash
python scripts/check_dependencies.py
```

### Step 2: 如果缺少依赖 / If Missing Dependencies

向用户确认后再安装 / Ask user before installing:

> 🇨🇳 "检测到缺少 [X] 个依赖，需要下载约 [Y]MB。是否安装？"
> 🇬🇧 "Found [X] missing dependencies, ~[Y]MB download required. Install now?"

### Step 3: 首次使用引导 / First-run Wizard
```bash
python scripts/dependency_manager.py wizard
```

让用户选择安装级别 / Let user choose:
- 基础 / Basic (~600MB)
- 完整 / Full (~1.5GB)
- 高级 / Advanced (~3GB)
- 按需 / On-demand

### Step 4: 执行处理 / Process Files

依赖就绪后才执行文件处理。
Only process files after dependencies are ready.

---

## Overview | 概述

**Version**: 2.0.0  
**Python**: 3.10-3.12 (required)  
**Compatibility**: Claude Code, Cursor, Antigravity, Windsurf, and more

### 核心功能 / Core Features

- 🎬 **会议录屏转文字** - Meeting recordings to text
- 📄 **PDF 文档提取** - PDF text extraction (with OCR)
- 🎵 **音频转录** - Audio transcription
- 🖼️ **图像 OCR** - Image text recognition

### 高级功能 / Advanced Features (v2.0)

- 👥 **说话人分离** - Speaker diarization (requires HuggingFace Token)
- 📺 **YouTube 转录** - YouTube video transcription
- 📊 **表格提取** - PDF table extraction
- 📝 **多格式输出** - SRT/VTT/JSON export

---

## Quick Start | 快速开始

### Step 1: Clone to IDE Skills Folder | 克隆到 IDE 技能目录

```bash
# Claude Code
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.claude/skills/PDF-Audio-Video-to-Markdown-with-AI

# Cursor
git clone https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI.git ~/.cursor/skills/PDF-Audio-Video-to-Markdown-with-AI
```

### Step 2: Ask AI to Setup | 让 AI 帮你配置

**无需手动输入任何命令！No manual commands needed!**

只需告诉 AI / Just tell AI:

> 🇨🇳 "请帮我安装 PDF-Audio-Video-to-Markdown-with-AI 的依赖"
> 🇬🇧 "Please install dependencies for PDF-Audio-Video-to-Markdown-with-AI skill"

AI 会自动 / AI will automatically:
- 检查当前依赖状态 / Check dependency status
- 询问你的安装偏好 / Ask your installation preference
- 自动安装并重试直到成功 / Install with retry until success

### Step 3: Use It | 开始使用

告诉 AI 要处理什么 / Tell AI what to process:

> 🇨🇳 "请把 meeting.mp4 转成文字"
> 🇬🇧 "Please transcribe meeting.mp4"

---

## 功能详情 / Feature Details

### 基础功能 (Basic) ~600MB

| 功能 Feature | 说明 Description |
|--------------|------------------|
| PDF 文本提取 | Extract text from PDF / 提取 PDF 中的文字内容 |
| 音视频转录 | Transcribe MP3/MP4/WAV / 音视频转为文字 |
| 智能路由 | Auto-select best strategy / 自动选择最佳处理策略 |

### OCR 功能 ~50MB

| 功能 Feature | 说明 Description |
|--------------|------------------|
| 扫描 PDF | OCR scanned PDFs / 识别扫描版 PDF 中的文字 |
| 图像识别 | Extract text from images / 从图片中提取文字 |

### YouTube 功能 ~5MB

| 功能 Feature | 说明 Description |
|--------------|------------------|
| 字幕获取 | Get YouTube subtitles / 获取 YouTube 视频字幕 |
| 本地转录 | Local transcription / 无字幕时下载并本地转录 |

### 表格提取 ~100MB

| 功能 Feature | 说明 Description |
|--------------|------------------|
| PDF 表格 | Extract PDF tables / 提取 PDF 中的表格为 Markdown |
| HTML 输出 | HTML output / 同时生成 HTML 格式 |

### 说话人分离 ~2GB (需要 HuggingFace Token)

| 功能 Feature | 说明 Description |
|--------------|------------------|
| 多人识别 | Identify speakers / 识别不同说话人 |
| 时间标记 | Timestamps / 每段标注说话人和时间 |

> 📖 申请指南 / Guide: `references/huggingface_token_guide.md`

---

## 输出格式 / Output Formats

- **Markdown** (.md) - 默认格式 / Default format
- **SRT** (.srt) - 视频字幕格式 / Video subtitle format
- **VTT** (.vtt) - Web 字幕格式 / Web subtitle format
- **JSON** (.json) - 结构化数据 / Structured data
- **TXT** (.txt) - 纯文本 / Plain text

---

## 🔒 Privacy | 隐私保障

**100% Local Processing** - Your data never leaves your machine!

- ✅ 无云端上传 / No cloud upload
- ✅ 配置后无需联网 / Offline after setup
- ✅ 无数据收集 / No data collection
- ✅ 开源可审计 / Open source

---

## 💻 Requirements | 系统要求

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10-3.12 | 3.11 |
| RAM | 8 GB | 16 GB |
| Storage | 5 GB | 10 GB |
| OS | Windows 10+ / macOS 10.15+ / Linux | - |

GPU (可选/Optional): NVIDIA CUDA 支持可加速说话人分离 / CUDA support accelerates speaker diarization

---

## Reference Docs | 参考文档

- `references/routing_strategies.md` - 处理逻辑详情 / Processing logic
- `references/troubleshooting.md` - 常见问题解决 / Troubleshooting
- `references/huggingface_token_guide.md` - HuggingFace Token 申请 / Token guide
- `references/workflow_templates.md` - 工作流模板 / Workflow templates

---

## Scripts | 脚本说明

| 脚本 Script | 功能 Function |
|-------------|---------------|
| `check_dependencies.py` | 检查依赖状态 / Check dependencies |
| `dependency_manager.py` | 智能依赖安装 / Smart dependency install |
| `process_file.py` | 单文件处理 / Single file processing |
| `process_all.py` | 批量处理 / Batch processing |
| `youtube_transcript.py` | YouTube 转录 / YouTube transcription |
| `output_formats.py` | 格式转换 / Format conversion |
| `advanced_features.py` | 高级功能 / Advanced features |

---

## IDE Installation | IDE 安装路径

| IDE | Path |
|-----|------|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Cursor | `~/.cursor/skills/` or `.cursor/skills/` |
| Antigravity | `~/.antigravity/skills/` |
| Windsurf | `~/.windsurf/skills/` |

---

## 常用命令 / Common Prompts

### 中文提示词 Chinese Prompts
- "转录这个音频文件"
- "把会议录屏转成文字"
- "提取 PDF 中的文本"
- "识别图片中的文字"
- "获取 YouTube 视频字幕"
- "批量处理文件夹中的所有文件"
- "导出为 SRT 字幕格式"

### English Prompts
- "Transcribe this audio file"
- "Convert meeting recording to text"
- "Extract text from PDF"
- "OCR this image"
- "Get YouTube video subtitles"
- "Batch process all files in folder"
- "Export to SRT subtitle format"

---

## Author | 作者

**evan966890** - evan966890@gmail.com

GitHub: https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI
