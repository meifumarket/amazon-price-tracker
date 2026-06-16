"""
主爬虫模块
组合 HTTP + 解析器，提供高层 API
"""
import logging
from typing import List
from datetime import datetime

from .http_client import SafeHTTP
from .parser import AmazonParser, Product, Review

logger = logging.getLogger(__name__)


class AmazonScraper:
    """Amazon 主爬虫"""

    BASE_URL = "https://www.amazon.com"

    def __init__(self, config: dict = None):
        self.config = config or {}
        delay_range = self.config.get("delay", (2.0, 5.0))
        self.http = SafeHTTP(
            min_delay=delay_range[0],
            max_delay=delay_range[1],
        )

    def get_product(self, asin: str) -> Product:
        url = f"{self.BASE_URL}/dp/{asin}"
        logger.info(f"fetching product: {asin}")
        resp = self.http.get(url)
        if not resp:
            logger.error(f"failed to fetch {asin}")
            return Product(asin=asin, url=url)
        return AmazonParser.parse_product(resp.text, asin, url)

    def get_reviews(self, asin: str, max_pages: int = 3) -> List[Review]:
        all_reviews = []
        for page in range(1, max_pages + 1):
            url = (
                f"{self.BASE_URL}/product-reviews/{asin}"
                f"?pageNumber={page}&sortBy=recent"
            )
            logger.info(f"fetching reviews page {page}: {asin}")
            resp = self.http.get(url)
            if not resp:
                break
            page_reviews = AmazonParser.parse_reviews(resp.text)
            if not page_reviews:
                break
            all_reviews.extend(page_reviews)
        return all_reviews

    def batch_products(self, asins: List[str]):
        results = []
        for asin in asins:
            p = self.get_product(asin)
            results.append(p)
        return results

    def close(self):
        self.http.session.close()
