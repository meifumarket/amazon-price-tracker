# Project Structure

```
amazon-price-tracker/
├── README.md                 # Project overview & usage guide
├── LICENSE                   # MIT License
├── CONTRIBUTING.md           # Contribution guidelines
├── requirements.txt          # Python dependencies
├── .gitignore               # Ignored files (output/, __pycache__, venv)
├── simulate_demo.py         # Standalone demo script
├── preview.png              # Price trend chart screenshot
├── src/
│   ├── __init__.py          # Package init + version
│   ├── __main__.py          # python -m amazon_price_tracker entry
│   ├── cli.py               # CLI argument parser & subcommands
│   ├── scraper.py           # AmazonScraper orchestrator
│   ├── parser.py            # BeautifulSoup HTML parsers (Product, Review)
│   ├── http_client.py       # SafeHTTP with retries, UA rotation, rate limiting
│   └── exporter.py          # CSV + Excel (with openpyxl charts)
├── output/                  # Generated data files (gitignored)
│   ├── competitive_analysis_demo.xlsx
│   ├── B0FKTFMH2F_product.csv
│   └── ...
└── tests/                   # Unit tests (add your own!)
```

## Module Dependencies

```
cli.py ──→ scraper.py ──→ http_client.py
              │                    │
              ▼                    ▼
          parser.py          requests.Session
              │
              ▼
         exporter.py ──→ pandas + openpyxl
```
