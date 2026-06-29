# Contributing to Amazon Price Intelligence Engine

Thank you for your interest in contributing! This project is open-source under the MIT License.

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Commit with descriptive messages: `git commit -m "feat: add X"`
5. Push and open a Pull Request

## Development Setup

```bash
git clone https://github.com/meifumarket/amazon-price-tracker.git
cd amazon-price-tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Adding Tests

Tests go in the `tests/` directory. Run with:
```bash
python -m pytest tests/ -v
```

## Code Style

- Follow PEP 8 conventions
- Type hints for public APIs
- Docstrings for all public functions/classes
