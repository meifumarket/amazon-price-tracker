"""
导出模块
将抓取结果导出为 CSV 和 Excel (.xlsx)
若包含价格历史，自动生成折线图
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
            f.write("asin,title,price,currency,rating,review_count,availability,url\n")
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
            f.write("reviewer,rating,title,body,date,verified\n")
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
    """导出 Excel；若提供 history 则含价格走势折线图"""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # 主 sheet
    df = pd.DataFrame([p.to_dict() for p in products])

    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Products", index=False)

        # 评论汇总
        if history:
            history_rows = []
            for asin, points in history.items():
                for date, price in points:
                    history_rows.append({"asin": asin, "date": date, "price": price})
            if history_rows:
                hdf = pd.DataFrame(history_rows)
                hdf.to_excel(writer, sheet_name="Price History", index=False)

                # 添加折线图
                try:
                    wb = writer.book
                    ws = wb["Price History"]
                    chart = LineChart()
                    chart.title = "Price Trends"
                    chart.y_axis.title = "Price"
                    chart.x_axis.title = "Date"
                    data = Reference(
                        ws, min_col=3, min_row=1, max_col=3,
                        max_row=len(history_rows) + 1,
                    )
                    chart.add_data(data, titles_from_data=True)
                    ws.add_chart(chart, "E2")
                except Exception as e:
                    logger.warning(f"failed to add chart: {e}")

    logger.info(f"excel exported: {out}")


# 公开 API
__all__ = [
    "export_products_csv",
    "export_reviews_csv",
    "export_products_excel",
]
