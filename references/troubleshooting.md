# 故障排查指南

常见问题及解决方案。

## 环境问题

### Python 版本不兼容

**错误信息:**
```
[FAIL] Python 3.13 版本过高
```

**解决方案:**
- 安装 Python 3.10、3.11 或 3.12
- Windows: 使用 `py -3.12` 指定版本运行

### 依赖安装失败

**错误信息:**
```
[FAIL] funasr 安装失败
```

**解决方案:**
1. 检查网络连接
2. 尝试使用国内镜像：
   ```bash
   pip install funasr -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
3. 手动安装依赖：
   ```bash
   pip install torch torchvision torchaudio
   pip install funasr modelscope
   ```

### FFmpeg 未安装

**错误信息:**
```
[WARN] FFmpeg 未安装
```

**解决方案:**
1. Windows: 下载 https://ffmpeg.org/download.html
2. 解压后将 `bin` 目录添加到 PATH
3. 验证: `ffmpeg -version`

## PDF 处理问题

### OCR 识别失败

**错误信息:**
```
OCR 失败: ...
```

**解决方案:**
1. 检查图片质量（DPI 建议 ≥200）
2. 确认 RapidOCR 已正确安装
3. 检查内存是否充足

### PDF 打开失败

**错误信息:**
```
cannot open document
```

**解决方案:**
1. 确认文件未损坏
2. 检查文件是否有密码保护
3. 尝试用其他 PDF 阅读器打开验证

## 音频/视频处理问题

### 内存不足

**错误信息:**
```
RuntimeError: [enforce fail at alloc_cpu.cpp] not enough memory
```

**解决方案:**
- 文件会自动分段处理
- 如仍失败，减小 `AUDIO_CHUNK_DURATION_SEC` 值：
  ```python
  AUDIO_CHUNK_DURATION_SEC = 15  # 改为 15 秒
  ```

### ASR 模型下载失败

**错误信息:**
```
HTTPError: 404 Client Error
```

**解决方案:**
1. 检查网络连接
2. 手动下载模型：
   ```python
   from modelscope.hub.snapshot_download import snapshot_download
   snapshot_download('iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch')
   ```

### 音频格式不支持

**错误信息:**
```
CouldntDecodeError: Decoding failed
```

**解决方案:**
1. 安装 FFmpeg
2. 转换格式：
   ```bash
   ffmpeg -i input.xxx -acodec pcm_s16le output.wav
   ```

## 编码问题

### Windows 中文乱码

**错误信息:**
```
UnicodeEncodeError: 'gbk' codec can't encode character
```

**解决方案:**
```powershell
$env:PYTHONIOENCODING='utf-8'
python scripts/process_file.py ...
```

## 通用问题

### 文件路径包含空格

**解决方案:**
使用引号包裹路径：
```bash
python scripts/process_file.py "D:\My Files\meeting.mp4"
```

### 权限问题

**错误信息:**
```
PermissionError: [Errno 13] Permission denied
```

**解决方案:**
1. 以管理员身份运行
2. 检查文件是否被其他程序占用
3. 更换输出目录

## 获取帮助

如以上方案无法解决问题：

1. 查看详细错误日志：`output/processing_log.json`
2. 检查 Python 版本和依赖版本
3. 尝试在干净的虚拟环境中重新配置
