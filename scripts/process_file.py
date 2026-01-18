#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DocPipe 单文件处理脚本

功能：
1. 智能检测文件类型
2. 自动选择处理策略
3. 内置重试机制
4. 详细的处理日志

用法：
    python process_file.py <文件路径> [输出目录]
    
示例：
    python process_file.py ./input/meeting.mp4
    python process_file.py ./input/report.pdf ./output
"""

import sys
import json
import time
import hashlib
import traceback
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

# 配置
MAX_RETRIES = 3
AUDIO_SIZE_THRESHOLD_MB = 10  # 超过此大小使用分段处理
AUDIO_CHUNK_DURATION_SEC = 30  # 分段时长
PDF_TEXT_MIN_CHARS = 50  # 每页最少字符数，低于此值需要 OCR


@dataclass
class ProcessResult:
    """处理结果"""
    success: bool = False
    file_path: str = ""
    file_type: str = ""
    strategy: str = ""
    output_path: str = ""
    text_length: int = 0
    error: Optional[str] = None
    attempts: int = 0
    duration_sec: float = 0
    timestamp: str = ""


# 文件类型映射
FILE_TYPE_MAP = {
    ".pdf": "pdf",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".tiff": "image", ".tif": "image",
    ".mp3": "audio", ".wav": "audio", ".m4a": "audio", ".flac": "audio", ".ogg": "audio",
    ".mp4": "video", ".avi": "video", ".mkv": "video", ".mov": "video", ".webm": "video",
}


def detect_file_type(path: Path) -> str:
    """检测文件类型"""
    ext = path.suffix.lower()
    return FILE_TYPE_MAP.get(ext, "unknown")


def get_file_hash(path: Path) -> str:
    """计算文件 SHA256"""
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()[:16]


# ============== PDF 处理 ==============

def init_ocr_engine():
    """初始化 OCR 引擎"""
    try:
        from rapidocr_onnxruntime import RapidOCR
        return RapidOCR()
    except ImportError:
        print("  [WARN] RapidOCR 未安装，OCR 功能不可用")
        return None


def ocr_page(page, ocr_engine, dpi: int = 200) -> str:
    """对 PDF 页面进行 OCR"""
    if ocr_engine is None:
        return ""
    
    try:
        import fitz
        import numpy as np
        
        # 将页面转换为图像
        mat = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        img = np.frombuffer(mat.samples, dtype=np.uint8).reshape(mat.height, mat.width, mat.n)
        
        # RGB -> BGR for OpenCV
        if mat.n == 4:  # RGBA
            img = img[:, :, :3]
        if mat.n >= 3:
            img = img[:, :, ::-1].copy()
        
        # 执行 OCR
        result = ocr_engine(img)
        if result and result[0]:
            return "\n".join([item[1] for item in result[0]])
    except Exception as e:
        print(f"    OCR 失败: {e}")
    
    return ""


def process_pdf(path: Path, output_dir: Path) -> ProcessResult:
    """处理 PDF 文件"""
    result = ProcessResult(file_path=str(path), file_type="pdf")
    
    try:
        import fitz
        
        doc = fitz.open(path)
        total_pages = len(doc)
        all_text = []
        ocr_pages = 0
        
        # 检查是否需要 OCR
        ocr_engine = None
        
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            
            # 判断是否需要 OCR
            if len(text.strip()) < PDF_TEXT_MIN_CHARS:
                if ocr_engine is None:
                    ocr_engine = init_ocr_engine()
                
                print(f"    第 {page_num + 1}/{total_pages} 页: OCR 识别中...", end="", flush=True)
                ocr_text = ocr_page(page, ocr_engine)
                if ocr_text:
                    text = ocr_text
                    ocr_pages += 1
                    print(f" {len(text)} 字符")
                else:
                    print(" 无结果")
            else:
                print(f"    第 {page_num + 1}/{total_pages} 页: 文字提取 {len(text)} 字符")
            
            if text.strip():
                all_text.append(text)
        
        doc.close()
        
        # 保存结果
        full_text = "\n\n".join(all_text)
        output_file = output_dir / f"{path.stem}.md"
        output_file.write_text(f"# {path.name}\n\n{full_text}", encoding="utf-8")
        
        result.success = True
        result.strategy = f"pdf_{'ocr' if ocr_pages > 0 else 'text'}"
        result.output_path = str(output_file)
        result.text_length = len(full_text)
        
        print(f"    策略: {result.strategy} (OCR {ocr_pages}/{total_pages} 页)")
        
    except Exception as e:
        result.error = str(e)
        traceback.print_exc()
    
    return result


# ============== 音频/视频处理 ==============

def get_audio_duration(path: Path) -> float:
    """获取音频时长（秒）"""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(str(path))
        return len(audio) / 1000.0
    except Exception:
        # 根据文件大小估算（假设 128kbps）
        return path.stat().st_size / (128 * 1024 / 8)


def process_audio_direct(path: Path) -> str:
    """直接处理音频"""
    from funasr import AutoModel
    
    print("    加载 ASR 模型...", flush=True)
    model = AutoModel(model="paraformer-zh", device="cpu", disable_update=True)
    
    print("    转写中...", flush=True)
    result = model.generate(input=str(path))
    
    if result and len(result) > 0:
        return result[0].get("text", "")
    return ""


def process_audio_chunked(path: Path, chunk_sec: int = AUDIO_CHUNK_DURATION_SEC) -> str:
    """分段处理大音频文件"""
    from pydub import AudioSegment
    from funasr import AutoModel
    import tempfile
    
    print("    加载音频文件...", flush=True)
    audio = AudioSegment.from_file(str(path))
    duration_ms = len(audio)
    chunk_ms = chunk_sec * 1000
    num_chunks = (duration_ms + chunk_ms - 1) // chunk_ms
    
    print(f"    音频时长: {duration_ms/1000:.1f}s, 分 {num_chunks} 段处理")
    
    print("    加载 ASR 模型...", flush=True)
    model = AutoModel(model="paraformer-zh", device="cpu", disable_update=True)
    
    all_text = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, start in enumerate(range(0, duration_ms, chunk_ms)):
            end = min(start + chunk_ms, duration_ms)
            chunk = audio[start:end]
            chunk_path = Path(temp_dir) / f"chunk_{i}.wav"
            chunk.export(str(chunk_path), format="wav")
            
            print(f"    处理分段 {i+1}/{num_chunks}...", end="", flush=True)
            result = model.generate(input=str(chunk_path))
            if result and len(result) > 0:
                text = result[0].get("text", "")
                all_text.append(text)
                print(f" {len(text)} 字符")
            else:
                print(" 无结果")
    
    return "".join(all_text)


def process_audio(path: Path, output_dir: Path) -> ProcessResult:
    """处理音频文件"""
    result = ProcessResult(file_path=str(path), file_type="audio")
    
    try:
        file_size_mb = path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > AUDIO_SIZE_THRESHOLD_MB:
            print(f"    大文件 ({file_size_mb:.1f}MB)，使用分段处理")
            text = process_audio_chunked(path)
            result.strategy = "audio_chunked"
        else:
            print(f"    小文件 ({file_size_mb:.1f}MB)，直接处理")
            text = process_audio_direct(path)
            result.strategy = "audio_direct"
        
        # 保存结果
        output_file = output_dir / f"{path.stem}.md"
        output_file.write_text(f"# {path.name}\n\n{text}", encoding="utf-8")
        
        result.success = True
        result.output_path = str(output_file)
        result.text_length = len(text)
        
    except Exception as e:
        result.error = str(e)
        traceback.print_exc()
    
    return result


def process_video(path: Path, output_dir: Path) -> ProcessResult:
    """处理视频文件（提取音频后处理）"""
    result = ProcessResult(file_path=str(path), file_type="video")
    
    try:
        import tempfile
        from pydub import AudioSegment
        
        print("    提取音频...", flush=True)
        
        # 直接用 pydub 提取音频
        audio = AudioSegment.from_file(str(path))
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            audio.export(str(tmp_path), format="wav")
        
        # 处理提取的音频
        file_size_mb = tmp_path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > AUDIO_SIZE_THRESHOLD_MB:
            text = process_audio_chunked(tmp_path)
            result.strategy = "video_chunked"
        else:
            text = process_audio_direct(tmp_path)
            result.strategy = "video_direct"
        
        # 清理临时文件
        tmp_path.unlink()
        
        # 保存结果
        output_file = output_dir / f"{path.stem}.md"
        output_file.write_text(f"# {path.name}\n\n{text}", encoding="utf-8")
        
        result.success = True
        result.output_path = str(output_file)
        result.text_length = len(text)
        
    except Exception as e:
        result.error = str(e)
        traceback.print_exc()
    
    return result


# ============== 图像处理 ==============

def process_image(path: Path, output_dir: Path) -> ProcessResult:
    """处理图像文件"""
    result = ProcessResult(file_path=str(path), file_type="image")
    
    try:
        import cv2
        from rapidocr_onnxruntime import RapidOCR
        
        ocr = RapidOCR()
        img = cv2.imread(str(path))
        
        print("    OCR 识别中...", flush=True)
        ocr_result = ocr(img)
        
        if ocr_result and ocr_result[0]:
            text = "\n".join([item[1] for item in ocr_result[0]])
        else:
            text = ""
        
        # 保存结果
        output_file = output_dir / f"{path.stem}.md"
        output_file.write_text(f"# {path.name}\n\n{text}", encoding="utf-8")
        
        result.success = True
        result.strategy = "image_ocr"
        result.output_path = str(output_file)
        result.text_length = len(text)
        
    except Exception as e:
        result.error = str(e)
        traceback.print_exc()
    
    return result


# ============== 主处理函数 ==============

def process_with_retry(path: Path, output_dir: Path, max_retries: int = MAX_RETRIES) -> ProcessResult:
    """带重试的处理"""
    file_type = detect_file_type(path)
    result = ProcessResult(file_path=str(path), file_type=file_type)
    
    for attempt in range(max_retries):
        result.attempts = attempt + 1
        print(f"\n  尝试 {attempt + 1}/{max_retries}")
        
        try:
            if file_type == "pdf":
                result = process_pdf(path, output_dir)
            elif file_type == "audio":
                result = process_audio(path, output_dir)
            elif file_type == "video":
                result = process_video(path, output_dir)
            elif file_type == "image":
                result = process_image(path, output_dir)
            else:
                result.error = f"不支持的文件类型: {file_type}"
                break
            
            result.attempts = attempt + 1
            
            if result.success:
                break
                
        except Exception as e:
            result.error = f"{e}\n{traceback.format_exc()}"
        
        if attempt < max_retries - 1 and not result.success:
            print(f"  [RETRY] 处理失败，重试中...")
            time.sleep(1)
    
    return result


def main(input_path: str, output_dir: str = "./output"):
    """主函数"""
    path = Path(input_path).resolve()
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    
    if not path.exists():
        print(f"[ERROR] 文件不存在: {path}")
        return ProcessResult(error="File not found")
    
    print(f"\n{'='*60}")
    print(f"处理文件: {path.name}")
    print(f"{'='*60}")
    print(f"  路径: {path}")
    print(f"  类型: {detect_file_type(path)}")
    print(f"  大小: {path.stat().st_size / 1024:.1f} KB")
    print(f"  输出: {output}")
    
    start_time = time.time()
    result = process_with_retry(path, output)
    result.duration_sec = time.time() - start_time
    result.timestamp = datetime.now().isoformat()
    
    print(f"\n{'='*60}")
    if result.success:
        print(f"[SUCCESS] 处理成功")
        print(f"  策略: {result.strategy}")
        print(f"  输出: {result.output_path}")
        print(f"  字数: {result.text_length}")
        print(f"  用时: {result.duration_sec:.1f}s")
        print(f"  尝试: {result.attempts} 次")
    else:
        print(f"[FAILED] 处理失败")
        print(f"  错误: {result.error}")
        print(f"  尝试: {result.attempts} 次")
    print(f"{'='*60}")
    
    # 保存处理日志
    log_file = output / "processing_log.json"
    logs = []
    if log_file.exists():
        try:
            logs = json.loads(log_file.read_text(encoding="utf-8"))
        except:
            logs = []
    logs.append(asdict(result))
    log_file.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python process_file.py <文件路径> [输出目录]")
        print("示例: python process_file.py ./input/meeting.mp4")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    result = main(input_path, output_dir)
    sys.exit(0 if result.success else 1)
