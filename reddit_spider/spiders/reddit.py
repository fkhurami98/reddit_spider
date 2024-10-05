import scrapy
from reddit_spider.items import RedditPostItem
from scrapy_playwright.page import PageMethod
import logging


class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = [
        "https://www.reddit.com/r/Jokes/new/",
        "https://www.reddit.com/r/explainlikeimfive/new/",
        "https://www.reddit.com/r/LifeProTips/new/",
        "https://www.reddit.com/r/TrueOffMyChest/new/",
        "https://www.reddit.com/r/talesfromtechsupport/new/",
        "https://www.reddit.com/r/AskUK/new/",
        "https://www.reddit.com/r/tifu/new/",
        "https://www.reddit.com/r/AmItheAsshole/new/",
        "https://www.reddit.com/r/legaladvice/new/",
        "https://www.reddit.com/r/whowouldwin/new/",
        "https://www.reddit.com/r/AskReddit/new/",
        "https://www.reddit.com/r/HFY/new/",
        "https://www.reddit.com/r/AskHistorians/new/",
        "https://www.reddit.com/r/talesfromretail/new/",
        "https://www.reddit.com/r/talesfromtechsupport/new/",
        "https://www.reddit.com/r/wouldyourather/new/",
        "https://www.reddit.com/r/stories/new/",
        "https://www.reddit.com/r/answers/new/",
    ]

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
                f"Scraped post: {postItem['title']} by {postItem['author']} from {postItem['start_url']}"
            )

            yield postItem
