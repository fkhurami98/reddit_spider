import scrapy
from reddit_spider.items import RedditPostItem
from scrapy_playwright.page import PageMethod

class RedditSpider(scrapy.Spider):
    name = "reddit_spider"
    start_urls = ["https://www.reddit.com/r/Python/new/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_load_state", "networkidle")
                    ],
                }
            )
    
    async def parse(self, response):
        posts = response.css("shreddit-post")
        if not posts:
            self.logger.info("No posts found.")
            return

        for post in posts:
            postItem = RedditPostItem()
            postItem["title"] = post.attrib.get("post-title")
            postItem["author"] = post.attrib.get("author")
            postItem["comments"] = post.attrib.get("comment-count")
            postItem["permalink"] = post.attrib.get("permalink")
            postItem["created_timestamp"] = post.attrib.get("created-timestamp")
            yield postItem