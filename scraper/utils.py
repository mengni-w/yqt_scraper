"""
工具函数模块
"""

import json
import logging
import os
from typing import Any, Dict, List
from config.settings import LOG_LEVEL, LOG_FORMAT, OUTPUT_ENCODING, JSON_INDENT


def setup_logging(level: str = LOG_LEVEL) -> logging.Logger:
    """
    设置日志配置
    
    Args:
        level: 日志级别
    
    Returns:
        配置好的logger对象
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('scraper.log', encoding=OUTPUT_ENCODING)
        ]
    )
    return logging.getLogger(__name__)


def save_to_json(data: List[Dict[str, Any]], output_path: str) -> bool:
    """
    将数据保存为JSON文件
    
    Args:
        data: 要保存的数据
        output_path: 输出文件路径
    
    Returns:
        是否保存成功
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding=OUTPUT_ENCODING) as f:
            json.dump(data, f, ensure_ascii=False, indent=JSON_INDENT)
        return True
    except Exception as e:
        logging.error(f"保存JSON文件失败: {e}")
        return False


def clean_text(text: str) -> str:
    """
    清理文本内容
    
    Args:
        text: 原始文本
    
    Returns:
        清理后的文本
    """
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = ' '.join(text.split())
    # 移除首尾空白
    text = text.strip()
    
    return text


def validate_url(url: str) -> bool:
    """
    验证URL格式
    
    Args:
        url: 要验证的URL
    
    Returns:
        URL是否有效
    """
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None