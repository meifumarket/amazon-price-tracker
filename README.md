# 📦 Amazon Product Intelligence Tracker / 亚马逊产品情报追踪器

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production--Ready-green.svg)]()
[![GitHub stars](https://img.shields.io/github/stars/meifumarket/amazon-price-tracker.svg?style=social)](https://github.com/meifumarket/amazon-price-tracker/stargazers)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Made for e-commerce](https://img.shields.io/badge/Made%20for-eCommerce-orange.svg)]()

**English:**
**Amazon Product Intelligence Tracker** is an end-to-end data collection tool designed for cross-border e-commerce sellers, market analysts, and product managers. It not only efficiently scrapes product prices and reviews 
but also transforms raw data into decision-ready **Business Excel Reports (with automated trend charts)**.

> ⭐ **If this saved you time, give it a star — it helps other sellers find this tool.**
> 🚀 **Need custom scraping, dashboard, or LLM-powered analysis? Hire the author on Fiverr →** [fiverr.com/meifumarket](https://www.fiverr.com/meifumarket)
**中文：**
**Amazon Product Intelligence Tracker** 是一款专为跨境电商、市场分析师和产品经理设计的端到端数据采集工具。它不仅能高效抓取商品价格和评论，还能将原始数据直接转化为可用于决策的 **Excel 商业报表（含自动化趋势图表）**。

![Price Trends Preview](./preview.png)

---

## 🚀 Core Value / 核心价值

**English:**
In a competitive e-commerce environment, manually monitoring competitor prices is inefficient. This tool solves these pain points:
- **From "Data" to "Report"**: No more manual copy-pasting; generate structured Excel files with pricing, ratings, and reviews in one click.
- **Anti-Scraping Engineering**: Built-in User-Agent rotation, smart retry mechanisms, and rate limiting to minimize ban risks.
- **Batch Processing**: Support ASIN list imports to quickly build a competitor pricing matrix.

**中文：**
在竞争激烈的电商环境下，手动监控竞品价格低效且容易遗漏。本工具解决了以下痛点：
- **从“数据”到“报表”**：不再需要手动复制粘贴，一键生成包含价格、评分、评论的结构化 Excel 文件。
- **反爬虫工程化**：内置 User-Agent 轮换、智能重试机制与速率限制，最大程度降低封号风险。
- **批量化作业**：支持 ASIN 列表导入，快速构建竞品定价矩阵。

## ✨ Key Features / 核心特性

- 🛒 **Full-Dimension Collection / 全维度采集**: Support single product or batch ASIN scraping, covering title, real-time price, currency, rating, review count, and availability.
- 💬 **Deep Review Mining / 深度评论挖掘**: Customizable review page scraping, extracting reviewer, rating, title, body, and verified purchase status.
- 📊 **Automated Export / 自动化导出**:
  - **CSV**: For fast data import and analysis.
  - **Excel (.xlsx)**: Professional reports generated via `openpyxl` with **built-in price trend line charts**.
- 🛡️ **Industrial Stability / 工业级稳定性**: Dynamic User-Agent pool and exception handling to ensure stability during network fluctuations.
- 🧰 **Developer Friendly / 开发者友好**: Simple CLI interface with a `demo` mode for rapid verification.

## 🛠️ Installation / 安装指南

### 1. Clone Repository / 克隆仓库
```bash
git clone https://github.com/meifumarket/amazon-price-tracker.git
cd amazon-price-tracker
```

### 2. Install Dependencies / 安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## 📖 Quick Start / 快速上手

### 1. Demo Mode / 快速演示 (No Network)
```bash
python -m src.cli demo
```

### 2. Single Product / 抓取单个商品
```bash
# Scrape product B08N5WRWNW and its first 3 pages of reviews
python -m src.cli product B08N5WRWNW --reviews --pages 3
```

### 3. Batch Collection / 批量采集竞品
Create `asins.txt` with one ASIN per line:
```text
B08N5WRWNW
B0BSHF7WHW
B0C1234567
```
Run batch task:
```bash
python -m src.cli batch asins.txt
```

## 📁 Output / 输出结果
- `output/{ASIN}_product.csv` $\rightarrow$ Basic product info / 商品基础信息
- `output/{ASIN}_reviews.csv` $\rightarrow$ Detailed reviews / 详细评论列表
- `output/batch_products.xlsx` $\rightarrow$ **Competitive Matrix with Trends / 竞品对比总表（含趋势图）**

## 🛠️ Architecture / 项目架构
```text
amazon-price-tracker/
├── src/
│   ├── http_client.py   # Request layer: UA rotation, retry, rate limit
│   ├── parser.py        # Parsing layer: HTML extraction via BeautifulSoup
│   ├── scraper.py       # Business layer: High-level scraping logic
│   ├── exporter.py      # Output layer: CSV/Excel formatting & charts
│   └── cli.py           # Interaction layer: CLI argument parsing
├── tests/               # Unit tests
├── output/              # Data output directory
└── requirements.txt     # Dependency list
```

## 💼 Freelance Services / 定制开发服务

**English:**
If you need more powerful data collection solutions, I provide the following custom enhancements:
- ✅ **Advanced Anti-Scraping**: Integration with Playwright/Selenium for complex JS rendered pages.
- ✅ **Automated Scheduling**: Cron-job systems for daily price monitoring and alerts.
- ✅ **Intelligent Analysis**: Integration with LLMs (GPT-4/DeepSeek) for sentiment analysis of reviews.
- ✅ **Data Dashboard**: Connecting data to Grafana or Streamlit for real-time monitoring.

**中文：**
如果您需要更强大的数据采集方案，我提供以下定制化增强服务：
- ✅ **高级反爬绕过**：集成 Playwright/Selenium 模拟真实用户行为，处理复杂 JS 渲染页面。
- ✅ **自动化调度**：构建定时任务系统，每日自动监控价格变动并推送告警。
- ✅ **智能分析**：集成 LLM (GPT-4/DeepSeek) 对海量评论进行情感分析与痛点总结。
- ✅ **数据可视化看板**：将数据对接至 Grafana 或 Streamlit，构建实时价格监控大屏。

📩 **Contact / 联系方式**: 
- **Fiverr**: [fiverr.com/meifumarket](https://www.fiverr.com/meifumarket) (preferred)
- **GitHub**: [@meifumarket](https://github.com/meifumarket)
- **Email**: 858679@qq.com

---

> ⚠️ **Compliance / 合规提示**: For technical research and small-scale experiments only. Please adhere to Amazon's `robots.txt` and Terms of Service. For production needs, the official [Amazon Product Advertising API](https://affiliate-program.amazon.com/) is strongly recommended.
