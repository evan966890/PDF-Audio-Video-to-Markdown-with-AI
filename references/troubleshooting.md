# Troubleshooting Guide / 故障排查指南

Common problems and solutions.

常见问题及解决方案。

---

## Environment Issues / 环境问题

### Python Version Incompatible / Python 版本不兼容

**Error / 错误信息:**
```
[FAIL] Python 3.13 版本过高
[FAIL] Python version too high
```

**Solution / 解决方案:**
- Install Python 3.10, 3.11, or 3.12 / 安装 Python 3.10、3.11 或 3.12
- Windows: Use `py -3.12` to specify version / 使用 `py -3.12` 指定版本运行

### Dependency Installation Failed / 依赖安装失败

**Error / 错误信息:**
```
[FAIL] funasr installation failed
[FAIL] funasr 安装失败
```

**Solution / 解决方案:**

1. Check network connection / 检查网络连接

2. Try mirror source (China) / 尝试使用国内镜像：
   ```bash
   pip install funasr -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. Manual installation / 手动安装依赖：
   ```bash
   pip install torch torchvision torchaudio
   pip install funasr modelscope
   ```

### FFmpeg Not Installed / FFmpeg 未安装

**Error / 错误信息:**
```
[WARN] FFmpeg not found
[WARN] FFmpeg 未安装
```

**Solution / 解决方案:**

| OS | Command |
|----|---------|
| Windows | `winget install FFmpeg` or download from https://ffmpeg.org |
| macOS | `brew install ffmpeg` |
| Linux | `sudo apt install ffmpeg` |

After installation, verify / 安装后验证: `ffmpeg -version`

---

## PDF Processing Issues / PDF 处理问题

### OCR Recognition Failed / OCR 识别失败

**Error / 错误信息:**
```
OCR failed: ...
OCR 失败: ...
```

**Solution / 解决方案:**
1. Check image quality (DPI ≥200 recommended) / 检查图片质量（DPI 建议 ≥200）
2. Confirm RapidOCR is properly installed / 确认 RapidOCR 已正确安装
3. Check if memory is sufficient / 检查内存是否充足

### PDF Open Failed / PDF 打开失败

**Error / 错误信息:**
```
cannot open document
```

**Solution / 解决方案:**
1. Confirm file is not corrupted / 确认文件未损坏
2. Check if file is password protected / 检查文件是否有密码保护
3. Try opening with another PDF reader / 尝试用其他 PDF 阅读器打开验证

---

## Audio/Video Processing Issues / 音频/视频处理问题

### Out of Memory / 内存不足

**Error / 错误信息:**
```
RuntimeError: [enforce fail at alloc_cpu.cpp] not enough memory
```

**Solution / 解决方案:**
- Files are automatically chunked / 文件会自动分段处理
- If still failing, reduce `AUDIO_CHUNK_DURATION_SEC` / 如仍失败，减小分段时长：
  ```python
  AUDIO_CHUNK_DURATION_SEC = 15  # Change to 15 seconds / 改为 15 秒
  ```

### ASR Model Download Failed / ASR 模型下载失败

**Error / 错误信息:**
```
HTTPError: 404 Client Error
```

**Solution / 解决方案:**

1. Check network connection / 检查网络连接

2. Manual model download / 手动下载模型：
   ```python
   from modelscope.hub.snapshot_download import snapshot_download
   snapshot_download('iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch')
   ```

### Audio Format Not Supported / 音频格式不支持

**Error / 错误信息:**
```
CouldntDecodeError: Decoding failed
```

**Solution / 解决方案:**

1. Install FFmpeg / 安装 FFmpeg

2. Convert format / 转换格式：
   ```bash
   ffmpeg -i input.xxx -acodec pcm_s16le output.wav
   ```

---

## Encoding Issues / 编码问题

### Windows Chinese Garbled Text / Windows 中文乱码

**Error / 错误信息:**
```
UnicodeEncodeError: 'gbk' codec can't encode character
```

**Solution / 解决方案:**
```powershell
$env:PYTHONIOENCODING='utf-8'
python scripts/process_file.py ...
```

Or add to script / 或在脚本中添加:
```python
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

---

## General Issues / 通用问题

### File Path Contains Spaces / 文件路径包含空格

**Solution / 解决方案:**

Use quotes to wrap path / 使用引号包裹路径：
```bash
python scripts/process_file.py "D:\My Files\meeting.mp4"
```

### Permission Error / 权限问题

**Error / 错误信息:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution / 解决方案:**
1. Run as administrator / 以管理员身份运行
2. Check if file is locked by another program / 检查文件是否被其他程序占用
3. Change output directory / 更换输出目录

### Processing Takes Too Long / 处理时间过长

**Solution / 解决方案:**

| Issue 问题 | Solution 解决方案 |
|-----------|-------------------|
| Large video / 大视频 | Use higher RAM or chunk smaller / 使用更大内存或减小分段 |
| Slow OCR / OCR 较慢 | Reduce DPI in config / 降低配置中的 DPI |
| CPU at 100% / CPU 满载 | Normal for transcription / 转录时正常 |

---

## Getting Help / 获取帮助

If the above solutions don't work:

如以上方案无法解决问题：

1. **Check detailed error log / 查看详细错误日志:**
   ```
   output/processing_log.json
   ```

2. **Verify environment / 检查环境:**
   ```bash
   python scripts/check_dependencies.py
   ```

3. **Try clean virtual environment / 尝试干净的虚拟环境:**
   ```bash
   python -m venv fresh_env
   fresh_env\Scripts\activate  # Windows
   source fresh_env/bin/activate  # Linux/macOS
   python scripts/setup_environment.py
   ```

4. **Open an issue / 提交问题:**
   - GitHub: https://github.com/evan966890/PDF-Audio-Video-to-Markdown-with-AI/issues
   - Include: error log, Python version, OS / 附上：错误日志、Python版本、操作系统

---

## Quick Reference / 快速参考

| Problem 问题 | Quick Fix 快速修复 |
|--------------|-------------------|
| Python version / Python 版本 | Install 3.10-3.12 / 安装 3.10-3.12 |
| FFmpeg missing / FFmpeg 缺失 | `winget install FFmpeg` |
| Out of memory / 内存不足 | Reduce chunk size / 减小分段大小 |
| Chinese garbled / 中文乱码 | `$env:PYTHONIOENCODING='utf-8'` |
| Permission denied / 权限拒绝 | Run as admin / 管理员运行 |
