#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI Multi-format Output Module
多格式输出模块

Supported formats / 支持的格式:
- Markdown (.md)
- Plain Text (.txt) / 纯文本
- SRT subtitles (.srt) / SRT字幕
- VTT subtitles (.vtt) / VTT字幕
- JSON (.json) / JSON结构化数据

Usage / 用法:
    python scripts/output_formats.py input.md --format srt
    python scripts/output_formats.py input.md --format vtt --output custom_name
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import timedelta

@dataclass
class TranscriptSegment:
    """Transcript segment / 转录片段"""
    index: int
    start_time: float  # seconds
    end_time: float    # seconds
    text: str
    speaker: Optional[str] = None

def parse_markdown_transcript(content: str) -> List[TranscriptSegment]:
    """
    Parse transcript segments from Markdown content / 从Markdown内容解析转录片段
    Supported formats / 支持的格式:
    - [00:00:00] text content / 时间戳文本
    - [00:00:00 - 00:00:05] text content / 时间范围文本
    - **Speaker A** [00:00:00]: text content / 说话人标记文本
    """
    segments = []
    index = 0
    
    # Timestamp patterns / 时间戳模式
    patterns = [
        # [00:00:00 - 00:00:05] text
        r'\[(\d{1,2}:\d{2}:\d{2})\s*-\s*(\d{1,2}:\d{2}:\d{2})\]\s*(.+)',
        # [00:00:00] text
        r'\[(\d{1,2}:\d{2}:\d{2})\]\s*(.+)',
        # **Speaker** [00:00:00]: text
        r'\*\*(.+?)\*\*\s*\[(\d{1,2}:\d{2}:\d{2})\]:\s*(.+)',
    ]
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                groups = match.groups()
                
                if len(groups) == 3 and ':' in groups[0] and ':' in groups[1]:
                    # [start - end] text
                    start = parse_timestamp(groups[0])
                    end = parse_timestamp(groups[1])
                    text = groups[2]
                    speaker = None
                elif len(groups) == 2:
                    # [time] text
                    start = parse_timestamp(groups[0])
                    end = start + 5.0  # default 5 seconds
                    text = groups[1]
                    speaker = None
                elif len(groups) == 3:
                    # **Speaker** [time]: text
                    speaker = groups[0]
                    start = parse_timestamp(groups[1])
                    end = start + 5.0
                    text = groups[2]
                else:
                    continue
                
                index += 1
                segments.append(TranscriptSegment(
                    index=index,
                    start_time=start,
                    end_time=end,
                    text=text,
                    speaker=speaker
                ))
                break
    
    return segments

def parse_timestamp(ts: str) -> float:
    """Parse timestamp to seconds (HH:MM:SS or MM:SS) / 解析时间戳为秒数"""
    parts = ts.split(':')
    if len(parts) == 3:
        h, m, s = map(float, parts)
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:
        m, s = map(float, parts)
        return m * 60 + s
    return 0.0

def format_srt_timestamp(seconds: float) -> str:
    """Format to SRT timestamp (HH:MM:SS,mmm) / 格式化为SRT时间戳"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(int(td.total_seconds()), 3600)
    minutes, secs = divmod(remainder, 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_vtt_timestamp(seconds: float) -> str:
    """Format to VTT timestamp (HH:MM:SS.mmm) / 格式化为VTT时间戳"""
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(int(td.total_seconds()), 3600)
    minutes, secs = divmod(remainder, 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def to_srt(segments: List[TranscriptSegment]) -> str:
    """Convert to SRT format / 转换为SRT格式"""
    lines = []
    for seg in segments:
        lines.append(str(seg.index))
        lines.append(f"{format_srt_timestamp(seg.start_time)} --> {format_srt_timestamp(seg.end_time)}")
        text = seg.text
        if seg.speaker:
            text = f"[{seg.speaker}] {text}"
        lines.append(text)
        lines.append("")
    return "\n".join(lines)

def to_vtt(segments: List[TranscriptSegment]) -> str:
    """Convert to VTT format / 转换为VTT格式"""
    lines = ["WEBVTT", ""]
    for seg in segments:
        lines.append(f"{format_vtt_timestamp(seg.start_time)} --> {format_vtt_timestamp(seg.end_time)}")
        text = seg.text
        if seg.speaker:
            text = f"<v {seg.speaker}>{text}"
        lines.append(text)
        lines.append("")
    return "\n".join(lines)

def to_json(segments: List[TranscriptSegment]) -> str:
    """Convert to JSON format / 转换为JSON格式"""
    data = {
        "format": "PDF-Audio-Video-to-Markdown-with-AI transcript",
        "version": "1.0",
        "segments": [asdict(seg) for seg in segments]
    }
    return json.dumps(data, indent=2, ensure_ascii=False)

def to_txt(segments: List[TranscriptSegment]) -> str:
    """Convert to plain text format / 转换为纯文本格式"""
    lines = []
    for seg in segments:
        if seg.speaker:
            lines.append(f"{seg.speaker}: {seg.text}")
        else:
            lines.append(seg.text)
    return "\n".join(lines)

def convert_file(input_path: str, output_format: str, output_path: Optional[str] = None) -> str:
    """Convert file format / 转换文件格式"""
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    content = input_file.read_text(encoding="utf-8")
    segments = parse_markdown_transcript(content)
    
    if not segments:
        # If no timestamps, treat entire content as one segment
        segments = [TranscriptSegment(
            index=1,
            start_time=0.0,
            end_time=0.0,
            text=content
        )]
    
    # Convert format / 转换格式
    converters = {
        "srt": (to_srt, ".srt"),
        "vtt": (to_vtt, ".vtt"),
        "json": (to_json, ".json"),
        "txt": (to_txt, ".txt"),
    }
    
    if output_format not in converters:
        raise ValueError(f"Unsupported format: {output_format}. Supported: {list(converters.keys())}")
    
    converter, ext = converters[output_format]
    result = converter(segments)
    
    # Determine output path / 确定输出路径
    if output_path:
        out_file = Path(output_path)
    else:
        out_file = input_file.with_suffix(ext)
    
    out_file.write_text(result, encoding="utf-8")
    print(f"[OK] Exported: {out_file}")
    
    return str(out_file)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-format output converter")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("--format", "-f", 
                       choices=["srt", "vtt", "json", "txt"],
                       required=True, help="Output format")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    
    args = parser.parse_args()
    
    try:
        convert_file(args.input, args.format, args.output)
    except Exception as e:
        print(f"[X] Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
