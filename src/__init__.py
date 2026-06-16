"""
Amazon Price & Review Tracker
=============================

一个端到端的 Amazon 商品价格与评论抓取工具，输出 CSV/Excel。

适用场景：
    - 跨境电商选品分析
    - 竞品定价监控
    - 评论分析

特性：
    - 支持多功能：仅价格 / 价格+评论 / 关键词批量
    - 速率限制、重试、User-Agent 轮换
    - 直接输出 Excel (.xlsx)，含价格走势折线图
    - CLI 友好（一条命令运行）

⚠️ 合规提示：
    - 请遵守 Amazon Robots.txt 与服务条款
    - 生产环境建议使用 Amazon Product Advertising API
    - 本工具体现原理，商用前请评估法律风险
"""

__version__ = "0.1.0"
