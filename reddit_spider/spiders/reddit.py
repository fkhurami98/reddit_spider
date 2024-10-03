import scrapy
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async
from scrapy_playwright.page import PageMethod

# def get_random_user_agent():
#     return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

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
                        PageMethod("evaluate", "window.scrollBy(0, window.innerHeight * 60);"),
                        PageMethod("wait_for_load_state", "networkidle"),  # Wait for network idle
                        PageMethod("evaluate", "window.scrollBy(0, window.innerHeight * 60);"),  # Scroll down again
                        PageMethod("wait_for_load_state", "networkidle"),  # Wait for network idle
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

        response.follow(response.url, callback=self.parse, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("evaluate", "(window.scrollBy(0, document.body.scrollHeight))"),
                PageMethod("wait_for_selector", "shreddit-post", timeout=10000),
            ]
        })