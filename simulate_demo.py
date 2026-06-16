
import os
import random
from datetime import datetime, timedelta
from src.parser import Product
from src.exporter import export_products_excel

# 模拟 5 个竞品 ASIN
asins = ["B0FKTFMH2F", "B08N5WRWNW", "B0BSHF7WHW", "B0C1234567", "B0D9876543"]
products_data = []

print("Generating simulation data for competitive analysis...")

for asin in asins:
    # 基础价格
    base_price = random.uniform(100, 200)
    
    # 模拟过去 7 天的价格走势
    for i in range(7):
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
        products_data.append(p)

# 创建输出目录
os.makedirs("output", exist_ok=True)

# 调用原有的导出函数
try:
    export_products_excel(products_data, out_path="output/competitive_analysis_demo.xlsx")
    print("\n✓ Success: 'output/competitive_analysis_demo.xlsx' generated.")
    print("This file now contains a price trend matrix for 5 products over 7 days.")
except Exception as e:
    print(f"\n❌ Error: {e}")
