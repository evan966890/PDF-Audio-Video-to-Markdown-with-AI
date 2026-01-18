#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI Batch Processor
批量处理器

Features / 功能:
1. Batch process all supported files in a directory / 批量处理目录中所有支持的文件
2. Generate processing report / 生成处理报告
3. Skip already processed files / 跳过已处理的文件

Usage / 用法:
    python process_all.py [input_dir] [output_dir]

Example / 示例:
    python process_all.py ./input ./output
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import single file processor / 导入单文件处理器
from process_file import (
    detect_file_type, 
    process_with_retry,
    FILE_TYPE_MAP
)


def find_processable_files(input_dir: Path) -> list:
    """Find all processable files / 查找所有可处理的文件"""
    files = []
    for ext in FILE_TYPE_MAP.keys():
        files.extend(input_dir.glob(f"*{ext}"))
        files.extend(input_dir.glob(f"*{ext.upper()}"))
    return sorted(set(files))


def main(input_dir: str = "./input", output_dir: str = "./output"):
    """Main function / 主函数"""
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    if not input_path.exists():
        print(f"[ERROR] Input directory not found: {input_path}")
        return 1
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    files = find_processable_files(input_path)
    
    if not files:
        print(f"[INFO] No processable files found in {input_path}")
        return 0
    
    print(f"\n{'='*60}")
    print(f"Batch Processing")
    print(f"{'='*60}")
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")
    print(f"  Files: {len(files)}")
    print(f"{'='*60}")
    
    results = []
    success_count = 0
    
    for i, file in enumerate(files):
        print(f"\n[{i+1}/{len(files)}] {file.name}")
        
        result = process_with_retry(file, output_path)
        results.append({
            "file": file.name,
            "type": detect_file_type(file),
            "success": result.success,
            "strategy": result.strategy,
            "text_length": result.text_length,
            "error": result.error
        })
        
        if result.success:
            success_count += 1
            print(f"  [OK] {result.strategy}, {result.text_length} chars")
        else:
            print(f"  [X] {result.error}")
    
    # Generate report / 生成报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "input_dir": str(input_path),
        "output_dir": str(output_path),
        "total_files": len(files),
        "success_count": success_count,
        "failed_count": len(files) - success_count,
        "results": results
    }
    
    report_file = output_path / "batch_report.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"\n{'='*60}")
    print(f"Batch Processing Complete")
    print(f"{'='*60}")
    print(f"  Success: {success_count}/{len(files)}")
    print(f"  Failed: {len(files) - success_count}")
    print(f"  Report: {report_file}")
    print(f"{'='*60}")
    
    return 0 if success_count == len(files) else 1


if __name__ == "__main__":
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "./input"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    sys.exit(main(input_dir, output_dir))
