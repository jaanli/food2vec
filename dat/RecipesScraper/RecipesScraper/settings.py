"""
Scrapy settings for RecipesScraper project.
"""
# Names
BOT_NAME = 'RecipesScraper'

SPIDER_MODULES = ['RecipesScraper.spiders']
NEWSPIDER_MODULE = 'RecipesScraper.spiders'



# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    'RecipesScraper.pipelines.JsonPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False
