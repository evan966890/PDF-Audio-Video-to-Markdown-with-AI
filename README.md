# PDF-Audio-video2Markdown

[![Python 3.10-3.12](https://img.shields.io/badge/Python-3.10--3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

将 PDF / 音频 / 视频 / 图像 智能转换为 Markdown 文本的命令行工具。

## 功能特点

- **多格式支持**: PDF、音频(MP3/WAV/M4A)、视频(MP4/AVI/MKV)、图像(PNG/JPG)
- **智能处理**: 自动识别文件类型，智能选择最优处理策略
- **PDF 智能识别**: 自动判断文字层/扫描件，按需 OCR
- **大文件处理**: 音视频自动分段，避免内存溢出
- **重试机制**: 内置自动重试，确保处理成功
- **完全离线**: 所有处理本地完成，保护隐私
- **零配置**: 自动安装依赖，开箱即用

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/PDF-Audio-video2Markdown.git
cd PDF-Audio-video2Markdown
```

### 2. 配置环境

```bash
cd scripts
python setup_environment.py
```

脚本会自动：
- 检查 Python 版本（需 3.10-3.12）
- 安装所有依赖
- 验证各引擎可用性

### 3. 运行测试

```bash
python run_e2e_test.py
```

## 使用方法

### 处理单个文件

```bash
python scripts/process_file.py <文件路径> [输出目录]

# 示例
python scripts/process_file.py ./input/meeting.mp4
python scripts/process_file.py ./input/report.pdf ./output
```

### 批量处理

```bash
python scripts/process_all.py [输入目录] [输出目录]

# 示例
python scripts/process_all.py ./input ./output
```

### 端到端测试

```bash
python scripts/run_e2e_test.py
```

会交互式询问测试文件目录，自动配置环境并循环测试直到成功。

## 支持的文件格式

| 类型 | 格式 | 说明 |
|------|------|------|
| 视频 | MP4, AVI, MKV, MOV | 会议录屏、培训视频 |
| 音频 | MP3, WAV, M4A, FLAC | 会议录音、语音 |
| PDF | PDF | 文字版/扫描版自动识别 |
| 图像 | PNG, JPG, JPEG, TIFF | 截图、扫描件 |

## 处理策略

### PDF
- **有文字层**: 直接提取（约 0.1 秒/页）
- **扫描件**: 自动 OCR（约 2 秒/页）
- **混合文档**: 逐页判断，智能处理

### 音频/视频
- **小文件 (≤10MB)**: 直接转写
- **大文件 (>10MB)**: 30 秒分段处理，避免内存溢出

## 输出格式

```
output/
├── meeting.md          # 转写文本（Markdown）
├── document.md         # PDF 提取文本
├── screenshot.md       # 图像 OCR 结果
└── processing_log.json # 处理日志
```

## 目录结构

```
PDF-Audio-video2Markdown/
├── README.md                   # 项目说明
├── SKILL.md                    # AI 技能描述
├── LICENSE                     # MIT 许可证
├── scripts/
│   ├── setup_environment.py    # 环境配置
│   ├── process_file.py         # 单文件处理
│   ├── process_all.py          # 批量处理
│   └── run_e2e_test.py         # 端到端测试
├── references/
│   ├── routing_strategies.md   # 路由策略详解
│   └── troubleshooting.md      # 故障排查指南
├── input/                      # 输入文件目录
└── output/                     # 输出文件目录
```

## 系统要求

- **Python**: 3.10 - 3.12（必须，3.13+ 不兼容）
- **FFmpeg**: 推荐安装（音视频处理）
- **内存**: 建议 8GB+
- **系统**: Windows / macOS / Linux

## 依赖

自动安装，无需手动配置：

| 类别 | 依赖 | 用途 |
|------|------|------|
| PDF | pymupdf | PDF 文本提取 |
| OCR | rapidocr-onnxruntime | 图像/扫描件识别 |
| ASR | funasr | 语音转文字 |
| 音频 | pydub | 音频处理/分段 |
| 工具 | psutil | 系统资源检测 |

## 常见问题

### Python 版本错误

```
[FAIL] Python 3.13 版本过高
```

解决：安装 Python 3.10-3.12，或使用 `py -3.12` 指定版本。

### 中文乱码 (Windows)

```powershell
$env:PYTHONIOENCODING='utf-8'
python scripts/process_file.py ...
```

### 内存不足

大文件会自动分段处理。如仍失败，可修改 `scripts/process_file.py` 中的：
```python
AUDIO_CHUNK_DURATION_SEC = 15  # 改为更小的分段
```

更多问题请参考 `references/troubleshooting.md`。

## 技术架构

```
输入文件 → 文件类型检测 → 智能路由 → 处理引擎 → Markdown 输出
                              │
                    ┌─────────┴─────────┐
                    │                   │
              PDF 路由              音频路由
              │     │               │     │
           文字层  扫描件        小文件  大文件
              │     │               │     │
           PyMuPDF RapidOCR     直接处理 分段处理
                                    │
                                 FunASR
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF 处理
- [RapidOCR](https://github.com/RapidAI/RapidOCR) - OCR 引擎
- [FunASR](https://github.com/alibaba-damo-academy/FunASR) - 语音识别
