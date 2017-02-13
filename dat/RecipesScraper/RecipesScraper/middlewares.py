"""
Middleware for RecipesScraper, defines spider's workings.
"""
from scrapy import signals


class RecipesscraperSpiderMiddleware(object):
  """RecipesScraper middleware."""
  # Not all methods need to be defined. If a method is not defined,
  # scrapy acts as if the spider middleware does not modify the
  # passed objects.

  @classmethod
  def from_crawler(cls, crawler):
    # This method is used by Scrapy to create your spiders.
    s = cls()
    crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
    return s

  @staticmethod
  def process_spider_output(result):
    # Called with the results returned from the Spider, after
    # it has processed the response.

    # Must return an iterable of Request, dict or Item objects.
    for i in result:
      yield i

  @staticmethod
  def process_start_requests(start_requests):
    # Called with the start requests of the spider, and works
    # similarly to the process_spider_output() method, except
    # that it doesn't have a response associated.

    # Must return only requests (not items).
    for r in start_requests:
      yield r

  @staticmethod
  def spider_opened(spider):
    spider.logger.info('Spider opened: %s' % spider.name)
