# Routing Strategies / 路由策略详解

The skill uses a smart routing system to automatically select the optimal processing strategy.

本技能使用智能路由系统自动选择最优处理策略。

---

## PDF Routing / PDF 路由策略

### Detection Logic / 判断逻辑

```
Characters per page >= 50 → Has text layer → Direct extract
每页文字字符数 >= 50 → 有文字层 → 直接提取

Characters per page < 50 → Needs OCR → RapidOCR processing
每页文字字符数 < 50 → 需要 OCR → RapidOCR 处理
```

### Strategy Types / 策略类型

| Strategy 策略 | Trigger Condition 触发条件 | Method 处理方式 | Speed 速度 |
|--------------|---------------------------|-----------------|-----------|
| `pdf_text` | All pages have text layer / 所有页面有文字层 | PyMuPDF direct extract / 直接提取 | ~0.1s/page |
| `pdf_ocr` | Some pages need OCR / 有页面需要 OCR | RapidOCR recognition / OCR 识别 | ~2s/page |
| `pdf_hybrid` | Mixed situation / 混合情况 | Per-page detection / 逐页判断 | Depends on OCR ratio |

### Threshold Configuration / 阈值配置

```python
PDF_TEXT_MIN_CHARS = 50  # Min chars per page / 每页最少字符数
```

---

## Audio/Video Routing / 音频/视频路由策略

### Detection Logic / 判断逻辑

```
File size <= 10MB → Small file → Direct processing
文件大小 <= 10MB → 小文件 → 直接处理

File size > 10MB → Large file → Chunked processing (30s/chunk)
文件大小 > 10MB → 大文件 → 分段处理（30秒/段）
```

### Strategy Types / 策略类型

| Strategy 策略 | Trigger Condition 触发条件 | Method 处理方式 | Advantage 优点 |
|--------------|---------------------------|-----------------|---------------|
| `audio_direct` | File ≤10MB | Load and process at once / 一次性加载处理 | Fast / 快速 |
| `audio_chunked` | File >10MB | 30s chunk processing / 30秒分段处理 | Memory safe / 内存安全 |
| `video_direct` | Extracted audio ≤10MB | Direct processing / 直接处理 | Fast / 快速 |
| `video_chunked` | Extracted audio >10MB | Chunked processing / 分段处理 | Memory safe / 内存安全 |

### Threshold Configuration / 阈值配置

```python
AUDIO_SIZE_THRESHOLD_MB = 10     # Max file size for direct processing / 直接处理最大文件大小
AUDIO_CHUNK_DURATION_SEC = 30    # Chunk duration (seconds) / 分段时长（秒）
```

### Memory Estimation / 内存估算

```
File size (MB) × 0.45 ≈ Required memory (GB)

Examples 示例:
- 10MB audio → ~4.5GB memory
- 24MB audio → ~11GB memory (needs chunking / 需要分段)
```

---

## Image Routing / 图像路由策略

### Strategy Types / 策略类型

| Strategy 策略 | Method 处理方式 |
|--------------|-----------------|
| `image_ocr` | RapidOCR recognition / RapidOCR 识别 |

Image processing is straightforward, uniformly using OCR.

图像处理相对简单，统一使用 OCR。

---

## Video Processing Flow / 视频处理流程

```
Video file → pydub extract audio → Temp WAV file → Audio routing → Process
视频文件 → pydub 提取音频 → 临时 WAV 文件 → 音频路由判断 → 处理
```

---

## Retry Mechanism / 重试机制

Each file processing retries up to 3 times:
每个文件处理最多重试 3 次：

```python
MAX_RETRIES = 3
```

End-to-end test retries up to 10 times:
端到端测试最多重试 10 次：

```python
MAX_TOTAL_RETRIES = 10
```

---

## Custom Configuration / 自定义配置

To modify thresholds, edit `scripts/process_file.py`:
如需修改阈值，编辑 `scripts/process_file.py`：

```python
MAX_RETRIES = 3                    # Single file retry count / 单文件重试次数
AUDIO_SIZE_THRESHOLD_MB = 10       # Audio chunking threshold / 音频分段阈值
AUDIO_CHUNK_DURATION_SEC = 30      # Chunk duration / 分段时长
PDF_TEXT_MIN_CHARS = 50            # PDF OCR detection threshold / PDF OCR 判断阈值
```

---

## Performance Tips / 性能优化建议

| Scenario 场景 | Recommendation 建议 |
|--------------|---------------------|
| Large PDF (>100 pages) / 大型 PDF | Process in batches / 分批处理 |
| Long video (>1 hour) / 长视频 | Use 16GB+ RAM / 使用 16GB+ 内存 |
| Slow OCR / OCR 较慢 | Reduce DPI setting / 降低 DPI 设置 |
| Out of memory / 内存不足 | Reduce chunk duration / 减小分段时长 |
