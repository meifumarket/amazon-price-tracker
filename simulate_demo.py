
import os
import random
from datetime import datetime, timedelta
from src.parser import Product
from src.exporter import export_products_excel

# 模拟 5 个竞品 ASIN
asins = ["B0FKTFMH2F", "B08N5WRWNW", "B0BSHF7WHW", "B0C1234567", "B0D9876543"]
products_data = []

print("Generating professional competitive analysis matrix...")

for asin in asins:
    base_price = random.uniform(100, 200)
    
    for i in range(7):
        # 模拟过去 7 天的日期
        date_val = (datetime.now() - timedelta(days=6-i)).strftime("%Y-%m-%d")
        # 随机波动 +/- 5%
        price = base_price * (1 + random.uniform(-0.05, 0.05))
        
        p = Product(
            asin=asin,
            title=f"Competitive Product {asin}",
            price=round(price, 2),
            currency="USD",
            rating=round(random.uniform(3.8, 4.8), 1),
            review_count=random.randint(100, 2000),
            availability="In Stock",
            url=f"https://www.amazon.com/dp/{asin}"
        )
        # 【关键】：注入 date 属性，新版 exporter 会识别这个属性来构建时间轴
        p.date = date_val
        products_data.append(p)

os.makedirs("output", exist_ok=True)

try:
    # 使用新版 export_products_excel
    export_products_excel(products_data, out_path="output/competitive_analysis_demo.xlsx")
    print("\n✓ Success: 'output/competitive_analysis_demo.xlsx' generated.")
    print("Now open the file and check the 'Price Trends' sheet for the chart!")
except Exception as e:
    print(f"\n❌ Error: {e}")
