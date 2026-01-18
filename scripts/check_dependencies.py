#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI Dependency Check Script
依赖检查脚本

Run this script before any operation to check dependency status.
在执行任何功能前，先运行此脚本检查依赖状态。

Usage / 用法:
    python scripts/check_dependencies.py [--level basic|full|advanced]
"""

import sys
import importlib
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Dependency level definitions / 依赖级别定义
DEPENDENCY_LEVELS = {
    "basic": {
        "description": "Basic - PDF text extraction, audio/video transcription",
        "description_cn": "基础功能 - PDF文本提取、音视频转写",
        "packages": {
            "pymupdf": {"import": "fitz", "size": "~15MB"},
            "pydub": {"import": "pydub", "size": "~1MB"},
            "funasr": {"import": "funasr", "size": "~500MB"},
            "modelscope": {"import": "modelscope", "size": "~50MB"},
            "psutil": {"import": "psutil", "size": "~1MB"},
        },
        "system": ["ffmpeg"]
    },
    "ocr": {
        "description": "OCR - Scanned PDF and image text recognition",
        "description_cn": "OCR功能 - 扫描PDF和图片文字识别",
        "packages": {
            "rapidocr-onnxruntime": {"import": "rapidocr_onnxruntime", "size": "~50MB"},
            "opencv-python-headless": {"import": "cv2", "size": "~30MB"},
        }
    },
    "youtube": {
        "description": "YouTube - Get YouTube video subtitles",
        "description_cn": "YouTube转录 - 获取YouTube视频字幕",
        "packages": {
            "yt-dlp": {"import": "yt_dlp", "size": "~5MB"},
        }
    },
    "table": {
        "description": "Table extraction - Extract tables from PDF",
        "description_cn": "表格提取 - 从PDF提取表格数据",
        "packages": {
            "rapid-table": {"import": "rapid_table", "size": "~100MB"},
            "beautifulsoup4": {"import": "bs4", "size": "~1MB"},
        }
    },
    "speaker": {
        "description": "Speaker diarization - Identify speakers (requires HuggingFace Token)",
        "description_cn": "说话人分离 - 识别不同说话人 (需要HuggingFace Token)",
        "packages": {
            "pyannote.audio": {"import": "pyannote.audio", "size": "~200MB"},
            "torch": {"import": "torch", "size": "~2GB"},
        },
        "requires_token": "HUGGINGFACE_TOKEN"
    }
}

def check_python_version() -> Tuple[bool, str]:
    """Check Python version / 检查 Python 版本"""
    version = sys.version_info
    if 3 <= version.major and 10 <= version.minor <= 12:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (need 3.10-3.12 / 需要 3.10-3.12)"

def check_package(package_name: str, import_name: str) -> Tuple[bool, str]:
    """Check if a package is installed / 检查包是否已安装"""
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "installed / 已安装")
        return True, version
    except ImportError:
        return False, "not installed / 未安装"

def check_system_dependency(name: str) -> Tuple[bool, str]:
    """Check system dependency / 检查系统依赖"""
    path = shutil.which(name)
    if path:
        return True, path
    return False, "not found / 未找到"

def check_level(level: str) -> Dict:
    """Check dependencies for a specific level / 检查指定级别的依赖"""
    if level not in DEPENDENCY_LEVELS:
        return {"error": f"Unknown level / 未知级别: {level}"}
    
    config = DEPENDENCY_LEVELS[level]
    results = {
        "level": level,
        "description": config["description"],
        "description_cn": config.get("description_cn", ""),
        "packages": {},
        "system": {},
        "all_ok": True,
        "missing": []
    }
    
    # Check Python packages / 检查 Python 包
    for pkg_name, pkg_info in config.get("packages", {}).items():
        ok, version = check_package(pkg_name, pkg_info["import"])
        results["packages"][pkg_name] = {
            "installed": ok,
            "version": version,
            "size": pkg_info["size"]
        }
        if not ok:
            results["all_ok"] = False
            results["missing"].append(pkg_name)
    
    # Check system dependencies / 检查系统依赖
    for sys_dep in config.get("system", []):
        ok, path = check_system_dependency(sys_dep)
        results["system"][sys_dep] = {
            "found": ok,
            "path": path
        }
        if not ok:
            results["all_ok"] = False
            results["missing"].append(f"[system] {sys_dep}")
    
    return results

def check_all() -> Dict:
    """Check all dependency levels / 检查所有依赖级别"""
    results = {}
    for level in DEPENDENCY_LEVELS:
        results[level] = check_level(level)
    return results

def print_status_report(results: Dict):
    """Print status report / 打印状态报告"""
    print("\n" + "="*60)
    print("PDF-Audio-Video-to-Markdown-with-AI Dependency Status")
    print("PDF-Audio-Video-to-Markdown-with-AI 依赖状态")
    print("="*60)
    
    # Python version / Python 版本
    py_ok, py_ver = check_python_version()
    status = "[OK]" if py_ok else "[X]"
    print(f"\n{status} Python: {py_ver}")
    
    # Each level status / 各级别状态
    for level, data in results.items():
        if "error" in data:
            continue
        
        status = "[OK]" if data["all_ok"] else "[X]"
        desc = data['description']
        desc_cn = data.get('description_cn', '')
        print(f"\n{status} {level.upper()}: {desc}")
        if desc_cn:
            print(f"       {desc_cn}")
        
        for pkg, info in data.get("packages", {}).items():
            pkg_status = "[OK]" if info["installed"] else "[X]"
            print(f"    {pkg_status} {pkg}: {info['version']} ({info['size']})")
        
        for sys_dep, info in data.get("system", {}).items():
            sys_status = "[OK]" if info["found"] else "[X]"
            print(f"    {sys_status} {sys_dep}: {info['path']}")
    
    # Summary / 总结
    print("\n" + "-"*60)
    all_missing = []
    for level, data in results.items():
        if "missing" in data:
            all_missing.extend(data["missing"])
    
    if not all_missing:
        print("[OK] All dependencies are installed! / 所有依赖已安装!")
    else:
        print(f"[X] Missing {len(all_missing)} dependencies / 缺少 {len(all_missing)} 个依赖:")
        for m in all_missing:
            print(f"  - {m}")
        print("\nTip / 提示:")
        print("  CN: 告诉 AI '请安装缺少的依赖'")
        print("  EN: Tell AI 'Please install missing dependencies'")

def get_install_estimate(levels: List[str]) -> str:
    """Get installation estimate info / 获取安装估算信息"""
    total_size = 0
    packages = []
    
    for level in levels:
        if level in DEPENDENCY_LEVELS:
            for pkg, info in DEPENDENCY_LEVELS[level].get("packages", {}).items():
                size_str = info["size"]
                if "GB" in size_str:
                    total_size += float(size_str.replace("~", "").replace("GB", "")) * 1024
                elif "MB" in size_str:
                    total_size += float(size_str.replace("~", "").replace("MB", ""))
                packages.append(pkg)
    
    if total_size > 1024:
        size_display = f"{total_size/1024:.1f}GB"
    else:
        size_display = f"{total_size:.0f}MB"
    
    return f"Need to install {len(packages)} packages, ~{size_display} / 需安装 {len(packages)} 个包，约 {size_display}"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Check dependency status / 检查依赖状态"
    )
    parser.add_argument(
        "--level", 
        choices=list(DEPENDENCY_LEVELS.keys()) + ["all"], 
        default="all", 
        help="Dependency level to check / 要检查的依赖级别"
    )
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output JSON format / 输出 JSON 格式"
    )
    
    args = parser.parse_args()
    
    if args.level == "all":
        results = check_all()
    else:
        results = {args.level: check_level(args.level)}
    
    if args.json:
        import json
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_status_report(results)
