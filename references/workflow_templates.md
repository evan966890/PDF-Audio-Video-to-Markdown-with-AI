# 工作流模板 / Workflow Templates

本文档提供常见场景的处理模板，直接告诉 AI 即可使用。
This document provides templates for common scenarios. Just tell AI what you need!

---

## 1. 会议录音转录 / Meeting Recording Transcription

### 场景 / Scenario
团队会议、项目讨论、客户会议的录音转录
Team meetings, project discussions, client meeting recordings

### 使用方法 / How to Use
告诉 AI / Tell AI:
> 🇨🇳 "请帮我转录这个会议录音: [文件路径]，需要识别不同说话人"
> 🇬🇧 "Please transcribe this meeting recording: [file path], identify different speakers"

### 推荐设置 / Recommended Settings
- 开启说话人分离 / Enable speaker diarization
- 输出格式 / Output: Markdown + SRT

---

## 2. 访谈记录 / Interview Recording

### 场景 / Scenario
用户访谈、专家采访、播客录制
User interviews, expert interviews, podcast recordings

### 使用方法 / How to Use
> 🇨🇳 "转录访谈录音，识别两位说话人"
> 🇬🇧 "Transcribe this interview, identify 2 speakers"

---

## 3. 课程/讲座 / Lecture / Course

### 场景 / Scenario
在线课程、学术讲座、培训视频
Online courses, academic lectures, training videos

### 使用方法 / How to Use
> 🇨🇳 "转录这个教学视频，生成带时间戳的笔记"
> 🇬🇧 "Transcribe this lecture video with timestamps"

---

## 4. YouTube 视频 / YouTube Video

### 场景 / Scenario
学习 YouTube 教程、提取演讲内容
Learning from YouTube tutorials, extracting speech content

### 使用方法 / How to Use
> 🇨🇳 "帮我获取这个 YouTube 视频的字幕: [URL]"
> 🇬🇧 "Get subtitles for this YouTube video: [URL]"

### 无字幕时 / When No Subtitles Available
> 🇨🇳 "下载 YouTube 视频并本地转录"
> 🇬🇧 "Download and transcribe YouTube video locally"

---

## 5. PDF 文档提取 / PDF Document Extraction

### 场景 / Scenario
论文、报告、合同等 PDF 文档
Papers, reports, contracts in PDF format

### 基本提取 / Basic Extraction
> 🇨🇳 "提取这个 PDF 的文本内容: [文件路径]"
> 🇬🇧 "Extract text from this PDF: [file path]"

### 带表格 / With Tables
> 🇨🇳 "提取这个 PDF，包括里面的表格"
> 🇬🇧 "Extract this PDF including tables"

### 扫描件 OCR / Scanned PDF OCR
> 🇨🇳 "这是扫描的 PDF，需要 OCR 识别"
> 🇬🇧 "This is a scanned PDF, needs OCR"

---

## 6. 批量处理 / Batch Processing

### 场景 / Scenario
一次性处理多个文件
Process multiple files at once

### 使用方法 / How to Use
> 🇨🇳 "帮我批量处理 input 文件夹下的所有文件"
> 🇬🇧 "Batch process all files in the input folder"

---

## 7. 格式转换 / Format Conversion

### 场景 / Scenario
将已有的 Markdown 转录导出为其他格式
Export existing Markdown transcripts to other formats

### 使用方法 / How to Use
> 🇨🇳 "把这个转录结果导出为 SRT 字幕"
> 🇬🇧 "Export this transcript to SRT subtitles"

### 支持格式 / Supported Formats
- SRT - 视频字幕 / Video subtitles
- VTT - Web 字幕 / Web subtitles
- JSON - 结构化数据 / Structured data
- TXT - 纯文本 / Plain text

---

## 8. 图像文字识别 / Image OCR

### 场景 / Scenario
从截图、照片中提取文字
Extract text from screenshots, photos

### 使用方法 / How to Use
> 🇨🇳 "识别这张图片中的文字"
> 🇬🇧 "Extract text from this image"

---

## 自定义组合 / Custom Combinations

你可以组合使用多个功能 / You can combine multiple features:

> 🇨🇳 "转录会议录音，识别说话人，生成会议纪要，并导出 SRT 字幕"
> 🇬🇧 "Transcribe meeting, identify speakers, generate summary, export SRT"

> 🇨🇳 "批量处理 PDF 文件夹，提取所有文本和表格"
> 🇬🇧 "Batch process PDF folder, extract all text and tables"

AI 会根据你的需求自动选择合适的处理流程。
AI will automatically choose the best processing workflow for your needs.

---

## 语言提示 / Language Tips

- 用中文提问，AI 会用中文回复 / Ask in Chinese, get Chinese response
- Ask in English, AI responds in English
- 可以随时切换语言 / You can switch languages anytime
