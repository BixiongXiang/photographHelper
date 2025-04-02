#!/usr/bin/env python3
import subprocess
from pathlib import Path

def check_tag_installed():
    """检查是否安装了 tag 命令"""
    try:
        subprocess.run(['tag', '--version'], check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_tags(file_path):
    """获取文件的标签列表"""
    try:
        result = subprocess.run(['tag', '--list', '--no-name', file_path],
                              capture_output=True, text=True, check=True)
        tags = [t.strip() for t in result.stdout.split(',') if t.strip()]
        return tags
    except subprocess.CalledProcessError:
        return []

def set_tags(file_path, tags):
    """设置文件的标签"""
    if not tags:
        return False
    
    try:
        subprocess.run(['tag', '--set', ','.join(tags), file_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting tags for {file_path}: {e}")
        return False

def copy_tags(source_file, target_file):
    """复制标签从源文件到目标文件"""
    tags = get_tags(source_file)
    if tags:
        print(f"Copying tags from {source_file} to {target_file}: {tags}")
        if set_tags(target_file, tags):
            print("✅ Tags copied successfully")
            return True
        else:
            print("❌ Failed to copy tags")
            return False
    else:
        print(f"No tags found in {source_file}")
        return False

def process_directory(directory):
    """处理目录中的所有JPG文件"""
    directory = Path(directory)
    jpg_files = list(directory.glob('*.JPG')) + list(directory.glob('*.jpg'))
    
    for jpg_file in jpg_files:
        # 查找对应的ARW文件
        for ext in ['.ARW', '.arw']:
            arw_file = directory / (jpg_file.stem + ext)
            if arw_file.exists():
                copy_tags(jpg_file, arw_file)
                break
        else:
            print(f"ARW file not found for {jpg_file}")

def main():
    if not check_tag_installed():
        print("Error: 'tag' command not found. Please install it first:")
        print("  brew install tag")
        return
    
    import os
    target_dir = input("Enter directory path (or press Enter for current dir): ").strip()
    if not target_dir:
        target_dir = os.getcwd()
    
    print(f"Processing directory: {target_dir}")
    process_directory(target_dir)
    print("Done!")

if __name__ == "__main__":
    main()