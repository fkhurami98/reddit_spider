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
        user_agent = response.request.headers.get("User-Agent").decode("utf-8")

        logging.info(f"User-Agent: {user_agent}")

        posts = response.css("shreddit-post")

        for post in posts:
            postItem = RedditPostItem()
            postItem["title"] = post.attrib.get("post-title")
            postItem["author"] = post.attrib.get("author")
            postItem["comments"] = post.attrib.get("comment-count")
            postItem["permalink"] = post.attrib.get("permalink")
            postItem["created_timestamp"] = post.attrib.get("created-timestamp")
            postItem["start_url"] = response.meta["start_url"]

            logging.info(
                f"Scraped post: {postItem['title'][:40]} by {postItem['author']} from {postItem['start_url']}"
            )

            yield postItem