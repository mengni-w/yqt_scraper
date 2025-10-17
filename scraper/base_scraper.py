"""
基础爬虫类
"""

import requests
import time
import logging
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import (
    REQUEST_DELAY, 
    TIMEOUT, 
    RETRY_ATTEMPTS, 
    USER_AGENT
)
from .utils import clean_text, validate_url


class BaseScraper:
    """基础网页爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.session = self._setup_session()
        self.logger = logging.getLogger(__name__)
    
    def _setup_session(self) -> requests.Session:
        """
        设置requests会话
        
        Returns:
            配置好的session对象
        """
        session = requests.Session()
        
        # 设置重试策略
        retry_strategy = Retry(
            total=RETRY_ATTEMPTS,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # 设置请求头
        session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        return session
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        获取网页内容
        
        Args:
            url: 目标URL
        
        Returns:
            网页HTML内容，失败返回None
        """
        if not validate_url(url):
            self.logger.error(f"无效的URL: {url}")
            return None
        
        try:
            self.logger.info(f"正在获取页面: {url}")
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            
            # 添加请求延迟
            time.sleep(REQUEST_DELAY)
            
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求失败: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        解析HTML内容
        
        Args:
            html: HTML字符串
        
        Returns:
            BeautifulSoup对象
        """
        return BeautifulSoup(html, 'lxml')
    
    def extract_basic_info(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        提取基本信息
        
        Args:
            soup: BeautifulSoup对象
            url: 页面URL
        
        Returns:
            基本信息字典
        """
        return {
            'url': url,
            'title': clean_text(soup.title.string if soup.title else ''),
            'meta_description': self._get_meta_content(soup, 'description'),
            'meta_keywords': self._get_meta_content(soup, 'keywords'),
        }
    
    def _get_meta_content(self, soup: BeautifulSoup, name: str) -> str:
        """
        获取meta标签内容
        
        Args:
            soup: BeautifulSoup对象
            name: meta标签的name属性
        
        Returns:
            meta标签的content内容
        """
        meta_tag = soup.find('meta', attrs={'name': name})
        if meta_tag and meta_tag.get('content'):
            return clean_text(meta_tag['content'])
        return ''
    
    def scrape(self, url: str) -> List[Dict[str, Any]]:
        """
        爬取网页数据
        
        Args:
            url: 目标URL
        
        Returns:
            爬取到的数据列表
        """
        html = self.fetch_page(url)
        if not html:
            return []
        
        soup = self.parse_html(html)
        basic_info = self.extract_basic_info(soup, url)
        
        # 这里应该根据具体网站结构实现数据提取逻辑
        # 子类应该重写这个方法来实现具体的数据提取
        return [basic_info]