# 📦 Amazon Product Intelligence Tracker

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production--Ready-green.svg)]()

**Amazon Product Intelligence Tracker** 是一款专为跨境电商、市场分析师和产品经理设计的端到端数据采集工具。它不仅能高效抓取商品价格和评论，还能将原始数据直接转化为可用于决策的 **Excel 商业报表（含自动化趋势图表）**。

---

## 🚀 核心价值 (Why this tool?)

在竞争激烈的电商环境下，手动监控竞品价格低效且容易遗漏。本工具解决了以下痛点：
- **从“数据”到“报表”**：不再需要手动复制粘贴，一键生成包含价格、评分、评论的结构化 Excel 文件。
- **反爬虫工程化**：内置 User-Agent 轮换、智能重试机制与速率限制，最大程度降低封号风险。
- **批量化作业**：支持 ASIN 列表导入，快速构建竞品定价矩阵。

## ✨ 核心特性

- 🛒 **全维度采集**：支持单商品或批量 ASIN 抓取，涵盖标题、实时价格、货币、评分、评论数及库存状态。
- 💬 **深度评论挖掘**：可自定义抓取评论页数，提取评论者、评分、标题、正文及是否验证购买。
- 📊 **自动化导出**：
  - **CSV**：适用于快速数据导入与分析。
  - **Excel (.xlsx)**：利用 `openpyxl` 自动生成专业的报表，**内置价格走势折线图**，直观呈现价格波动。
- 🛡️ **工业级稳定性**：
  - 动态 User-Agent 池，模拟真实浏览器行为。
  - 异常处理机制，确保在网络波动时自动重试而不崩溃。
- 🧰 **开发者友好**：提供简洁的 CLI 命令行界面，支持 `demo` 模式快速验证。

## 🛠️ 安装指南

### 1. 克隆仓库
```bash
git clone https://github.com/your-username/amazon-price-tracker.git
cd amazon-price-tracker
```

### 2. 安装依赖
建议在虚拟环境下运行：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## 📖 快速上手

### 1. 快速演示 (Demo Mode)
无需联网，立即生成样本数据以验证安装是否成功：
```bash
python -m src.cli demo
```

### 2. 抓取单个商品 (含评论)
```bash
# 抓取商品 B08N5WRWNW 及其前 3 页评论
python -m src.cli product B08N5WRWNW --reviews --pages 3
```

### 3. 批量采集竞品
创建 `asins.txt`，每行一个 ASIN：
```text
B08N5WRWNW
B0BSHF7WHW
B0C1234567
```
运行批量任务：
```bash
python -m src.cli batch asins.txt
```

## 📁 输出结果
所有结果将保存在 `output/` 目录下：
- `output/{ASIN}_product.csv` $\rightarrow$ 商品基础信息
- `output/{ASIN}_reviews.csv` $\rightarrow$ 详细评论列表
- `output/batch_products.xlsx` $\rightarrow$ **竞品对比总表（含趋势图）**

## 🛠️ 项目架构
```text
amazon-price-tracker/
├── src/
│   ├── http_client.py   # 核心请求层：UA轮换、重试、速率限制
│   ├── parser.py        # 解析层：基于 BeautifulSoup 的 HTML 结构提取
│   ├── scraper.py       # 业务层：封装高层抓取逻辑
│   ├── exporter.py      # 输出层：CSV/Excel 格式化与图表生成
│   └── cli.py           # 交互层：命令行参数解析与流程控制
├── tests/               # 单元测试集
├── output/              # 数据输出目录
└── requirements.txt     # 依赖清单
```

## 💼 定制开发服务 (Freelance Services)

如果您需要更强大的数据采集方案，我提供以下定制化增强服务：
- ✅ **高级反爬绕过**：集成 Playwright/Selenium 模拟真实用户行为，处理复杂 JS 渲染页面。
- ✅ **自动化调度**：构建定时任务系统，每日自动监控价格变动并推送告警。
- ✅ **智能分析**：集成 LLM (GPT-4/DeepSeek) 对海量评论进行情感分析与痛点总结。
- ✅ **数据可视化看板**：将数据对接至 Grafana 或 Streamlit，构建实时价格监控大屏。

📩 **联系方式**：[您的 GitHub / Email / LinkedIn]

---

> ⚠️ **合规提示**：本工具仅用于技术研究与小规模数据实验。请务必遵守 Amazon 的 `robots.txt` 及服务条款。对于大规模生产需求，强烈建议使用官方 [Amazon Product Advertising API](https://affiliate-program.amazon.com/)。
