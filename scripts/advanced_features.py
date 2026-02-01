#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI Advanced Features Module
高级功能模块

Features / 功能:
1. Speaker Diarization - requires HuggingFace Token / 说话人分离 - 需要HuggingFace Token
2. Table Extraction / 表格提取
3. Reading Order optimization / 阅读顺序优化
4. Text Coverage calculation / 文本覆盖率计算

Usage / 用法:
    python scripts/advanced_features.py diarize audio.mp3 --output result.md
    python scripts/advanced_features.py extract-tables document.pdf
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# ============================================================
# Speaker Diarization / 说话人分离
# ============================================================

def check_speaker_diarization_deps() -> Tuple[bool, str]:
    """Check speaker diarization dependencies / 检查说话人分离依赖"""
    try:
        import torch
        import pyannote.audio
        
        token = os.environ.get('HUGGINGFACE_TOKEN') or os.environ.get('HF_TOKEN')
        if not token:
            return False, "Need to set HUGGINGFACE_TOKEN environment variable"
        
        return True, "Ready"
    except ImportError as e:
        return False, f"Missing dependency: {e}"

def run_speaker_diarization(audio_path: str, num_speakers: Optional[int] = None) -> List[Dict]:
    """
    Run speaker diarization / 运行说话人分离
    
    Args / 参数:
        audio_path: Audio file path / 音频文件路径
        num_speakers: Number of speakers (optional, auto-detect) / 说话人数量（可选，自动检测）
    
    Returns / 返回:
        Speaker segments list [{speaker, start, end}, ...] / 说话人片段列表
    """
    ok, msg = check_speaker_diarization_deps()
    if not ok:
        print(f"[X] Speaker diarization not available: {msg}")
        print("\nPlease follow these steps:")
        print("1. Tell AI: 'Please install speaker diarization feature'")
        print("2. Follow the guide to get HuggingFace Token")
        return []
    
    from pyannote.audio import Pipeline
    import torch
    import soundfile as sf  # Use soundfile to avoid torchcodec issues
    
    token = os.environ.get('HUGGINGFACE_TOKEN') or os.environ.get('HF_TOKEN')
    
    print("Loading speaker diarization model...")
    
    # pyannote 3.x uses 'token' instead of 'use_auth_token'
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=token
    )
    
    if torch.cuda.is_available():
        pipeline.to(torch.device("cuda"))
        print("[OK] Using GPU acceleration")
    
    print(f"Analyzing audio: {audio_path}")
    
    # Load audio using soundfile to avoid torchcodec compatibility issues
    try:
        data, sample_rate = sf.read(audio_path)
        waveform = torch.from_numpy(data).float()
        if len(waveform.shape) == 1:
            waveform = waveform.unsqueeze(0)
        else:
            waveform = waveform.T
        audio_in_memory = {"waveform": waveform, "sample_rate": sample_rate}
        
        if num_speakers:
            result = pipeline(audio_in_memory, num_speakers=num_speakers)
        else:
            result = pipeline(audio_in_memory)
    except Exception as e:
        print(f"[WARN] Memory loading failed, trying file path: {e}")
        # Fallback to file path
        if num_speakers:
            result = pipeline(audio_path, num_speakers=num_speakers)
        else:
            result = pipeline(audio_path)
    
    # pyannote 3.x: access Annotation via speaker_diarization attribute
    diarization = result.speaker_diarization if hasattr(result, 'speaker_diarization') else result
    
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            'speaker': speaker,
            'start': turn.start,
            'end': turn.end
        })
    
    unique_speakers = len(set(s['speaker'] for s in segments))
    print(f"[OK] Identified {unique_speakers} speakers")
    return segments

# ============================================================
# Table Extraction / 表格提取
# ============================================================

def check_table_extraction_deps() -> Tuple[bool, str]:
    """Check table extraction dependencies / 检查表格提取依赖"""
    try:
        from rapid_table import RapidTable
        return True, "Ready"
    except ImportError:
        return False, "Missing rapid-table dependency"

def extract_tables_from_pdf(pdf_path: str, output_dir: str = './output') -> List[str]:
    """
    Extract tables from PDF / 从PDF提取表格
    
    Args / 参数:
        pdf_path: PDF file path / PDF文件路径
        output_dir: Output directory / 输出目录
    
    Returns / 返回:
        List of extracted table HTML file paths / 提取的表格HTML文件路径列表
    """
    ok, msg = check_table_extraction_deps()
    if not ok:
        print(f"[X] Table extraction not available: {msg}")
        print("Tell AI: 'Please install table extraction dependencies'")
        return []
    
    import fitz
    from rapid_table import RapidTable
    import cv2
    import numpy as np
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    pdf_name = Path(pdf_path).stem
    table_engine = RapidTable()
    
    print(f"Extracting tables from: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    extracted_files = []
    table_count = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        
        img_array = np.frombuffer(pix.samples, dtype=np.uint8)
        img = img_array.reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        
        result, _ = table_engine(img)
        
        if result:
            table_count += 1
            html_file = output_path / f"{pdf_name}_table_{page_num+1}_{table_count}.html"
            html_file.write_text(result, encoding='utf-8')
            extracted_files.append(str(html_file))
            print(f"  [OK] Page {page_num+1}: extracted 1 table")
    
    doc.close()
    
    if table_count == 0:
        print("  No tables detected")
    else:
        print(f"[OK] Extracted {table_count} tables total")
    
    return extracted_files

def table_html_to_markdown(html_content: str) -> str:
    """Convert table HTML to Markdown / 将表格HTML转换为Markdown"""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return html_content
    
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    if not table:
        return html_content
    
    rows = table.find_all('tr')
    if not rows:
        return html_content
    
    md_lines = []
    
    for i, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])
        cell_texts = [cell.get_text(strip=True) for cell in cells]
        md_lines.append('| ' + ' | '.join(cell_texts) + ' |')
        
        if i == 0:
            md_lines.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
    
    return '\n'.join(md_lines)

