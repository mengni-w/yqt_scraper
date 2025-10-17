"""
网页爬虫模块初始化文件
"""

from .base_scraper import BaseScraper
from .dynamic_scraper import DynamicScraper
from .utils import setup_logging, save_to_json

__version__ = "1.0.0"
__author__ = "Web Scraper"

__all__ = [
    'BaseScraper',
    'DynamicScraper',
    'setup_logging',
    'save_to_json'
]