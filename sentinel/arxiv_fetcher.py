import os
import time
import requests
from urllib.parse import urlencode

class ArXivFetcher:
    """
    轻量级 arXiv 论文抓取器（兼容哨兵模块）
    遵守 arXiv API 使用政策：每秒最多 1 次请求
    开源版本 - 禁止用于商业数据采集服务
    """
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, delay=1.0):
        self.delay = delay  # 请求间隔（秒）
    
    def search(self, query, max_results=50, sort_by="submittedDate"):
        """
        查询 arXiv 论文
        
        Args:
            query (str): 搜索关键词，如 "all:3D human reconstruction"
            max_results (int): 最大返回数量
            sort_by (str): 排序方式 ("submittedDate", "relevance")
        
        Returns:
            list[dict]: 论文列表，含 title, id, summary, published
        """
        params = {
            "search_query": query,
            "max_results": min(max_results, 100),
            "sortBy": sort_by,
            "sortOrder": "descending"
        }
        
        url = f"{self.BASE_URL}?{urlencode(params)}"
        response = requests.get(url)
        response.raise_for_status()
        
        # 简单解析 XML（实际项目建议用 feedparser）
        # 此处为简化演示，仅返回原始文本供后续处理
        raw_xml = response.text
        
        # 模拟解析（真实场景应提取字段）
        print(f"📡 已获取 {len(raw_xml)} 字节的 arXiv 响应")
        time.sleep(self.delay)  # 尊重速率限制
        
        return raw_xml  # 后续由 predictor.py 解析

# 示例用法（不会自动执行）
if __name__ == "__main__":
    fetcher = ArXivFetcher()
    xml_data = fetcher.search("ti:%223D%20human%22", max_results=10)
    print("示例抓取完成（开源版）")