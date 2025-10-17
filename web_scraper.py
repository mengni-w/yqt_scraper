#!/usr/bin/env python3
"""
网页数据采集主程序
针对 https://www.yqt365.com/staticweb/#/yqmonitor/index/yqpage/yqlist?tid=3smHV9Q1Dukr11LL&funId=5993248
进行数据采集并输出JSON格式
"""

import argparse
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import DynamicScraper, setup_logging, save_to_json


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='网页数据采集工具')
    parser.add_argument('--url', 
                       default='https://www.yqt365.com/staticweb/#/yqmonitor/index/yqpage/yqlist?tid=3smHV9Q1Dukr11LL&funId=5993248',
                       help='要采集的网页URL')
    parser.add_argument('--output', 
                       default='output/yqt_data.json',
                       help='输出文件路径')
    parser.add_argument('--headless', 
                       action='store_true',
                       default=True,
                       help='使用无头浏览器模式')
    parser.add_argument('--verbose', 
                       action='store_true',
                       help='详细输出模式')
    
    args = parser.parse_args()
    
    # 设置日志
    logger = setup_logging('DEBUG' if args.verbose else 'INFO')
    
    # 创建爬虫实例
    scraper = DynamicScraper(headless=args.headless)
    
    try:
        logger.info("开始数据采集...")
        logger.info(f"目标URL: {args.url}")
        
        # 爬取数据
        data = scraper.scrape_yqt_website(args.url)
        
        if not data:
            logger.warning("未采集到任何数据")
            return
        
        logger.info(f"成功采集到 {len(data)} 条数据")
        
        # 添加采集时间戳
        for item in data:
            item['scraped_at'] = datetime.now().isoformat()
        
        # 保存数据
        if save_to_json(data, args.output):
            logger.info(f"数据已保存到: {args.output}")
            
            # 输出样本数据
            if data:
                logger.info("样本数据预览:")
                for i, item in enumerate(data[:3]):  # 只显示前3条
                    logger.info(f"第 {i+1} 条:")
                    logger.info(f"  标题: {item.get('title', 'N/A')}")
                    logger.info(f"  内容: {item.get('content', 'N/A')[:100]}...")
                    logger.info(f"  地址: {item.get('address', 'N/A')}")
                    logger.info(f"  链接: {item.get('link', 'N/A')}")
                    logger.info("---")
        else:
            logger.error("数据保存失败")
    
    except KeyboardInterrupt:
        logger.info("用户中断操作")
    except Exception as e:
        logger.error(f"采集过程中发生错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
    finally:
        # 确保释放资源
        scraper.close()
        logger.info("采集完成")


if __name__ == "__main__":
    main()