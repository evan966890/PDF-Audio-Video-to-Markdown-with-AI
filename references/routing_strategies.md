# 路由策略详解

DocPipe 使用智能路由系统自动选择最优处理策略。

## PDF 路由策略

### 判断逻辑

```
每页文字字符数 >= 50 → 有文字层 → 直接提取
每页文字字符数 <  50 → 需要 OCR → RapidOCR 处理
```

### 策略类型

| 策略 | 触发条件 | 处理方式 | 速度 |
|------|----------|----------|------|
| `pdf_text` | 所有页面有文字层 | PyMuPDF 直接提取 | ~0.1s/页 |
| `pdf_ocr` | 有页面需要 OCR | RapidOCR 识别 | ~2s/页 |
| `pdf_hybrid` | 混合情况 | 逐页判断 | 取决于 OCR 比例 |

### 阈值配置

```python
PDF_TEXT_MIN_CHARS = 50  # 每页最少字符数
```

## 音频/视频路由策略

### 判断逻辑

```
文件大小 <= 10MB → 小文件 → 直接处理
文件大小 >  10MB → 大文件 → 分段处理（30秒/段）
```

### 策略类型

| 策略 | 触发条件 | 处理方式 | 优点 |
|------|----------|----------|------|
| `audio_direct` | 文件 ≤10MB | 一次性加载处理 | 快速 |
| `audio_chunked` | 文件 >10MB | 30秒分段处理 | 内存安全 |
| `video_direct` | 提取音频 ≤10MB | 提取后直接处理 | 快速 |
| `video_chunked` | 提取音频 >10MB | 提取后分段处理 | 内存安全 |

### 阈值配置

```python
AUDIO_SIZE_THRESHOLD_MB = 10     # 直接处理最大文件大小
AUDIO_CHUNK_DURATION_SEC = 30    # 分段时长（秒）
```

### 内存估算

```
文件大小(MB) × 0.45 ≈ 所需内存(GB)

示例：
- 10MB 音频 → ~4.5GB 内存
- 24MB 音频 → ~11GB 内存（需要分段）
```

## 图像路由策略

### 策略类型

| 策略 | 处理方式 |
|------|----------|
| `image_ocr` | RapidOCR 识别 |

图像处理相对简单，统一使用 OCR。

## 视频处理流程

```
视频文件 → pydub 提取音频 → 临时 WAV 文件 → 音频路由判断 → 处理
```

## 重试机制

每个文件处理最多重试 3 次：

```python
MAX_RETRIES = 3
```

端到端测试最多重试 10 次：

```python
MAX_TOTAL_RETRIES = 10
```

## 自定义配置

如需修改阈值，编辑 `scripts/process_file.py` 中的配置：

```python
MAX_RETRIES = 3                    # 单文件重试次数
AUDIO_SIZE_THRESHOLD_MB = 10       # 音频分段阈值
AUDIO_CHUNK_DURATION_SEC = 30      # 分段时长
PDF_TEXT_MIN_CHARS = 50            # PDF OCR 判断阈值
```
