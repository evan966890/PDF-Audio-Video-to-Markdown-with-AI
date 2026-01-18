#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI Single File Processor
单文件处理器

Features / 功能:
1. Smart file type detection / 智能文件类型检测
2. Auto-select processing strategy / 自动选择处理策略
3. Built-in retry mechanism / 内置重试机制
4. Detailed processing logs / 详细处理日志

Usage / 用法:
    python process_file.py <file_path> [output_dir]
    
Example / 示例:
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

# Config / 配置
MAX_RETRIES = 3
AUDIO_SIZE_THRESHOLD_MB = 10  # Use chunked processing above this size / 大于此大小使用分段处理
AUDIO_CHUNK_DURATION_SEC = 30  # Chunk duration / 分段时长（秒）
PDF_TEXT_MIN_CHARS = 50  # Min chars per page, below needs OCR / 每页最少字符数，低于此需要OCR


@dataclass
class ProcessResult:
    """Processing result / 处理结果"""
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


# File type mapping / 文件类型映射
FILE_TYPE_MAP = {
    ".pdf": "pdf",
    ".png": "image", ".jpg": "image", ".jpeg": "image", ".tiff": "image", ".tif": "image",
    ".mp3": "audio", ".wav": "audio", ".m4a": "audio", ".flac": "audio", ".ogg": "audio",
    ".mp4": "video", ".avi": "video", ".mkv": "video", ".mov": "video", ".webm": "video",
}


def detect_file_type(path: Path) -> str:
    """Detect file type / 检测文件类型"""
    ext = path.suffix.lower()
    return FILE_TYPE_MAP.get(ext, "unknown")


def get_file_hash(path: Path) -> str:
    """Calculate file SHA256 / 计算文件SHA256"""
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()[:16]


# ============== PDF Processing / PDF处理 ==============

def init_ocr_engine():
    """Initialize OCR engine / 初始化OCR引擎"""
    try:
        from rapidocr_onnxruntime import RapidOCR
        return RapidOCR()
    except ImportError:
        print("  [WARN] RapidOCR not installed, OCR unavailable")
        return None


def ocr_page(page, ocr_engine, dpi: int = 200) -> str:
    """OCR a PDF page / OCR处理PDF页面"""
    if ocr_engine is None:
        return ""
    
    try:
        import fitz
        import numpy as np
        
        mat = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        img = np.frombuffer(mat.samples, dtype=np.uint8).reshape(mat.height, mat.width, mat.n)
        
        if mat.n == 4:  # RGBA
            img = img[:, :, :3]
        if mat.n >= 3:
            img = img[:, :, ::-1].copy()
        
        result = ocr_engine(img)
        if result and result[0]:
            return "\n".join([item[1] for item in result[0]])
    except Exception as e:
        print(f"    OCR failed: {e}")
    
    return ""


def process_pdf(path: Path, output_dir: Path) -> ProcessResult:
    """Process PDF file / 处理PDF文件"""
    result = ProcessResult(file_path=str(path), file_type="pdf")
    
    try:
        import fitz
        
        doc = fitz.open(path)
        total_pages = len(doc)
        all_text = []
        ocr_pages = 0
        
        ocr_engine = None
        
        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()
            
            if len(text.strip()) < PDF_TEXT_MIN_CHARS:
                if ocr_engine is None:
                    ocr_engine = init_ocr_engine()
                
                print(f"    Page {page_num + 1}/{total_pages}: OCR...", end="", flush=True)
                ocr_text = ocr_page(page, ocr_engine)
                if ocr_text:
                    text = ocr_text
                    ocr_pages += 1
                    print(f" {len(text)} chars")
                else:
                    print(" no result")
            else:
                print(f"    Page {page_num + 1}/{total_pages}: text extracted {len(text)} chars")
            
            if text.strip():
                all_text.append(text)
        
        doc.close()
        
        full_text = "\n\n".join(all_text)
        output_file = output_dir / f"{path.stem}.md"
        output_file.write_text(f"# {path.name}\n\n{full_text}", encoding="utf-8")
        
        result.success = True
        result.strategy = f"pdf_{'ocr' if ocr_pages > 0 else 'text'}"
        result.output_path = str(output_file)
        result.text_length = len(full_text)
        
        print(f"    Strategy: {result.strategy} (OCR {ocr_pages}/{total_pages} pages)")
        
    except Exception as e:
        result.error = str(e)
        traceback.print_exc()
    
    return result


# ============== Audio/Video Processing / 音视频处理 ==============

def get_audio_duration(path: Path) -> float:
    """Get audio duration in seconds / 获取音频时长（秒）"""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(str(path))
        return len(audio) / 1000.0
    except Exception:
        return path.stat().st_size / (128 * 1024 / 8)


def process_audio_direct(path: Path) -> str:
    """Process audio directly / 直接处理音频"""
    from funasr import AutoModel
    
    print("    Loading ASR model...", flush=True)
    model = AutoModel(model="paraformer-zh", device="cpu", disable_update=True)
    
    print("    Transcribing...", flush=True)
    result = model.generate(input=str(path))
    
    if result and len(result) > 0:
        return result[0].get("text", "")
    return ""


