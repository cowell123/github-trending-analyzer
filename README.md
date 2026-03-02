# GitHub Trending Analyzer

这是一个自动化分析 GitHub 趋势项目的工具，能够获取当前最热门的开源项目，并将其汇总后通过邮件发送。

## 功能特性

1. 自动爬取 GitHub Trending 页面的前 5 个热门项目
2. 获取每个项目的详细信息（名称、描述、编程语言、Star 数量等）
3. 提取每个项目的 README 文件内容
4. 生成中文摘要报告
5. 自动发送邮件到指定邮箱

## 依赖安装

在使用前，请先安装所需依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：直接运行主脚本

```bash
python main.py
```

默认会发送邮件到 18838085199@139.com，也可以指定其他邮箱：

```bash
python main.py --email your-email@example.com
```

### 方法二：分步执行

1. 首先收集数据：

```bash
python collect_data.py
```

这将生成一个包含所有项目信息的 JSON 文件。

2. 然后发送邮件：

```bash
python send_email.py --json-file github_trending_summary_YYYYMMDD_HHMMSS.json
```

或者使用最新生成的 JSON 文件：

```bash
python send_email.py
```

## 邮件发送配置

邮件发送功能已预配置好 SMTP 信息。当前使用以下设置：

- 发件人邮箱: cosir_123@2925.com
- SMTP 服务器: smtp.2925.com
- SMTP 端口: 465 (SSL)
- 用户名: cosir_123@2925.com
- 密码: ly1314006

如果需要更改配置，请在 `send_email.py` 文件中修改 `send_email` 函数内的 `smtp_config` 设置。

支持的服务器信息：
- POP3 (收信): pop3.2925.com, 端口 110 (标准) 或 995 (SSL)
- SMTP (发信): smtp.2925.com, 端口 25 (标准) 或 465/587 (SSL/TLS)
- IMAP (收信): imap.2925.com, 端口 143 (标准) 或 993 (SSL)

## 输出格式

程序会生成一个 JSON 文件，包含以下信息：

- 收集时间
- 项目排名
- 项目名称及链接
- 项目描述
- 编程语言
- Star 数量
- 今日新增 Star 数量
- README 内容预览

邮件中会包含中文摘要，包括项目简介、解决的问题、技术栈和 Star 数量等关键信息。

## 示例输出

邮件内容示例：
```
GitHub 今日热门项目 Top 5 摘要 (2026-03-02 23:09:12)

第 1 名: ruvnet /wifi-densepose
项目地址: https://github.com/ruvnet/wifi-densepose
项目描述: WiFi DensePose turns commodity WiFi signals into real-time human pose estimation vital sign monitoring and presence detection — all without a single pixel of video.
解决的问题: 该项目主要解决了开发中的实际问题，提供了特定领域的解决方案
技术栈: Rust
Star 数量: 20,508 (今日新增: 5,080)
项目简介: WiFi DensePose turns commodity WiFi signals into real-time human pose estimation vital sign monitoring and presence detection — all without a single pixel of video.

...
```

## 自动执行配置

您可以配置此技能每天自动运行并发送报告。详情请参考 [AUTO_RUN_GUIDE.md](AUTO_RUN_GUIDE.md) 和 [SECURE_AUTOMATION.md](SECURE_AUTOMATION.md)。

### 推荐方案：GitHub Actions（云端自动执行）

最安全和便捷的方式是使用GitHub Actions，这样无需保持本地计算机开机，而且能安全地管理敏感信息。

快速设置方法：
1. 将此技能文件上传到GitHub仓库
2. 在仓库设置中配置Secrets（邮箱信息）
3. 使用提供的GitHub Actions工作流文件
4. 详情请参见 [SECURE_AUTOMATION.md](SECURE_AUTOMATION.md)

### 本地自动执行
如果选择在本地运行：
1. 安装依赖: `pip install schedule`
2. 运行自动执行脚本: `python auto_runner.py`
3. 或使用Windows任务计划程序设置定时执行

## 注意事项

- 请遵守 GitHub 的使用条款和爬虫政策
- 建议适当控制爬取频率，避免对服务器造成过大压力
- 邮件发送功能需要有效的 SMTP 配置才能使用
- 自动执行功能需要保持计算机在设定时间处于开机状态