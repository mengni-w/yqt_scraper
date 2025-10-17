# 网页数据采集项目

这是一个专业的Python网页数据采集工具，用于抓取动态网页内容并以JSON格式输出数据。

## 功能特性

- ✅ 支持静态和动态网页内容抓取
- ✅ 自动处理JavaScript渲染的内容
- ✅ 智能数据解析和清洗
- ✅ JSON格式数据输出
- ✅ 支持多种网站结构
- ✅ 内置错误处理和重试机制
- ✅ 遵循网站robots.txt协议

## 技术栈

- **Python 3.8+** - 主要编程语言
- **requests** - HTTP请求处理
- **beautifulsoup4** - HTML解析
- **selenium** - 动态内容处理
- **webdriver-manager** - 自动管理浏览器驱动
- **aiohttp** - 异步HTTP请求
- **lxml** - 高性能XML/HTML解析

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python web_scraper.py --url "https://example.com" --output data.json
```

### 针对动态内容的网站

```bash
python web_scraper.py --url "https://spa-website.com" --dynamic --output data.json
```

## 项目结构

```
.
├── web_scraper.py          # 主要的爬虫脚本
├── scraper/               # 爬虫模块
│   ├── __init__.py
│   ├── base_scraper.py    # 基础爬虫类
│   ├── dynamic_scraper.py # 动态内容爬虫
│   └── utils.py           # 工具函数
├── config/                # 配置文件
│   └── settings.py        # 设置参数
├── output/                # 输出目录
├── requirements.txt       # 依赖包列表
└── README.md              # 项目说明

```

## 配置说明

可以在 `config/settings.py` 中调整以下参数：

- `REQUEST_DELAY`: 请求间隔时间
- `TIMEOUT`: 请求超时时间
- `RETRY_ATTEMPTS`: 重试次数
- `USER_AGENT`: 用户代理字符串

## 注意事项

1. 使用前请确保遵守目标网站的 robots.txt 协议
2. 建议设置合理的请求延迟，避免对服务器造成压力
3. 对于需要登录的网站，请在代码中添加相应的认证逻辑

## 许可证

MIT License