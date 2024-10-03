import scrapy
from scrapy_playwright.page import PageMethod

class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = ["https://www.reddit.com/r/Python"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("evaluate", "(window.scrollBy(0, document.body.scrollHeight))"),
                        PageMethod("wait_for_selector", "shreddit-post", timeout=10000),
                    ],
                }
            )

    async def parse(self, response):
        posts = response.css("shreddit-post")

        for post in posts:
            yield {
                "title": post.attrib.get("post-title"),
                "author": post.attrib.get("author"),
                "comments": post.attrib.get("comment-count"),
                "permalink": post.attrib.get("permalink"),
                "created_timestamp": post.attrib.get("created-timestamp"),
            }

        # Dont think this scroll works properly
        await response.follow(response.url, callback=self.parse, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("evaluate", "(window.scrollBy(0, document.body.scrollHeight))"),
                PageMethod("wait_for_selector", "shreddit-post", timeout=10000),
            ]
        })