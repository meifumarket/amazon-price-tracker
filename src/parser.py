"""
Amazon 商品/评论 解析模块
使用 BeautifulSoup 解析商品页和评论数据
"""
import re
import logging
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class Product:
    asin: str = ""
    title: str = ""
    price: Optional[float] = None
    currency: str = "USD"
    rating: Optional[float] = None
    review_count: int = 0
    availability: str = ""
    url: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Review:
    reviewer: str = ""
    rating: float = 0.0
    title: str = ""
    body: str = ""
    date: str = ""
    verified: bool = False

    def to_dict(self):
        return asdict(self)


class AmazonParser:
    """Amazon HTML 解析器（针对 amazon.com 的 HTML 结构）"""

    @staticmethod
    def parse_product(html: str, asin: str, url: str) -> Product:
        soup = BeautifulSoup(html, "lxml")
        product = Product(asin=asin, url=url)

        # 标题
        title_el = soup.select_one("#productTitle")
        if title_el:
            product.title = title_el.get_text(strip=True)

        # 价格 — 多种 selector 兼容
        price_selectors = [
            "span.a-price span.a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            "span#price_inside_buybox",
        ]
        for sel in price_selectors:
            el = soup.select_one(sel)
            if el:
                text = el.get_text(strip=True)
                match = re.search(r"([0-9,]+\.?[0-9]*)", text)
                if match:
                    try:
                        product.price = float(match.group(1).replace(",", ""))
                        # 简单判断货币
                        if "€" in text:
                            product.currency = "EUR"
                        elif "£" in text:
                            product.currency = "GBP"
                        elif "¥" in text:
                            product.currency = "JPY"
                        break
                    except ValueError:
                        continue

        # 评分
        rating_el = soup.select_one(
            "i.a-icon-star span.a-icon-alt, "
            "[data-hook='average-star-rating'] span.a-icon-alt"
        )
        if rating_el:
            match = re.search(r"([0-9]+\.?[0-9]*)", rating_el.get_text())
            if match:
                product.rating = float(match.group(1))

        # 评论数
        count_el = soup.select_one("#acrCustomerReviewText")
        if count_el:
            match = re.search(r"([0-9,]+)", count_el.get_text())
            if match:
                product.review_count = int(match.group(1).replace(",", ""))

        # 库存
        avail_el = soup.select_one("#availability span")
        if avail_el:
            product.availability = avail_el.get_text(strip=True)

        logger.info(
            f"parsed product: {product.title[:50]}… "
            f"price={product.price} {product.currency} "
            f"rating={product.rating} reviews={product.review_count}"
        )
        return product

    @staticmethod
    def parse_reviews(html: str) -> List[Review]:
        soup = BeautifulSoup(html, "lxml")
        reviews = []

        # 兼容新旧两种 review 容器
        review_containers = soup.select(
            "[data-hook='review'], div.review"
        )

        for c in review_containers:
            r = Review()

            rating_el = c.select_one(
                "[data-hook='review-star-rating'] span, "
                "i.review-rating span"
            )
            if rating_el:
                match = re.search(r"([0-9]+\.?[0-9]*)", rating_el.get_text())
                if match:
                    r.rating = float(match.group(1))

            title_el = c.select_one(
                "[data-hook='review-title'] span, "
                "span.review-title"
            )
            if title_el:
                r.title = title_el.get_text(strip=True)

            body_el = c.select_one(
                "[data-hook='review-body'] span, "
                "div.review-text"
            )
            if body_el:
                r.body = body_el.get_text(strip=True)

            reviewer_el = c.select_one(".a-profile-name")
            if reviewer_el:
                r.reviewer = reviewer_el.get_text(strip=True)

            date_el = c.select_one("[data-hook='review-date']")
            if date_el:
                r.date = date_el.get_text(strip=True)

            verified_el = c.select_one("[data-hook='avp-badge']")
            r.verified = verified_el is not None

            if r.body:  # 至少要有 body 才算有效评论
                reviews.append(r)

        logger.info(f"parsed {len(reviews)} reviews")
        return reviews
