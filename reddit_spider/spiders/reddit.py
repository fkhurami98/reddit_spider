import scrapy
from reddit_spider.items import RedditPostItem
from reddit_spider.settings import START_URLS
from scrapy_playwright.page import PageMethod
import logging


class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = START_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod(
                            "evaluate", "window.scrollBy(0, window.innerHeight * 60);"
                        ),
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod(
                            "add_init_script",
                            """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            });
                        """,
                        ),
                    ],
                    "start_url": url,
                },
            )

    async def parse(self, response):
        yield scrapy.Request(
            url="https://httpbin.org/ip",
            callback=self.log_exit_ip_and_continue,
            meta={"original_response": response},
            dont_filter=True,
        )

    def log_exit_ip_and_continue(self, response):
        actual_exit_ip = response.json().get("origin")
        original_response = response.meta["original_response"]
        start_url = original_response.meta["start_url"]
        proxy = original_response.meta.get("proxy")

        user_agent = original_response.request.headers.get("User-Agent", b"").decode(
            "utf-8"
        )

        print("\n" + "=" * 138)
        logging.info(f"User-Agent used: {user_agent}")
        logging.info(f"Exit IP (Tor Node): {actual_exit_ip}")
        if proxy:
            logging.info(f"Proxy IP (Docker): {proxy}")
        posts = original_response.css("shreddit-post")
        for post in posts:
            postItem = RedditPostItem()
            postItem["title"] = post.attrib.get("post-title")
            postItem["author"] = post.attrib.get("author")
            postItem["comments"] = post.attrib.get("comment-count")
            postItem["permalink"] = post.attrib.get("permalink")
            postItem["created_timestamp"] = post.attrib.get("created-timestamp")
            postItem["start_url"] = start_url
            yield postItem

        logging.info(f"Scraped all posts from subreddit: {start_url} ")
        print("=" * 138 + "\n")
