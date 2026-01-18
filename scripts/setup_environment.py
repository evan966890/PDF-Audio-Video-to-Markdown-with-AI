#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI Environment Setup Script
环境配置脚本

Features / 功能:
1. Check Python version / 检查Python版本
2. Auto-install dependencies / 自动安装依赖
3. Verify installation / 验证安装
4. Check FFmpeg / 检查FFmpeg

Usage / 用法:
    python setup_environment.py
"""

import sys
import subprocess
import shutil


def check_python_version():
    """Check Python version / 检查Python版本"""
    print("\n[1/4] Checking Python version / 检查Python版本...")
    
    version = sys.version_info
    print(f"  Current: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or not (10 <= version.minor <= 12):
        print(f"  [X] Python 3.10-3.12 required")
        print(f"      Please install a compatible Python version")
        return False
    
    print(f"  [OK] Python version compatible")
    return True


def install_dependencies():
    """Install Python dependencies / 安装Python依赖"""
    print("\n[2/4] Installing dependencies / 安装依赖...")
    
    packages = [
        "pymupdf",
        "pydub",
        "funasr",
        "modelscope",
        "psutil",
    ]
    
    optional_packages = [
        ("rapidocr-onnxruntime", "OCR support"),
        ("opencv-python-headless", "Image processing"),
    ]
    
    # Install core packages / 安装核心包
    for pkg in packages:
        print(f"  Installing {pkg}...", end="", flush=True)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                capture_output=True,
                timeout=300
            )
            if result.returncode == 0:
                print(" [OK]")
            else:
                print(f" [X] {result.stderr.decode()[:100]}")
        except Exception as e:
            print(f" [X] {e}")
    
    # Install optional packages / 安装可选包
    print("\n  Installing optional packages / 安装可选包...")
    for pkg, desc in optional_packages:
        print(f"  Installing {pkg} ({desc})...", end="", flush=True)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                capture_output=True,
                timeout=300
            )
            if result.returncode == 0:
                print(" [OK]")
            else:
                print(f" [SKIP]")
        except Exception as e:
            print(f" [SKIP]")
    
    return True


def verify_installation():
    """Verify installation / 验证安装"""
    print("\n[3/4] Verifying installation / 验证安装...")
    
    core_deps = [
        ("fitz", "PyMuPDF"),
        ("pydub", "pydub"),
        ("funasr", "FunASR"),
        ("modelscope", "ModelScope"),
        ("psutil", "psutil"),
    ]
    
    optional_deps = [
        ("rapidocr_onnxruntime", "RapidOCR"),
        ("cv2", "OpenCV"),
    ]
    
    all_ok = True
    
    for import_name, display_name in core_deps:
        try:
            __import__(import_name)
            print(f"  [OK] {display_name}")
        except ImportError:
            print(f"  [X] {display_name} - REQUIRED")
            all_ok = False
    
    for import_name, display_name in optional_deps:
        try:
            __import__(import_name)
            print(f"  [OK] {display_name} (optional)")
        except ImportError:
            print(f"  [--] {display_name} (optional, not installed)")
    
    return all_ok


def check_ffmpeg():
    """Check FFmpeg installation / 检查FFmpeg安装"""
    print("\n[4/4] Checking FFmpeg / 检查FFmpeg...")
    
    ffmpeg_path = shutil.which("ffmpeg")
    
    if ffmpeg_path:
        print(f"  [OK] FFmpeg found: {ffmpeg_path}")
        return True
    else:
        print("  [WARN] FFmpeg not found")
        print("  Audio/video processing may have issues")
        print("\n  Install FFmpeg:")
        print("    Windows: winget install FFmpeg")
        print("    macOS: brew install ffmpeg")
        print("    Linux: sudo apt install ffmpeg")
        return True  # Not blocking, just warning


def main():
    """Main function / 主函数"""
    print("="*60)
    print("PDF-Audio-Video-to-Markdown-with-AI Environment Setup")
    print("="*60)
    
    # Step 1: Check Python
    if not check_python_version():
        return 1
    
    # Step 2: Install dependencies
    install_dependencies()
    
    # Step 3: Verify
    if not verify_installation():
        print("\n[ERROR] Some required dependencies failed to install")
        print("  Try running: pip install pymupdf pydub funasr modelscope psutil")
        return 1
    
    # Step 4: Check FFmpeg
    check_ffmpeg()
    
    print("\n" + "="*60)
    print("[SUCCESS] Environment setup complete!")
    print("="*60)
    print("\nYou can now use the skill:")
    print("  python scripts/process_file.py <file_path>")
    print("  python scripts/process_all.py <input_dir>")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
