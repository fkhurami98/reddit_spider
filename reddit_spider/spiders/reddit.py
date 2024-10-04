import scrapy
from reddit_spider.items import RedditPostItem
from scrapy_playwright.page import PageMethod


class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = [
        "https://www.reddit.com/r/Jokes/",
        "https://www.reddit.com/r/explainlikeimfive/",
        "https://www.reddit.com/r/LifeProTips/",
        "https://www.reddit.com/r/TrueOffMyChest/",
        "https://www.reddit.com/r/talesfromtechsupport/",
        "https://www.reddit.com/r/AskUK/",
        "https://www.reddit.com/r/tifu/",
        "https://www.reddit.com/r/AmItheAsshole/",
        "https://www.reddit.com/r/legaladvice/",
        "https://www.reddit.com/r/whowouldwin/",
        "https://www.reddit.com/r/AskReddit/",
        "https://www.reddit.com/r/HFY/",
        "https://www.reddit.com/r/AskHistorians/",
        "https://www.reddit.com/r/talesfromretail/",
        "https://www.reddit.com/r/talesfromtechsupport/",
        "https://www.reddit.com/r/wouldyourather/",
        "https://www.reddit.com/r/stories/",
        "https://www.reddit.com/r/answers/",
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
            yield postItem
