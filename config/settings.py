# 网页爬虫配置设置

# 请求设置
REQUEST_DELAY = 1  # 请求间隔时间（秒）
TIMEOUT = 30       # 请求超时时间（秒）
RETRY_ATTEMPTS = 3 # 重试次数

# 用户代理设置
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Selenium设置
SELENIUM_IMPLICIT_WAIT = 10  # 隐式等待时间（秒）
SELENIUM_PAGE_LOAD_TIMEOUT = 30  # 页面加载超时时间（秒）

# 输出设置
OUTPUT_ENCODING = 'utf-8'
JSON_INDENT = 2

# 日志设置
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'