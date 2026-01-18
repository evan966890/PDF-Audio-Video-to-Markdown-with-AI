#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DocPipe 环境自动配置脚本

功能：
1. 检测 Python 版本（需 3.10-3.12）
2. 检测并安装依赖
3. 验证各引擎可用性
4. 自动重试失败的安装

用法：
    python setup_environment.py
"""

import sys
import subprocess
import importlib
from pathlib import Path

# Python 版本要求
REQUIRED_PYTHON_MIN = (3, 10)
REQUIRED_PYTHON_MAX = (3, 12)

# 依赖分组
DEPENDENCIES = {
    "core": [
        "pymupdf",      # PDF 处理
        "pydantic",     # 数据模型
        "pyyaml",       # 配置文件
    ],
    "ocr": [
        "rapidocr-onnxruntime",  # OCR 引擎
        "opencv-python-headless",
        "numpy",
    ],
    "asr": [
        "funasr",       # ASR 引擎
        "modelscope",   # 模型管理
        "pydub",        # 音频处理
    ],
    "utils": [
        "psutil",       # 系统资源检测
    ]
}

# 引擎模块映射
ENGINE_MODULES = {
    "PyMuPDF": "fitz",
    "RapidOCR": "rapidocr_onnxruntime",
    "FunASR": "funasr",
    "pydub": "pydub",
    "psutil": "psutil",
}


def print_header(title: str):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def check_python_version() -> bool:
    """检查 Python 版本"""
    print_header("检查 Python 版本")
    
    version = sys.version_info[:2]
    version_str = f"{version[0]}.{version[1]}"
    
    if version < REQUIRED_PYTHON_MIN:
        print(f"[FAIL] Python {version_str} 版本过低")
        print(f"       需要 Python 3.10 - 3.12")
        return False
    
    if version > REQUIRED_PYTHON_MAX:
        print(f"[FAIL] Python {version_str} 版本过高")
        print(f"       需要 Python 3.10 - 3.12")
        print(f"       建议安装 Python 3.12")
        return False
    
    print(f"[OK] Python {version_str}")
    return True


def install_package(package: str, max_retries: int = 3) -> bool:
    """安装单个包，支持重试"""
    for attempt in range(max_retries):
        try:
            print(f"  安装 {package}... (尝试 {attempt + 1}/{max_retries})", end="", flush=True)
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "-q", "--disable-pip-version-check"],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            if result.returncode == 0:
                print(" [OK]")
                return True
            else:
                print(" [RETRY]")
                if attempt == max_retries - 1:
                    print(f"    错误: {result.stderr[:200] if result.stderr else 'Unknown error'}")
        except subprocess.TimeoutExpired:
            print(" [TIMEOUT]")
        except Exception as e:
            print(f" [ERROR] {e}")
    
    print(f"  [FAIL] {package} 安装失败")
    return False


def install_dependencies() -> dict:
    """安装所有依赖"""
    print_header("安装依赖")
    
    results = {"success": [], "failed": []}
    
    for group, packages in DEPENDENCIES.items():
        print(f"\n[{group.upper()}] 安装依赖组...")
        for pkg in packages:
            if install_package(pkg):
                results["success"].append(pkg)
            else:
                results["failed"].append(pkg)
    
    return results


def verify_engines() -> dict:
    """验证各引擎是否可用"""
    print_header("验证引擎")
    
    status = {}
    
    for name, module in ENGINE_MODULES.items():
        try:
            importlib.import_module(module)
            print(f"  [OK] {name}")
            status[name] = True
        except ImportError as e:
            print(f"  [FAIL] {name}: {e}")
            status[name] = False
        except Exception as e:
            print(f"  [WARN] {name}: {e}")
            status[name] = False
    
    return status


def check_ffmpeg() -> bool:
    """检查 FFmpeg 是否可用"""
    print_header("检查 FFmpeg")
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  [OK] {version_line[:60]}")
            return True
    except FileNotFoundError:
        print("  [WARN] FFmpeg 未安装")
        print("         音视频处理可能受限")
        print("         下载地址: https://ffmpeg.org/download.html")
    except Exception as e:
        print(f"  [WARN] FFmpeg 检查失败: {e}")
    
    return False


def print_summary(install_results: dict, engine_status: dict, ffmpeg_ok: bool):
    """打印配置摘要"""
    print_header("配置结果")
    
    print(f"\n依赖安装:")
    print(f"  成功: {len(install_results['success'])} 个")
    print(f"  失败: {len(install_results['failed'])} 个")
    
    if install_results['failed']:
        print(f"  失败列表: {', '.join(install_results['failed'])}")
    
    print(f"\n引擎状态:")
    for name, ok in engine_status.items():
        print(f"  {name}: {'[OK]' if ok else '[FAIL]'}")
    
    print(f"\nFFmpeg: {'[OK]' if ffmpeg_ok else '[WARN] 未安装'}")
    
    # 判断整体状态
    critical_engines = ["PyMuPDF", "RapidOCR", "FunASR"]
    all_critical_ok = all(engine_status.get(e, False) for e in critical_engines)
    
    print(f"\n{'='*60}")
    if all_critical_ok and len(install_results['failed']) == 0:
        print(" [SUCCESS] 环境配置完成，可以开始处理文件！")
        return True
    elif all_critical_ok:
        print(" [WARNING] 环境基本可用，部分依赖安装失败")
        return True
    else:
        print(" [FAILED] 关键引擎未就绪，请检查错误信息")
        return False


def main():
    """主函数"""
    print("\n" + "="*60)
    print("        DocPipe 环境自动配置")
    print("="*60)
    print(f"Python: {sys.version}")
    print(f"路径: {sys.executable}")
    
    # 1. 检查 Python 版本
    if not check_python_version():
        print("\n[ABORT] Python 版本不兼容，请安装 Python 3.10-3.12")
        return {"success": False, "reason": "Python version incompatible"}
    
    # 2. 安装依赖
    install_results = install_dependencies()
    
    # 3. 验证引擎
    engine_status = verify_engines()
    
    # 4. 检查 FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    # 5. 打印摘要
    success = print_summary(install_results, engine_status, ffmpeg_ok)
    
    return {
        "success": success,
        "installed": install_results['success'],
        "failed": install_results['failed'],
        "engines": engine_status,
        "ffmpeg": ffmpeg_ok
    }


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result.get("success") else 1)
