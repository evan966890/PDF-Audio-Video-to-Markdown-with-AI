#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI End-to-End Test Script
端到端测试脚本

Features / 功能:
1. Auto-configure environment / 自动配置环境
2. Interactive test directory selection / 交互式选择测试目录
3. Retry until success (max 10 times) / 重试直到成功（最多10次）

Usage / 用法:
    python run_e2e_test.py
"""

import sys
import time
from pathlib import Path

# Get script directory / 获取脚本目录
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent

# Add to path / 添加到路径
sys.path.insert(0, str(SCRIPT_DIR))


def check_environment():
    """Check if environment is ready / 检查环境是否就绪"""
    print("\n[1/4] Checking environment / 检查环境...")
    
    # Check Python version / 检查Python版本
    version = sys.version_info
    if not (3 <= version.major and 10 <= version.minor <= 12):
        print(f"  [X] Python {version.major}.{version.minor} not supported")
        print(f"      Need Python 3.10-3.12")
        return False
    print(f"  [OK] Python {version.major}.{version.minor}.{version.micro}")
    
    # Check core dependencies / 检查核心依赖
    deps = [
        ("fitz", "PyMuPDF"),
        ("pydub", "pydub"),
        ("funasr", "FunASR"),
    ]
    
    for import_name, display_name in deps:
        try:
            __import__(import_name)
            print(f"  [OK] {display_name}")
        except ImportError:
            print(f"  [X] {display_name} not installed")
            return False
    
    return True


def setup_environment():
    """Run environment setup / 运行环境配置"""
    print("\n[2/4] Setting up environment / 配置环境...")
    
    setup_script = SCRIPT_DIR / "setup_environment.py"
    if setup_script.exists():
        import subprocess
        result = subprocess.run([sys.executable, str(setup_script)], 
                              capture_output=False)
        return result.returncode == 0
    else:
        print("  [WARN] setup_environment.py not found")
        return True


def find_test_files(test_dir: Path) -> list:
    """Find test files / 查找测试文件"""
    from process_file import FILE_TYPE_MAP
    
    files = []
    for ext in FILE_TYPE_MAP.keys():
        files.extend(test_dir.glob(f"*{ext}"))
        files.extend(test_dir.glob(f"*{ext.upper()}"))
    return sorted(set(files))


def run_test(test_dir: Path, output_dir: Path) -> bool:
    """Run test on directory / 在目录上运行测试"""
    from process_file import process_with_retry
    
    files = find_test_files(test_dir)
    
    if not files:
        print(f"  [X] No test files found in {test_dir}")
        return False
    
    print(f"  Found {len(files)} test file(s)")
    
    success_count = 0
    for file in files:
        print(f"\n  Testing: {file.name}")
        result = process_with_retry(file, output_dir, max_retries=3)
        
        if result.success:
            success_count += 1
            print(f"    [OK] {result.strategy}, {result.text_length} chars")
        else:
            print(f"    [X] {result.error}")
    
    return success_count > 0


def main():
    """Main function / 主函数"""
    print("="*60)
    print("PDF-Audio-Video-to-Markdown-with-AI E2E Test")
    print("="*60)
    
    # Step 1: Check environment / 步骤1: 检查环境
    if not check_environment():
        print("\n[INFO] Running environment setup...")
        if not setup_environment():
            print("[ERROR] Environment setup failed")
            return 1
        
        # Re-check
        if not check_environment():
            print("[ERROR] Environment still not ready")
            return 1
    
    # Step 2: Get test directory / 步骤2: 获取测试目录
    print("\n[3/4] Test directory setup / 测试目录设置...")
    
    default_input = PROJECT_DIR / "input"
    default_output = PROJECT_DIR / "output"
    
    print(f"  Default input: {default_input}")
    print(f"  Default output: {default_output}")
    
    user_input = input("\n  Enter test directory (or press Enter for default): ").strip()
    
    if user_input:
        test_dir = Path(user_input).resolve()
    else:
        test_dir = default_input
    
    output_dir = default_output
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not test_dir.exists():
        print(f"\n  [X] Directory not found: {test_dir}")
        print(f"  Please place test files in: {default_input}")
        default_input.mkdir(parents=True, exist_ok=True)
        return 1
    
    # Step 3: Run test with retry / 步骤3: 运行测试（带重试）
    print(f"\n[4/4] Running E2E test / 运行端到端测试...")
    print(f"  Input: {test_dir}")
    print(f"  Output: {output_dir}")
    
    max_attempts = 10
    for attempt in range(max_attempts):
        print(f"\n--- Attempt {attempt + 1}/{max_attempts} ---")
        
        try:
            if run_test(test_dir, output_dir):
                print("\n" + "="*60)
                print("[SUCCESS] E2E test passed!")
                print("="*60)
                return 0
        except Exception as e:
            print(f"  [ERROR] {e}")
        
        if attempt < max_attempts - 1:
            print(f"\n  Retrying in 3 seconds...")
            time.sleep(3)
    
    print("\n" + "="*60)
    print("[FAILED] E2E test failed after all attempts")
    print("="*60)
    return 1


if __name__ == "__main__":
    sys.exit(main())
