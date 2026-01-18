#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DocPipe 批量处理脚本

功能：
1. 扫描目录下所有支持的文件
2. 智能排序（PDF 优先，然后按大小）
3. 批量处理，跳过已处理文件
4. 生成处理报告

用法：
    python process_all.py [输入目录] [输出目录]
    
示例：
    python process_all.py ./input ./output
    python process_all.py  # 使用默认目录
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# 导入处理函数
from process_file import (
    detect_file_type,
    process_with_retry,
    ProcessResult,
    FILE_TYPE_MAP
)


# 支持的文件扩展名
SUPPORTED_EXTENSIONS = set(FILE_TYPE_MAP.keys())

# 处理优先级（数字越小优先级越高）
TYPE_PRIORITY = {
    "pdf": 1,
    "image": 2,
    "audio": 3,
    "video": 4,
}


def scan_files(input_dir: Path) -> List[Path]:
    """扫描目录下所有支持的文件"""
    files = []
    
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(input_dir.glob(f"*{ext}"))
        files.extend(input_dir.glob(f"*{ext.upper()}"))
    
    return list(set(files))


def sort_files(files: List[Path]) -> List[Path]:
    """按优先级和大小排序文件"""
    def sort_key(path: Path):
        file_type = detect_file_type(path)
        priority = TYPE_PRIORITY.get(file_type, 99)
        size = path.stat().st_size
        return (priority, size)
    
    return sorted(files, key=sort_key)


def get_processed_files(output_dir: Path) -> set:
    """获取已处理的文件列表"""
    processed = set()
    log_file = output_dir / "processing_log.json"
    
    if log_file.exists():
        try:
            logs = json.loads(log_file.read_text(encoding="utf-8"))
            for log in logs:
                if log.get("success"):
                    processed.add(Path(log.get("file_path", "")).name)
        except:
            pass
    
    return processed


def print_header(title: str):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def main(input_dir: str = "./input", output_dir: str = "./output"):
    """主函数"""
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    print_header("DocPipe 批量处理")
    print(f"输入目录: {input_path}")
    print(f"输出目录: {output_path}")
    
    # 检查输入目录
    if not input_path.exists():
        print(f"\n[WARN] 输入目录不存在，已创建: {input_path}")
        input_path.mkdir(parents=True, exist_ok=True)
        print("请将待处理文件放入该目录后重新运行")
        return {"success": False, "reason": "No input directory"}
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 扫描文件
    print_header("扫描文件")
    files = scan_files(input_path)
    
    if not files:
        print(f"[INFO] 未找到支持的文件")
        print(f"支持的格式: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
        return {"success": True, "processed": 0, "reason": "No files found"}
    
    # 排序
    files = sort_files(files)
    
    # 获取已处理文件
    processed_files = get_processed_files(output_path)
    
    # 过滤未处理的文件
    pending_files = [f for f in files if f.name not in processed_files]
    
    print(f"总文件数: {len(files)}")
    print(f"已处理: {len(files) - len(pending_files)}")
    print(f"待处理: {len(pending_files)}")
    
    if not pending_files:
        print("\n[INFO] 所有文件已处理完成")
        return {"success": True, "processed": 0, "reason": "All files processed"}
    
    # 显示待处理文件
    print("\n待处理文件:")
    for i, f in enumerate(pending_files[:10]):
        file_type = detect_file_type(f)
        size_kb = f.stat().st_size / 1024
        print(f"  {i+1}. [{file_type}] {f.name} ({size_kb:.1f} KB)")
    
    if len(pending_files) > 10:
        print(f"  ... 还有 {len(pending_files) - 10} 个文件")
    
    # 批量处理
    print_header("开始处理")
    
    results: List[Dict] = []
    success_count = 0
    fail_count = 0
    total_time = 0
    
    for i, file_path in enumerate(pending_files):
        print(f"\n[{i+1}/{len(pending_files)}] 处理: {file_path.name}")
        
        start_time = time.time()
        result = process_with_retry(file_path, output_path)
        elapsed = time.time() - start_time
        total_time += elapsed
        
        if result.success:
            success_count += 1
            print(f"  [OK] {result.text_length} 字符, {elapsed:.1f}s")
        else:
            fail_count += 1
            print(f"  [FAIL] {result.error}")
        
        results.append({
            "file": file_path.name,
            "type": result.file_type,
            "success": result.success,
            "strategy": result.strategy,
            "text_length": result.text_length,
            "duration": elapsed,
            "error": result.error
        })
    
    # 打印摘要
    print_header("处理完成")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"总用时: {total_time:.1f}s")
    
    # 保存处理报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "input_dir": str(input_path),
        "output_dir": str(output_path),
        "total_files": len(pending_files),
        "success": success_count,
        "failed": fail_count,
        "total_time_sec": total_time,
        "results": results
    }
    
    report_file = output_path / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告已保存: {report_file}")
    
    return {
        "success": fail_count == 0,
        "processed": success_count,
        "failed": fail_count,
        "total_time": total_time
    }


if __name__ == "__main__":
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "./input"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    
    result = main(input_dir, output_dir)
    sys.exit(0 if result.get("success") else 1)