def process_audio_chunked(path: Path, chunk_sec: int = AUDIO_CHUNK_DURATION_SEC) -> str:
    """Process large audio file in chunks / 分段处理大音频文件"""
    from pydub import AudioSegment
    from funasr import AutoModel
    import tempfile
    
    print("    Loading audio file...", flush=True)
    audio = AudioSegment.from_file(str(path))
    duration_ms = len(audio)
    chunk_ms = chunk_sec * 1000
    num_chunks = (duration_ms + chunk_ms - 1) // chunk_ms
    
    print(f"    Duration: {duration_ms/1000:.1f}s, {num_chunks} chunks")
    
    print("    Loading ASR model...", flush=True)
    model = AutoModel(model="paraformer-zh", device="cpu", disable_update=True)
    
    all_text = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, start in enumerate(range(0, duration_ms, chunk_ms)):
            end = min(start + chunk_ms, duration_ms)
            chunk = audio[start:end]
            chunk_path = Path(temp_dir) / f"chunk_{i}.wav"
            chunk.export(str(chunk_path), format="wav")
            
            print(f"    Processing chunk {i+1}/{num_chunks}...", end="", flush=True)
            result = model.generate(input=str(chunk_path))
            if result and len(result) > 0:
                text = result[0].get("text", "")
                all_text.append(text)
                print(f" {len(text)} chars")
            else:
                print(" no result")
    
    return "".join(all_text)


def process_audio(path: Path, output_dir: Path) -> ProcessResult:
    """Process audio file / 处理音频文件"""
    result = ProcessResult(file_path=str(path), file_type="audio")
    
    try:
        file_size_mb = path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > AUDIO_SIZE_THRESHOLD_MB:
            print(f"    Large file ({file_size_mb:.1f}MB), using chunked processing")
            text = process_audio_chunked(path)
            result.strategy = "audio_chunked"
        else:
            print(f"    Small file ({file_size_mb:.1f}MB), direct processing")
            text = process_audio_direct(path)
            result.strategy = "audio_direct"
        
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
    """Process video file (extract audio then process) / 处理视频文件（提取音频后处理）"""
    result = ProcessResult(file_path=str(path), file_type="video")
    
    try:
        import tempfile
        from pydub import AudioSegment
        
        print("    Extracting audio...", flush=True)
        
        audio = AudioSegment.from_file(str(path))
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = Path(tmp.name)
            audio.export(str(tmp_path), format="wav")
        
        file_size_mb = tmp_path.stat().st_size / (1024 * 1024)
        
        if file_size_mb > AUDIO_SIZE_THRESHOLD_MB:
            text = process_audio_chunked(tmp_path)
            result.strategy = "video_chunked"
        else:
            text = process_audio_direct(tmp_path)
            result.strategy = "video_direct"
        
        tmp_path.unlink()
        
        output_file = output_dir / f"{path.stem}.md"
        output_file.write_text(f"# {path.name}\n\n{text}", encoding="utf-8")
        
        result.success = True
        result.output_path = str(output_file)
        result.text_length = len(text)
        
    except Exception as e:
        result.error = str(e)
        traceback.print_exc()
    
    return result


# ============== Image Processing / 图像处理 ==============

def process_image(path: Path, output_dir: Path) -> ProcessResult:
    """Process image file / 处理图像文件"""
    result = ProcessResult(file_path=str(path), file_type="image")
    
    try:
        import cv2
        from rapidocr_onnxruntime import RapidOCR
        
        ocr = RapidOCR()
        img = cv2.imread(str(path))
        
        print("    OCR processing...", flush=True)
        ocr_result = ocr(img)
        
        if ocr_result and ocr_result[0]:
            text = "\n".join([item[1] for item in ocr_result[0]])
        else:
            text = ""
        
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


# ============== Main Processing / 主处理逻辑 ==============

def process_with_retry(path: Path, output_dir: Path, max_retries: int = MAX_RETRIES) -> ProcessResult:
    """Process with retry / 带重试的处理"""
    file_type = detect_file_type(path)
    result = ProcessResult(file_path=str(path), file_type=file_type)
    
    for attempt in range(max_retries):
        result.attempts = attempt + 1
        print(f"\n  Attempt {attempt + 1}/{max_retries}")
        
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
                result.error = f"Unsupported file type: {file_type}"
                break
            
            result.attempts = attempt + 1
            
            if result.success:
                break
                
        except Exception as e:
            result.error = f"{e}\n{traceback.format_exc()}"
        
        if attempt < max_retries - 1 and not result.success:
            print(f"  [RETRY] Processing failed, retrying...")
            time.sleep(1)
    
    return result


def main(input_path: str, output_dir: str = "./output"):
    """Main function / 主函数"""
    path = Path(input_path).resolve()
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        return ProcessResult(error="File not found")
    
    print(f"\n{'='*60}")
    print(f"Processing: {path.name}")
    print(f"{'='*60}")
    print(f"  Path: {path}")
    print(f"  Type: {detect_file_type(path)}")
    print(f"  Size: {path.stat().st_size / 1024:.1f} KB")
    print(f"  Output: {output}")
    
    start_time = time.time()
    result = process_with_retry(path, output)
    result.duration_sec = time.time() - start_time
    result.timestamp = datetime.now().isoformat()
    
    print(f"\n{'='*60}")
    if result.success:
        print(f"[SUCCESS] Processing complete")
        print(f"  Strategy: {result.strategy}")
        print(f"  Output: {result.output_path}")
        print(f"  Length: {result.text_length} chars")
        print(f"  Duration: {result.duration_sec:.1f}s")
        print(f"  Attempts: {result.attempts}")
    else:
        print(f"[FAILED] Processing failed")
        print(f"  Error: {result.error}")
        print(f"  Attempts: {result.attempts}")
    print(f"{'='*60}")
    
    # Save processing log / 保存处理日志
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
        print("Usage: python process_file.py <file_path> [output_dir]")
        print("Example: python process_file.py ./input/meeting.mp4")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    result = main(input_path, output_dir)
    sys.exit(0 if result.success else 1)
