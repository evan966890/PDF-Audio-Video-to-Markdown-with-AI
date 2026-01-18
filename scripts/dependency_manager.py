#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF-Audio-Video-to-Markdown-with-AI Smart Dependency Manager
智能依赖管理器

Features / 功能:
1. Install dependencies on demand / 按需安装依赖
2. First-run setup wizard / 首次使用引导
3. Auto-retry installation / 自动重试安装
4. API key setup guidance / API Key 引导

Usage / 用法:
    python scripts/dependency_manager.py install --level basic
    python scripts/dependency_manager.py install --level full
    python scripts/dependency_manager.py wizard
"""

import sys
import subprocess
import time
from pathlib import Path
from typing import List, Optional

# Import dependency check module
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from check_dependencies import DEPENDENCY_LEVELS, check_level, check_package

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def install_package(package_name: str, retries: int = MAX_RETRIES) -> bool:
    """Install a single package with retry support / 安装单个包，支持重试"""
    for attempt in range(retries):
        print(f"\n[{attempt+1}/{retries}] Installing / 正在安装 {package_name}...")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name, "-q"],
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            if result.returncode == 0:
                print(f"[OK] {package_name} installed successfully / 安装成功")
                return True
            else:
                print(f"[X] Installation failed / 安装失败: {result.stderr[:200]}")
                
        except subprocess.TimeoutExpired:
            print(f"[X] Installation timeout / 安装超时")
        except Exception as e:
            print(f"[X] Error / 错误: {e}")
        
        if attempt < retries - 1:
            print(f"  Retrying in {RETRY_DELAY}s... / {RETRY_DELAY}秒后重试...")
            time.sleep(RETRY_DELAY)
    
    return False

def install_level(level: str) -> bool:
    """Install all dependencies for a specific level / 安装指定级别的所有依赖"""
    if level not in DEPENDENCY_LEVELS:
        print(f"Unknown level / 未知级别: {level}")
        return False
    
    config = DEPENDENCY_LEVELS[level]
    packages = list(config.get("packages", {}).keys())
    
    print(f"\n{'='*50}")
    print(f"Installing {level.upper()} level dependencies")
    print(f"正在安装 {level.upper()} 级别依赖")
    print(f"Description / 说明: {config['description']}")
    print(f"Packages / 包数量: {len(packages)}")
    print(f"{'='*50}")
    
    success_count = 0
    failed = []
    
    for pkg in packages:
        pkg_info = config["packages"][pkg]
        # Check if already installed
        ok, _ = check_package(pkg, pkg_info["import"])
        if ok:
            print(f"[OK] {pkg} already installed / 已安装")
            success_count += 1
            continue
        
        if install_package(pkg):
            success_count += 1
        else:
            failed.append(pkg)
    
    print(f"\n{'='*50}")
    print(f"Installation complete / 安装完成: {success_count}/{len(packages)} successful / 成功")
    
    if failed:
        print(f"Failed packages / 失败的包: {', '.join(failed)}")
        return False
    
    return True

def first_run_wizard():
    """First-run setup wizard / 首次运行设置向导"""
    print("\n" + "="*60)
    print("Welcome to PDF-Audio-Video-to-Markdown-with-AI!")
    print("欢迎使用 PDF-Audio-Video-to-Markdown-with-AI!")
    print("="*60)
    print("\nThis is your first time using this skill. Let's set up.")
    print("这是您第一次使用此技能，让我们来配置环境。")
    print("\n" + "-"*60)
    print("\nPlease select installation mode / 请选择安装模式:\n")
    print("  [1] Basic / 基础 (~600MB)")
    print("      PDF text extraction + Audio/Video transcription")
    print("      PDF文本提取 + 音视频转录")
    print()
    print("  [2] Full / 完整 (~1.5GB)")
    print("      Basic + OCR + YouTube + Table extraction")
    print("      基础 + OCR + YouTube + 表格提取")
    print()
    print("  [3] Advanced / 高级 (~3GB)")
    print("      Full + Speaker diarization (requires HuggingFace Token)")
    print("      完整 + 说话人分离 (需要HuggingFace Token)")
    print()
    print("  [4] On-demand / 按需安装")
    print("      Install dependencies when needed later")
    print("      稍后在需要时再安装依赖")
    print()
    
    print("-"*60)
    print("\nTip: You don't need to type any commands!")
    print("提示: 您不需要输入任何命令!")
    print("\nJust tell the AI your choice, for example / 只需告诉 AI 您的选择:")
    print('  CN: "我选择基础模式" / "安装完整功能" / "按需安装"')
    print('  EN: "I choose basic mode" / "Install full features" / "Install on demand"')
    print("\nAI will handle all installations with auto-retry on errors.")
    print("AI 会处理所有安装，出错时自动重试直到成功。")

def show_huggingface_guide():
    """Show HuggingFace Token application guide / 显示 HuggingFace Token 申请指南"""
    print("\n" + "="*60)
    print("HuggingFace Token Application Guide")
    print("HuggingFace Token 申请指南")
    print("="*60)
    print("""
Speaker diarization requires a HuggingFace Token.
说话人分离功能需要 HuggingFace Token。

Application Steps / 申请步骤:

1. Visit / 访问: https://huggingface.co/join
   Register an account / 注册账号 (email or GitHub login)

2. After login, visit / 登录后访问: https://huggingface.co/settings/tokens

3. Click "New token" to create a new token
   点击 "New token" 创建新令牌

4. Name can be anything, select "read" permission
   名称随意，权限选择 "read"

5. Copy the generated token (starts with hf_)
   复制生成的令牌 (以 hf_ 开头)

6. Accept model license agreements / 接受模型许可协议:
   - https://huggingface.co/pyannote/speaker-diarization-3.1
   - https://huggingface.co/pyannote/segmentation-3.0
   
   Visit links above and click "Agree and access repository"
   访问上述链接，点击 "Agree and access repository"

7. Set environment variable / 设置环境变量:
   
   Windows: set HUGGINGFACE_TOKEN=hf_your_token_here
   Linux/Mac: export HUGGINGFACE_TOKEN=hf_your_token_here

When done, tell AI / 完成后告诉 AI:
  CN: "我已经获取了 HuggingFace Token"
  EN: "I have obtained the HuggingFace Token"
""")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Smart Dependency Manager / 智能依赖管理器"
    )
    subparsers = parser.add_subparsers(dest="command")
    
    # install command
    install_parser = subparsers.add_parser(
        "install", 
        help="Install dependencies / 安装依赖"
    )
    install_parser.add_argument(
        "--level", 
        choices=["basic", "ocr", "youtube", "table", "speaker", "full"],
        required=True, 
        help="Installation level / 安装级别"
    )
    
    # wizard command
    subparsers.add_parser(
        "wizard", 
        help="First-run wizard / 首次使用向导"
    )
    
    # guide command
    subparsers.add_parser(
        "hf-guide", 
        help="HuggingFace Token guide / HuggingFace Token 指南"
    )
    
    args = parser.parse_args()
    
    if args.command == "install":
        if args.level == "full":
            # Install basic + ocr + youtube + table
            for level in ["basic", "ocr", "youtube", "table"]:
                if not install_level(level):
                    print(f"\nWarning / 警告: {level} level installation incomplete / 安装不完整")
        else:
            install_level(args.level)
    
    elif args.command == "wizard":
        first_run_wizard()
    
    elif args.command == "hf-guide":
        show_huggingface_guide()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
