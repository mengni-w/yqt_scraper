<!-- 使用此文件为工作区提供特定的 Copilot 自定义指令。更多详情请访问 https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# 网页数据采集项目

这是一个Python网页数据采集项目，专门用于采集动态网站内容并以JSON格式输出。

## 项目功能
- 网页内容抓取
- 处理JavaScript动态内容
- 数据解析和清洗
- JSON格式输出
- 支持多种网站结构

## 技术栈
- Python 3.8+
- requests - HTTP请求
- beautifulsoup4 - HTML解析
- selenium - 动态内容处理
- json - 数据序列化

## 开发指南
- 优先使用异步方式处理网络请求
- 遵循robots.txt协议
- 添加适当的请求延迟
- 实现错误处理和重试机制
- 保持代码简洁和可维护性