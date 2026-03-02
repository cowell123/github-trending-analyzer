"""
GitHub Trending Analyzer - Main Script

This script combines both steps:
1. Collects trending repositories data
2. Generates summary and sends email
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse


def run_collection_step():
    """Run the data collection step"""
    print("开始执行数据收集步骤...")
    result = subprocess.run([sys.executable, 'collect_data.py'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("数据收集完成！")
        print(result.stdout)
        
        # Find the generated JSON file
        json_files = list(Path('.').glob('github_trending_summary_*.json'))
        if json_files:
            latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
            print(f"生成的数据文件: {latest_file}")
            return str(latest_file)
        else:
            print("未找到生成的数据文件")
            return None
    else:
        print("数据收集失败！")
        print(result.stderr)
        return None


def run_email_step(json_file, recipient_email):
    """Run the email sending step"""
    print(f"开始执行邮件发送步骤，使用数据文件: {json_file}")
    
    cmd = [sys.executable, 'send_email.py', '--json-file', json_file, '--email', recipient_email]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("邮件发送步骤完成！")
        print(result.stdout)
    else:
        print("邮件发送步骤失败！")
        print(result.stderr)


def main(recipient_email='18838085199@139.com'):
    """Main function to run the entire process"""
    print("GitHub Trending Analyzer 启动")
    print(f"目标邮箱: {recipient_email}")
    
    # Step 1: Collect data
    json_file = run_collection_step()
    
    if json_file:
        # Step 2: Send email with summary
        run_email_step(json_file, recipient_email)
    else:
        print("流程终止：数据收集失败")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GitHub Trending Analyzer')
    parser.add_argument('--email', type=str, default='18838085199@139.com', 
                        help='Recipient email address (default: 18838085199@139.com)')
    
    args = parser.parse_args()
    
    main(args.email)