"""
导出模块
将抓取结果导出为 CSV 和 Excel (.xlsx)
支持将价格历史数据转化为矩阵格式并自动生成折线图
"""
import logging
from typing import List
from datetime import datetime
import csv
from pathlib import Path

import pandas as pd
from openpyxl.chart import LineChart, Reference

from .parser import Product, Review

logger = logging.getLogger(__name__)


def export_products_csv(products: List[Product], out_path: str):
    """导出为 CSV"""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", newline="", encoding="utf-8") as f:
        if not products:
            f.write("asin,title,price,currency,rating,review_count,availability,url\\n")
            return
        writer = csv.DictWriter(f, fieldnames=products[0].to_dict().keys())
        writer.writeheader()
        for p in products:
            writer.writerow(p.to_dict())
    logger.info(f"csv exported: {out}")


def export_reviews_csv(reviews: List[Review], out_path: str):
    """导出评论为 CSV"""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        if not reviews:
            f.write("reviewer,rating,title,body,date,verified\\n")
            return
        writer = csv.DictWriter(f, fieldnames=reviews[0].to_dict().keys())
        writer.writeheader()
        for r in reviews:
            writer.writerow(r.to_dict())
    logger.info(f"reviews csv exported: {out}")


def export_products_excel(
    products: List[Product],
    history: dict = None,  # {asin: [(date, price), ...]}
    out_path: str = "output/products.xlsx",
):
    """
    导出 Excel。
    如果 products 列表包含重复 ASIN 且有时间属性，或提供了 history，
    则会自动创建 'Price Trends' 工作表并生成可视化折线图。
    """
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # 1. 主数据表 (Products)
    # 如果 products 里有重复 ASIN，我们只取最新的一个作为主表记录
    unique_products = {p.asin: p for p in products}.values()
    df_main = pd.DataFrame([p.to_dict() for p in unique_products])

    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df_main.to_excel(writer, sheet_name="Products", index=False)

        # 2. 处理价格历史与图表
        # 尝试从 products 列表中提取历史数据 (如果 Product 对象被注入了 date 属性)
        history_data = history if history else {}
        
        # 如果没有显式 history，检查 products 是否包含重复 ASIN 的时间序列
        if not history_data:
            temp_history = {}
            for p in products:
                # 检查是否有 date 属性 (模拟脚本注入的)
                date = getattr(p, 'date', datetime.now().strftime("%Y-%m-%d"))
                if p.asin not in temp_history:
                    temp_history[p.asin] = []
                temp_history[p.asin].append((date, p.price))
            history_data = temp_history

        if history_data:
            # 将历史数据转化为矩阵格式: 行=日期, 列=ASIN, 值=价格
            all_records = []
            for asin, points in history_data.items():
                for date, price in points:
                    all_records.append({"Date": date, "ASIN": asin, "Price": price})
            
            if all_records:
                df_raw = pd.DataFrame(all_records)
                # 透视表: Index=Date, Columns=ASIN, Values=Price
                df_pivot = df_raw.pivot(index="Date", columns="ASIN", values="Price")
                df_pivot.to_excel(writer, sheet_name="Price Trends")

                # 3. 在 Price Trends 表中添加折线图
                try:
                    wb = writer.book
                    ws = wb["Price Trends"]
                    
                    chart = LineChart()
                    chart.title = "Price Trends Comparison"
                    chart.style = 13
                    chart.y_axis.title = "Price (USD)"
                    chart.x_axis.title = "Date"

                    # 数据范围: 从 B2 到 最后一列最后一行
                    # min_col=2 (ASINs), min_row=1 (Headers)
                    data = Reference(
                        ws, 
                        min_col=2, 
                        min_row=1, 
                        max_col=len(df_pivot.columns) + 1, 
                        max_row=len(df_pivot) + 1
                    )
                    # 类别范围: A2 到 A最后一行 (日期)
                    cats = Reference(
                        ws, 
                        min_col=1, 
                        min_row=2, 
                        max_row=len(df_pivot) + 1
                    )
                    
                    chart.add_data(data, titles_from_data=True)
                    chart.set_categories(cats)
                    
                    # 将图表放在数据右侧
                    ws.add_chart(chart, "H2")
                except Exception as e:
                    logger.warning(f"failed to add chart: {e}")

    logger.info(f"excel exported: {out}")


# 公开 API
__all__ = [
    "export_products_csv",
    "export_reviews_csv",
    "export_products_excel",
]
