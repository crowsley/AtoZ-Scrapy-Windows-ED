"""
Universal Multi-Site Web Scraper Spider for AtoZ Scrapy Windows ED

Extracts articles, headlines, wiki summaries, paragraphs, comments, and links
from ANY website URL (News sites, Wikipedia, Forums, Blogs, E-commerce, etc.)
with keyword and phrase filtering support.
"""

import re
import json
import scrapy
from urllib.parse import urlparse


class UniversalSpider(scrapy.Spider):
    name = "universal"
    aliases = ["news", "wikipedia", "wiki", "general", "articles"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    }

    def __init__(self, target_url=None, url=None, keywords=None, phrase=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        target = target_url or url or "https://en.wikipedia.org/wiki/Artificial_intelligence"
        if not target.startswith("http"):
            target = "https://" + target
        self.start_urls = [target]

        kw_str = keywords or phrase or ""
        self.keywords_list = [k.strip().lower() for k in kw_str.split(",") if k.strip()]

    def parse(self, response):
        domain = urlparse(response.url).netloc.lower()

        # 1. Wikipedia Specific Extraction
        if "wikipedia.org" in domain:
            page_title = response.css("h1#firstHeading::text, span.mw-page-title-main::text").get() or "Wikipedia Article"
            
            # Extract all paragraphs using string() xpath for clean text
            paragraphs = [p.strip() for p in response.css("div.mw-parser-output p").xpath("string()").getall() if len(p.strip()) > 30]

            for i, p in enumerate(paragraphs[:10], 1):
                if self._matches_keywords(page_title + " " + p):
                    yield {
                        "type": "wikipedia_section",
                        "title": f"{page_title.strip()} (Section {i})",
                        "text": p[:300] + ("..." if len(p) > 300 else ""),
                        "url": response.url
                    }

            # Follow related Wikipedia article links
            for link in response.css("div.mw-parser-output a::attr(href)").getall()[:15]:
                if link.startswith("/wiki/") and ":" not in link:
                    yield response.follow(link, callback=self.parse)

        # 2. General News & Article Extraction (BBC, CNN, Blogs, General Sites)
        else:
            page_title = (
                response.css("h1::text, article h1::text, meta[property='og:title']::attr(content)").get()
                or response.css("title::text").get()
                or "Article"
            ).strip()

            # Extract main paragraph contents
            article_p = [p.strip() for p in response.css("article p, main p, div.content p, p").xpath("string()").getall() if len(p.strip()) > 30]

            for i, p in enumerate(article_p[:10], 1):
                if self._matches_keywords(page_title + " " + p):
                    yield {
                        "type": "article_paragraph",
                        "title": f"{page_title[:60]} (Para {i})",
                        "text": p[:300] + ("..." if len(p) > 300 else ""),
                        "url": response.url
                    }

            # Extract headlines / links on index pages
            for article in response.css("article, div.card, div.post, div.story, li.news-item"):
                h_title = article.css("h1::text, h2::text, h3::text, a::text").get()
                link = response.urljoin(article.css("a::attr(href)").get() or "")
                if h_title and link and self._matches_keywords(h_title):
                    yield {
                        "type": "headline",
                        "title": h_title.strip(),
                        "url": link
                    }

            # Follow subpages within same domain
            for link in response.css("a::attr(href)").getall()[:20]:
                if link and not link.startswith("#") and not link.startswith("javascript:"):
                    link_domain = urlparse(response.urljoin(link)).netloc.lower()
                    if link_domain == domain:
                        yield response.follow(link, callback=self.parse)

    def _matches_keywords(self, text: str) -> bool:
        if not self.keywords_list:
            return True
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.keywords_list)


class NewsAlias(UniversalSpider):
    name = "news"


class WikipediaAlias(UniversalSpider):
    name = "wikipedia"


class WikiAlias(UniversalSpider):
    name = "wiki"