# ============================================================
# Reading Order optimization / 阅读顺序优化
# ============================================================

def sort_by_reading_order(blocks: List[Dict]) -> List[Dict]:
    """
    Sort text blocks by reading order / 按阅读顺序排序文本块
    
    Args / 参数:
        blocks: Text blocks list, each with {x0, y0, x1, y1, text} / 文本块列表
    
    Returns / 返回:
        Sorted text blocks list / 排序后的文本块列表
    """
    if not blocks:
        return blocks
    
    line_threshold = 10
    
    lines = []
    current_line = []
    last_y = None
    
    sorted_blocks = sorted(blocks, key=lambda b: (b.get('y0', 0), b.get('x0', 0)))
    
    for block in sorted_blocks:
        y = block.get('y0', 0)
        
        if last_y is None or abs(y - last_y) <= line_threshold:
            current_line.append(block)
        else:
            if current_line:
                lines.append(sorted(current_line, key=lambda b: b.get('x0', 0)))
            current_line = [block]
        
        last_y = y
    
    if current_line:
        lines.append(sorted(current_line, key=lambda b: b.get('x0', 0)))
    
    result = []
    for line in lines:
        result.extend(line)
    
    return result

# ============================================================
# Text Coverage calculation / 文本覆盖率计算
# ============================================================

def calculate_text_coverage(pdf_path: str) -> Dict:
    """
    Calculate PDF text coverage / 计算PDF文本覆盖率
    
    Args / 参数:
        pdf_path: PDF file path / PDF文件路径
    
    Returns / 返回:
        {pages: [...], average_coverage: float, needs_ocr: bool}
    """
    import fitz
    
    doc = fitz.open(pdf_path)
    results = {
        'pages': [],
        'total_text_area': 0,
        'total_page_area': 0,
        'average_coverage': 0,
        'needs_ocr': False
    }
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        rect = page.rect
        page_area = rect.width * rect.height
        
        text_area = 0
        for block in page.get_text("dict")["blocks"]:
            if block["type"] == 0:
                bbox = block["bbox"]
                text_area += (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        
        coverage = (text_area / page_area * 100) if page_area > 0 else 0
        
        results['pages'].append({
            'page': page_num + 1,
            'coverage': round(coverage, 2)
        })
        results['total_text_area'] += text_area
        results['total_page_area'] += page_area
    
    doc.close()
    
    if results['total_page_area'] > 0:
        results['average_coverage'] = round(
            results['total_text_area'] / results['total_page_area'] * 100, 2
        )
    
    # Coverage below 5% likely needs OCR / 覆盖率低于5%可能需要OCR
    results['needs_ocr'] = results['average_coverage'] < 5
    
    return results

# ============================================================
# CLI Entry / 命令行入口
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Features Module")
    subparsers = parser.add_subparsers(dest="command")
    
    # Speaker diarization
    diarize_parser = subparsers.add_parser("diarize", help="Speaker diarization")
    diarize_parser.add_argument("audio", help="Audio file path")
    diarize_parser.add_argument("--speakers", "-n", type=int, help="Number of speakers")
    diarize_parser.add_argument("--output", "-o", help="Output file")
    
    # Table extraction
    table_parser = subparsers.add_parser("extract-tables", help="Table extraction")
    table_parser.add_argument("pdf", help="PDF file path")
    table_parser.add_argument("--output", "-o", default="./output", help="Output directory")
    
    # Text coverage
    coverage_parser = subparsers.add_parser("coverage", help="Calculate text coverage")
    coverage_parser.add_argument("pdf", help="PDF file path")
    
    args = parser.parse_args()
    
    if args.command == "diarize":
        segments = run_speaker_diarization(args.audio, args.speakers)
        if segments and args.output:
            import json
            Path(args.output).write_text(
                json.dumps(segments, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print(f"[OK] Results saved: {args.output}")
    
    elif args.command == "extract-tables":
        extract_tables_from_pdf(args.pdf, args.output)
    
    elif args.command == "coverage":
        result = calculate_text_coverage(args.pdf)
        print(f"\nText Coverage Analysis")
        print(f"{'='*40}")
        print(f"Average coverage: {result['average_coverage']}%")
        print(f"Needs OCR: {'Yes' if result['needs_ocr'] else 'No'}")
        print(f"\nPer-page coverage:")
        for p in result['pages']:
            print(f"  Page {p['page']}: {p['coverage']}%")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
