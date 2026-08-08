"""
AtoZ Scrapy Windows ED 0.0.1 - Demo Quotes Spider

A sample spider targeting quotes.toscrape.com for testing live GUI feed item streaming.
"""

import scrapy


class DemoQuotesSpider(scrapy.Spider):
    name = "demo_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapy.pipelines.gui_pipeline.GuiItemPipeline": 100,
        }
    }

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "title": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
                "url": response.url,
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
