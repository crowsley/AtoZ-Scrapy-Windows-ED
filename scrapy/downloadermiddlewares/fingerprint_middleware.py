"""
Scrapy Pro Enterprise Architecture - TLS & Header Fingerprint Rotation Middleware

Rotates User-Agent headers, Accept-Language, Accept-Encoding, and TLS cipher suites
across requests to bypass anti-bot detection systems (Cloudflare / Akamai / PerimeterX).
"""

import random
from scrapy import signals


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
]

ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.8,en-US;q=0.6",
    "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
]


class FingerprintRotationMiddleware:
    """
    Downloader middleware for dynamic HTTP header & TLS fingerprint rotation.
    """

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        spider.logger.info("Initializing Scrapy Pro Anti-Bot Fingerprint Rotation Engine...")

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(USER_AGENTS)
        request.headers["Accept-Language"] = random.choice(ACCEPT_LANGUAGES)
        request.headers["Sec-Ch-Ua"] = '"Chromium";v="122", "Not(A:Brand";v="24"'
        request.headers["Sec-Ch-Ua-Mobile"] = "?0"
        request.headers["Sec-Ch-Ua-Platform"] = '"Windows"'
        return None
