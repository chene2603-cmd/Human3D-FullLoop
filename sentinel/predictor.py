import os
import time
import arxiv
import csv
from datetime import datetime, timedelta

class CVPR3DPredictor:
    """
    哨兵·预言者：基于 arXiv 论文元数据，零样本预测 CVPR 3D 人体重建方向热点。
    开源版 - 无商业授权禁止用于盈利系统。
    """
    
    def __init__(self):
        self.keywords = [
            "3D human reconstruction", "SMPL", "Gaussian Splatting",
            "neural avatar", "human pose estimation", "cloth simulation"
        ]
        self.high_impact_authors = {
            "Michael J. Black", "Angjoo Kanazawa", "Yaser Sheikh"
        }
    
    def fetch_recent_papers(self, days=7):
        """抓取最近 N 天的 arXiv 论文"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        search = arxiv.Search(
            query="cat:cs.CV OR cat:cs.AI",
            max_results=100,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for result in search.results():
            if result.published >= start_date:
                papers.append(result)
            time.sleep(1)  # 遵守 arXiv API 速率限制
        return papers
    
    def score_paper(self, paper):
        """计算论文与 3D 人体重建的相关性得分"""
        title = paper.title.lower()
        abstract = paper.summary.lower()
        authors = {str(a) for a in paper.authors}
        
        score = 0.0
        for kw in self.keywords:
            if kw.lower() in title or kw.lower() in abstract:
                score += 0.3
        if authors & self.high_impact_authors:
            score += 0.5
        return min(score, 1.0)
    
    def generate_priority_list(self, output_path="sentinel_output.csv"):
        """生成高优先级论文列表"""
        papers = self.fetch_recent_papers()
        scored = [(p, self.score_paper(p)) for p in papers]
        scored.sort(key=lambda x: x, reverse=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["arxiv_id", "title", "confidence", "priority"])
            for i, (paper, conf) in enumerate(scored[:20]):
                priority = "HIGH" if conf > 0.6 else "MEDIUM"
                writer.writerow([paper.get_short_id(), paper.title, round(conf, 2), priority])
        
        print(f"✅ 哨兵任务完成！输出至 {output_path}")