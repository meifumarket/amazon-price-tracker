"""
CLI 入口
用法:
    python -m amazon_price_tracker product B08N5WRWNW
    python -m amazon_price_tracker product B08N5WRWNW --reviews --pages 3
    python -m amazon_price_tracker batch asins.txt
    python -m amazon_price_tracker demo
"""
import argparse
import json
import logging
import sys
from pathlib import Path

# 让脚本既能作为模块运行，也能直接运行
if __name__ == "__main__" and __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "amazon_price_tracker"

from .scraper import AmazonScraper
from .exporter import (
    export_products_csv,
    export_reviews_csv,
    export_products_excel,
)


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def cmd_product(args):
    scraper = AmazonScraper()
    try:
        product = scraper.get_product(args.asin)
        print(json.dumps(product.to_dict(), indent=2, ensure_ascii=False))

        export_products_csv([product], f"output/{args.asin}_product.csv")

        if args.reviews:
            reviews = scraper.get_reviews(args.asin, max_pages=args.pages)
            export_reviews_csv(reviews, f"output/{args.asin}_reviews.csv")
            print(f"\n✓ {len(reviews)} reviews exported")
    finally:
        scraper.close()


def cmd_batch(args):
    asin_file = Path(args.file)
    if not asin_file.exists():
        print(f"error: {args.file} not found")
        sys.exit(1)
    asins = [line.strip() for line in asin_file.read_text().splitlines() if line.strip()]
    print(f"loaded {len(asins)} asins")

    scraper = AmazonScraper()
    try:
        products = scraper.batch_products(asins)
        export_products_excel(products, out_path="output/batch_products.xlsx")
        print(f"\n✓ {len(products)} products exported")
    finally:
        scraper.close()


def cmd_demo(args):
    """使用 sandbox 演示模式（不真实请求 Amazon）"""
    print("demo mode: generating sample data without network calls")
    from .parser import Product, Review

    sample = Product(
        asin="DEMO0001",
        title="Sample Product (Demo Mode)",
        price=29.99,
        currency="USD",
        rating=4.5,
        review_count=1234,
        availability="In Stock",
        url="https://example.com/demo",
    )
    export_products_csv([sample], "output/demo_product.csv")
    export_products_excel([sample], out_path="output/demo_product.xlsx")

    sample_reviews = [
        Review(reviewer="Alice", rating=5.0, title="Love it!",
               body="Works as expected.", date="2025-01-01", verified=True),
        Review(reviewer="Bob", rating=4.0, title="Pretty good",
               body="Value for money.", date="2025-01-02", verified=False),
    ]
    export_reviews_csv(sample_reviews, "output/demo_reviews.csv")
    print("✓ demo files generated in output/")


def main():
    parser = argparse.ArgumentParser(description="Amazon Price & Review Tracker")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("product", help="抓取单个商品")
    p1.add_argument("asin", help="商品 ASIN")
    p1.add_argument("--reviews", action="store_true", help="同时抓评论")
    p1.add_argument("--pages", type=int, default=2, help="评论页数")
    p1.set_defaults(func=cmd_product)

    p2 = sub.add_parser("batch", help="批量抓取，asin 列表存到文件里")
    p2.add_argument("file", help="文件，每行一个 ASIN")
    p2.set_defaults(func=cmd_batch)

    p3 = sub.add_parser("demo", help="生成 demo 文件（不连网）")
    p3.set_defaults(func=cmd_demo)

    args = parser.parse_args()
    setup_logging(args.verbose)
    args.func(args)


if __name__ == "__main__":
    main()
