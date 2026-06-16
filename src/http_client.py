"""
HTTP 请求模块
统一封装 requests.session，提供：
- User-Agent 轮换
- 自动重试
- 指数退避
- 速率限制
"""
import random
import time
import logging
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


class SafeHTTP:
    """带速率限制 & 自动重试的 HTTP 客户端"""

    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 5.0,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout = timeout
        self.session = self._build_session(max_retries)

    def _build_session(self, max_retries: int) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        delay = random.uniform(self.min_delay, self.max_delay)
        logger.debug(f"sleeping {delay:.2f}s before request")
        time.sleep(delay)

        headers = kwargs.pop("headers", {})
        headers.setdefault(
            "User-Agent", random.choice(USER_AGENTS)
        )
        headers.setdefault(
            "Accept-Language", "en-US,en;q=0.9"
        )

        try:
            response = self.session.get(
                url, headers=headers, timeout=self.timeout, **kwargs
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"request failed: {url} → {e}")
            return None
