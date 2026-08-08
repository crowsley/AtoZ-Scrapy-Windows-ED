"""
Reddit Comments & Posts Spider for AtoZ Scrapy Windows ED

Scrapes posts, app ideas, descriptions, and comments from any Subreddit or Reddit thread URL.
Supports spider names: 'reddit', 'reddit_comments', 'app_ideas', or 'app ideas'.
"""

import scrapy


class RedditSpider(scrapy.Spider):
    name = "reddit"
    aliases = ["reddit_comments", "app_ideas", "app ideas"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    }

    def __init__(self, target_url=None, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        target = target_url or url or "https://old.reddit.com/r/Appideas/"
        if "reddit.com" in target and "old.reddit.com" not in target:
            target = target.replace("www.reddit.com", "old.reddit.com").replace("https://reddit.com", "https://old.reddit.com")
        if not target.startswith("http"):
            target = "https://old.reddit.com/r/Appideas/"
        self.start_urls = [target]

    def parse(self, response):
        # 1. Scrape posts / app ideas from subreddit page
        posts = response.css("div.thing")
        for post in posts:
            title = post.css("a.title::text").get()
            author = post.css("a.author::text").get() or "anonymous"
            comments_count = post.css("a.comments::text").get() or "0 comments"
            score = post.css("div.score.unvoted::text").get() or post.css("div.score::text").get() or "0"
            permalink = response.urljoin(post.css("a.title::attr(href)").get() or "")

            if title:
                yield {
                    "title": title.strip(),
                    "author": author.strip(),
                    "score": score.strip(),
                    "comments_count": comments_count.strip(),
                    "text": title.strip(),
                    "url": permalink
                }

                # Follow thread to scrape inner comments
                if "/comments/" in permalink:
                    yield scrapy.Request(permalink, callback=self.parse_comments)

        # Scrape pagination
        next_button = response.css("span.next-button a::attr(href)").get()
        if next_button:
            yield response.follow(next_button, callback=self.parse)

    def parse_comments(self, response):
        # 2. Scrape individual comments inside thread
        post_title = response.css("a.title::text").get() or response.css("h1::text").get() or ""
        comments = response.css("div.comment")
        for comment in comments:
            author = comment.css("a.author::text").get() or "anonymous"
            body = "".join(comment.css("div.usertext-body p::text").getall()).strip()
            score = comment.css("span.score.unvoted::text").get() or "1 point"

            if body:
                yield {
                    "title": f"Comment on: {post_title.strip()[:40]}",
                    "author": author.strip(),
                    "score": score.strip(),
                    "text": body,
                    "url": response.url
                }


class RedditCommentsAlias(RedditSpider):
    name = "reddit_comments"


class AppIdeasAlias(RedditSpider):
    name = "app_ideas"


class AppIdeasSpacesAlias(RedditSpider):
    name = "app ideas"
