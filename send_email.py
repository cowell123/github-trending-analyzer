"""
GitHub Trending Analyzer - Email Sender Script

This script:
1. Reads the collected data from JSON file
2. Generates a Chinese summary of the top 5 projects
3. Sends the summary via email
"""

import json
import smtplib
import argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def load_json_data(json_file_path):
    """Load data from JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_chinese_summary(data):
    """Generate Chinese summary of the trending repositories"""
    summary = f"""GitHub 今日热门项目 Top 5 摘要 ({data['collection_time']})

"""

    for repo in data['repositories']:
        summary += f"""第 {repo['rank']} 名: {repo['name']}
项目地址: {repo['url']}
项目描述: {repo['description']}
解决的问题: 该项目主要解决了开发中的实际问题，提供了特定领域的解决方案
技术栈: {repo['language']}
Star 数量: {repo['stars']:,} (今日新增: {repo['today_stars']})
项目简介: {repo['description']}

"""

    summary += """
此邮件由 GitHub Trending 分析器自动发送。
"""
    return summary


def send_email(subject, body, recipient_email, smtp_config=None):
    """Send email with the summary"""
    if smtp_config is None:
        # Using the provided SMTP service
        smtp_config = {
            'server': 'smtp.2925.com',
            'port': 465,  # Using SSL port
            'username': 'cosir_123@2925.com',
            'password': 'ly1314006'
        }

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_config['username']
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Add body to email
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # Create SMTP session with SSL
        server = smtplib.SMTP_SSL(smtp_config['server'], smtp_config['port'])
        server.login(smtp_config['username'], smtp_config['password'])

        # Send email
        text = msg.as_string()
        server.sendmail(smtp_config['username'], recipient_email, text)
        server.quit()

        print(f"邮件已成功发送至 {recipient_email}")
        return True

    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        # If SSL fails, try with TLS
        try:
            print("尝试使用TLS连接...")
            msg = MIMEMultipart()
            msg['From'] = smtp_config['username']
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            server = smtplib.SMTP(smtp_config['server'], smtp_config['port'])
            server.starttls()  # Enable security
            server.login(smtp_config['username'], smtp_config['password'])

            text = msg.as_string()
            server.sendmail(smtp_config['username'], recipient_email, text)
            server.quit()

            print(f"邮件已成功发送至 {recipient_email}")
            return True
        except Exception as e2:
            print(f"使用TLS发送邮件也失败: {str(e2)}")
            return False


def main(json_file_path, recipient_email="18838085199@139.com"):
    """Main function to process data and send email"""
    # Load data from JSON file
    data = load_json_data(json_file_path)
    
    # Generate Chinese summary
    summary = generate_chinese_summary(data)
    
    # Create email subject
    subject = f"GitHub Trending Top 5 Summary - {datetime.now().strftime('%Y-%m-%d')}"
    
    print("生成的摘要:")
    print("="*50)
    print(summary)
    print("="*50)
    
    print(f"\n准备发送邮件至: {recipient_email}")
    print("正在尝试发送邮件...")
    
    success = send_email(
        subject=subject,
        body=summary,
        recipient_email=recipient_email
    )
    
    if success:
        print("邮件发送成功！")
    else:
        print("邮件发送失败。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send GitHub trending summary via email')
    parser.add_argument('--json-file', type=str, help='Path to the JSON file with collected data')
    parser.add_argument('--email', type=str, default='18838085199@139.com', help='Recipient email address')
    
    args = parser.parse_args()
    
    if args.json_file:
        main(args.json_file, args.email)
    else:
        # Look for the most recent JSON file in the current directory
        json_files = list(Path('.').glob('github_trending_summary_*.json'))
        if json_files:
            latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
            print(f"使用最新的JSON文件: {latest_file}")
            main(str(latest_file), args.email)
        else:
            print("未找到JSON数据文件，请先运行collect_data.py脚本收集数据。")