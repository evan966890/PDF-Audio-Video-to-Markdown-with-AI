#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DocPipe 端到端测试脚本

功能：
1. 自动配置环境
2. 交互式询问测试文件路径
3. 运行 PDF 和音视频测试
4. 循环重试直到成功

用法：
    python run_e2e_test.py
"""

import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# 配置
MAX_TOTAL_RETRIES = 10  # 每种类型最大重试次数
DEFAULT_INPUT_DIR = "./input"
DEFAULT_OUTPUT_DIR = "./output"


def print_header(title: str):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def run_setup() -> bool:
    """运行环境配置"""
    print_header("步骤 1: 环境配置")
    
    script_dir = Path(__file__).parent
    setup_script = script_dir / "setup_environment.py"
    
    if not setup_script.exists():
        print(f"[ERROR] 找不到环境配置脚本: {setup_script}")
        return False
    
    result = subprocess.run(
        [sys.executable, str(setup_script)],
        capture_output=False
    )
    
    return result.returncode == 0


def get_test_directory() -> Path:
    """交互式获取测试目录"""
    print_header("步骤 2: 选择测试目录")
    
    print(f"请输入测试文件目录路径")
    print(f"（留空则使用默认目录 {DEFAULT_INPUT_DIR}）")
    print(f"支持的格式: PDF, PNG, JPG, MP3, WAV, M4A, MP4, AVI, MKV")
    
    user_input = input("\n>>> ").strip()
    
    if not user_input:
        test_dir = Path(DEFAULT_INPUT_DIR)
    else:
        test_dir = Path(user_input)
    
    # 转换为绝对路径
    if not test_dir.is_absolute():
        test_dir = Path(__file__).parent.parent / test_dir
    
    test_dir = test_dir.resolve()
    
    if not test_dir.exists():
        print(f"\n[INFO] 目录不存在，已创建: {test_dir}")
        test_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"测试目录: {test_dir}")
    return test_dir


def find_test_files(test_dir: Path) -> dict:
    """查找测试文件"""
    # PDF 文件
    pdf_files = list(test_dir.glob("*.pdf")) + list(test_dir.glob("*.PDF"))
    
    # 音视频文件
    audio_video_files = []
    for ext in [".mp3", ".wav", ".m4a", ".flac", ".mp4", ".avi", ".mkv", ".mov"]:
        audio_video_files.extend(test_dir.glob(f"*{ext}"))
        audio_video_files.extend(test_dir.glob(f"*{ext.upper()}"))
    
    # 图像文件
    image_files = []
    for ext in [".png", ".jpg", ".jpeg", ".tiff"]:
        image_files.extend(test_dir.glob(f"*{ext}"))
        image_files.extend(test_dir.glob(f"*{ext.upper()}"))
    
    # 选择最小的文件进行测试（加快测试速度）
    def get_smallest(files):
        if not files:
            return None
        return min(files, key=lambda f: f.stat().st_size)
    
    return {
        "pdf": get_smallest(pdf_files),
        "audio_video": get_smallest(audio_video_files),
        "image": get_smallest(image_files),
    }


def run_process(file_path: Path, output_dir: Path) -> bool:
    """运行处理脚本"""
    script_dir = Path(__file__).parent
    process_script = script_dir / "process_file.py"
    
    result = subprocess.run(
        [sys.executable, str(process_script), str(file_path), str(output_dir)],
        capture_output=False
    )
    
    return result.returncode == 0


def test_file_type(name: str, file_path: Path, output_dir: Path, max_retries: int) -> bool:
    """测试单个文件类型"""
    if file_path is None:
        print(f"\n[SKIP] 未找到 {name} 测试文件")
        return True  # 没有文件视为成功
    
    print(f"\n测试文件: {file_path.name}")
    print(f"大小: {file_path.stat().st_size / 1024:.1f} KB")
    
    for attempt in range(max_retries):
        print(f"\n>>> {name} 测试 (尝试 {attempt + 1}/{max_retries})")
        
        if run_process(file_path, output_dir):
            print(f"\n[SUCCESS] {name} 处理成功！")
            return True
        else:
            if attempt < max_retries - 1:
                print(f"[RETRY] {name} 处理失败，等待 2 秒后重试...")
                time.sleep(2)
    
    print(f"\n[FAILED] {name} 测试失败，已达到最大重试次数")
    return False


def run_e2e_test():
    """运行端到端测试"""
    print("\n" + "="*60)
    print("         DocPipe 端到端测试")
    print("="*60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version.split()[0]}")
    
    # 1. 环境配置
    if not run_setup():
        print("\n[ERROR] 环境配置失败，请查看上方错误信息")
        return False
    
    # 2. 获取测试目录
    test_dir = get_test_directory()
    
    # 3. 查找测试文件
    print_header("步骤 3: 查找测试文件")
    test_files = find_test_files(test_dir)
    
    has_files = any(f is not None for f in test_files.values())
    
    if not has_files:
        print(f"\n[INFO] 在 {test_dir} 中未找到测试文件")
        print("\n支持的格式:")
        print("  - PDF: *.pdf")
        print("  - 音频: *.mp3, *.wav, *.m4a, *.flac")
        print("  - 视频: *.mp4, *.avi, *.mkv, *.mov")
        print("  - 图像: *.png, *.jpg, *.jpeg")
        print("\n请将测试文件放入该目录后重新运行")
        return False
    
    print("找到的测试文件:")
    for name, path in test_files.items():
        if path:
            print(f"  {name}: {path.name} ({path.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  {name}: (无)")
    
    # 4. 创建输出目录
    output_dir = Path(__file__).parent.parent / DEFAULT_OUTPUT_DIR
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n输出目录: {output_dir}")
    
    # 5. 运行测试
    results = {}
    
    # PDF 测试
    print_header("步骤 4: PDF 处理测试")
    results["pdf"] = test_file_type("PDF", test_files["pdf"], output_dir, MAX_TOTAL_RETRIES)
    
    # 音视频测试
    print_header("步骤 5: 音视频处理测试")
    results["audio_video"] = test_file_type("音视频", test_files["audio_video"], output_dir, MAX_TOTAL_RETRIES)
    
    # 图像测试（可选）
    if test_files["image"]:
        print_header("步骤 6: 图像处理测试")
        results["image"] = test_file_type("图像", test_files["image"], output_dir, MAX_TOTAL_RETRIES)
    
    # 6. 总结
    print_header("测试结果")
    
    all_success = True
    for name, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"  {name}: {status}")
        if not success:
            all_success = False
    
    print(f"\n输出目录: {output_dir}")
    
    if all_success:
        print("\n" + "="*60)
        print("  [SUCCESS] 端到端测试全部通过！")
        print("  DocPipe 已准备就绪，可以开始处理文件")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("  [FAILED] 部分测试未通过")
        print("  请查看上方错误信息进行排查")
        print("="*60)
    
    return all_success


def main():
    """主函数"""
    try:
        success = run_e2e_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[ABORT] 用户取消测试")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
