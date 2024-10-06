from scrapy import Spider


class GenerateStartURL(Spider):
    """
    A Scrapy spider that scrapes the list of subreddits from the Reddit /subreddits page,
    to dynamically generate the 'START_URL' list object for scraping subreddit metadata.

    Variables can be configured to control the scraping behavior.
    """

    name = "generate_start_url"
    allowed_domains = []
    start_urls = []

    # Config
    subreddit_category = "popular"  # Can be 'new', 'popular', 'top'
    limit_subreddits = 100  # Maximum number of subreddits to scrape

    def parse(self, response):
        pass
