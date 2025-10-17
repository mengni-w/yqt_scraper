"""
动态内容爬虫类
"""

import time
import logging
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import (
    SELENIUM_IMPLICIT_WAIT,
    SELENIUM_PAGE_LOAD_TIMEOUT,
    REQUEST_DELAY,
    USER_AGENT
)
from .base_scraper import BaseScraper
from .utils import clean_text


class DynamicScraper(BaseScraper):
    """动态内容爬虫类，使用Selenium处理JavaScript渲染的页面"""
    
    def __init__(self, headless: bool = True):
        """
        初始化动态爬虫
        
        Args:
            headless: 是否使用无头模式
        """
        super().__init__()
        self.headless = headless
        self.driver = None
        self.logger = logging.getLogger(__name__)
    
    def _setup_driver(self) -> webdriver.Chrome:
        """
        设置Chrome浏览器驱动
        
        Returns:
            配置好的Chrome WebDriver
        """
        options = Options()
        
        if self.headless:
            options.add_argument('--headless')
        
        # 添加常用选项
        options.add_argument(f'--user-agent={USER_AGENT}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 自动下载和设置ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(SELENIUM_IMPLICIT_WAIT)
        driver.set_page_load_timeout(SELENIUM_PAGE_LOAD_TIMEOUT)
        
        # 移除webdriver属性
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def fetch_dynamic_page(self, url: str, wait_element: str = None, wait_time: int = 10) -> Optional[str]:
        """
        获取动态渲染的网页内容
        
        Args:
            url: 目标URL
            wait_element: 等待的元素选择器
            wait_time: 等待时间
        
        Returns:
            渲染后的HTML内容
        """
        try:
            if not self.driver:
                self.driver = self._setup_driver()
            
            self.logger.info(f"正在加载动态页面: {url}")
            self.driver.get(url)
            
            # 等待特定元素加载（如果指定）
            if wait_element:
                try:
                    WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_element))
                    )
                except TimeoutException:
                    self.logger.warning(f"等待元素 {wait_element} 超时")
            
            # 等待页面完全加载
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # 添加额外延迟确保JavaScript执行完成
            time.sleep(REQUEST_DELAY)
            
            return self.driver.page_source
            
        except WebDriverException as e:
            self.logger.error(f"Selenium错误: {e}")
            return None
        except Exception as e:
            self.logger.error(f"获取动态页面失败: {e}")
            return None
    
    def scroll_to_load_content(self, scroll_pause_time: float = 2) -> None:
        """
        滚动页面加载更多内容
        
        Args:
            scroll_pause_time: 滚动间隔时间
        """
        if not self.driver:
            return
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # 滚动到页面底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # 等待页面加载
            time.sleep(scroll_pause_time)
            
            # 计算新的滚动高度
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
            
            last_height = new_height
    
    def extract_yqt_data(self, soup) -> List[Dict[str, Any]]:
        """
        专门针对yqt365.com网站的数据提取
        
        Args:
            soup: BeautifulSoup对象
        
        Returns:
            提取的数据列表
        """
        data_list = []
        
        try:
            # 根据实际页面结构调整选择器
            # 这里需要根据具体的网页结构来编写
            items = soup.find_all('div', class_='item') or soup.find_all('li') or soup.find_all('article')
            
            for item in items:
                item_data = {
                    'content': '',
                    'address': '',
                    'title': '',
                    'link': '',
                    'description': ''
                }
                
                # 提取标题
                title_elem = item.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or item.find(class_='title')
                if title_elem:
                    item_data['title'] = clean_text(title_elem.get_text())
                
                # 提取链接
                link_elem = item.find('a')
                if link_elem and link_elem.get('href'):
                    item_data['link'] = link_elem['href']
                
                # 提取内容
                content_elem = item.find(class_='content') or item.find(class_='description')
                if content_elem:
                    item_data['content'] = clean_text(content_elem.get_text())
                else:
                    item_data['content'] = clean_text(item.get_text())
                
                # 提取地址信息
                address_elem = item.find(class_='address') or item.find(class_='location')
                if address_elem:
                    item_data['address'] = clean_text(address_elem.get_text())
                
                # 只保存有内容的项目
                if item_data['content'] or item_data['title']:
                    data_list.append(item_data)
        
        except Exception as e:
            self.logger.error(f"数据提取失败: {e}")
        
        return data_list
    
    def scrape_yqt_website(self, url: str) -> List[Dict[str, Any]]:
        """
        专门爬取yqt365.com网站的方法
        
        Args:
            url: 目标URL
        
        Returns:
            爬取到的数据列表
        """
        # 等待页面中的关键元素加载
        html = self.fetch_dynamic_page(url, wait_element='.list-item, .item, li', wait_time=15)
        
        if not html:
            return []
        
        # 尝试滚动加载更多内容
        self.scroll_to_load_content()
        
        # 获取最终的页面源码
        final_html = self.driver.page_source
        soup = self.parse_html(final_html)
        
        # 提取基本信息
        basic_info = self.extract_basic_info(soup, url)
        
        # 提取列表数据
        data_list = self.extract_yqt_data(soup)
        
        # 如果没有找到列表数据，返回基本信息
        if not data_list:
            return [basic_info]
        
        return data_list
    
    def close(self):
        """关闭浏览器驱动"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __del__(self):
        """析构函数，确保资源释放"""
        self.close()