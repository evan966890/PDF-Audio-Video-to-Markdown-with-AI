---
name: PDF-Audio-video2Markdown
description: >
  智能多模态文档转 Markdown 技能，支持 PDF、音频、视频（会议录屏）、图像的统一处理。
  该技能应在用户需要将文档转换为 Markdown、音视频转录、OCR 识别、会议录屏转文字时使用。
  包含自动环境配置、智能路由、重试机制和端到端测试功能。
  完全可移植，可复制到任何电脑使用。
---

# PDF-Audio-video2Markdown

将 PDF / 音频 / 视频 / 图像 智能转换为 Markdown 文本

## 概述

PDF-Audio-video2Markdown 是一个**完全可移植**的多模态文档智能解析工具，特别适合：
- 会议录屏转文字
- PDF 文档提取与 OCR
- 音频转录
- 图像文字识别

**版本**: 1.0.0  
**Python**: 3.10-3.12（必须）

## 快速开始

### 1. 复制到目标电脑

将整个 `PDF-Audio-video2Markdown/` 文件夹复制到目标电脑。

### 2. 配置环境

```bash
cd PDF-Audio-video2Markdown/scripts
python setup_environment.py
```

### 3. 准备文件

将待处理文件放入 `./input/` 目录。

### 4. 运行测试

```bash
python scripts/run_e2e_test.py
```

## 使用方法

### 处理单个文件

```bash
python scripts/process_file.py <文件路径> [输出目录]
```

### 批量处理

```bash
python scripts/process_all.py [输入目录] [输出目录]
```

## 支持格式

| 类型 | 格式 |
|------|------|
| 视频 | MP4, AVI, MKV, MOV |
| 音频 | MP3, WAV, M4A, FLAC |
| PDF | PDF（文字版/扫描版自动识别） |
| 图像 | PNG, JPG, JPEG, TIFF |

## 参考文档

- `references/routing_strategies.md` - 路由策略详解
- `references/troubleshooting.md` - 常见问题排查
